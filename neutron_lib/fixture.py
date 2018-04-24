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

import fixtures
import mock

from neutron_lib.api import attributes
from neutron_lib.api import definitions
from neutron_lib.callbacks import manager
from neutron_lib.callbacks import registry
from neutron_lib.db import api as db_api
from neutron_lib.db import model_base
from neutron_lib.db import model_query
from neutron_lib.plugins import directory


class PluginDirectoryFixture(fixtures.Fixture):

    def __init__(self, plugin_directory=None):
        super(PluginDirectoryFixture, self).__init__()
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
        super(CallbackRegistryFixture, self).__init__()
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


class SqlFixture(fixtures.Fixture):

    # flag to indicate that the models have been loaded
    _TABLES_ESTABLISHED = False

    def _setUp(self):
        # Register all data models
        engine = db_api.get_context_manager().writer.get_engine()
        if not SqlFixture._TABLES_ESTABLISHED:
            model_base.BASEV2.metadata.create_all(engine)
            SqlFixture._TABLES_ESTABLISHED = True

        def clear_tables():
            with engine.begin() as conn:
                for table in reversed(
                        model_base.BASEV2.metadata.sorted_tables):
                    conn.execute(table.delete())

        self.addCleanup(clear_tables)


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
        super(PlacementAPIClientFixture, self).__init__()
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
