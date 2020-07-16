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

import pkgutil
import sys

from oslo_concurrency import lockutils
from oslo_log import log as logging
from oslo_utils import importutils
from stevedore import driver
from stevedore import enabled

from neutron_lib._i18n import _


LOG = logging.getLogger(__name__)
SYNCHRONIZED_PREFIX = 'neutron-'

# common synchronization decorator
synchronized = lockutils.synchronized_with_prefix(SYNCHRONIZED_PREFIX)


class NamespacedPlugins(object):
    """Wraps a stevedore plugin namespace to load/access its plugins."""

    def __init__(self, namespace):
        self.namespace = namespace
        self._extension_manager = None
        self._extensions = {}
        self.reload()

    def reload(self):
        """Force a reload of the plugins for this instances namespace.

        :returns: None.
        """
        self._extensions = {}
        self._extension_manager = enabled.EnabledExtensionManager(
            self.namespace, lambda x: True,
            invoke_on_load=False)

        if not self._extension_manager.names():
            LOG.debug("No plugins found in namespace: ", self.namespace)
            return
        self._extension_manager.map(self._add_extension)

    def _add_extension(self, ext):
        if ext.name in self._extensions:
            msg = _("Plugin '%(p)s' already in namespace: %(ns)s") % {
                'p': ext.name, 'ns': self.namespace}
            raise KeyError(msg)

        LOG.debug("Loaded plugin '%s' from namespace: %s",
                  ext.name, self.namespace)
        self._extensions[ext.name] = ext

    def _assert_plugin_loaded(self, plugin_name):
        if plugin_name not in self._extensions:
            msg = _("Plugin '%(p)s' not in namespace: %(ns)s") % {
                'p': plugin_name, 'ns': self.namespace}
            raise KeyError(msg)

    def get_plugin_class(self, plugin_name):
        """Gets a reference to a loaded plugin's class.

        :param plugin_name: The name of the plugin to get the class for.
        :returns: A reference to the loaded plugin's class.
        :raises: KeyError if plugin_name is not loaded.
        """
        self._assert_plugin_loaded(plugin_name)
        return self._extensions[plugin_name].plugin

    def new_plugin_instance(self, plugin_name, *args, **kwargs):
        """Create a new instance of a plugin.

        :param plugin_name: The name of the plugin to instantiate.
        :param args: Any args to pass onto the constructor.
        :param kwargs: Any kwargs to pass onto the constructor.
        :returns: A new instance of plugin_name.
        :raises: KeyError if plugin_name is not loaded.
        """
        self._assert_plugin_loaded(plugin_name)
        return self.get_plugin_class(plugin_name)(*args, **kwargs)

    @property
    def loaded_plugin_names(self):
        return self._extensions.keys()


def load_class_by_alias_or_classname(namespace, name):
    """Load a class using stevedore alias or the class name.

    :param namespace: The namespace where the alias is defined.
    :param name: The alias or class name of the class to be loaded.
    :returns: Class if it can be loaded.
    :raises ImportError: if class cannot be loaded.
    """
    if not name:
        LOG.error("Alias or class name is not set")
        raise ImportError(_("Class not found."))
    try:
        # Try to resolve class by alias
        mgr = driver.DriverManager(
            namespace, name, warn_on_missing_entrypoint=False)
        class_to_load = mgr.driver
    except RuntimeError:
        e1_info = sys.exc_info()
        # Fallback to class name
        try:
            class_to_load = importutils.import_class(name)
        except (ImportError, ValueError) as e:
            LOG.error("Error loading class by alias",
                      exc_info=e1_info)
            LOG.error("Error loading class by class name",
                      exc_info=True)
            raise ImportError(_("Class not found.")) from e
    return class_to_load


def list_package_modules(package_name):
    """Get a list of the modules for a given package.

    :param package_name: The package name to get modules for.
    :returns: A list of module objects for the said package name.
    """
    pkg_mod = importutils.import_module(package_name)
    modules = [pkg_mod]

    for mod in pkgutil.walk_packages(pkg_mod.__path__):
        _, mod_name, _ = mod
        fq_name = pkg_mod.__name__ + "." + mod_name
        modules.append(importutils.import_module(fq_name))

    return modules
