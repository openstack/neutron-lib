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

from stevedore import enabled

from neutron_lib.tests import _base as base
from neutron_lib.utils import runtime


class _DummyDriver(object):
    driver = mock.sentinel.dummy_driver


class TestRunTime(base.BaseTestCase):

    @mock.patch.object(runtime, 'LOG')
    def test_load_class_by_alias_or_classname_no_name(self, mock_log):
        self.assertRaises(
            ImportError,
            runtime.load_class_by_alias_or_classname, 'ns', None)

    @mock.patch.object(runtime.driver, 'DriverManager',
                       return_value=_DummyDriver)
    @mock.patch.object(runtime, 'LOG')
    def test_load_class_by_alias_or_classname_dummy_driver(
            self, mock_log, mock_driver):
        self.assertEqual(_DummyDriver.driver,
                         runtime.load_class_by_alias_or_classname('ns', 'n'))

    @mock.patch.object(runtime, 'LOG')
    def test_load_class_by_alias_or_classname_bad_classname(self, mock_log):
        self.assertRaises(
            ImportError,
            runtime.load_class_by_alias_or_classname, 'ns', '_NoClass')

    @mock.patch.object(runtime.importutils, 'import_class',
                       return_value=mock.sentinel.dummy_class)
    @mock.patch.object(runtime, 'LOG')
    def test_load_class_by_alias_or_classname_with_classname(
            self, mock_log, mock_import):
        self.assertEqual(
            mock.sentinel.dummy_class,
            runtime.load_class_by_alias_or_classname('ns', 'n'))


class TestNamespacedPlugins(base.BaseTestCase):

    @mock.patch.object(enabled, 'EnabledExtensionManager')
    def test_init_reload(self, mock_mgr):
        plugins = runtime.NamespacedPlugins('_test_ns_')
        mock_mgr.assert_called_with(
            '_test_ns_', mock.ANY, invoke_on_load=False)
        mock_mgr().map.assert_called_with(plugins._add_extension)

    @mock.patch.object(runtime, 'LOG')
    @mock.patch.object(enabled, 'EnabledExtensionManager')
    def test_init_reload_no_plugins(self, mock_mgr, mock_log):
        mock_mgr().names.return_value = []
        plugins = runtime.NamespacedPlugins('_test_ns_')
        mock_log.debug.assert_called_once()
        mock_mgr().map.assert_not_called()
        self.assertDictEqual({}, plugins._extensions)

    @mock.patch.object(enabled, 'EnabledExtensionManager')
    def test_add_duplicate_names(self, mock_mgr):
        mock_ep = mock.Mock()
        mock_ep.name = 'a'
        mock_mgr().names.return_value = ['a', 'a']
        # return 2 EPs with the same name
        mock_mgr().map = lambda f: [f(ep) for ep in [mock_ep, mock_ep]]
        self.assertRaises(KeyError, runtime.NamespacedPlugins, '_test_ns_')

    @mock.patch.object(enabled, 'EnabledExtensionManager')
    def test_get_plugin_class(self, mock_mgr):
        mock_epa = mock.Mock()
        mock_epa.name = 'a'
        mock_epa.plugin = 'A'
        mock_epb = mock.Mock()
        mock_epb.name = 'b'
        mock_epb.plugin = 'B'
        mock_mgr().names.return_value = ['a', 'b']
        mock_mgr().map = lambda f: [f(ep) for ep in [mock_epa, mock_epb]]

        plugins = runtime.NamespacedPlugins('_test_ns_')
        self.assertEqual('A', plugins.get_plugin_class('a'))
        self.assertEqual('B', plugins.get_plugin_class('b'))

    @mock.patch.object(enabled, 'EnabledExtensionManager')
    def test_new_plugin_instance(self, mock_mgr):
        mock_epa = mock.Mock()
        mock_epa.name = 'a'
        mock_epb = mock.Mock()
        mock_epb.name = 'b'
        mock_mgr().names.return_value = ['a', 'b']
        mock_mgr().map = lambda f: [f(ep) for ep in [mock_epa, mock_epb]]

        plugins = runtime.NamespacedPlugins('_test_ns_')
        plugins.new_plugin_instance('a', 'c', 'd', karg='kval')
        plugins.new_plugin_instance('b')
        mock_epa.plugin.assert_called_once_with('c', 'd', karg='kval')
        mock_epb.plugin.assert_called_once_with()


class TestListPackageModules(base.BaseTestCase):

    def test_list_package_modules(self):
        # mainly just to ensure we can import modules for both PY2/PY3
        self.assertGreater(
            len(runtime.list_package_modules('neutron_lib.exceptions')), 3)
