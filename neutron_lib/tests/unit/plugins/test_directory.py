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

from neutron_lib.plugins import directory
from neutron_lib.tests import _base as base


def fake_plugin():
    pass


class DirectoryTestCase(base.BaseTestCase):

    def test__create_plugin_directory(self):
        self.assertIsNotNone(directory._create_plugin_directory())

    def test__get_plugin_directory(self):
        self.assertIsNotNone(directory._get_plugin_directory())

    def test_add_plugin(self):
        directory.add_plugin('foo', fake_plugin)
        self.assertIn('foo', directory.get_plugins())

    def test_get_plugin_core_none(self):
        self.assertIsNone(directory.get_plugin())

    def test_get_plugin_alias_none(self):
        self.assertIsNone(directory.get_plugin('foo'))

    def test_get_plugin_core(self):
        directory.add_plugin('CORE', fake_plugin)
        self.assertIsNotNone(directory.get_plugin())

    def test_get_plugin_alias(self):
        directory.add_plugin('foo', fake_plugin)
        self.assertIsNotNone(directory.get_plugin('foo'))

    def test_get_plugins_none(self):
        self.assertFalse(directory.get_plugins())

    def test_get_unique_plugins_none(self):
        self.assertFalse(directory.get_unique_plugins())

    def test_get_plugins(self):
        directory.add_plugin('CORE', fake_plugin)
        self.assertIsNotNone(directory.get_plugins())

    def test_get_unique_plugins(self):
        directory.add_plugin('foo1', fake_plugin)
        directory.add_plugin('foo2', fake_plugin)
        self.assertEqual(1, len(directory.get_unique_plugins()))

    def test_is_loaded(self):
        self.assertFalse(directory.is_loaded())
        directory.add_plugin('foo1', fake_plugin)
        self.assertTrue(directory.is_loaded())


class PluginDirectoryTestCase(base.BaseTestCase):

    def setUp(self):
        super().setUp()
        self.plugin_directory = directory._PluginDirectory()

    def test_add_plugin(self):
        self.plugin_directory.add_plugin('foo', 'bar')
        self.assertEqual(1, len(self.plugin_directory._plugins))

    def test_get_plugin_not_found(self):
        self.assertIsNone(self.plugin_directory.get_plugin('foo'))

    def test_get_plugin_found(self):
        self.plugin_directory._plugins = {'foo': lambda *x, **y: 'bar'}
        plugin = self.plugin_directory.get_plugin('foo')
        self.assertEqual('bar', plugin())

    def test_plugins(self):
        self.plugin_directory._plugins = {'foo': lambda *x, **y: 'bar'}
        self.assertIsNotNone(self.plugin_directory.plugins)

    def test_unique_plugins(self):
        self.plugin_directory._plugins = {
            'foo1': fake_plugin,
            'foo2': fake_plugin,
        }
        self.assertEqual(1, len(self.plugin_directory.unique_plugins))

    def test_is_loaded(self):
        self.assertFalse(self.plugin_directory.is_loaded)
        self.plugin_directory._plugins = {'foo': lambda *x, **y: 'bar'}
        self.assertTrue(self.plugin_directory.is_loaded)
