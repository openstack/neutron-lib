# All Rights Reserved.
#
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

import weakref

from oslo_concurrency import lockutils

from neutron_lib.plugins import constants


_synchronized = lockutils.synchronized_with_prefix("neutron-")


class _PluginDirectory(object):
    """A directory of activated plugins in a Neutron Deployment.

    The directory is bootstrapped by a Neutron Manager running in
    the context of a Neutron Server process.
    """

    def __init__(self):
        self._plugins = {}

    def add_plugin(self, alias, plugin):
        """Add a plugin of type 'alias'."""
        self._plugins[alias] = plugin

    def get_plugin(self, alias):
        """Get a plugin for a given alias or None if not present."""
        p = self._plugins.get(alias)
        return weakref.proxy(p) if p else None

    @property
    def plugins(self):
        """The mapping alias -> weak reference to the plugin."""
        return dict((x, weakref.proxy(y))
                    for x, y in self._plugins.items())

    @property
    def unique_plugins(self):
        """A sequence of the unique plugins activated in the environments."""
        return tuple(weakref.proxy(x) for x in set(self._plugins.values()))

    @property
    def is_loaded(self):
        """True if the directory is non empty."""
        return len(self._plugins) > 0


# Create a singleton plugins directory for the Neutron server instance.
# Accessing these methods before a Neutron Manager has had the chance
# to load the environment may result in callers handling an empty directory.
_PLUGIN_DIRECTORY = None


@_synchronized("plugin-directory")
def _create_plugin_directory():
    global _PLUGIN_DIRECTORY
    if _PLUGIN_DIRECTORY is None:
        _PLUGIN_DIRECTORY = _PluginDirectory()
    return _PLUGIN_DIRECTORY


def _get_plugin_directory():
    if _PLUGIN_DIRECTORY is None:
        return _create_plugin_directory()
    return _PLUGIN_DIRECTORY


def add_plugin(alias, plugin):
    _get_plugin_directory().add_plugin(alias, plugin)


def get_plugin(alias=constants.CORE):
    return _get_plugin_directory().get_plugin(alias)


def get_plugins():
    return _get_plugin_directory().plugins


def get_unique_plugins():
    return _get_plugin_directory().unique_plugins


def is_loaded():
    return _get_plugin_directory().is_loaded
