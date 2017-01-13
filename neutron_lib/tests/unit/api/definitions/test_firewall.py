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

from neutron_lib.api.definitions import firewall
from neutron_lib.tests.unit.api.definitions import base


class FirewallDefinitionTestCase(base.DefinitionBaseTestCase):
    extension_module = firewall
    extension_resources = ('firewalls', 'firewall_policies', 'firewall_rules')
    extension_attributes = ('action', 'admin_state_up', 'audited',
                            'destination_ip_address', 'destination_port',
                            'enabled', 'firewall_policy_id', 'firewall_rules',
                            'ip_version', 'position', 'protocol',
                            'source_ip_address', 'source_port')
