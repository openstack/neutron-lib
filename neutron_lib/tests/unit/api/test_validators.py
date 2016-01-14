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

import string

import mock
import netaddr

from neutron_lib._i18n import _
from neutron_lib.api import converters
from neutron_lib.api import validators
from neutron_lib import constants
from neutron_lib import exceptions as n_exc
from neutron_lib.tests import _base as base


def dummy_validator(data, valid_values=None):
    pass


class TestAttributeValidation(base.BaseTestCase):

    def _construct_dict_and_constraints(self):
        """Constructs a test dictionary and a definition of constraints.

        :return: A (dictionary, constraint) tuple
        """

        constraints = {'key1': {'type:values': ['val1', 'val2'],
                                'required': True},
                       'key2': {'type:string': None,
                                'required': False},
                       'key3': {'type:dict': {'k4': {'type:string': None,
                                                     'required': True}},
                                'required': True}}

        dictionary = {'key1': 'val1',
                      'key2': 'a string value',
                      'key3': {'k4': 'a string value'}}

        return dictionary, constraints

    def test_adding_validator(self):
        validators.add_validator('new_type', dummy_validator)
        self.assertIn('type:new_type', validators.validators)
        self.assertEqual(dummy_validator,
                         validators.validators['type:new_type'])

    def test_fail_adding_duplicate_validator(self):
        self.assertRaises(KeyError,
                          validators.add_validator,
                          'dict', dummy_validator)

    def test_is_attr_set(self):
        data = constants.ATTR_NOT_SPECIFIED
        self.assertIs(validators.is_attr_set(data), False)

        data = None
        self.assertIs(validators.is_attr_set(data), False)

        data = "I'm set"
        self.assertIs(validators.is_attr_set(data), True)

    def test_validate_values(self):
        msg = validators.validate_values(4, [4, 6])
        self.assertIsNone(msg)

        msg = validators.validate_values(4, (4, 6))
        self.assertIsNone(msg)

        msg = validators.validate_values(7, [4, 6])
        self.assertEqual("'7' is not in [4, 6]", msg)

        msg = validators.validate_values(7, (4, 6))
        self.assertEqual("'7' is not in (4, 6)", msg)

    def test_validate_not_empty_string(self):
        msg = validators.validate_not_empty_string('    ', None)
        self.assertEqual(u"'    ' Blank strings are not permitted", msg)
        msg = validators.validate_not_empty_string(123, None)
        self.assertEqual(u"'123' is not a valid string", msg)

    def test_validate_not_empty_string_or_none(self):
        msg = validators.validate_not_empty_string_or_none('    ', None)
        self.assertEqual(u"'    ' Blank strings are not permitted", msg)

        msg = validators.validate_not_empty_string_or_none(None, None)
        self.assertIsNone(msg)

    def test_validate_string_or_none(self):
        msg = validators.validate_string_or_none('test', None)
        self.assertIsNone(msg)

        msg = validators.validate_string_or_none(None, None)
        self.assertIsNone(msg)

    def test_validate_string(self):
        msg = validators.validate_string(None, None)
        self.assertEqual("'None' is not a valid string", msg)

        # 0 == len(data) == max_len
        msg = validators.validate_string("", 0)
        self.assertIsNone(msg)

        # 0 == len(data) < max_len
        msg = validators.validate_string("", 9)
        self.assertIsNone(msg)

        # 0 < len(data) < max_len
        msg = validators.validate_string("123456789", 10)
        self.assertIsNone(msg)

        # 0 < len(data) == max_len
        msg = validators.validate_string("123456789", 9)
        self.assertIsNone(msg)

        # 0 < max_len < len(data)
        msg = validators.validate_string("1234567890", 9)
        self.assertEqual("'1234567890' exceeds maximum length of 9", msg)

        msg = validators.validate_string("123456789", None)
        self.assertIsNone(msg)

    def test_validate_list_of_unique_strings(self):
        data = "TEST"
        msg = validators.validate_list_of_unique_strings(data, None)
        self.assertEqual("'TEST' is not a list", msg)

        data = ["TEST01", "TEST02", "TEST01"]
        msg = validators.validate_list_of_unique_strings(data, None)
        self.assertEqual(
            "Duplicate items in the list: 'TEST01, TEST02, TEST01'", msg)

        data = ["12345678", "123456789"]
        msg = validators.validate_list_of_unique_strings(data, 8)
        self.assertEqual("'123456789' exceeds maximum length of 8", msg)

        data = ["TEST01", "TEST02", "TEST03"]
        msg = validators.validate_list_of_unique_strings(data, None)
        self.assertIsNone(msg)

    def test_validate_boolean(self):
        msg = validators.validate_boolean(True)
        self.assertIsNone(msg)
        msg = validators.validate_boolean(0)
        self.assertIsNone(msg)
        msg = validators.validate_boolean("false")
        self.assertIsNone(msg)
        msg = validators.validate_boolean("fasle")
        self.assertEqual("'fasle' is not a valid boolean value", msg)

    def test_validate_no_whitespace(self):
        data = 'no_white_space'
        result = validators.validate_no_whitespace(data)
        self.assertEqual(data, result)

        self.assertRaises(n_exc.InvalidInput,
                          validators.validate_no_whitespace,
                          'i have whitespace')

        self.assertRaises(n_exc.InvalidInput,
                          validators.validate_no_whitespace,
                          'i\thave\twhitespace')

        for ws in string.whitespace:
            self.assertRaises(n_exc.InvalidInput,
                              validators.validate_no_whitespace,
                              '%swhitespace-at-head' % ws)
            self.assertRaises(n_exc.InvalidInput,
                              validators.validate_no_whitespace,
                              'whitespace-at-tail%s' % ws)

    def test_validate_range(self):
        msg = validators.validate_range(1, [1, 9])
        self.assertIsNone(msg)

        msg = validators.validate_range(5, [1, 9])
        self.assertIsNone(msg)

        msg = validators.validate_range(9, [1, 9])
        self.assertIsNone(msg)

        msg = validators.validate_range(1, (1, 9))
        self.assertIsNone(msg)

        msg = validators.validate_range(5, (1, 9))
        self.assertIsNone(msg)

        msg = validators.validate_range(9, (1, 9))
        self.assertIsNone(msg)

        msg = validators.validate_range(0, [1, 9])
        self.assertEqual("'0' is too small - must be at least '1'", msg)

        msg = validators.validate_range(10, (1, 9))
        self.assertEqual("'10' is too large - must be no larger than '9'", msg)

        msg = validators.validate_range("bogus", (1, 9))
        self.assertEqual("'bogus' is not an integer", msg)

        msg = validators.validate_range(10, (validators.UNLIMITED,
                                             validators.UNLIMITED))
        self.assertIsNone(msg)

        msg = validators.validate_range(10, (1, validators.UNLIMITED))
        self.assertIsNone(msg)

        msg = validators.validate_range(1, (validators.UNLIMITED, 9))
        self.assertIsNone(msg)

        msg = validators.validate_range(-1, (0, validators.UNLIMITED))
        self.assertEqual("'-1' is too small - must be at least '0'", msg)

        msg = validators.validate_range(10, (validators.UNLIMITED, 9))
        self.assertEqual("'10' is too large - must be no larger than '9'", msg)

    def _test_validate_mac_address(self, validator, allow_none=False):
        mac_addr = "ff:16:3e:4f:00:00"
        msg = validator(mac_addr)
        self.assertIsNone(msg)

        mac_addr = "ffa:16:3e:4f:00:00"
        msg = validator(mac_addr)
        err_msg = "'%s' is not a valid MAC address"
        self.assertEqual(err_msg % mac_addr, msg)

        for invalid_mac_addr in constants.INVALID_MAC_ADDRESSES:
            msg = validator(invalid_mac_addr)
            self.assertEqual(err_msg % invalid_mac_addr, msg)

        mac_addr = "123"
        msg = validator(mac_addr)
        self.assertEqual(err_msg % mac_addr, msg)

        mac_addr = None
        msg = validator(mac_addr)
        if allow_none:
            self.assertIsNone(msg)
        else:
            self.assertEqual(err_msg % mac_addr, msg)

        mac_addr = "ff:16:3e:4f:00:00\r"
        msg = validator(mac_addr)
        self.assertEqual(err_msg % mac_addr, msg)

    def test_validate_mac_address(self):
        self._test_validate_mac_address(validators.validate_mac_address)

    def test_validate_mac_address_or_none(self):
        self._test_validate_mac_address(
            validators.validate_mac_address_or_none, allow_none=True)

    def test_validate_ip_address(self):
        ip_addr = '1.1.1.1'
        msg = validators.validate_ip_address(ip_addr)
        self.assertIsNone(msg)

        ip_addr = '1111.1.1.1'
        msg = validators.validate_ip_address(ip_addr)
        self.assertEqual("'%s' is not a valid IP address" % ip_addr, msg)

        # Depending on platform to run UTs, this case might or might not be
        # an equivalent to test_validate_ip_address_bsd.
        ip_addr = '1' * 59
        msg = validators.validate_ip_address(ip_addr)
        self.assertEqual("'%s' is not a valid IP address" % ip_addr, msg)

        ip_addr = '1.1.1.1 has whitespace'
        msg = validators.validate_ip_address(ip_addr)
        self.assertEqual("'%s' is not a valid IP address" % ip_addr, msg)

        ip_addr = '111.1.1.1\twhitespace'
        msg = validators.validate_ip_address(ip_addr)
        self.assertEqual("'%s' is not a valid IP address" % ip_addr, msg)

        ip_addr = '111.1.1.1\nwhitespace'
        msg = validators.validate_ip_address(ip_addr)
        self.assertEqual("'%s' is not a valid IP address" % ip_addr, msg)

        for ws in string.whitespace:
            ip_addr = '%s111.1.1.1' % ws
            msg = validators.validate_ip_address(ip_addr)
            self.assertEqual("'%s' is not a valid IP address" % ip_addr, msg)

        for ws in string.whitespace:
            ip_addr = '111.1.1.1%s' % ws
            msg = validators.validate_ip_address(ip_addr)
            self.assertEqual("'%s' is not a valid IP address" % ip_addr, msg)

    def test_validate_ip_address_with_leading_zero(self):
        ip_addr = '1.1.1.01'
        expected_msg = ("'%(data)s' is not an accepted IP address, "
                        "'%(ip)s' is recommended")
        msg = validators.validate_ip_address(ip_addr)
        self.assertEqual(expected_msg % {"data": ip_addr, "ip": '1.1.1.1'},
                         msg)

        ip_addr = '1.1.1.011'
        msg = validators.validate_ip_address(ip_addr)
        self.assertEqual(expected_msg % {"data": ip_addr, "ip": '1.1.1.11'},
                         msg)

        ip_addr = '1.1.1.09'
        msg = validators.validate_ip_address(ip_addr)
        self.assertEqual(expected_msg % {"data": ip_addr, "ip": '1.1.1.9'},
                         msg)

        ip_addr = "fe80:0:0:0:0:0:0:0001"
        msg = validators.validate_ip_address(ip_addr)
        self.assertIsNone(msg)

    def test_validate_ip_address_bsd(self):
        # NOTE(yamamoto):  On NetBSD and OS X, netaddr.IPAddress() accepts
        # '1' * 59 as a valid address.  The behaviour is inherited from
        # libc behaviour there.  This test ensures that our validator reject
        # such addresses on such platforms by mocking netaddr to emulate
        # the behaviour.
        ip_addr = '1' * 59
        with mock.patch('netaddr.IPAddress') as ip_address_cls:
            msg = validators.validate_ip_address(ip_addr)
        ip_address_cls.assert_called_once_with(ip_addr,
                                               flags=netaddr.core.ZEROFILL)
        self.assertEqual("'%s' is not a valid IP address" % ip_addr, msg)

    def test_validate_ip_pools(self):
        pools = [[{'end': '10.0.0.254'}],
                 [{'start': '10.0.0.254'}],
                 [{'start': '1000.0.0.254',
                   'end': '1.1.1.1'}],
                 [{'start': '10.0.0.2', 'end': '10.0.0.254',
                   'forza': 'juve'}],
                 [{'start': '10.0.0.2', 'end': '10.0.0.254'},
                  {'end': '10.0.0.254'}],
                 [None],
                 None]
        for pool in pools:
            msg = validators.validate_ip_pools(pool)
            self.assertIsNotNone(msg)

        pools = [[{'end': '10.0.0.254', 'start': '10.0.0.2'},
                  {'start': '11.0.0.2', 'end': '11.1.1.1'}],
                 [{'start': '11.0.0.2', 'end': '11.0.0.100'}]]
        for pool in pools:
            msg = validators.validate_ip_pools(pool)
            self.assertIsNone(msg)

        invalid_ip = '10.0.0.2\r'
        pools = [[{'end': '10.0.0.254', 'start': invalid_ip}]]
        for pool in pools:
            msg = validators.validate_ip_pools(pool)
            self.assertEqual("'%s' is not a valid IP address" % invalid_ip,
                             msg)

    def test_validate_fixed_ips(self):
        fixed_ips = [
            {'data': [{'subnet_id': '00000000-ffff-ffff-ffff-000000000000',
                       'ip_address': '1111.1.1.1'}],
             'error_msg': "'1111.1.1.1' is not a valid IP address"},
            {'data': [{'subnet_id': 'invalid',
                       'ip_address': '1.1.1.1'}],
             'error_msg': "'invalid' is not a valid UUID"},
            {'data': None,
             'error_msg': "Invalid data format for fixed IP: 'None'"},
            {'data': "1.1.1.1",
             'error_msg': "Invalid data format for fixed IP: '1.1.1.1'"},
            {'data': ['00000000-ffff-ffff-ffff-000000000000', '1.1.1.1'],
             'error_msg': "Invalid data format for fixed IP: "
                          "'00000000-ffff-ffff-ffff-000000000000'"},
            {'data': [['00000000-ffff-ffff-ffff-000000000000', '1.1.1.1']],
             'error_msg': "Invalid data format for fixed IP: "
                          "'['00000000-ffff-ffff-ffff-000000000000', "
                          "'1.1.1.1']'"},
            {'data': [{'subnet_id': '00000000-0fff-ffff-ffff-000000000000',
                       'ip_address': '1.1.1.1'},
                      {'subnet_id': '00000000-ffff-ffff-ffff-000000000000',
                       'ip_address': '1.1.1.1'}],
             'error_msg': "Duplicate IP address '1.1.1.1'"}]
        for fixed in fixed_ips:
            msg = validators.validate_fixed_ips(fixed['data'])
            self.assertEqual(fixed['error_msg'], msg)

        fixed_ips = [[{'subnet_id': '00000000-ffff-ffff-ffff-000000000000',
                       'ip_address': '1.1.1.1'}],
                     [{'subnet_id': '00000000-0fff-ffff-ffff-000000000000',
                       'ip_address': '1.1.1.1'},
                      {'subnet_id': '00000000-ffff-ffff-ffff-000000000000',
                       'ip_address': '1.1.1.2'}]]
        for fixed in fixed_ips:
            msg = validators.validate_fixed_ips(fixed)
            self.assertIsNone(msg)

    def test_validate_nameservers(self):
        ns_pools = [['1.1.1.2', '1.1.1.2'],
                    ['www.hostname.com', 'www.hostname.com'],
                    ['1000.0.0.1'],
                    ['www.hostname.com'],
                    ['www.great.marathons.to.travel'],
                    ['valid'],
                    ['77.hostname.com'],
                    ['1' * 59],
                    ['www.internal.hostname.com'],
                    None]

        for ns in ns_pools:
            msg = validators.validate_nameservers(ns, None)
            self.assertIsNotNone(msg)

        ns_pools = [['100.0.0.2'],
                    ['1.1.1.1', '1.1.1.2']]

        for ns in ns_pools:
            msg = validators.validate_nameservers(ns, None)
            self.assertIsNone(msg)

    def test_validate_hostroutes(self):
        hostroute_pools = [[{'destination': '100.0.0.0/24'}],
                           [{'nexthop': '10.0.2.20'}],
                           [{'nexthop': '10.0.2.20',
                             'forza': 'juve',
                             'destination': '100.0.0.0/8'}],
                           [{'nexthop': '1110.0.2.20',
                             'destination': '100.0.0.0/8'}],
                           [{'nexthop': '10.0.2.20',
                             'destination': '100.0.0.0'}],
                           [{'nexthop': '10.0.2.20',
                             'destination': '100.0.0.0/8'},
                            {'nexthop': '10.0.2.20',
                             'destination': '100.0.0.0/8'}],
                           [None],
                           None]
        for host_routes in hostroute_pools:
            msg = validators.validate_hostroutes(host_routes, None)
            self.assertIsNotNone(msg)

        hostroute_pools = [[{'destination': '100.0.0.0/24',
                             'nexthop': '10.0.2.20'}],
                           [{'nexthop': '10.0.2.20',
                             'destination': '100.0.0.0/8'},
                            {'nexthop': '10.0.2.20',
                             'destination': '101.0.0.0/8'}]]
        for host_routes in hostroute_pools:
            msg = validators.validate_hostroutes(host_routes, None)
            self.assertIsNone(msg)

    def test_validate_ip_address_or_none(self):
        ip_addr = None
        msg = validators.validate_ip_address_or_none(ip_addr)
        self.assertIsNone(msg)

        ip_addr = '1.1.1.1'
        msg = validators.validate_ip_address_or_none(ip_addr)
        self.assertIsNone(msg)

        ip_addr = '1111.1.1.1'
        msg = validators.validate_ip_address_or_none(ip_addr)
        self.assertEqual("'%s' is not a valid IP address" % ip_addr, msg)

    def test_uuid_pattern(self):
        data = 'garbage'
        msg = validators.validate_regex(data, constants.UUID_PATTERN)
        self.assertIsNotNone(msg)

        data = '00000000-ffff-ffff-ffff-000000000000'
        msg = validators.validate_regex(data, constants.UUID_PATTERN)
        self.assertIsNone(msg)

    def test_mac_pattern(self):
        # Valid - 3 octets
        base_mac = "fa:16:3e:00:00:00"
        msg = validators.validate_regex(base_mac, validators.MAC_PATTERN)
        self.assertIsNone(msg)

        # Valid - 4 octets
        base_mac = "fa:16:3e:4f:00:00"
        msg = validators.validate_regex(base_mac, validators.MAC_PATTERN)
        self.assertIsNone(msg)

        # Invalid - not unicast
        base_mac = "01:16:3e:4f:00:00"
        msg = validators.validate_regex(base_mac, validators.MAC_PATTERN)
        self.assertIsNotNone(msg)

        # Invalid - invalid format
        base_mac = "a:16:3e:4f:00:00"
        msg = validators.validate_regex(base_mac, validators.MAC_PATTERN)
        self.assertIsNotNone(msg)

        # Invalid - invalid format
        base_mac = "ffa:16:3e:4f:00:00"
        msg = validators.validate_regex(base_mac, validators.MAC_PATTERN)
        self.assertIsNotNone(msg)

        # Invalid - invalid format
        base_mac = "01163e4f0000"
        msg = validators.validate_regex(base_mac, validators.MAC_PATTERN)
        self.assertIsNotNone(msg)

        # Invalid - invalid format
        base_mac = "01-16-3e-4f-00-00"
        msg = validators.validate_regex(base_mac, validators.MAC_PATTERN)
        self.assertIsNotNone(msg)

        # Invalid - invalid format
        base_mac = "00:16:3:f:00:00"
        msg = validators.validate_regex(base_mac, validators.MAC_PATTERN)
        self.assertIsNotNone(msg)

        # Invalid - invalid format
        base_mac = "12:3:4:5:67:89ab"
        msg = validators.validate_regex(base_mac, validators.MAC_PATTERN)
        self.assertIsNotNone(msg)

    def _test_validate_subnet(self, validator, allow_none=False):
        # Valid - IPv4
        cidr = "10.0.2.0/24"
        msg = validator(cidr, None)
        self.assertIsNone(msg)

        # Valid - IPv6 without final octets
        cidr = "fe80::/24"
        msg = validator(cidr, None)
        self.assertIsNone(msg)

        # Valid - IPv6 with final octets
        cidr = "fe80::/24"
        msg = validator(cidr, None)
        self.assertIsNone(msg)

        # Valid - uncompressed ipv6 address
        cidr = "fe80:0:0:0:0:0:0:0/128"
        msg = validator(cidr, None)
        self.assertIsNone(msg)

        # Valid - ipv6 address with multiple consecutive zero
        cidr = "2001:0db8:0:0:1::1/128"
        msg = validator(cidr, None)
        self.assertIsNone(msg)

        # Valid - ipv6 address with multiple consecutive zero
        cidr = "2001:0db8::1:0:0:1/128"
        msg = validator(cidr, None)
        self.assertIsNone(msg)

        # Valid - ipv6 address with multiple consecutive zero
        cidr = "2001::0:1:0:0:1100/120"
        msg = validator(cidr, None)
        self.assertIsNone(msg)

        # Invalid - abbreviated ipv4 address
        cidr = "10/24"
        msg = validator(cidr, None)
        error = _("'%(data)s' isn't a recognized IP subnet cidr,"
                  " '%(cidr)s' is recommended") % {"data": cidr,
                                                   "cidr": "10.0.0.0/24"}
        self.assertEqual(error, msg)

        # Invalid - IPv4 missing mask
        cidr = "10.0.2.0"
        msg = validator(cidr, None)
        error = _("'%(data)s' isn't a recognized IP subnet cidr,"
                  " '%(cidr)s' is recommended") % {"data": cidr,
                                                   "cidr": "10.0.2.0/32"}
        self.assertEqual(error, msg)

        # Valid - IPv4 with non-zero masked bits is ok
        for i in range(1, 255):
            cidr = "192.168.1.%s/24" % i
            msg = validator(cidr, None)
            self.assertIsNone(msg)

        # Invalid - IPv6 without final octets, missing mask
        cidr = "fe80::"
        msg = validator(cidr, None)
        error = _("'%(data)s' isn't a recognized IP subnet cidr,"
                  " '%(cidr)s' is recommended") % {"data": cidr,
                                                   "cidr": "fe80::/128"}
        self.assertEqual(error, msg)

        # Invalid - IPv6 with final octets, missing mask
        cidr = "fe80::0"
        msg = validator(cidr, None)
        error = _("'%(data)s' isn't a recognized IP subnet cidr,"
                  " '%(cidr)s' is recommended") % {"data": cidr,
                                                   "cidr": "fe80::/128"}
        self.assertEqual(error, msg)

        # Invalid - Address format error
        cidr = 'invalid'
        msg = validator(cidr, None)
        error = "'%s' is not a valid IP subnet" % cidr
        self.assertEqual(error, msg)

        cidr = None
        msg = validator(cidr, None)
        if allow_none:
            self.assertIsNone(msg)
        else:
            error = "'%s' is not a valid IP subnet" % cidr
            self.assertEqual(error, msg)

        # Invalid - IPv4 with trailing CR
        cidr = "10.0.2.0/24\r"
        msg = validator(cidr, None)
        error = "'%s' is not a valid IP subnet" % cidr
        self.assertEqual(error, msg)

    def test_validate_subnet(self):
        self._test_validate_subnet(validators.validate_subnet)

    def test_validate_subnet_or_none(self):
        self._test_validate_subnet(validators.validate_subnet_or_none,
                                   allow_none=True)

    def test_validate_subnet_list(self):
        msg = validators.validate_subnet_list('abc')
        self.assertEqual(u"'abc' is not a list", msg)
        msg = validators.validate_subnet_list(['10.1.0.0/24',
                                               '10.2.0.0/24',
                                               '10.1.0.0/24'])
        self.assertEqual(u"Duplicate items in the list: '10.1.0.0/24, "
                         u"10.2.0.0/24, 10.1.0.0/24'", msg)
        msg = validators.validate_subnet_list(['10.1.0.0/24', '10.2.0.0'])
        self.assertEqual(u"'10.2.0.0' isn't a recognized IP subnet cidr, "
                         u"'10.2.0.0/32' is recommended", msg)

    def _test_validate_regex(self, validator, allow_none=False):
        pattern = '[hc]at'

        data = None
        msg = validator(data, pattern)
        if allow_none:
            self.assertIsNone(msg)
        else:
            self.assertEqual("'None' is not a valid input", msg)

        data = 'bat'
        msg = validator(data, pattern)
        self.assertEqual("'%s' is not a valid input" % data, msg)

        data = 'hat'
        msg = validator(data, pattern)
        self.assertIsNone(msg)

        data = 'cat'
        msg = validator(data, pattern)
        self.assertIsNone(msg)

    def test_validate_regex(self):
        self._test_validate_regex(validators.validate_regex)

    def test_validate_regex_or_none(self):
        self._test_validate_regex(validators.validate_regex_or_none,
                                  allow_none=True)

    def test_validate_subnetpool_id(self):
        msg = validators.validate_subnetpool_id(constants.IPV6_PD_POOL_ID)
        self.assertIsNone(msg)

        msg = validators.validate_subnetpool_id(
            '00000000-ffff-ffff-ffff-000000000000')
        self.assertIsNone(msg)

    def test_validate_subnetpool_id_or_none(self):
        msg = validators.validate_subnetpool_id_or_none(None)
        self.assertIsNone(msg)

        msg = validators.validate_subnetpool_id_or_none(
            '00000000-ffff-ffff-ffff-000000000000')
        self.assertIsNone(msg)

    def test_validate_uuid(self):
        invalid_uuids = [None,
                         123,
                         '123',
                         't5069610-744b-42a7-8bd8-ceac1a229cd4',
                         'e5069610-744bb-42a7-8bd8-ceac1a229cd4']
        for uuid in invalid_uuids:
            msg = validators.validate_uuid(uuid)
            error = "'%s' is not a valid UUID" % uuid
            self.assertEqual(error, msg)

        msg = validators.validate_uuid('00000000-ffff-ffff-ffff-000000000000')
        self.assertIsNone(msg)

    def test__validate_list_of_items(self):
        # check not a list
        items = [None,
                 123,
                 'e5069610-744b-42a7-8bd8-ceac1a229cd4',
                 '12345678123456781234567812345678',
                 {'uuid': 'e5069610-744b-42a7-8bd8-ceac1a229cd4'}]
        for item in items:
            msg = validators._validate_list_of_items(mock.Mock(), item)
            error = "'%s' is not a list" % item
            self.assertEqual(error, msg)

        # check duplicate items in a list
        duplicate_items = ['e5069610-744b-42a7-8bd8-ceac1a229cd4',
                           'f3eeab00-8367-4524-b662-55e64d4cacb5',
                           'e5069610-744b-42a7-8bd8-ceac1a229cd4']
        msg = validators._validate_list_of_items(mock.Mock(), duplicate_items)
        error = ("Duplicate items in the list: "
                 "'%s'" % ', '.join(duplicate_items))
        self.assertEqual(error, msg)

        # check valid lists
        valid_lists = [[],
                       [1, 2, 3],
                       ['a', 'b', 'c']]
        for list_obj in valid_lists:
            msg = validators._validate_list_of_items(
                mock.Mock(return_value=None), list_obj)
            self.assertIsNone(msg)

    def test_validate_dict_type(self):
        for value in (None, True, '1', []):
            self.assertEqual("'%s' is not a dictionary" % value,
                             validators.validate_dict(value))

    def test_validate_dict_without_constraints(self):
        msg = validators.validate_dict({})
        self.assertIsNone(msg)

        # Validate a dictionary without constraints.
        msg = validators.validate_dict({'key': 'value'})
        self.assertIsNone(msg)

    def test_validate_a_valid_dict_with_constraints(self):
        dictionary, constraints = self._construct_dict_and_constraints()

        msg = validators.validate_dict(dictionary, constraints)
        self.assertIsNone(msg, 'Validation of a valid dictionary failed.')

    def test_validate_dict_with_invalid_validator(self):
        dictionary, constraints = self._construct_dict_and_constraints()

        constraints['key1'] = {'type:unsupported': None, 'required': True}
        msg = validators.validate_dict(dictionary, constraints)
        self.assertEqual("Validator 'type:unsupported' does not exist.", msg)

    def test_validate_dict_not_required_keys(self):
        dictionary, constraints = self._construct_dict_and_constraints()

        del dictionary['key2']
        msg = validators.validate_dict(dictionary, constraints)
        self.assertIsNone(msg, 'Field that was not required by the specs was'
                               'required by the validator.')

    def test_validate_dict_required_keys(self):
        dictionary, constraints = self._construct_dict_and_constraints()

        del dictionary['key1']
        msg = validators.validate_dict(dictionary, constraints)
        self.assertIn('Expected keys:', msg)

    def test_validate_dict_wrong_values(self):
        dictionary, constraints = self._construct_dict_and_constraints()

        dictionary['key1'] = 'UNSUPPORTED'
        msg = validators.validate_dict(dictionary, constraints)
        self.assertIsNotNone(msg)

    def test_validate_dict_convert_boolean(self):
        dictionary, constraints = self._construct_dict_and_constraints()

        constraints['key_bool'] = {
            'type:boolean': None,
            'required': False,
            'convert_to': converters.convert_to_boolean}
        dictionary['key_bool'] = 'true'
        msg = validators.validate_dict(dictionary, constraints)
        self.assertIsNone(msg)
        # Explicitly comparing with literal 'True' as assertTrue
        # succeeds also for 'true'
        self.assertIs(True, dictionary['key_bool'])

    def test_subdictionary(self):
        dictionary, constraints = self._construct_dict_and_constraints()

        del dictionary['key3']['k4']
        dictionary['key3']['k5'] = 'a string value'
        msg = validators.validate_dict(dictionary, constraints)
        self.assertIn('Expected keys:', msg)

    def test_validate_dict_or_none(self):
        dictionary, constraints = self._construct_dict_and_constraints()

        # Check whether None is a valid value.
        msg = validators.validate_dict_or_none(None, constraints)
        self.assertIsNone(msg, 'Validation of a None dictionary failed.')

        # Check validation of a regular dictionary.
        msg = validators.validate_dict_or_none(dictionary, constraints)
        self.assertIsNone(msg, 'Validation of a valid dictionary failed.')

    def test_validate_dict_or_empty(self):
        dictionary, constraints = self._construct_dict_and_constraints()

        # Check whether an empty dictionary is valid.
        msg = validators.validate_dict_or_empty({}, constraints)
        self.assertIsNone(msg, 'Validation of a None dictionary failed.')

        # Check validation of a regular dictionary.
        msg = validators.validate_dict_or_empty(dictionary, constraints)
        self.assertIsNone(msg, 'Validation of a valid dictionary failed.')

    def test_validate_dict_or_nodata(self):
        dictionary, constraints = self._construct_dict_and_constraints()

        # Check whether no data is a valid value.
        msg = validators.validate_dict_or_nodata(None, constraints)
        self.assertIsNone(msg, 'Validation of None for no-data failed.')
        msg = validators.validate_dict_or_nodata({}, constraints)
        self.assertIsNone(msg, 'Validation of empty dict for no-data failed.')

        # Check validation of a regular dictionary.
        msg = validators.validate_dict_or_nodata(dictionary, constraints)
        self.assertIsNone(msg, 'Validation of a valid dictionary failed.')

    def test_validate_non_negative(self):
        msg = validators.validate_non_negative('abc')
        self.assertEqual("'abc' is not an integer", msg)

        for value in (-1, '-2'):
            self.assertEqual("'%s' should be non-negative" % value,
                             validators.validate_non_negative(value))

        for value in (0, 1, '2', True, False):
            msg = validators.validate_non_negative(value)
            self.assertIsNone(msg)
