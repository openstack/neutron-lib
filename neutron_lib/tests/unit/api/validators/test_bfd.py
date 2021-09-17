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

from neutron_lib.api.definitions import bfd_monitor as bfd_api
from neutron_lib.api.validators import bfd
from neutron_lib.tests import _base as base


class TestBfdValidators(base.BaseTestCase):
    def test_validate_bfd_mode(self):
        self.assertIn('Blank strings', bfd.validate_bfd_mode('', None))
        for mode in bfd_api.VALID_MODES:
            self.assertIsNone(bfd.validate_bfd_mode(mode, bfd_api.VALID_MODES))

        expected = 'BFD monitor mode can be only one of'
        msg = bfd.validate_bfd_mode('apple', bfd_api.VALID_MODES)
        self.assertIn(expected, msg)

    def test_validate_bfd_auth_type(self):
        self.assertIsNone(bfd.validate_bfd_auth_type('', None))
        for a_type in bfd_api.VALID_AUTH_TYPES:
            self.assertIsNone(
                bfd.validate_bfd_auth_type(a_type, bfd_api.VALID_AUTH_TYPES))

        expected = 'BFD monitor aut_type can only one of'
        msg = bfd.validate_bfd_auth_type('apple', bfd_api.VALID_AUTH_TYPES)
        self.assertIn(expected, msg)
