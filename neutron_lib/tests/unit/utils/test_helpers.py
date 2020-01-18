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

import collections
import re

import testtools

from neutron_lib.tests import _base as base
from neutron_lib.utils import helpers


class TestParseMappings(base.BaseTestCase):

    def parse(self, mapping_list, unique_values=True, unique_keys=True):
        return helpers.parse_mappings(mapping_list, unique_values, unique_keys)

    def test_parse_mappings_fails_for_missing_separator(self):
        with testtools.ExpectedException(ValueError):
            self.parse(['key'])

    def test_parse_mappings_fails_for_missing_key(self):
        with testtools.ExpectedException(ValueError):
            self.parse([':val'])

    def test_parse_mappings_fails_for_missing_value(self):
        with testtools.ExpectedException(ValueError):
            self.parse(['key:'])

    def test_parse_mappings_fails_for_extra_separator(self):
        with testtools.ExpectedException(ValueError):
            self.parse(['key:val:junk'])

    def test_parse_mappings_fails_for_duplicate_key(self):
        with testtools.ExpectedException(ValueError):
            self.parse(['key:val1', 'key:val2'])

    def test_parse_mappings_fails_for_duplicate_value(self):
        with testtools.ExpectedException(ValueError):
            self.parse(['key1:val', 'key2:val'])

    def test_parse_mappings_succeeds_for_one_mapping(self):
        self.assertEqual({'key': 'val'}, self.parse(['key:val']))

    def test_parse_mappings_succeeds_for_n_mappings(self):
        self.assertEqual({'key1': 'val1', 'key2': 'val2'},
                         self.parse(['key1:val1', 'key2:val2']))

    def test_parse_mappings_succeeds_for_duplicate_value(self):
        self.assertEqual({'key1': 'val', 'key2': 'val'},
                         self.parse(['key1:val', 'key2:val'], False))

    def test_parse_mappings_succeeds_for_no_mappings(self):
        self.assertEqual({}, self.parse(['']))

    def test_parse_mappings_succeeds_for_nonuniq_key(self):
        self.assertEqual({'key': ['val1', 'val2']},
                         self.parse(['key:val1', 'key:val2', 'key:val2'],
                                    unique_keys=False))

    def test_parse_mappings_succeeds_for_nonuniq_key_duplicate_value(self):
        self.assertEqual({'key': ['val']},
                         self.parse(['key:val', 'key:val', 'key:val'],
                                    unique_keys=False))


class TestCompareElements(base.BaseTestCase):

    def test_compare_elements(self):
        self.assertFalse(helpers.compare_elements([], ['napoli']))
        self.assertFalse(helpers.compare_elements(None, ['napoli']))
        self.assertFalse(helpers.compare_elements(['napoli'], []))
        self.assertFalse(helpers.compare_elements(['napoli'], None))
        self.assertFalse(helpers.compare_elements(['napoli', 'juve'],
                                                  ['juve']))
        self.assertTrue(helpers.compare_elements(['napoli', 'juve'],
                                                 ['napoli', 'juve']))
        self.assertTrue(helpers.compare_elements(['napoli', 'juve'],
                                                 ['juve', 'napoli']))


class TestDictUtils(base.BaseTestCase):

    def test_dict2str(self):
        dic = {"key1": "value1", "key2": "value2", "key3": "value3"}
        expected = "key1=value1,key2=value2,key3=value3"
        self.assertEqual(expected, helpers.dict2str(dic))

    def test_str2dict(self):
        string = "key1=value1,key2=value2,key3=value3"
        expected = {"key1": "value1", "key2": "value2", "key3": "value3"}
        self.assertEqual(expected, helpers.str2dict(string))

    def test_dict_str_conversion(self):
        dic = {"key1": "value1", "key2": "value2"}
        self.assertEqual(dic, helpers.str2dict(helpers.dict2str(dic)))

    def test_diff_list_of_dict(self):
        old_list = [{"key1": "value1"},
                    {"key2": "value2"},
                    {"key3": "value3"}]
        new_list = [{"key1": "value1"},
                    {"key2": "value2"},
                    {"key4": "value4"}]
        added, removed = helpers.diff_list_of_dict(old_list, new_list)
        self.assertEqual(added, [dict(key4="value4")])
        self.assertEqual(removed, [dict(key3="value3")])


class TestDict2Tuples(base.BaseTestCase):

    def test_dict(self):
        input_dict = {'foo': 'bar', '42': 'baz', 'aaa': 'zzz'}
        expected = (('42', 'baz'), ('aaa', 'zzz'), ('foo', 'bar'))
        output_tuple = helpers.dict2tuple(input_dict)
        self.assertEqual(expected, output_tuple)


class TestCamelize(base.BaseTestCase):

    def test_camelize(self):
        data = {'bandwidth_limit': 'BandwidthLimit',
                'test': 'Test',
                'some__more__dashes': 'SomeMoreDashes',
                'a_penguin_walks_into_a_bar': 'APenguinWalksIntoABar'}

        for s, expected in data.items():
            self.assertEqual(expected, helpers.camelize(s))


class TestRoundVal(base.BaseTestCase):

    def test_round_val_ok(self):
        for expected, value in ((0, 0),
                                (0, 0.1),
                                (1, 0.5),
                                (1, 1.49),
                                (2, 1.5)):
            self.assertEqual(expected, helpers.round_val(value))


class TestGetRandomString(base.BaseTestCase):

    def test_get_random_string(self):
        length = 127
        random_string = helpers.get_random_string(length)
        self.assertEqual(length, len(random_string))
        regex = re.compile('^[0-9a-fA-F]+$')
        self.assertIsNotNone(regex.match(random_string))


class TestSafeDecodeUtf8(base.BaseTestCase):

    def test_py3_decoded_valid_bytes(self):
        s = bytes('test-py2', 'utf-8')
        decoded_str = helpers.safe_decode_utf8(s)
        self.assertIsInstance(decoded_str, str)
        self.assertEqual(s, decoded_str.encode('utf-8'))

    def test_py3_decoded_invalid_bytes(self):
        s = bytes('test-py2', 'utf_16')
        decoded_str = helpers.safe_decode_utf8(s)
        self.assertIsInstance(decoded_str, str)


class TestSafeSortKey(base.BaseTestCase):

    def test_safe_sort_key(self):
        data1 = {'k1': 'v1',
                 'k2': 'v2'}
        data2 = {'k2': 'v2',
                 'k1': 'v1'}
        self.assertEqual(helpers.safe_sort_key(data1),
                         helpers.safe_sort_key(data2))

    def _create_dict_from_list(self, list_data):
        d = collections.defaultdict(list)
        for k, v in list_data:
            d[k].append(v)
        return d

    def test_safe_sort_key_mapping_ne(self):
        list1 = [('yellow', 1), ('blue', 2), ('yellow', 3),
                 ('blue', 4), ('red', 1)]
        data1 = self._create_dict_from_list(list1)
        list2 = [('yellow', 3), ('blue', 4), ('yellow', 1),
                 ('blue', 2), ('red', 1)]
        data2 = self._create_dict_from_list(list2)
        self.assertNotEqual(helpers.safe_sort_key(data1),
                            helpers.safe_sort_key(data2))

    def test_safe_sort_key_mapping(self):
        list1 = [('yellow', 1), ('blue', 2), ('red', 1)]
        data1 = self._create_dict_from_list(list1)
        list2 = [('blue', 2), ('red', 1), ('yellow', 1)]
        data2 = self._create_dict_from_list(list2)
        self.assertEqual(helpers.safe_sort_key(data1),
                         helpers.safe_sort_key(data2))
