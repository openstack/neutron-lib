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

from neutron_lib.api.definitions import sfc
from neutron_lib.tests.unit.api.definitions import base


class SFCDefinitionTestCase(base.DefinitionBaseTestCase):
    extension_module = sfc
    extension_resources = tuple(sfc.RESOURCE_ATTRIBUTE_MAP.keys())
    extension_attributes = (  # from port_pair:
                              'type', 'ingress', 'egress',
                              'service_function_parameters',
                              # from port_pair_group:
                              'group_id', 'port_pairs',
                              'port_pair_group_parameters',
                              # from port_chain:
                              'chain_id', 'port_pair_groups',
                              'flow_classifiers', 'chain_parameters')
