# Copyright 2012 OpenStack Foundation
# All Rights Reserved.
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

from unittest import mock

import netaddr
import testtools

from neutron_lib.api import converters
from neutron_lib import constants
from neutron_lib import exceptions as n_exc
from neutron_lib.tests import _base as base
from neutron_lib.tests import tools


class TestConvertToBoolean(base.BaseTestCase):

    def test_convert_to_boolean_bool(self):
        self.assertIs(converters.convert_to_boolean(True), True)
        self.assertIs(converters.convert_to_boolean(False), False)

    def test_convert_to_boolean_int(self):
        self.assertIs(converters.convert_to_boolean(0), False)
        self.assertIs(converters.convert_to_boolean(1), True)
        self.assertRaises(n_exc.InvalidInput,
                          converters.convert_to_boolean,
                          7)

    def test_convert_to_boolean_str(self):
        self.assertIs(converters.convert_to_boolean('True'), True)
        self.assertIs(converters.convert_to_boolean('true'), True)
        self.assertIs(converters.convert_to_boolean('False'), False)
        self.assertIs(converters.convert_to_boolean('false'), False)
        self.assertIs(converters.convert_to_boolean('0'), False)
        self.assertIs(converters.convert_to_boolean('1'), True)
        self.assertRaises(n_exc.InvalidInput,
                          converters.convert_to_boolean,
                          '7')

    def test_convert_to_boolean_if_not_none(self):
        self.assertIsNone(converters.convert_to_boolean_if_not_none(None))
        self.assertIs(converters.convert_to_boolean_if_not_none(1), True)


class TestConvertToInt(base.BaseTestCase):

    def test_convert_to_int_int(self):
        self.assertEqual(-1, converters.convert_to_int(-1))
        self.assertEqual(0, converters.convert_to_int(0))
        self.assertEqual(1, converters.convert_to_int(1))

    def test_convert_to_int_if_not_none(self):
        self.assertEqual(-1, converters.convert_to_int_if_not_none(-1))
        self.assertEqual(0, converters.convert_to_int_if_not_none(0))
        self.assertEqual(1, converters.convert_to_int_if_not_none(1))
        self.assertIsNone(converters.convert_to_int_if_not_none(None))

    def test_convert_to_int_str(self):
        self.assertEqual(4, converters.convert_to_int('4'))
        self.assertEqual(6, converters.convert_to_int('6'))
        self.assertRaises(n_exc.InvalidInput,
                          converters.convert_to_int,
                          'garbage')

    def test_convert_to_int_none(self):
        self.assertRaises(n_exc.InvalidInput,
                          converters.convert_to_int,
                          None)

    def test_convert_none_to_empty_list_none(self):
        self.assertEqual([], converters.convert_none_to_empty_list(None))

    def test_convert_none_to_empty_dict(self):
        self.assertEqual({}, converters.convert_none_to_empty_dict(None))

    def test_convert_none_to_empty_list_value(self):
        values = ['1', 3, [], [1], {}, {'a': 3}]
        for value in values:
            self.assertEqual(
                value, converters.convert_none_to_empty_list(value))


class TestConvertToFloat(base.BaseTestCase):
    # NOTE: the routine being tested here is a plugin-specific extension
    # module. As the plugin split proceed towards its second phase this
    # test should either be remove, or the validation routine moved into
    # neutron.api.v2.attributes

    def test_convert_to_float_positve_value(self):
        self.assertEqual(
            1.111, converters.convert_to_positive_float_or_none(1.111))
        self.assertEqual(1, converters.convert_to_positive_float_or_none(1))
        self.assertEqual(0, converters.convert_to_positive_float_or_none(0))

    def test_convert_to_float_negative_value(self):
        self.assertRaises(n_exc.InvalidInput,
                          converters.convert_to_positive_float_or_none,
                          -1.11)

    def test_convert_to_float_string(self):
        self.assertEqual(4, converters.convert_to_positive_float_or_none('4'))
        self.assertEqual(
            4.44, converters.convert_to_positive_float_or_none('4.44'))
        self.assertRaises(n_exc.InvalidInput,
                          converters.convert_to_positive_float_or_none,
                          'garbage')

    def test_convert_to_float_none_value(self):
        self.assertIsNone(converters.convert_to_positive_float_or_none(None))


class TestConvertKvp(base.BaseTestCase):

    def test_convert_kvp_list_to_dict_succeeds_for_missing_values(self):
        result = converters.convert_kvp_list_to_dict(['True'])
        self.assertEqual({}, result)

    def test_convert_kvp_list_to_dict_succeeds_for_multiple_values(self):
        result = converters.convert_kvp_list_to_dict(
            ['a=b', 'a=c', 'a=c', 'b=a'])
        expected = {'a': tools.UnorderedList(['c', 'b']), 'b': ['a']}
        self.assertEqual(expected, result)

    def test_convert_kvp_list_to_dict_succeeds_for_values(self):
        result = converters.convert_kvp_list_to_dict(['a=b', 'c=d'])
        self.assertEqual({'a': ['b'], 'c': ['d']}, result)

    def test_convert_kvp_str_to_list_fails_for_missing_key(self):
        with testtools.ExpectedException(n_exc.InvalidInput):
            converters.convert_kvp_str_to_list('=a')

    def test_convert_kvp_str_to_list_fails_for_missing_equals(self):
        with testtools.ExpectedException(n_exc.InvalidInput):
            converters.convert_kvp_str_to_list('a')

    def test_convert_kvp_str_to_list_succeeds_for_one_equals(self):
        result = converters.convert_kvp_str_to_list('a=')
        self.assertEqual(['a', ''], result)

    def test_convert_kvp_str_to_list_succeeds_for_two_equals(self):
        result = converters.convert_kvp_str_to_list('a=a=a')
        self.assertEqual(['a', 'a=a'], result)


class TestConvertToList(base.BaseTestCase):

    def test_convert_to_empty_list(self):
        for item in (None, [], (), {}):
            self.assertEqual([], converters.convert_to_list(item))

    def test_convert_to_list_string(self):
        for item in ('', 'foo'):
            self.assertEqual([item], converters.convert_to_list(item))

    def test_convert_to_list_iterable(self):
        for item in ([None], [1, 2, 3], (1, 2, 3), {1, 2, 3}, ['foo']):
            self.assertEqual(list(item), converters.convert_to_list(item))

    def test_convert_to_list_non_iterable(self):
        for item in (True, False, 1, 1.2, object()):
            self.assertEqual([item], converters.convert_to_list(item))


class TestConvertIPv6AddrCanonicalFormat(base.BaseTestCase):

    def test_convert_ipv6_address_extended_add_with_zeroes(self):
        result = converters.convert_ip_to_canonical_format(
            '2001:0db8:0:0:0:0:0:0001')
        self.assertEqual('2001:db8::1', result)

    def test_convert_ipv6_compressed_address(self):
        result = converters.convert_ip_to_canonical_format(
            '2001:db8:0:1:1:1:1:1')
        self.assertEqual('2001:db8:0:1:1:1:1:1', result)

    def test_convert_ipv6_extended_addr_to_compressed(self):
        result = converters.convert_ip_to_canonical_format(
            "Fe80:0:0:0:0:0:0:1")
        self.assertEqual('fe80::1', result)

    def test_convert_ipv4_address(self):
        result = converters.convert_ip_to_canonical_format("192.168.1.1")
        self.assertEqual('192.168.1.1', result)

    def test_convert_None_address(self):
        result = converters.convert_ip_to_canonical_format(None)
        self.assertIsNone(result)

    def test_convert_invalid_address(self):
        result = converters.convert_ip_to_canonical_format("on")
        self.assertEqual("on", result)
        result = converters.convert_ip_to_canonical_format(
            '192.168.1.1/32')
        self.assertEqual('192.168.1.1/32', result)
        result = converters.convert_ip_to_canonical_format(
            '2001:db8:0:1:1:1:1:1/128')
        self.assertEqual('2001:db8:0:1:1:1:1:1/128', result)

    def test_convert_subnetpools(self):
        pools = [{'start': '1.1.1.1', 'end': '1.1.1.100'}]
        result = converters.convert_ip_to_canonical_format(pools)
        self.assertEqual(pools, result)


class TestConvertAllocationPoolsCanonicalFormat(base.BaseTestCase):

    def test_convert_allocation_pools_to_canonical_format_noop(self):
        pools = [{'start': '1.1.1.1', 'end': '1.1.1.100'}]
        result = converters.convert_allocation_pools_to_canonical_format(pools)
        self.assertEqual(pools, result)

    def test_convert_allocation_pools_to_canonical_format(self):
        pools = [
            {'start': 'Fe80:0:0:0:0:0:0:1', 'end': 'Fe80:0:0:0:0:0:0:100'},
        ]
        result = converters.convert_allocation_pools_to_canonical_format(pools)

        expected = [
            {'start': 'fe80::1', 'end': 'fe80::100'},
        ]
        self.assertEqual(expected, result)

    def test_convert_allocation_pools_to_canonical_format_None(self):
        result = converters.convert_allocation_pools_to_canonical_format(None)
        self.assertEqual([], result)

    def test_convert_allocation_pools_to_canonical_format_invalid_data(self):
        self.assertRaises(
            n_exc.InvalidInput,
            converters.convert_allocation_pools_to_canonical_format,
            '10.0.0.0/24')


class TestConvertIPv6CIDRCanonicalFormat(base.BaseTestCase):

    def test_convert_ipv4_address_with_CIDR(self):
        result = converters.convert_cidr_to_canonical_format('192.168.1.1/24')
        self.assertEqual('192.168.1.1/24', result)

    def test_convert_ipv6_extended_addr_withcidr_to_compressed(self):
        result = converters.convert_cidr_to_canonical_format(
            'Fe80:0:0:0:0:0:0:1/64')
        self.assertEqual('fe80::1/64', result)

    def test_convert_non_ip_addr_with_slash(self):
        with testtools.ExpectedException(n_exc.InvalidInput):
            converters.convert_cidr_to_canonical_format(
                "Dormamu/DarkSeid/Vulture")


class TestConvertStringToCaseInsensitive(base.BaseTestCase):

    def test_convert_string_to_lower(self):
        result = converters.convert_string_to_case_insensitive("THIS Is tEsT")
        self.assertIsInstance(result, str)

    def test_assert_error_on_non_string(self):
        for invalid in [[], 123]:
            with testtools.ExpectedException(n_exc.InvalidInput):
                converters.convert_string_to_case_insensitive(invalid)


class TestConvertProtocol(base.BaseTestCase):

    def test_tcp_is_valid(self):
        result = converters.convert_to_protocol(constants.PROTO_NAME_TCP)
        self.assertEqual(constants.PROTO_NAME_TCP, result)
        proto_num_str = str(constants.PROTO_NUM_TCP)
        result = converters.convert_to_protocol(proto_num_str)
        self.assertEqual(proto_num_str, result)

    def test_udp_is_valid(self):
        result = converters.convert_to_protocol(constants.PROTO_NAME_UDP)
        self.assertEqual(constants.PROTO_NAME_UDP, result)
        proto_num_str = str(constants.PROTO_NUM_UDP)
        result = converters.convert_to_protocol(proto_num_str)
        self.assertEqual(proto_num_str, result)

    def test_icmp_is_valid(self):
        result = converters.convert_to_protocol(constants.PROTO_NAME_ICMP)
        self.assertEqual(constants.PROTO_NAME_ICMP, result)
        proto_num_str = str(constants.PROTO_NUM_ICMP)
        result = converters.convert_to_protocol(proto_num_str)
        self.assertEqual(proto_num_str, result)

    def test_numeric_is_valid(self):
        proto_num_str = str(constants.PROTO_NUM_IGMP)
        result = converters.convert_to_protocol(proto_num_str)
        self.assertEqual(proto_num_str, result)

    def test_numeric_too_high(self):
        with testtools.ExpectedException(n_exc.InvalidInput):
            converters.convert_to_protocol("300")

    def test_numeric_too_low(self):
        with testtools.ExpectedException(n_exc.InvalidInput):
            converters.convert_to_protocol("-1")

    def test_unknown_string(self):
        with testtools.ExpectedException(n_exc.InvalidInput):
            converters.convert_to_protocol("Invalid")


class TestConvertToString(base.BaseTestCase):

    def test_data_is_string(self):
        self.assertEqual('10000', converters.convert_to_string('10000'))

    def test_data_is_integer(self):
        self.assertEqual('10000', converters.convert_to_string(10000))

    def test_data_is_integer_zero(self):
        self.assertEqual('0', converters.convert_to_string(0))

    def test_data_is_none(self):
        self.assertIsNone(converters.convert_to_string(None))

    def test_data_is_empty_list(self):
        self.assertEqual('[]', converters.convert_to_string([]))

    def test_data_is_list(self):
        self.assertEqual("[1, 2, 3]", converters.convert_to_string([1, 2, 3]))

    def test_data_is_empty_dict(self):
        self.assertEqual('{}', converters.convert_to_string({}))

    def test_data_is_dict(self):
        self.assertEqual("{'foo': 'bar'}",
                         converters.convert_to_string({'foo': 'bar'}))


class TestConvertUppercasePrefix(base.BaseTestCase):

    def test_prefix_not_present(self):
        self.assertEqual('foobar',
                         converters.convert_prefix_forced_case('foobar',
                                                               'bar'))

    def test_prefix_no_need_to_replace(self):
        self.assertEqual('FOObar',
                         converters.convert_prefix_forced_case('FOObar',
                                                               'FOO'))

    def test_ucfirst_prefix_converted_1(self):
        self.assertEqual('Foobar',
                         converters.convert_prefix_forced_case('foobar',
                                                               'Foo'))

    def test_lc_prefix_converted_2(self):
        self.assertEqual('foobar',
                         converters.convert_prefix_forced_case('fOobar',
                                                               'foo'))

    def test_mixed_prefix_converted_1(self):
        self.assertEqual('fOoXbar',
                         converters.convert_prefix_forced_case('Fooxbar',
                                                               'fOoX'))

    def test_shorter_string(self):
        self.assertEqual('fo',
                         converters.convert_prefix_forced_case('fo',
                                                               'foo'))


class TestConvertPortMacAddress(base.BaseTestCase):

    def test_mac_address_does_not_convert(self):
        valid_mac = 'fa:16:3e:b6:78:1f'
        self.assertEqual(valid_mac,
                         converters.convert_to_mac_if_none(valid_mac))

    @mock.patch('oslo_config.cfg.CONF')
    def test_convert_none_to_mac_address(self, CONF):
        CONF.base_mac = 'fa:16:3e:00:00:00'
        self.assertTrue(
            netaddr.valid_mac(converters.convert_to_mac_if_none(None)))


class TestConvertToSanitizedMacAddress(base.BaseTestCase):

    def test_sanitize_mac_address(self):
        input_exp = (('00:11:22:33:44:55', '00:11:22:33:44:55'),
                     ('00:11:22:33:44:5', '00:11:22:33:44:05'),
                     ('0:1:2:3:4:5', '00:01:02:03:04:05'),
                     ('ca:FE:cA:Fe:a:E', 'ca:fe:ca:fe:0a:0e'),
                     ('12345678901', '01:23:45:67:89:01'),
                     ('012345678901', '01:23:45:67:89:01'),
                     )
        for input, expected in input_exp:
            self.assertEqual(
                expected,
                converters.convert_to_sanitized_mac_address(input))
            eui_address = netaddr.EUI(input)
            self.assertEqual(
                expected,
                converters.convert_to_sanitized_mac_address(eui_address))

        # Not converted, those MAC address will fail in the validation step.
        self.assertEqual(
            '00:11:22:33:44',
            converters.convert_to_sanitized_mac_address('00:11:22:33:44'))
        self.assertEqual(
            '00:11:22:33:44:',
            converters.convert_to_sanitized_mac_address('00:11:22:33:44:'))


class TestConvertToSanitizedBindingProfileAllocation(base.BaseTestCase):

    RP_UUID = '41d7391e-1f69-11ec-a899-8f9d6d950f8d'
    PORT_ID = '64d01804-1f83-11ec-987c-7f6caec3998b'
    MIN_BW_RULE_ID = '52441596-1f83-11ec-93c5-9b759591a493'
    # uuid -v5 64d01804-1f83-11ec-987c-7f6caec3998b
    # 52441596-1f83-11ec-93c5-9b759591a493
    GROUP_UUID = '2a1be6ea-15b0-5ac1-9d70-643e2ae306cb'

    def test_sanitize_binding_profile_allocation(self):
        old_format = self.RP_UUID
        new_format = {self.GROUP_UUID: self.RP_UUID}
        min_bw_rules = [mock.MagicMock(id=self.MIN_BW_RULE_ID)]
        self.assertEqual(
            new_format,
            converters.convert_to_sanitized_binding_profile_allocation(
                old_format, self.PORT_ID, min_bw_rules))

        self.assertEqual(
            new_format,
            converters.convert_to_sanitized_binding_profile_allocation(
                new_format, self.PORT_ID, min_bw_rules))
