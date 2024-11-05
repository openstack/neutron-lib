# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from unittest import mock

from neutron_lib import context
from neutron_lib.policy import _engine as policy_engine

from neutron_lib.tests import _base as base


class TestPolicyEnforcer(base.BaseTestCase):
    def setUp(self):
        super().setUp()
        # Isolate one _ROLE_ENFORCER per test case
        mock.patch.object(policy_engine, '_ROLE_ENFORCER', None).start()

    def test_init_reset(self):
        self.assertIsNone(policy_engine._ROLE_ENFORCER)
        policy_engine.init()
        self.assertIsNotNone(policy_engine._ROLE_ENFORCER)

    def test_check_user_is_not_admin(self):
        ctx = context.Context('me', 'my_project')
        self.assertFalse(policy_engine.check_is_admin(ctx))

    def test_check_user_elevated_is_admin(self):
        ctx = context.Context('me', 'my_project', roles=['user']).elevated()
        self.assertTrue(policy_engine.check_is_admin(ctx))

    def test_check_is_admin_no_roles_no_admin(self):
        policy_engine.init(policy_file='dummy_policy.yaml')
        ctx = context.Context('me', 'my_project', roles=['user']).elevated()
        # With no admin role, elevated() should not work.
        self.assertFalse(policy_engine.check_is_admin(ctx))

    def test_check_user_elevated_is_admin_with_default_policy(self):
        policy_engine.init(policy_file='no_policy.yaml')
        ctx = context.Context('me', 'my_project', roles=['user']).elevated()
        self.assertTrue(policy_engine.check_is_admin(ctx))

    def test_check_is_advsvc_role(self):
        ctx = context.Context('me', 'my_project', roles=['advsvc'])
        self.assertTrue(policy_engine.check_is_advsvc(ctx))

    def test_check_is_not_advsvc_user(self):
        ctx = context.Context('me', 'my_project', roles=['user'])
        self.assertFalse(policy_engine.check_is_advsvc(ctx))

    def test_check_is_not_advsvc_admin(self):
        ctx = context.Context('me', 'my_project').elevated()
        self.assertTrue(policy_engine.check_is_admin(ctx))
        self.assertFalse(policy_engine.check_is_advsvc(ctx))

    def test_check_is_advsvc_no_roles_no_advsvc(self):
        policy_engine.init(policy_file='dummy_policy.yaml')
        ctx = context.Context('me', 'my_project', roles=['advsvc'])
        # No advsvc role in the policy file, so cannot assume the role.
        self.assertFalse(policy_engine.check_is_advsvc(ctx))

    def test_check_is_advsvc_role_with_default_policy(self):
        policy_engine.init(policy_file='no_policy.yaml')
        ctx = context.Context('me', 'my_project', roles=['advsvc'])
        self.assertTrue(policy_engine.check_is_advsvc(ctx))

    def test_check_is_service_role(self):
        ctx = context.Context('me', 'my_project', roles=['service'])
        self.assertTrue(policy_engine.check_is_service_role(ctx))

    def test_check_is_not_service_role_user(self):
        ctx = context.Context('me', 'my_project', roles=['member'])
        self.assertFalse(policy_engine.check_is_service_role(ctx))

    def test_check_is_not_service_role_admin(self):
        ctx = context.Context('me', 'my_project').elevated()
        self.assertTrue(policy_engine.check_is_admin(ctx))
        self.assertFalse(policy_engine.check_is_service_role(ctx))

    def test_check_is_service_role_no_roles_no_service_role(self):
        policy_engine.init(policy_file='dummy_policy.yaml')
        ctx = context.Context('me', 'my_project', roles=['service'])
        # No service role in the policy file, so cannot assume the role.
        self.assertFalse(policy_engine.check_is_service_role(ctx))

    def test_check_is_service_role_with_default_policy(self):
        policy_engine.init(policy_file='no_policy.yaml')
        ctx = context.Context('me', 'my_project', roles=['service'])
        self.assertTrue(policy_engine.check_is_service_role(ctx))
