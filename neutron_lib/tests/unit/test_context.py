#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from unittest import mock

from oslo_config import cfg
from oslo_context import context as oslo_context
from testtools import matchers

from neutron_lib import context
from neutron_lib.tests import _base


class TestNeutronContext(_base.BaseTestCase):

    def setUp(self):
        super().setUp()
        db_api = 'neutron_lib.db.api.get_writer_session'
        self._db_api_session_patcher = mock.patch(db_api)
        self.db_api_session = self._db_api_session_patcher.start()

    def test_neutron_context_create_positional(self):
        ctx = context.Context('user_id', 'project_id')
        self.assertEqual('user_id', ctx.user_id)
        self.assertEqual('project_id', ctx.project_id)
        self.assertEqual('project_id', ctx.tenant_id)
        request_id = ctx.request_id
        if isinstance(request_id, bytes):
            request_id = request_id.decode('utf-8')
        self.assertThat(request_id, matchers.StartsWith('req-'))
        self.assertIsNone(ctx.user_name)
        self.assertIsNone(ctx.tenant_name)
        self.assertIsNone(ctx.project_name)
        self.assertIsNone(ctx.auth_token)

    def _test_neutron_context_create(self, project_id, tenant_id):
        p_id = project_id or tenant_id
        ctx = context.Context('user_id', project_id=project_id,
                              tenant_id=tenant_id)
        self.assertEqual('user_id', ctx.user_id)
        self.assertEqual(p_id, ctx.project_id)
        self.assertEqual(p_id, ctx.tenant_id)
        request_id = ctx.request_id
        if isinstance(request_id, bytes):
            request_id = request_id.decode('utf-8')
        self.assertThat(request_id, matchers.StartsWith('req-'))
        self.assertIsNone(ctx.user_name)
        self.assertIsNone(ctx.tenant_name)
        self.assertIsNone(ctx.project_name)
        self.assertIsNone(ctx.auth_token)

    def test_neutron_context_create(self):
        self._test_neutron_context_create('project_id', None)

    def test_neutron_context_create_tenant_id(self):
        self._test_neutron_context_create(None, 'tenant_id')

    def _test_neutron_context_getter_setter(self, project_id, tenant_id):
        p_id = project_id or tenant_id
        ctx = context.Context('Anakin', project_id=project_id,
                              tenant_id=tenant_id)
        self.assertEqual('Anakin', ctx.user_id)
        self.assertEqual(p_id, ctx.tenant_id)
        ctx.user_id = 'Darth'
        ctx.project_id = 'Vader'
        self.assertEqual('Darth', ctx.user_id)
        self.assertEqual('Vader', ctx.tenant_id)
        self.assertEqual('Vader', ctx.project_id)

    def test_neutron_context_getter_setter(self):
        self._test_neutron_context_getter_setter('Skywalker', None)

    def test_neutron_context_getter_setter_tenant_id(self):
        self._test_neutron_context_getter_setter(None, 'Skywalker')

    def _test_neutron_context_create_with_name(
            self, project_name, tenant_name):
        project_name = project_name or tenant_name
        ctx = context.Context('user_id', 'project_id',
                              tenant_name=tenant_name, user_name='user_name',
                              project_name=project_name)
        # Check name is set
        self.assertEqual('user_name', ctx.user_name)
        self.assertEqual(project_name, ctx.tenant_name)
        self.assertEqual(project_name, ctx.project_name)
        # Check user/tenant contains its ID even if user/tenant_name is passed
        self.assertEqual('user_id', ctx.user_id)
        self.assertEqual('project_id', ctx.project_id)
        self.assertEqual('project_id', ctx.tenant_id)

    def test_neutron_context_create_with_name(self):
        self._test_neutron_context_create_with_name('project_name', None)

    def test_neutron_context_create_with_name_tenant_name(self):
        self._test_neutron_context_create_with_name(None, 'tenant_name')

    def test_neutron_context_create_with_request_id(self):
        ctx = context.Context('user_id', 'project_id', request_id='req_id_xxx')
        self.assertEqual('req_id_xxx', ctx.request_id)

    def test_neutron_context_create_with_timestamp(self):
        now = "Right Now!"
        ctx = context.Context('user_id', 'project_id', timestamp=now)
        self.assertEqual(now, ctx.timestamp)

    def test_neutron_context_create_is_advsvc(self):
        ctx = context.Context('user_id', 'project_id', is_advsvc=True)
        self.assertFalse(ctx.is_admin)
        self.assertTrue(ctx.is_advsvc)
        self.assertFalse(ctx.has_global_access)

    def test_neutron_context_create_is_service_role(self):
        ctx = context.Context('user_id', 'project_id', roles=['service'])
        self.assertFalse(ctx.is_admin)
        self.assertTrue(ctx.is_service_role)
        self.assertFalse(ctx.has_global_access)

    def test_neutron_context_create_with_auth_token(self):
        ctx = context.Context('user_id', 'project_id',
                              auth_token='auth_token_xxx')
        self.assertEqual('auth_token_xxx', ctx.auth_token)

    def test_neutron_context_from_dict(self):
        owner = {'user_id': 'Luke', 'project_id': 'Skywalker'}
        ctx = context.Context.from_dict(owner)
        self.assertEqual(owner['user_id'], ctx.user_id)
        self.assertEqual(owner['project_id'], ctx.project_id)
        self.assertEqual(owner['project_id'], ctx.tenant_id)

    def _test_neutron_context_from_dict_validate(
            self, project_id, project_name, tenant_id, tenant_name):
        project_id = project_id or tenant_id
        project_name = project_name or tenant_name
        ctx = context.Context(user_id='user_id1',
                              user_name='user',
                              project_id=project_id,
                              project_name=project_name,
                              tenant_id=tenant_id,
                              tenant_name=tenant_name,
                              request_id='request_id1',
                              auth_token='auth_token1')
        values = {'user_id': 'user_id1',
                  'user_name': 'user',
                  'project_id': project_id,
                  'project_name': project_name,
                  'tenant_id': project_id,
                  'tenant_name': project_name,
                  'request_id': 'request_id1',
                  'auth_token': 'auth_token1'}
        ctx2 = context.Context.from_dict(values)

        ctx_dict = ctx.to_dict()
        ctx_dict.pop('timestamp')
        ctx2_dict = ctx2.to_dict()
        ctx2_dict.pop('timestamp')
        self.assertEqual(ctx_dict, ctx2_dict)

    def test_neutron_context_from_dict_validate(self):
        self._test_neutron_context_from_dict_validate(
            'project_id', 'project_name', None, None)

    def test_neutron_context_from_dict_validate_tenant(self):
        self._test_neutron_context_from_dict_validate(
            None, None, 'tenant_id', 'tenant_name')

    def _test_neutron_context_to_dict(self, project_id, tenant_id):
        project_id = project_id or tenant_id
        ctx = context.Context('user_id', project_id, tenant_id=tenant_id)
        ctx_dict = ctx.to_dict()
        self.assertEqual('user_id', ctx_dict['user_id'])
        self.assertEqual(project_id, ctx_dict['project_id'])
        self.assertEqual(project_id, ctx_dict['tenant_id'])
        self.assertEqual(ctx.request_id, ctx_dict['request_id'])
        self.assertEqual('user_id', ctx_dict['user'])
        self.assertIsNone(ctx_dict['user_name'])
        self.assertIsNone(ctx_dict['tenant_name'])
        self.assertIsNone(ctx_dict['project_name'])
        self.assertIsNone(ctx_dict['auth_token'])

    def test_neutron_context_to_dict(self):
        self._test_neutron_context_to_dict('project_id', None)

    def test_neutron_context_to_dict_tenant(self):
        self._test_neutron_context_to_dict(None, 'tenant_id')

    def _test_neutron_context_to_dict_with_name(
            self, project_name, tenant_name):
        project_name = project_name or tenant_name
        ctx = context.Context('user_id', 'project_id',
                              project_name=project_name,
                              tenant_name=tenant_name,
                              user_name='user_name')
        ctx_dict = ctx.to_dict()
        self.assertEqual('user_name', ctx_dict['user_name'])
        self.assertEqual(project_name, ctx_dict['tenant_name'])
        self.assertEqual(project_name, ctx_dict['project_name'])

    def test_neutron_context_to_dict_with_name(self):
        self._test_neutron_context_to_dict_with_name('project_name', None)

    def test_neutron_context_to_dict_with_name_tenant(self):
        self._test_neutron_context_to_dict_with_name(None, 'tenant_name')

    def test_neutron_context_to_dict_with_auth_token(self):
        ctx = context.Context('user_id', 'project_id',
                              auth_token='auth_token_xxx')
        ctx_dict = ctx.to_dict()
        self.assertEqual('auth_token_xxx', ctx_dict['auth_token'])

    def test_neutron_context_admin_to_dict(self):
        self.db_api_session.return_value = 'fakesession'
        ctx = context.get_admin_context()
        ctx_dict = ctx.to_dict()
        self.assertIsNone(ctx_dict['user_id'])
        self.assertIsNone(ctx_dict['project_id'])
        self.assertIsNone(ctx_dict['tenant_id'])
        self.assertIsNone(ctx_dict['auth_token'])
        self.assertTrue(ctx_dict['is_admin'])
        self.assertTrue(ctx_dict['has_global_access'])
        self.assertIn('admin', ctx_dict['roles'])
        self.assertIsNotNone(ctx.session)
        self.assertNotIn('session', ctx_dict)

    def test_neutron_context_admin_without_session_to_dict(self):
        ctx = context.get_admin_context_without_session()
        ctx_dict = ctx.to_dict()
        self.assertIsNone(ctx_dict['user_id'])
        self.assertIsNone(ctx_dict['project_id'])
        self.assertIsNone(ctx_dict['tenant_id'])
        self.assertIsNone(ctx_dict['auth_token'])
        self.assertIn('admin', ctx_dict['roles'])
        self.assertFalse(hasattr(ctx, 'session'))

    def test_neutron_context_elevated_retains_request_id(self):
        expected_roles = ['admin', 'member', 'reader']
        ctx = context.Context('user_id', 'project_id')
        self.assertFalse(ctx.is_admin)
        req_id_before = ctx.request_id

        elevated_ctx = ctx.elevated()
        self.assertTrue(elevated_ctx.is_admin)
        self.assertEqual(req_id_before, elevated_ctx.request_id)
        for expected_role in expected_roles:
            self.assertIn(expected_role, elevated_ctx.roles)

    def test_neutron_context_elevated_idempotent(self):
        ctx = context.Context('user_id', 'project_id')
        expected_roles = ['admin', 'member', 'reader']
        self.assertFalse(ctx.is_admin)
        elevated_ctx = ctx.elevated()
        self.assertTrue(elevated_ctx.is_admin)
        for expected_role in expected_roles:
            self.assertIn(expected_role, elevated_ctx.roles)
        elevated2_ctx = elevated_ctx.elevated()
        self.assertTrue(elevated2_ctx.is_admin)
        for expected_role in expected_roles:
            self.assertIn(expected_role, elevated_ctx.roles)

    def test_neutron_context_elevated_system_scope_for_new_policies(self):
        cfg.CONF.set_override('enforce_scope', True, group='oslo_policy')
        expected_roles = ['admin', 'member', 'reader']
        ctx = context.Context('user_id', 'project_id')
        self.assertFalse(ctx.is_admin)
        self.assertNotEqual('all', ctx.system_scope)
        elevated_ctx = ctx.elevated()
        self.assertTrue(elevated_ctx.is_admin)
        self.assertTrue(elevated_ctx.has_global_access)
        for expected_role in expected_roles:
            self.assertIn(expected_role, elevated_ctx.roles)
        # make sure we do not set the system scope in context
        self.assertNotEqual('all', elevated_ctx.system_scope)

    def test_neutron_context_elevated_keeps_custom_roles(self):
        expected_admin_roles = ['admin', 'member', 'reader']
        custom_roles = ['custom_role']
        ctx = context.Context('user_id', 'project_id', roles=custom_roles)
        self.assertFalse(ctx.is_admin)
        self.assertFalse(ctx.has_global_access)
        self.assertNotEqual('all', ctx.system_scope)
        for expected_admin_role in expected_admin_roles:
            self.assertNotIn(expected_admin_role, ctx.roles)
        for custom_role in custom_roles:
            self.assertIn(custom_role, ctx.roles)

        elevated_ctx = ctx.elevated()
        self.assertTrue(elevated_ctx.is_admin)
        self.assertTrue(elevated_ctx.has_global_access)
        for expected_admin_role in expected_admin_roles:
            self.assertIn(expected_admin_role, elevated_ctx.roles)
        for custom_role in custom_roles:
            self.assertIn(custom_role, ctx.roles)

    def test_neutron_context_overwrite(self):
        ctx1 = context.Context('user_id', 'project_id')
        self.assertEqual(ctx1.request_id,
                         oslo_context.get_current().request_id)

        # If overwrite is not specified, request_id should be updated.
        ctx2 = context.Context('user_id', 'project_id')
        self.assertNotEqual(ctx2.request_id, ctx1.request_id)
        self.assertEqual(ctx2.request_id,
                         oslo_context.get_current().request_id)

        # If overwrite is specified, request_id should be kept.
        ctx3 = context.Context('user_id', 'project_id', overwrite=False)
        self.assertNotEqual(ctx3.request_id, ctx2.request_id)
        self.assertEqual(ctx2.request_id,
                         oslo_context.get_current().request_id)

    def test_neutron_context_get_admin_context_not_update_local_store(self):
        ctx = context.Context('user_id', 'project_id')
        req_id_before = oslo_context.get_current().request_id
        self.assertEqual(ctx.request_id, req_id_before)

        ctx_admin = context.get_admin_context()
        self.assertEqual(req_id_before, oslo_context.get_current().request_id)
        self.assertNotEqual(req_id_before, ctx_admin.request_id)

    def test_neutron_context_has_global_access(self):
        with mock.patch('neutron_lib.policy._engine.check_has_global_access',
                        return_value=False):
            ctx = context.Context('user_id', 'project_id')
            self.assertFalse(ctx.has_global_access)

        with mock.patch('neutron_lib.policy._engine.check_has_global_access',
                        return_value=True):
            ctx = context.Context('user_id', 'project_id')
            self.assertTrue(ctx.has_global_access)

    def test_to_policy_values(self):
        values = {
            'user_id': 'user_id',
            'project_id': 'project_id',
            'is_admin': 'is_admin',
            'project_name': 'project_name',
            'user_name': 'user_name',
            'domain_id': 'domain',
            'user_domain_id': 'user_domain',
            'project_domain_id': 'project_domain',
        }
        additional_values = {
            'user': 'user_id',
            'tenant': 'project_id',
            'tenant_id': 'project_id',
            'tenant_name': 'project_name',
        }
        ctx = context.Context(**values)
        # apply dict() to get a real dictionary, needed for newer oslo.context
        # that returns _DeprecatedPolicyValues object instead
        policy_values = dict(ctx.to_policy_values())
        self.assertDictSupersetOf(values, policy_values)
        self.assertDictSupersetOf(additional_values, policy_values)

    def test_session_cached(self):
        ctx = context.Context('user_id', 'project_id')
        session1 = ctx.session
        session2 = ctx.session
        self.assertIs(session1, session2)

    def test_add_get_remove_constraint(self):
        ctx = context.Context('user_id', 'project_id')
        self.assertIsNone(ctx.get_transaction_constraint())
        ctx.set_transaction_constraint('networks', 'net_id', 44)
        constraint = ctx.get_transaction_constraint()
        self.assertEqual(44, constraint.if_revision_match)
        self.assertEqual('networks', constraint.resource)
        self.assertEqual('net_id', constraint.resource_id)
        ctx.clear_transaction_constraint()
        self.assertIsNone(ctx.get_transaction_constraint())
