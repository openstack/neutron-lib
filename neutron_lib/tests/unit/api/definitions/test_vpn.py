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

from neutron_lib.api.definitions import vpn
from neutron_lib.api import validators
from neutron_lib.tests.unit.api.definitions import base


class VPNDefinitionTestCase(base.DefinitionBaseTestCase):
    extension_module = vpn
    extension_resources = ('vpnservices', 'ipsec_site_connections',
                           'ipsecpolicies', 'ikepolicies',)
    extension_attributes = ('auth_algorithm', 'auth_mode', 'dpd',
                            'encapsulation_mode', 'encryption_algorithm',
                            'external_v4_ip', 'external_v6_ip',
                            'ike_version', 'ikepolicy_id', 'initiator',
                            'ipsecpolicy_id', 'lifetime', 'local_ep_group_id',
                            'local_id', 'mtu', 'peer_address', 'peer_cidrs',
                            'peer_ep_group_id', 'peer_id', 'pfs',
                            'phase1_negotiation_mode', 'psk', 'route_mode',
                            'router_id', 'subnet_id', 'transform_protocol',
                            'vpnservice_id',)

    def _get_attr_spec(self, attr_name):
        attr_map = vpn.RESOURCE_ATTRIBUTE_MAP[vpn.IPSEC_SITE_CONNECTIONS]
        return attr_map[attr_name]

    def _validate(self, attr_name, value):
        spec = self._get_attr_spec(attr_name)
        validate = spec['validate']
        self.assertEqual(1, len(validate))
        validator_type, valid_values = next(iter(validate.items()))
        validator_func = validators.get_validator(validator_type)
        return validator_func(value, valid_values)

    def test_local_id_and_peer_id_use_ipsec_id_regex(self):
        for attr_name in ('local_id', 'peer_id'):
            spec = self._get_attr_spec(attr_name)
            self.assertEqual({'type:regex_or_none': vpn.IPSEC_ID_REGEX},
                             spec['validate'])

    def test_local_id_and_peer_id_accept_valid_values(self):
        valid_values = ('192.168.1.1', 'vpn.example.com',
                        'user@example.com', 'my-peer_01', '')
        for attr_name in ('local_id', 'peer_id'):
            for value in valid_values:
                self.assertIsNone(self._validate(attr_name, value))

    def test_local_id_and_peer_id_reject_injection_payloads(self):
        invalid_values = (
            'evil\nconn evil\n  leftupdown=/bin/sh',
            'peer\r\nauth=secret',
            'has space',
            'a;rm -rf /',
            'a,b=c',
        )
        for attr_name in ('local_id', 'peer_id'):
            for value in invalid_values:
                self.assertIsNotNone(self._validate(attr_name, value))
