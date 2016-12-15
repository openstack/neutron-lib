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

from neutron_lib.api.definitions import flowclassifier
from neutron_lib.tests.unit.api.definitions import base


class FlowClassifierDefinitionTestCase(base.DefinitionBaseTestCase):
    extension_module = flowclassifier
    extension_resources = (flowclassifier.COLLECTION_NAME,)
    extension_attributes = ('ethertype',
                            'protocol',
                            'source_port_range_min',
                            'source_port_range_max',
                            'destination_port_range_min',
                            'destination_port_range_max',
                            'source_ip_prefix',
                            'destination_ip_prefix',
                            'logical_destination_port',
                            'logical_source_port',
                            'l7_parameters')
