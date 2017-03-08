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
