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

import netaddr

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


def random_mac_generator(base_mac):
    """Generates random mac addresses from a specified base format.

    The first 3 octets of each MAC address will remain unchanged. If the 4th
    octet is not 00, it will also be used. The others will be randomly
    generated.

    :param base_mac: Base mac address represented by an array of 6 strings.
    :returns: A mac address string generator.
    """
    fixed = list(base_mac[0:3])
    to_generate = 3
    if base_mac[3] != '00':
        fixed = list(base_mac[0:4])
        to_generate = 2
    beginning = ':'.join(fixed) + ':'

    form = '{}' + ':'.join('{:02x}' for _ in range(to_generate))
    max_macs = 2 ** (to_generate * 8)
    seen = set()
    while len(seen) < max_macs:
        numbers = [random.getrandbits(8) for _ in range(to_generate)]
        mac = form.format(beginning, *numbers)
        if mac in seen:
            continue
        seen.add(mac)
        yield mac


def is_port_trusted(port):
    """Used to determine if port can be trusted not to attack network.

    Trust is currently based on the device_owner field starting with 'network:'
    since we restrict who can use that in the default policy.yaml file.

    :param port: The port dict to inspect the 'device_owner' for.
    :returns: True if the port dict's 'device_owner' value starts with the
        networking prefix. False otherwise.
    """
    return port['device_owner'].startswith(
        constants.DEVICE_OWNER_NETWORK_PREFIX)


class _AuthenticBase(object):
    def __init__(self, addr, **kwargs):
        super().__init__(addr, **kwargs)
        self._initial_value = addr

    def __str__(self):
        if isinstance(self._initial_value, str):
            return self._initial_value
        return super().__str__()

    # NOTE(ihrachys): override deepcopy because netaddr.* classes are
    # slot-based and hence would not copy _initial_value
    def __deepcopy__(self, memo):
        return self.__class__(self._initial_value)


class AuthenticIPNetwork(_AuthenticBase, netaddr.IPNetwork):
    '''AuthenticIPNetwork class

    This class retains the format of the IP network string passed during
    initialization.

    This is useful when we want to make sure that we retain the format passed
    by a user through API.
    '''


class AuthenticEUI(_AuthenticBase, netaddr.EUI):
    '''AuthenticEUI class

    This class retains the format of the MAC address string passed during
    initialization.

    This is useful when we want to make sure that we retain the format passed
    by a user through API.
    '''
