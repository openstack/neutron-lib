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

import random
import socket

from neutron_lib import constants


def get_hostname():
    """Get the hostname of the system.

    :returns: The hostname of the system.
    """
    return socket.gethostname()


def get_random_mac(base_mac):
    """Get a random MAC address string of the specified base format.

    The first 3 octets will remain unchanged. If the 4th octet is not
    00, it will also be used. The others will be randomly generated.

    :param base_mac: Base MAC address represented by an array of 6 strings/int
    :returns: The MAC address string.
    """

    mac = [int(base_mac[0], 16), int(base_mac[1], 16),
           int(base_mac[2], 16), random.getrandbits(8),
           random.getrandbits(8), random.getrandbits(8)]
    if base_mac[3] != '00':
        mac[3] = int(base_mac[3], 16)
    return ':'.join(["%02x" % x for x in mac])


def is_port_trusted(port):
    """Used to determine if port can be trusted not to attack network.

    Trust is currently based on the device_owner field starting with 'network:'
    since we restrict who can use that in the default policy.json file.

    :param port: The port dict to inspect the 'device_owner' for.
    :returns: True if the port dict's 'device_owner' value starts with the
        networking prefix. False otherwise.
    """
    return port['device_owner'].startswith(
        constants.DEVICE_OWNER_NETWORK_PREFIX)
