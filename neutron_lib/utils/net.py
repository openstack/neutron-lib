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


def get_hostname():
    """Get the hostname of the system.

    :returns: The hostname of the system.
    """
    return socket.gethostname()


def get_random_mac(base_mac):
    """Get a random MAC address string of the specified base format.

    :param base_mac: The base MAC address format for the MAC address string.
    :returns: The MAC address string.
    """
    mac = [int(base_mac[0], 16), int(base_mac[1], 16),
           int(base_mac[2], 16), random.randint(0x00, 0xff),
           random.randint(0x00, 0xff), random.randint(0x00, 0xff)]
    if base_mac[3] != '00':
        mac[3] = int(base_mac[3], 16)
    return ':'.join(["%02x" % x for x in mac])
