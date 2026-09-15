# All rights reserved.
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

from neutron_lib.api.definitions import taas
from neutron_lib.tests.unit.api.definitions import base


class TaasDefinitionTestCase(base.DefinitionBaseTestCase):
    extension_module = taas
    extension_resources = (taas.COLLECTION_NAME, taas.TAP_FLOWS,)
    extension_attributes = ('port_id', 'tap_service_id', 'source_port',
                            'direction')

    FILTERABLE_ATTRIBUTES = {
        taas.COLLECTION_NAME: (
            'id', 'tenant_id', 'name', 'description', 'port_id', 'status',
        ),
        taas.TAP_FLOWS: (
            'id', 'tenant_id', 'name', 'description', 'tap_service_id',
            'source_port', 'direction', 'status',
        ),
    }

    def test_scalar_attributes_are_filterable(self):
        for resource, attributes in self.FILTERABLE_ATTRIBUTES.items():
            attr_map = taas.RESOURCE_ATTRIBUTE_MAP[resource]
            for attribute in attributes:
                self.assertTrue(
                    attr_map[attribute].get('is_filter'),
                    f'{resource}.{attribute} must be filterable')
