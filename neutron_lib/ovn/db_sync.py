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

import abc
import threading
import time


class BaseOvnDbSynchronizer(metaclass=abc.ABCMeta):

    _required_mechanism_drivers = []
    _required_service_plugins = []
    _required_ml2_ext_drivers = []

    def __init__(self, core_plugin, ovn_driver, mode, is_maintenance=False):
        """Initialize the OVN DB synchronizer.

        :param core_plugin: The Neutron core plugin instance
        :param ovn_driver: The OVN driver instance containing the OVN NB and SB
                           API clients
        :param mode: The synchronization mode, valid values are:
                     'off', 'log', 'repair' or 'migrate'
        :param is_maintenance: Flag indicating if running in maintenance mode.
                               Defaults to False
        """
        self.core_plugin = core_plugin
        self.ovn_nb_api = ovn_driver.nb_ovn
        self.ovn_sb_api = ovn_driver.sb_ovn
        self.ovn_driver = ovn_driver
        self.mode = mode
        self.is_maintenance = is_maintenance
        self._thread = None

    def sync(self, delay_seconds=10):
        time.sleep(delay_seconds)
        self._thread = threading.Thread(target=self.do_sync)
        self._thread.start()

    @classmethod
    def _get_parent_class_attribute(cls, cls_attr):
        parent_attibutes = set()
        for parent in cls.__mro__:
            parent_attibutes |= set(getattr(parent, cls_attr, set()))
        return list(parent_attibutes | set(getattr(cls, cls_attr, [])))

    @classmethod
    def get_required_mechanism_drivers(cls):
        return cls._get_parent_class_attribute('_required_mechanism_drivers')

    @classmethod
    def get_required_service_plugins(cls):
        return cls._get_parent_class_attribute('_required_service_plugins')

    @classmethod
    def get_required_ml2_extension_drivers(cls):
        return cls._get_parent_class_attribute('_required_ml2_ext_drivers')

    @abc.abstractmethod
    def do_sync(self):
        """Method to sync the OVN DB."""

    def stop(self):
        # TODO(ralonsoh): this method and the function executed in the thread
        # should support a fast exit way.
        try:
            self._thread.join()
        except AttributeError:
            # Haven't started syncing
            pass
