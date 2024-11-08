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

from neutron_lib import constants


class LinuxInterfaceDriver(metaclass=abc.ABCMeta):

    DEV_NAME_LEN = constants.LINUX_DEV_LEN
    DEV_NAME_PREFIX = constants.TAP_DEVICE_PREFIX

    @abc.abstractmethod
    def plug_new(self, network_id, port_id, device_name, mac_address,
                 bridge=None, namespace=None, prefix=None, mtu=None,
                 link_up=True):
        """Plug in the interface only for new devices that don't exist yet."""

    @abc.abstractmethod
    def unplug(self, device_name, bridge=None, namespace=None, prefix=None):
        """Unplug the interface."""
