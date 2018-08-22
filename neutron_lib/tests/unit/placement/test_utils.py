# Copyright 2018 Ericsson
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import uuid

from neutron_lib.placement import utils as place_utils
from neutron_lib.tests import _base as base


class TestPlacementUtils(base.BaseTestCase):

    def setUp(self):
        super(TestPlacementUtils, self).setUp()

        self._uuid_ns = uuid.UUID('94fedd4d-1ce0-4bb3-9c9a-c9c0f56de154')

    def test_physnet_trait(self):
        self.assertEqual(
            'CUSTOM_PHYSNET_SOME_PHYSNET',
            place_utils.physnet_trait('some-physnet'))

    def test_vnic_type_trait(self):
        self.assertEqual(
            'CUSTOM_VNIC_TYPE_SOMEVNICTYPE',
            place_utils.vnic_type_trait('somevnictype'))

    def test_six_uuid5_literal(self):
        try:
            # assertNotRaises
            place_utils.six_uuid5(
                namespace=self._uuid_ns,
                name='may or may not be a unicode string' +
                     ' depending on Python version')
        except Exception:
            self.fail('could not generate uuid')

    def test_six_uuid5_unicode(self):
        try:
            # assertNotRaises
            place_utils.six_uuid5(
                namespace=self._uuid_ns,
                name=u'unicode string')
        except Exception:
            self.fail('could not generate uuid')

    def test_agent_resource_provider_uuid(self):
        try:
            # assertNotRaises
            place_utils.agent_resource_provider_uuid(
                namespace=self._uuid_ns,
                host='some host')
        except Exception:
            self.fail('could not generate agent resource provider uuid')

    def test_device_resource_provider_uuid(self):
        try:
            # assertNotRaises
            place_utils.device_resource_provider_uuid(
                namespace=self._uuid_ns,
                host='some host',
                device='some device')
        except Exception:
            self.fail('could not generate device resource provider uuid')

    def test_agent_resource_provider_uuid_stable(self):
        uuid_a = place_utils.agent_resource_provider_uuid(
            namespace=self._uuid_ns,
            host='somehost')
        uuid_b = place_utils.agent_resource_provider_uuid(
            namespace=self._uuid_ns,
            host='somehost')
        self.assertEqual(uuid_a, uuid_b)

    def test_device_resource_provider_uuid_stable(self):
        uuid_a = place_utils.device_resource_provider_uuid(
            namespace=self._uuid_ns,
            host='somehost',
            device='some-device')
        uuid_b = place_utils.device_resource_provider_uuid(
            namespace=self._uuid_ns,
            host='somehost',
            device='some-device')
        self.assertEqual(uuid_a, uuid_b)

    def test_parse_rp_bandwidths(self):
        self.assertEqual(
            {},
            place_utils.parse_rp_bandwidths([]),
        )

        self.assertEqual(
            {'eth0': {'egress': None, 'ingress': None}},
            place_utils.parse_rp_bandwidths(['eth0']),
        )

        self.assertEqual(
            {'eth0': {'egress': None, 'ingress': None}},
            place_utils.parse_rp_bandwidths(['eth0::']),
        )

        self.assertRaises(
            ValueError,
            place_utils.parse_rp_bandwidths,
            ['eth0::', 'eth0::'],
        )

        self.assertRaises(
            ValueError,
            place_utils.parse_rp_bandwidths,
            ['eth0:not a number:not a number'],
        )

        self.assertEqual(
            {'eth0': {'egress': 1, 'ingress': None}},
            place_utils.parse_rp_bandwidths(['eth0:1:']),
        )

        self.assertEqual(
            {'eth0': {'egress': None, 'ingress': 1}},
            place_utils.parse_rp_bandwidths(['eth0::1']),
        )

        self.assertEqual(
            {'eth0': {'egress': 1, 'ingress': 1}},
            place_utils.parse_rp_bandwidths(['eth0:1:1']),
        )

        self.assertEqual(
            {'eth0': {'egress': 1, 'ingress': 1},
             'eth1': {'egress': 10, 'ingress': 10}},
            place_utils.parse_rp_bandwidths(['eth0:1:1', 'eth1:10:10']),
        )

    def test_parse_rp_inventory_defaults(self):
        self.assertEqual(
            {},
            place_utils.parse_rp_inventory_defaults({}),
        )

        self.assertRaises(
            ValueError,
            place_utils.parse_rp_inventory_defaults,
            {'allocation_ratio': '-1.0'}
        )

        self.assertEqual(
            {'allocation_ratio': 1.0},
            place_utils.parse_rp_inventory_defaults(
                {'allocation_ratio': '1.0'}),
        )

        self.assertRaises(
            ValueError,
            place_utils.parse_rp_inventory_defaults,
            {'min_unit': '-1'}
        )

        self.assertEqual(
            {'min_unit': 1},
            place_utils.parse_rp_inventory_defaults(
                {'min_unit': '1'}),
        )

        self.assertRaises(
            ValueError,
            place_utils.parse_rp_inventory_defaults,
            {'no such inventory parameter': 1}
        )
