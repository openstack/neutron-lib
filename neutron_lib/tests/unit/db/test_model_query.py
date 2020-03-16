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

from neutron_lib.db import model_query
from neutron_lib import fixture
from neutron_lib.tests import _base
from neutron_lib.utils import helpers


# TODO(boden): find a way to test other model_query functions

class TestHooks(_base.BaseTestCase):

    def setUp(self):
        super(TestHooks, self).setUp()
        self.useFixture(fixture.DBQueryHooksFixture())

    def _mock_hook(self, x):
        return x

    def test_register_hook(self):
        mock_model = mock.Mock()
        model_query.register_hook(
            mock_model, 'hook1', self._mock_hook,
            self._mock_hook, result_filters=self._mock_hook)
        self.assertEqual(1, len(model_query._model_query_hooks.keys()))
        hook_ref = helpers.make_weak_ref(self._mock_hook)
        registered_hooks = model_query.get_hooks(mock_model)
        self.assertEqual(1, len(registered_hooks))
        for d in registered_hooks:
            for k in d.keys():
                self.assertEqual(hook_ref, d.get(k))

    def test_register_hook_non_callables(self):
        mock_model = mock.Mock()
        model_query.register_hook(
            mock_model, 'hook1', self._mock_hook, {}, result_filters={})
        self.assertEqual(1, len(model_query._model_query_hooks.keys()))
        hook_ref = helpers.make_weak_ref(self._mock_hook)
        registered_hooks = model_query.get_hooks(mock_model)
        self.assertEqual(1, len(registered_hooks))
        for d in registered_hooks:
            for k in d.keys():
                if k == 'query':
                    self.assertEqual(hook_ref, d.get(k))
                else:
                    self.assertEqual({}, d.get(k))

    def test_get_values(self):
        mock_model = mock.Mock()
        mock_context = mock.Mock()
        with mock.patch.object(
                model_query, 'query_with_hooks') as query_with_hooks:
            query_with_hooks.return_value = [['value1'], ['value2']]
            values = model_query.get_values(mock_context, mock_model,
                                            'fake_field')
        self.assertEqual(['value1', 'value2'], values)
        query_with_hooks.assert_called_with(
            mock_context, mock_model, field='fake_field')
