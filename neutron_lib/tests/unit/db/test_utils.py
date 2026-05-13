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

from unittest import mock

from oslo_config import cfg
from oslo_db.sqlalchemy import models
import sqlalchemy as sa
from sqlalchemy import orm

from neutron_lib.api import attributes
from neutron_lib import context
from neutron_lib.db import utils
from neutron_lib import exceptions as n_exc

from neutron_lib.tests import _base as base


class ModelBaseV2(orm.DeclarativeBase, models.ModelBase):
    pass


class FakePort(ModelBaseV2):
    __tablename__ = 'fakeports'
    port_id = sa.Column(sa.String(36), primary_key=True)
    name = sa.Column(sa.String(64))
    status = sa.Column(sa.String(16), nullable=False)


class FakeRouter(ModelBaseV2):
    __tablename__ = 'fakerouters'
    router_id = sa.Column(sa.String(36), primary_key=True)
    gw_port_id = sa.Column(sa.String(36), sa.ForeignKey(FakePort.port_id))
    gw_port = orm.relationship(FakePort, lazy='joined')


class TestUtilsLegacyPolicies(base.BaseTestCase):

    def setUp(self):
        cfg.CONF.set_override('enforce_scope', False, group='oslo_policy')
        super().setUp()

    def test_get_sort_dirs(self):
        sorts = [(1, True), (2, False), (3, True)]
        self.assertEqual(['asc', 'desc', 'asc'],
                         utils.get_sort_dirs(sorts))

    def test_get_sort_dirs_reversed(self):
        sorts = [(1, True), (2, False), (3, True)]
        self.assertEqual(['desc', 'asc', 'desc'],
                         utils.get_sort_dirs(sorts, page_reverse=True))

    def test_get_and_validate_sort_keys(self):
        sorts = [('name', False), ('status', True)]
        self.assertEqual(['name', 'status'],
                         utils.get_and_validate_sort_keys(sorts, FakePort))

    def test_get_and_validate_sort_keys_bad_key_fails(self):
        sorts = [('master', True)]
        self.assertRaises(n_exc.BadRequest,
                          utils.get_and_validate_sort_keys, sorts, FakePort)

    def test_get_and_validate_sort_keys_by_relationship_fails(self):
        sorts = [('gw_port', True)]
        self.assertRaises(n_exc.BadRequest,
                          utils.get_and_validate_sort_keys, sorts, FakeRouter)

    def test_get_marker_obj(self):
        plugin = mock.Mock()
        plugin._get_myr.return_value = 'obj'
        obj = utils.get_marker_obj(plugin, 'ctx', 'myr', 10, mock.ANY)
        self.assertEqual('obj', obj)
        plugin._get_myr.assert_called_once_with('ctx', mock.ANY)

    def test_get_marker_obj_no_limit_and_marker(self):
        self.assertIsNone(utils.get_marker_obj(
            mock.Mock(), 'ctx', 'myr', 0, mock.ANY))
        self.assertIsNone(utils.get_marker_obj(
            mock.Mock(), 'ctx', 'myr', 10, None))

    @mock.patch.object(attributes, 'populate_project_info')
    def test_resource_fields(self, mock_populate):
        r = {
            'name': 'n',
            'id': '1',
            'desc': None
        }
        utils.resource_fields(r, ['name'])
        mock_populate.assert_called_once_with({'name': 'n'})

    def test_model_query_scope_is_project_admin(self):
        ctx = context.Context(
            project_id='some project',
            is_admin=True,
            is_advsvc=False)
        model = mock.Mock(project_id='project')

        self.assertFalse(
            utils.model_query_scope_is_project(ctx, model))

        # Ensure that project_id isn't mocked
        del model.project_id
        self.assertFalse(
            utils.model_query_scope_is_project(ctx, model))

    def test_model_query_scope_is_project_advsvc(self):
        ctx = context.Context(
            project_id='some project',
            is_admin=False,
            is_advsvc=True)
        model = mock.Mock(project_id='project')

        self.assertFalse(
            utils.model_query_scope_is_project(ctx, model))

        # Ensure that project_id isn't mocked
        del model.project_id
        self.assertFalse(
            utils.model_query_scope_is_project(ctx, model))

    def test_model_query_scope_is_project_service_role(self):
        ctx = context.Context(
            project_id='some project',
            is_admin=False,
            roles=['service'])
        model = mock.Mock(project_id='project')

        self.assertFalse(
            utils.model_query_scope_is_project(ctx, model))

        # Ensure that project_id isn't mocked
        del model.project_id
        self.assertFalse(
            utils.model_query_scope_is_project(ctx, model))

    def test_model_query_scope_is_project_regular_user(self):
        ctx = context.Context(
            project_id='some project',
            is_admin=False,
            is_advsvc=False)
        model = mock.Mock(project_id='project')

        self.assertTrue(
            utils.model_query_scope_is_project(ctx, model))

        # Ensure that project_id isn't mocked
        del model.project_id
        self.assertFalse(
            utils.model_query_scope_is_project(ctx, model))

    def test_model_query_scope_is_project_system_scope(self):
        ctx = context.Context(system_scope='all')
        model = mock.Mock(project_id='project')

        self.assertTrue(
            utils.model_query_scope_is_project(ctx, model))

        # Ensure that project_id isn't mocked
        del model.project_id
        self.assertFalse(
            utils.model_query_scope_is_project(ctx, model))


class TestContextIfTransaction(base.BaseTestCase):

    @mock.patch('neutron_lib.db.api.CONTEXT_WRITER')
    def test_context_if_transaction_writer(self, mock_writer):
        ctx = mock.Mock()
        result = utils.context_if_transaction(ctx, transaction=True,
                                              writer=True)
        mock_writer.using.assert_called_once_with(ctx)
        self.assertEqual(mock_writer.using.return_value, result)

    @mock.patch('neutron_lib.db.api.CONTEXT_READER')
    def test_context_if_transaction_reader(self, mock_reader):
        ctx = mock.Mock()
        result = utils.context_if_transaction(ctx, transaction=True,
                                              writer=False)
        mock_reader.using.assert_called_once_with(ctx)
        self.assertEqual(mock_reader.using.return_value, result)

    def test_context_if_transaction_no_transaction(self):
        ctx = mock.Mock()
        cm = utils.context_if_transaction(ctx, transaction=False)
        with cm:
            pass


class TestSafeCreation(base.BaseTestCase):

    def test_safe_creation_success(self):
        ctx = mock.Mock()
        create_fn = mock.Mock(return_value={'id': 'obj-1'})
        updated = {'id': 'obj-1', 'extra': 'data'}
        create_bindings = mock.Mock(return_value=(updated, 'value'))
        delete_fn = mock.Mock()

        with mock.patch.object(utils, 'context_if_transaction',
                               return_value=utils._noop_context_manager()):
            obj, value = utils.safe_creation(
                ctx, create_fn, delete_fn, create_bindings)

        self.assertEqual(updated, obj)
        self.assertEqual('value', value)
        create_bindings.assert_called_once_with('obj-1')
        delete_fn.assert_not_called()

    def test_safe_creation_bindings_fail_triggers_delete(self):
        ctx = mock.Mock()
        create_fn = mock.Mock(return_value={'id': 'obj-1'})
        create_bindings = mock.Mock(side_effect=ValueError)
        delete_fn = mock.Mock()

        with mock.patch.object(utils, 'context_if_transaction',
                               return_value=utils._noop_context_manager()):
            self.assertRaises(ValueError, utils.safe_creation,
                              ctx, create_fn, delete_fn, create_bindings)
        delete_fn.assert_called_once_with('obj-1')

    def test_safe_creation_delete_also_fails(self):
        ctx = mock.Mock()
        create_fn = mock.Mock(return_value={'id': 'obj-1'})
        create_bindings = mock.Mock(side_effect=ValueError)
        delete_fn = mock.Mock(side_effect=EnvironmentError)

        with mock.patch.object(utils, 'context_if_transaction',
                               return_value=utils._noop_context_manager()):
            self.assertRaises(ValueError, utils.safe_creation,
                              ctx, create_fn, delete_fn, create_bindings)
        delete_fn.assert_called_once_with('obj-1')

    def test_safe_creation_returns_original_when_updated_is_none(self):
        ctx = mock.Mock()
        original = {'id': 'obj-1'}
        create_fn = mock.Mock(return_value=original)
        create_bindings = mock.Mock(return_value=(None, 'value'))
        delete_fn = mock.Mock()

        with mock.patch.object(utils, 'context_if_transaction',
                               return_value=utils._noop_context_manager()):
            obj, value = utils.safe_creation(
                ctx, create_fn, delete_fn, create_bindings)

        self.assertEqual(original, obj)
        self.assertEqual('value', value)


class TestUtilsWithScopeEnforcement(TestUtilsLegacyPolicies):

    def setUp(self):
        super().setUp()
        cfg.CONF.set_override('enforce_scope', True, group='oslo_policy')
