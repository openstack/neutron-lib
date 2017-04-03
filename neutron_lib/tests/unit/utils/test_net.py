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

import mock

from neutron_lib import constants
from neutron_lib.tests import _base as base
from neutron_lib.utils import net


class TestGetHostname(base.BaseTestCase):

    @mock.patch.object(socket, 'gethostname',
                       return_value='fake-host-name')
    def test_get_hostname(self, mock_gethostname):
        self.assertEqual('fake-host-name',
                         net.get_hostname())
        mock_gethostname.assert_called_once_with()


class TestGetRandomMac(base.BaseTestCase):

    def test_full_prefix_does_nothing(self):
        mac = net.get_random_mac(['aa', 'bb', 'cc', 'dd', 'ee', 'ff'])

        self.assertEqual('aa:bb:cc:dd:ee:ff', mac)

    @mock.patch.object(random, 'randint', side_effect=[0x11])
    def test_5_octets_prefix_replaces_1_part(self, mock_rnd):
        mac = net.get_random_mac(['aa', 'bb', 'cc', 'dd', 'ee', '00'])

        self.assertEqual('aa:bb:cc:dd:ee:11', mac)

        mock_rnd.assert_called_with(0x00, 0xff)

    @mock.patch.object(random, 'randint',
                       side_effect=[0x01, 0x02, 0x03, 0x04, 0x05])
    def test_1_octets_prefix_replaces_5_parts(self, mock_rnd):
        mac = net.get_random_mac(['aa', '00', '00', '00', '00', '00'])

        self.assertEqual('aa:01:02:03:04:05', mac)

        mock_rnd.assert_called_with(0x00, 0xff)

    @mock.patch.object(random, 'randint', return_value=0xa2)
    def test_no_prefix_replaces_all_parts(self, mock_rnd):
        mac = net.get_random_mac(['00', '00', '00', '00', '00', '00'])

        self.assertEqual('a2:a2:a2:a2:a2:a2', mac)

        mock_rnd.assert_called_with(0x00, 0xff)


class TestPortDeviceOwner(base.BaseTestCase):

    def test_is_port_trusted(self):
        self.assertTrue(net.is_port_trusted(
            {'device_owner':
             constants.DEVICE_OWNER_NETWORK_PREFIX + 'dev'}))

    def test_is_port_not_trusted(self):
        self.assertFalse(net.is_port_trusted(
            {'device_owner': constants.DEVICE_OWNER_COMPUTE_PREFIX + 'dev'}))
