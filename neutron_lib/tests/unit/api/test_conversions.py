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

import testtools

from neutron_lib.api import converters
from neutron_lib import exceptions as n_exc
from neutron_lib.tests import _base as base
from neutron_lib.tests import _tools as tools


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
        for item in ([None], [1, 2, 3], (1, 2, 3), set([1, 2, 3]), ['foo']):
            self.assertEqual(list(item), converters.convert_to_list(item))

    def test_convert_to_list_non_iterable(self):
        for item in (True, False, 1, 1.2, object()):
            self.assertEqual([item], converters.convert_to_list(item))
