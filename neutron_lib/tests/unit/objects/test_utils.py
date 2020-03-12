# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from unittest import mock

from neutron_lib.objects import utils as obj_utils
from neutron_lib.tests import _base as base


class TestUtils(base.BaseTestCase):

    def test_get_objects_with_filters_not_in(self):

        class FakeColumn(object):
            def __init__(self, column):
                self.column = column

            def in_(self, value):
                self.value = value
                return self

            def __invert__(self):
                return list(set(self.column) - set(self.value))

        filter_obj = obj_utils.NotIn([1, 2, 3])
        fake_column = FakeColumn([1, 2, 4, 5])
        self.assertEqual([4, 5],
                         sorted(filter_obj.filter(fake_column)))

        fake_column = FakeColumn([1, 2])
        self.assertEqual([], filter_obj.filter(fake_column))

        fake_column = FakeColumn([4, 5])
        self.assertEqual([4, 5],
                         sorted(filter_obj.filter(fake_column)))

    def test_get_objects_with_filters_not_equal(self):

        class FakeColumn(object):
            def __init__(self, column):
                self.column = column

            def __ne__(self, value):
                return [item for item in self.column if item != value]

        filter_obj = obj_utils.NotEqual(1)
        fake_column = FakeColumn([1, 2, 4, 5])
        self.assertEqual([2, 4, 5],
                         sorted(filter_obj.filter(fake_column)))

        fake_column = FakeColumn([1])
        self.assertEqual([], filter_obj.filter(fake_column))

        fake_column = FakeColumn([4, 5])
        self.assertEqual([4, 5],
                         sorted(filter_obj.filter(fake_column)))

    def test_get_updatable_fields(self):
        mock_class = mock.Mock()
        mock_class.fields_no_update = [0, 2, 6]

        mock_fields = mock.Mock()
        mock_fields.copy.return_value = {k: k for k in range(7)}

        updatable = obj_utils.get_updatable_fields(mock_class, mock_fields)
        self.assertEqual([1, 3, 4, 5],
                         sorted(list(updatable.keys())))
