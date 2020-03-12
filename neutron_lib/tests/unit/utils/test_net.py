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

import itertools
import random
import socket
from unittest import mock

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

    @mock.patch.object(random, 'getrandbits', return_value=0xa2)
    def test_first_4_octets_unchanged(self, mock_rnd):
        mac = net.get_random_mac(['aa', 'bb', '00', 'dd', 'ee', 'ff'])
        self.assertEqual('aa:bb:00:dd:a2:a2', mac)
        mock_rnd.assert_called_with(8)

    @mock.patch.object(random, 'getrandbits', return_value=0xa2)
    def test_first_4th_octet_generated(self, mock_rnd):
        mac = net.get_random_mac(['aa', 'bb', 'cc', '00', 'ee', 'ff'])
        self.assertEqual('aa:bb:cc:a2:a2:a2', mac)
        mock_rnd.assert_called_with(8)


class TestRandomMacGenerator(base.BaseTestCase):

    def test_all_macs_generated(self):
        mac = ['aa', 'bb', 'cc', 'dd', 'ee', 'ff']
        generator = itertools.islice(net.random_mac_generator(mac), 70000)
        self.assertEqual(2**16, len(list(generator)))

    @mock.patch.object(random, 'getrandbits', return_value=0xa2)
    def test_first_generated_mac(self, mock_rnd):
        mac = ['aa', 'bb', 'cc', '00', 'ee', 'ff']
        generator = itertools.islice(net.random_mac_generator(mac), 1)
        self.assertEqual(['aa:bb:cc:a2:a2:a2'], list(generator))
        mock_rnd.assert_called_with(8)

    @mock.patch.object(random, 'getrandbits', return_value=0xa2)
    def test_respected_early_zeroes_generated_mac(self, mock_rnd):
        mac1 = ['00', 'bb', 'cc', '00', 'ee', 'ff']

        generator = itertools.islice(net.random_mac_generator(mac1), 1)
        self.assertEqual(['00:bb:cc:a2:a2:a2'], list(generator))

        mac2 = ['aa', '00', 'cc', '00', 'ee', 'ff']
        generator = itertools.islice(net.random_mac_generator(mac2), 1)
        self.assertEqual(['aa:00:cc:a2:a2:a2'], list(generator))

        mac3 = ['aa', 'bb', '00', '00', 'ee', 'ff']
        generator = itertools.islice(net.random_mac_generator(mac3), 1)
        self.assertEqual(['aa:bb:00:a2:a2:a2'], list(generator))
        mock_rnd.assert_called_with(8)

    @mock.patch.object(random, 'getrandbits', return_value=0xa2)
    def test_short_supplied_mac(self, mock_rnd):
        mac_base = '12:34:56:78'
        mac = mac_base.split(':')
        generator = itertools.islice(net.random_mac_generator(mac), 1)
        self.assertEqual(['12:34:56:78:a2:a2'], list(generator))
        mock_rnd.assert_called_with(8)


class TestPortDeviceOwner(base.BaseTestCase):

    def test_is_port_trusted(self):
        self.assertTrue(net.is_port_trusted(
            {'device_owner':
             constants.DEVICE_OWNER_NETWORK_PREFIX + 'dev'}))

    def test_is_port_not_trusted(self):
        self.assertFalse(net.is_port_trusted(
            {'device_owner': constants.DEVICE_OWNER_COMPUTE_PREFIX + 'dev'}))
