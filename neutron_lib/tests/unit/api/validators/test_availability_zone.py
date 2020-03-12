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

from neutron_lib.api.validators import availability_zone as az_validator
from neutron_lib.db import constants as db_const
from neutron_lib import exceptions
from neutron_lib.tests import _base as base


class TestAvailabilityZoneValidator(base.BaseTestCase):

    @mock.patch.object(az_validator.validators,
                       'validate_list_of_unique_strings',
                       return_value='bad')
    def test__validate_availability_zone_hints_unique_strings(
            self, mock_unique_strs):
        self.assertEqual(
            'bad', az_validator._validate_availability_zone_hints(['a', 'a']))

    def test__validate_availability_zone_hints_excessive_len(self):
        self.assertRaisesRegex(
            exceptions.InvalidInput, 'Too many availability_zone_hints',
            az_validator._validate_availability_zone_hints,
            ['a' * (db_const.AZ_HINTS_DB_LEN + 1)])

    def test__validate_availability_zone_hints_valid_input(self):
        self.assertIsNone(
            az_validator._validate_availability_zone_hints(['a', 'b', 'c']))
