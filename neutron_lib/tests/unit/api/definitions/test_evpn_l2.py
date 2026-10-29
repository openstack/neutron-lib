# Copyright 2026 Red Hat, LLC
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

from neutron_lib.api import attributes
from neutron_lib.api.definitions import evpn_l2
from neutron_lib import constants
from neutron_lib import exceptions
from neutron_lib.tests.unit.api.definitions import base


class EVPNL2DefinitionTestCase(base.DefinitionBaseTestCase):
    extension_module = evpn_l2
    extension_attributes = (evpn_l2.EVPN_VNI, evpn_l2.EVPN_RT)

    def setUp(self):
        super().setUp()
        self.attr_info = attributes.AttributeInfo(
            evpn_l2.RESOURCE_ATTRIBUTE_MAP[evpn_l2.COLLECTION_NAME])

    def test_valid_vni(self):
        for value, expected in ((None, None), (0, 0), ('0', 0), (1, 1),
                                ('10000', 10000),
                                (constants.MAX_VXLAN_VNI,
                                 constants.MAX_VXLAN_VNI)):
            with self.subTest(value=value):
                request = {evpn_l2.EVPN_VNI: value}
                self.attr_info.fill_post_defaults(request)
                self.attr_info.convert_values(request)
                self.assertEqual({evpn_l2.EVPN_VNI: expected}, request)

    def test_invalid_vni(self):
        for value in (-1, constants.MAX_VXLAN_VNI + 1, '', 'invalid', [], {}):
            with self.subTest(value=value):
                self.assertRaises(
                    exceptions.InvalidInput, self.attr_info.convert_values,
                    {evpn_l2.EVPN_VNI: value})

    def test_valid_route_target(self):
        for value in (None, '0:0', '1:4294967295', '65535:4294967295',
                      '192.168.1.1:100', '255.255.255.255:65535',
                      '65536:65535', '4294967295:0', '4294967295:65535'):
            with self.subTest(value=value):
                request = {evpn_l2.EVPN_RT: value}
                self.attr_info.convert_values(request)
                self.assertEqual({evpn_l2.EVPN_RT: value}, request)

    def test_invalid_route_target(self):
        for value in ('', ':1', '1:', '42', '-1:1', '1:-1',
                      '65535:4294967296', '65536:65536', '4294967296:1',
                      '192.168.1.1:65536', '256.168.1.1:1', '2001:db8::1:1',
                      '1:1:1', ' 1:1', '1:1 ', 10000, [], {}, ['1:1']):
            with self.subTest(value=value):
                self.assertRaises(
                    exceptions.InvalidInput, self.attr_info.convert_values,
                    {evpn_l2.EVPN_RT: value})

    def test_route_target_not_allowed_on_create(self):
        for value in (None, '192.168.1.1:100'):
            with self.subTest(value=value):
                self.assertRaises(
                    exceptions.InvalidInput, self.attr_info.fill_post_defaults,
                    {evpn_l2.EVPN_RT: value})

    def test_unspecified_attributes_on_create(self):
        request = {}
        self.attr_info.fill_post_defaults(request)
        self.attr_info.convert_values(request)
        self.assertIs(constants.ATTR_NOT_SPECIFIED, request[evpn_l2.EVPN_VNI])
        self.assertNotIn(evpn_l2.EVPN_RT, request)

    def test_unspecified_attributes_on_update(self):
        request = {}
        self.attr_info.convert_values(request)
        self.assertEqual({}, request)

    def test_remove_vni_and_route_target(self):
        request = {evpn_l2.EVPN_VNI: None, evpn_l2.EVPN_RT: None}
        self.attr_info.convert_values(request)
        self.assertEqual(
            {evpn_l2.EVPN_VNI: None, evpn_l2.EVPN_RT: None}, request)
