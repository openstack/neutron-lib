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

import mock

from oslotest import base

from neutron_lib.callbacks import registry
from neutron_lib import fixture
from neutron_lib.plugins import directory


class PluginDirectoryFixtureTestCase(base.BaseTestCase):

    def setUp(self):
        super(PluginDirectoryFixtureTestCase, self).setUp()
        self.directory = mock.Mock()
        self.useFixture(fixture.PluginDirectoryFixture(
            plugin_directory=self.directory))

    def test_fixture(self):
        directory.add_plugin('foo', 'foo')
        self.assertTrue(self.directory.add_plugin.called)


class CallbackRegistryFixtureTestCase(base.BaseTestCase):

    def setUp(self):
        super(CallbackRegistryFixtureTestCase, self).setUp()
        self.manager = mock.Mock()
        self.useFixture(fixture.CallbackRegistryFixture(
            callback_manager=self.manager))

    def test_fixture(self):
        registry.notify('a', 'b', self)
        self.assertTrue(self.manager.notify.called)
