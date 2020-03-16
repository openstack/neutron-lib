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

from oslo_config import cfg
from webob import exc

from neutron_lib.api.validators import allowedaddresspairs as validator
from neutron_lib.exceptions import allowedaddresspairs as addr_exc
from neutron_lib.tests import _base as base


class TestAllowedAddressPairs(base.BaseTestCase):

    def test__validate_allowed_address_pairs_not_a_list(self):
        for d in [{}, set(), 'abc', True, 1]:
            self.assertRaisesRegex(
                exc.HTTPBadRequest, 'must be a list',
                validator._validate_allowed_address_pairs, d)

    @mock.patch.object(cfg, 'CONF')
    def test__validate_allowed_address_pairs_exhausted(self, mock_conf):
        mock_conf.max_allowed_address_pair = 1
        self.assertRaises(
            addr_exc.AllowedAddressPairExhausted,
            validator._validate_allowed_address_pairs,
            [{}, {}])

    @mock.patch.object(cfg, 'CONF')
    def test__validate_allowed_address_pairs_invalid_mac(self, mock_conf):
        mock_conf.max_allowed_address_pair = 3
        self.assertRaisesRegex(
            exc.HTTPBadRequest, 'is not a valid MAC address',
            validator._validate_allowed_address_pairs,
            [{'mac_address': 1}])

    @mock.patch.object(cfg, 'CONF')
    def test__validate_allowed_address_pairs_missing_ip(self, mock_conf):
        mock_conf.max_allowed_address_pair = 3
        self.assertRaises(
            addr_exc.AllowedAddressPairsMissingIP,
            validator._validate_allowed_address_pairs,
            [{'ip_adress': '192.168.1.11'}])

    @mock.patch.object(cfg, 'CONF')
    def test__validate_allowed_address_pairs_duplicate(self, mock_conf):
        mock_conf.max_allowed_address_pair = 3
        self.assertRaises(
            addr_exc.DuplicateAddressPairInRequest,
            validator._validate_allowed_address_pairs,
            [{'ip_address': '192.168.1.11'},
             {'ip_address': '192.168.1.11'}])

    @mock.patch.object(cfg, 'CONF')
    def test__validate_allowed_address_pairs_invalid_attrs(self, mock_conf):
        mock_conf.max_allowed_address_pair = 3
        self.assertRaisesRegex(
            exc.HTTPBadRequest, 'Unrecognized attribute',
            validator._validate_allowed_address_pairs,
            [{'ip_address': '192.168.1.11'},
             {'ip_address': '192.168.1.12', 'idk': True}])

    @mock.patch.object(cfg, 'CONF')
    def test__validate_allowed_address_pairs_invalid_subnet(self, mock_conf):
        mock_conf.max_allowed_address_pair = 3
        self.assertRaisesRegex(
            exc.HTTPBadRequest, 'is not a valid IP subnet',
            validator._validate_allowed_address_pairs,
            [{'ip_address': '192.168.1.11'},
             {'ip_address': '192.168.1.0/a'}])

    @mock.patch.object(cfg, 'CONF')
    def test__validate_allowed_address_pairs_invalid_ip_address(
            self, mock_conf):
        mock_conf.max_allowed_address_pair = 3
        self.assertRaisesRegex(
            exc.HTTPBadRequest, 'is not a valid IP address',
            validator._validate_allowed_address_pairs,
            [{'ip_address': '192.168.1.a'},
             {'ip_address': '192.168.1.2'}])

    @mock.patch.object(cfg, 'CONF')
    def test__validate_allowed_address_pairs_good_data(self, mock_conf):
        mock_conf.max_allowed_address_pair = 3
        self.assertIsNone(validator._validate_allowed_address_pairs(
            [{'ip_address': '192.1.1.11'}, {'ip_address': '19.1.1.11'}]))
