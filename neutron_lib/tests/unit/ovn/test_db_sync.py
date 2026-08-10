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

import tempfile
from unittest import mock

from oslo_config import cfg

from neutron_lib.ovn import db_sync
from neutron_lib.tests import _base as base


class TestBaseOvnDbSynchronizer(base.BaseTestCase):

    def setUp(self):
        super().setUp()
        self.core_plugin = mock.Mock()
        self.ovn_driver = mock.Mock()
        self.ovn_driver.nb_ovn = mock.Mock()
        self.ovn_driver.sb_ovn = mock.Mock()

    def _create_synchronizer(self):
        class TestSynchronizer(db_sync.BaseOvnDbSynchronizer):
            def do_sync(self):
                pass

        return TestSynchronizer(
            self.core_plugin, self.ovn_driver, 'repair')

    @mock.patch('neutron_lib.ovn.db_sync.threading.Thread')
    @mock.patch('neutron_lib.ovn.db_sync.time.sleep')
    def test_sync_with_default_delay(self, mock_sleep, mock_thread):
        synchronizer = self._create_synchronizer()
        mock_thread_instance = mock.Mock()
        mock_thread.return_value = mock_thread_instance

        synchronizer.sync()

        # Verify sleep was called with default delay
        mock_sleep.assert_called_once_with(10)
        # Verify thread was created with correct target
        mock_thread.assert_called_once_with(target=synchronizer.do_sync)
        # Verify thread was started
        mock_thread_instance.start.assert_called_once()

    @mock.patch('neutron_lib.ovn.db_sync.threading.Thread')
    @mock.patch('neutron_lib.ovn.db_sync.time.sleep')
    def test_sync_with_custom_delay(self, mock_sleep, mock_thread):
        synchronizer = self._create_synchronizer()
        mock_thread_instance = mock.Mock()
        mock_thread.return_value = mock_thread_instance

        synchronizer.sync(delay_seconds=5)

        # Verify sleep was called with custom delay
        mock_sleep.assert_called_once_with(5)
        mock_thread.assert_called_once_with(target=synchronizer.do_sync)
        mock_thread_instance.start.assert_called_once()

    @mock.patch('neutron_lib.ovn.db_sync.threading.Thread')
    @mock.patch('neutron_lib.ovn.db_sync.time.sleep')
    def test_stop_after_sync(self, mock_sleep, mock_thread):
        synchronizer = self._create_synchronizer()
        mock_thread_instance = mock.Mock()
        mock_thread.return_value = mock_thread_instance

        synchronizer.sync()
        synchronizer.stop()

        # Verify thread join was called
        mock_thread_instance.join.assert_called_once()

    def test_stop_without_sync(self):
        synchronizer = self._create_synchronizer()

        # Should not raise an exception
        synchronizer.stop()

    def test_single_level_inheritance_with_requirements(self):
        class DummySynchronizer(db_sync.BaseOvnDbSynchronizer):
            _required_mechanism_drivers = ['driver1', 'driver2']
            _required_service_plugins = ['plugin1']
            _required_ml2_ext_drivers = ['ext_driver1']

            def do_sync(self):
                pass

        self.assertEqual(['driver1', 'driver2'],
                         sorted(DummySynchronizer.
                                get_required_mechanism_drivers()))
        self.assertEqual(['plugin1'],
                         DummySynchronizer.get_required_service_plugins())
        self.assertEqual(['ext_driver1'],
                         DummySynchronizer.
                         get_required_ml2_extension_drivers())

    def test_multi_level_inheritance(self):
        class FirstLevelSynchronizer(db_sync.BaseOvnDbSynchronizer):
            _required_mechanism_drivers = ['driver1', 'driver2']
            _required_service_plugins = ['plugin1']
            _required_ml2_ext_drivers = ['ext_driver1']

            def do_sync(self):
                pass

        class SecondLevelSynchronizer(FirstLevelSynchronizer):
            # Include a duplicate 'driver1' from parent
            _required_mechanism_drivers = ['driver1', 'driver3']
            _required_service_plugins = ['plugin2', 'plugin3']
            _required_ml2_ext_drivers = ['ext_driver2']

            def do_sync(self):
                pass

        # Second level should have requirements from both levels
        # without duplicates
        mechanism_drivers = SecondLevelSynchronizer.\
            get_required_mechanism_drivers()
        self.assertEqual(3, len(mechanism_drivers))
        self.assertEqual(['driver1', 'driver2', 'driver3'],
                         sorted(mechanism_drivers))

        service_plugins = SecondLevelSynchronizer.\
            get_required_service_plugins()
        self.assertEqual(3, len(service_plugins))
        self.assertEqual(['plugin1', 'plugin2', 'plugin3'],
                         sorted(service_plugins))

        ml2_ext_drivers = SecondLevelSynchronizer.\
            get_required_ml2_extension_drivers()
        self.assertEqual(['ext_driver1', 'ext_driver2'],
                         sorted(ml2_ext_drivers))


class TestPluginConfiguration(base.BaseTestCase):

    _testplugin_config_file_opt = cfg.ListOpt(
        'testplugin_config_file', default=[])

    def test_register_additional_cli_opts(self):
        conf = cfg.ConfigOpts()

        class TestSynchronizer(db_sync.BaseOvnDbSynchronizer):
            @classmethod
            def register_additional_cli_opts(cls, conf):
                conf.register_cli_opts(
                    [TestPluginConfiguration._testplugin_config_file_opt])

            def do_sync(self):
                pass

        TestSynchronizer.register_additional_cli_opts(conf)
        conf(['--testplugin_config_file', '/tmp/test.conf'])
        self.assertEqual(['/tmp/test.conf'], conf.testplugin_config_file)

    def test_load_plugin_configuration(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write('[testgroup]\n')
            f.write('test_value = plugin_value\n')
            config_path = f.name

        conf = cfg.ConfigOpts()
        conf.register_cli_opts([self._testplugin_config_file_opt])
        conf(['--testplugin_config_file', config_path])

        class TestSynchronizer(db_sync.BaseOvnDbSynchronizer):
            @classmethod
            def register_additional_cli_opts(cls, conf):
                conf.register_cli_opts(
                    [TestPluginConfiguration._testplugin_config_file_opt])

            @classmethod
            def register_plugin_config_opts(cls, conf):
                conf.register_opts(
                    [cfg.StrOpt('test_value', default='default')],
                    group='testgroup')

            @classmethod
            def get_plugin_config_files(cls, global_conf):
                return global_conf.testplugin_config_file

            def do_sync(self):
                pass

        plugin_conf = TestSynchronizer.load_plugin_configuration(conf)
        self.assertEqual('plugin_value', plugin_conf.testgroup.test_value)

    def test_load_plugin_configuration_returns_none_without_files(self):
        conf = cfg.ConfigOpts()

        class TestSynchronizer(db_sync.BaseOvnDbSynchronizer):
            def do_sync(self):
                pass

        self.assertIsNone(
            TestSynchronizer.load_plugin_configuration(conf))

    def test_plugin_conf_does_not_affect_global_conf(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write('[testgroup]\n')
            f.write('test_value = plugin_value\n')
            config_path = f.name

        global_conf = cfg.ConfigOpts()
        global_conf.register_opts(
            [cfg.StrOpt('test_value', default='global_value')],
            group='testgroup')
        global_conf.register_cli_opts([self._testplugin_config_file_opt])
        global_conf(['--testplugin_config_file', config_path])

        class TestSynchronizer(db_sync.BaseOvnDbSynchronizer):
            @classmethod
            def register_plugin_config_opts(cls, conf):
                conf.register_opts(
                    [cfg.StrOpt('test_value', default='default')],
                    group='testgroup')

            @classmethod
            def get_plugin_config_files(cls, global_conf):
                return global_conf.testplugin_config_file

            def do_sync(self):
                pass

        plugin_conf = TestSynchronizer.load_plugin_configuration(global_conf)
        self.assertEqual('global_value', global_conf.testgroup.test_value)
        self.assertEqual('plugin_value', plugin_conf.testgroup.test_value)

    def test_synchronizer_stores_plugin_conf(self):
        plugin_conf = cfg.ConfigOpts()
        ovn_driver = mock.Mock()
        ovn_driver.nb_ovn = mock.Mock()
        ovn_driver.sb_ovn = mock.Mock()

        class TestSynchronizer(db_sync.BaseOvnDbSynchronizer):
            def do_sync(self):
                pass

        sync_obj = TestSynchronizer(
            mock.Mock(), ovn_driver, 'repair', plugin_conf=plugin_conf)
        self.assertIs(plugin_conf, sync_obj.plugin_conf)
