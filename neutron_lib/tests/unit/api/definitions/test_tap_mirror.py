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

from neutron_lib.api.definitions import tap_mirror
from neutron_lib.tests.unit.api.definitions import base


class TapMirrorDefinitionTestCase(base.DefinitionBaseTestCase):
    extension_module = tap_mirror
    extension_resources = (tap_mirror.COLLECTION_NAME, )
    extension_attributes = ('port_id', 'remote_ip', 'directions',
                            'mirror_type')

    FILTERABLE_ATTRIBUTES = (
        'id', 'project_id', 'name', 'description', 'port_id',
        'remote_ip', 'mirror_type',
    )
    NON_FILTERABLE_ATTRIBUTES = ('directions',)

    def test_scalar_attributes_are_filterable(self):
        attr_map = tap_mirror.RESOURCE_ATTRIBUTE_MAP[
            tap_mirror.COLLECTION_NAME]
        for attribute in self.FILTERABLE_ATTRIBUTES:
            self.assertTrue(
                attr_map[attribute].get('is_filter'),
                f'{attribute} must be filterable')
        for attribute in self.NON_FILTERABLE_ATTRIBUTES:
            self.assertNotIn('is_filter', attr_map[attribute])
