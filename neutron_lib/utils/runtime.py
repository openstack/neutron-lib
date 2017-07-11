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

import sys

from oslo_concurrency import lockutils
from oslo_log import log as logging
from oslo_utils import importutils
from stevedore import driver

from neutron_lib._i18n import _

LOG = logging.getLogger(__name__)
SYNCHRONIZED_PREFIX = 'neutron-'


# common synchronization decorator
synchronized = lockutils.synchronized_with_prefix(SYNCHRONIZED_PREFIX)


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
        except (ImportError, ValueError):
            LOG.error("Error loading class by alias",
                      exc_info=e1_info)
            LOG.error("Error loading class by class name",
                      exc_info=True)
            raise ImportError(_("Class not found."))
    return class_to_load
