# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import copy
from unittest import mock
import warnings

import fixtures
from oslo_config import cfg
from oslo_db.sqlalchemy import enginefacade
from oslo_db.sqlalchemy import provision
from oslo_db.sqlalchemy import session
from oslo_messaging import conffixture

from neutron_lib.api import attributes
from neutron_lib.api import definitions
from neutron_lib.callbacks import manager
from neutron_lib.callbacks import registry
from neutron_lib.db import api as db_api
from neutron_lib.db import model_base
from neutron_lib.db import model_query
from neutron_lib.db import resource_extend
from neutron_lib.plugins import directory
from neutron_lib import rpc
from neutron_lib.tests.unit import fake_notifier


CONF = cfg.CONF


class PluginDirectoryFixture(fixtures.Fixture):

    def __init__(self, plugin_directory=None):
        super().__init__()
        self.plugin_directory = (
            plugin_directory or directory._PluginDirectory())

    def _setUp(self):
        self._orig_directory = directory._PLUGIN_DIRECTORY
        directory._PLUGIN_DIRECTORY = self.plugin_directory
        self.addCleanup(self._restore)

    def _restore(self):
        directory._PLUGIN_DIRECTORY = self._orig_directory


class CallbackRegistryFixture(fixtures.Fixture):
    """Callback registry fixture.

    This class is intended to be used as a fixture within unit tests and
    therefore consumers must register it using useFixture() within their
    unit test class. The implementation optionally allows consumers to pass
    in the CallbacksManager manager to use for your tests.
    """

    def __init__(self, callback_manager=None):
        """Creates a new RegistryFixture.

        :param callback_manager: If specified, the return value to use for
        _get_callback_manager(). Otherwise a new instance of CallbacksManager
        is used.
        """
        super().__init__()
        self.callback_manager = callback_manager or manager.CallbacksManager()
        self.patcher = None

    def _setUp(self):
        self._orig_manager = registry._get_callback_manager()
        self.patcher = mock.patch.object(
            registry, '_get_callback_manager',
            return_value=self.callback_manager)
        self.patcher.start()
        self.addCleanup(self._restore)

    def _restore(self):
        registry._CALLBACK_MANAGER = self._orig_manager
        self.patcher.stop()


class _EnableSQLiteFKsFixture(fixtures.Fixture):
    """Turn SQLite PRAGMA foreign keys on and off for tests.

    FIXME(zzzeek): figure out some way to get oslo.db test_base to honor
    oslo_db.engines.create_engine() arguments like sqlite_fks as well
    as handling that it needs to be turned off during drops.

    """

    def __init__(self, engine):
        self.engine = engine

    def _setUp(self):
        if self.engine.name == 'sqlite':
            with self.engine.connect() as conn:
                cursor = conn.connection.cursor()
                cursor.execute('PRAGMA foreign_keys=ON')
                cursor.close()


class SqlFixture(fixtures.Fixture):

    @classmethod
    def _generate_schema(cls, engine):
        model_base.BASEV2.metadata.create_all(engine)

    def _delete_from_schema(self, engine):
        with engine.begin() as conn:
            for table in reversed(
                    model_base.BASEV2.metadata.sorted_tables):
                conn.execute(table.delete())

    def _init_resources(self):
        pass

    def _setUp(self):
        self._init_resources()

        # check if the fixtures failed to get
        # an engine.  The test setUp() itself should also be checking
        # this and raising skipTest.
        if not hasattr(self, 'engine'):
            return

        engine = self.engine
        self.addCleanup(lambda: self._delete_from_schema(engine))

        self.sessionmaker = session.get_maker(engine)

        _restore_factory = db_api.get_context_manager()._root_factory

        self.enginefacade_factory = enginefacade._TestTransactionFactory(
            self.engine, self.sessionmaker, from_factory=_restore_factory,
            apply_global=False)

        db_api.get_context_manager()._root_factory = self.enginefacade_factory

        engine = db_api.CONTEXT_WRITER.get_engine()

        self.addCleanup(
            lambda: setattr(
                db_api.get_context_manager(),
                "_root_factory", _restore_factory))

        self.useFixture(_EnableSQLiteFKsFixture(engine))


class StaticSqlFixture(SqlFixture):

    _GLOBAL_RESOURCES = False

    @classmethod
    def _init_resources(cls):
        # this is a classlevel version of what testresources
        # does w/ the resources attribute as well as the
        # setUpResources() step (which requires a test instance, that
        # SqlFixture does not have).  Because this is a SQLite memory
        # database, we don't actually tear it down, so we can keep
        # it running throughout all tests.
        if cls._GLOBAL_RESOURCES:
            return
        else:
            cls._GLOBAL_RESOURCES = True
            cls.schema_resource = provision.SchemaResource(
                provision.DatabaseResource(
                    "sqlite", db_api.get_context_manager()),
                cls._generate_schema, teardown=False)
            dependency_resources = {}
            for name, resource in cls.schema_resource.resources:
                dependency_resources[name] = resource.getResource()
            cls.schema_resource.make(dependency_resources)
            cls.engine = dependency_resources['database'].engine


class APIDefinitionFixture(fixtures.Fixture):
    """Test fixture for testing neutron-lib API definitions.

    Extension API definition RESOURCE_ATTRIBUTE_MAP dicts get updated as
    part of standard extension processing/handling. While this behavior is
    fine for service runtime, it can impact testing scenarios whereby test1
    updates the attribute map (globally) and test2 doesn't expect the
    test1 updates.

    This fixture saves and restores 1 or more neutron-lib API definitions
    attribute maps. It should be used anywhere multiple tests can be run
    that might update an extension attribute map.

    In addition the fixture backs up and restores the global attribute
    RESOURCES base on the boolean value of its backup_global_resources
    attribute.
    """

    def __init__(self, *api_definitions):
        """Create a new instance.

        Consumers can also control if the fixture should handle the global
        attribute RESOURCE map using the backup_global_resources of the
        fixture instance. If True the fixture will also handle
        neutron_lib.api.attributes.RESOURCES.

        :param api_definitions: Zero or more API definitions the fixture
        should handle. If no api_definitions are passed, the default is
        to handle all neutron_lib API definitions as well as the global
        RESOURCES attribute map.
        """
        self.definitions = api_definitions or definitions._ALL_API_DEFINITIONS
        self._orig_attr_maps = {}
        self._orig_resources = {}
        self.backup_global_resources = True

    def _setUp(self):
        for api_def in self.definitions:
            self._orig_attr_maps[api_def.ALIAS] = (
                api_def, {k: copy.deepcopy(v)
                          for k, v in api_def.RESOURCE_ATTRIBUTE_MAP.items()})
        if self.backup_global_resources:
            for resource, attrs in attributes.RESOURCES.items():
                self._orig_resources[resource] = copy.deepcopy(attrs)
        self.addCleanup(self._restore)

    def _restore(self):
        # clear + repopulate so consumer refs don't change
        for alias, def_and_map in self._orig_attr_maps.items():
            api_def, attr_map = def_and_map[0], def_and_map[1]
            api_def.RESOURCE_ATTRIBUTE_MAP.clear()
            api_def.RESOURCE_ATTRIBUTE_MAP.update(attr_map)
        if self.backup_global_resources:
            attributes.RESOURCES.clear()
            attributes.RESOURCES.update(self._orig_resources)

    @classmethod
    def all_api_definitions_fixture(cls):
        """Return a fixture that handles all neutron-lib api-defs."""
        return APIDefinitionFixture(*tuple(definitions._ALL_API_DEFINITIONS))


class PlacementAPIClientFixture(fixtures.Fixture):
    """Placement API client fixture.

    This class is intended to be used as a fixture within unit tests and
    therefore consumers must register it using useFixture() within their
    unit test class.
    """

    def __init__(self, placement_api_client):
        """Creates a new PlacementAPIClientFixture.

        :param placement_api_client: Placement API client object.
        """
        super().__init__()
        self.placement_api_client = placement_api_client

    def _setUp(self):
        self.addCleanup(self._restore)

        def mock_create_client():
            self.placement_api_client.client = mock.Mock()

        self._mock_create_client = mock.patch.object(
            self.placement_api_client, '_create_client',
            side_effect=mock_create_client)
        self._mock_get = mock.patch.object(self.placement_api_client, '_get')
        self._mock_post = mock.patch.object(self.placement_api_client, '_post')
        self._mock_put = mock.patch.object(self.placement_api_client, '_put')
        self._mock_delete = mock.patch.object(self.placement_api_client,
                                              '_delete')
        self._mock_create_client.start()
        self.mock_get = self._mock_get.start()
        self.mock_post = self._mock_post.start()
        self.mock_put = self._mock_put.start()
        self.mock_delete = self._mock_delete.start()

    def _restore(self):
        self._mock_create_client.stop()
        self._mock_get.stop()
        self._mock_post.stop()
        self._mock_put.stop()
        self._mock_delete.stop()


class DBRetryErrorsFixture(fixtures.Fixture):

    def __init__(self, **retry_kwargs):
        self._retry_kwargs = retry_kwargs
        self._patchers = []

    def _setUp(self):
        for k, v in self._retry_kwargs.items():
            patcher = mock.patch.object(db_api._retry_db_errors, k, new=v)
            patcher.start()
            self._patchers.append(patcher)
        self.addCleanup(self._restore)

    def _restore(self):
        for p in self._patchers:
            p.stop()


class DBAPIContextManagerFixture(fixtures.Fixture):

    def __init__(self, mock_context_manager=mock.ANY):
        self.cxt_manager = (mock.Mock() if mock_context_manager == mock.ANY
                            else mock_context_manager)
        self._backup_mgr = None

    def _setUp(self):
        self._backup_mgr = db_api._CTX_MANAGER
        db_api._CTX_MANAGER = self.cxt_manager
        self.addCleanup(self._restore)

    def _restore(self):
        db_api._CTX_MANAGER = self._backup_mgr


class DBQueryHooksFixture(fixtures.Fixture):

    def _setUp(self, query_hooks=None):
        self._backup = model_query._model_query_hooks
        model_query._model_query_hooks = query_hooks or {}
        self.addCleanup(self._restore)

    def _restore(self):
        model_query._model_query_hooks = self._backup


class RPCFixture(fixtures.Fixture):

    def _setUp(self):
        # don't actually start RPC listeners when testing
        mock.patch.object(rpc.Connection, 'consume_in_threads',
                          return_value=[]).start()
        self.useFixture(fixtures.MonkeyPatch(
            'oslo_messaging.Notifier', fake_notifier.FakeNotifier))

        self.messaging_conf = conffixture.ConfFixture(CONF)
        self.messaging_conf.transport_url = 'fake:/'
        # NOTE(russellb) We want all calls to return immediately.
        self.messaging_conf.response_timeout = 0
        self.useFixture(self.messaging_conf)

        self.addCleanup(rpc.cleanup)
        rpc.init(CONF)


class DBResourceExtendFixture(fixtures.Fixture):

    def __init__(self, extended_functions=None):
        self.extended_functions = extended_functions or {}

    def _setUp(self):
        self._backup = copy.deepcopy(
            resource_extend._resource_extend_functions)
        resource_extend._resource_extend_functions = self.extended_functions
        self.addCleanup(self._restore)

    def _restore(self):
        resource_extend._resource_extend_functions = self._backup


class OpenFixture(fixtures.Fixture):
    """Mock access to a specific file while preserving open for others."""

    def __init__(self, filepath, contents=''):
        self.path = filepath
        self.contents = contents

    def _setUp(self):
        self.mock_open = mock.mock_open(read_data=self.contents)
        self._orig_open = open

        def replacement_open(name, *args, **kwargs):
            method = self.mock_open if name == self.path else self._orig_open
            return method(name, *args, **kwargs)

        self._patch = mock.patch('builtins.open', new=replacement_open)
        self._patch.start()
        self.addCleanup(self._patch.stop)


class WarningsFixture(fixtures.Fixture):
    """Filters out warnings during test runs."""

    warning_types = (
        DeprecationWarning, PendingDeprecationWarning, ImportWarning
    )

    def __init__(self, module_re=None):
        """Create a new WarningsFixture.

        :param module_re: A list of regular expression strings that will be
            used with filterwarnings. Multiple expressions are or'd together.
        """
        self._modules = ['^neutron_lib\\.']
        if module_re:
            self._modules.extend(module_re)

    def _setUp(self):
        self.addCleanup(warnings.resetwarnings)
        for wtype in self.warning_types:
            warnings.filterwarnings(
                "once", category=wtype, module='|'.join(self._modules))
