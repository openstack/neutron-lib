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

import fixtures

from neutron_lib.callbacks import manager
from neutron_lib.callbacks import registry
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

    def _setUp(self):
        self._orig_manager = registry._CALLBACK_MANAGER
        registry._CALLBACK_MANAGER = self.callback_manager
        self.addCleanup(self._restore)

    def _restore(self):
        registry._CALLBACK_MANAGER = self._orig_manager
