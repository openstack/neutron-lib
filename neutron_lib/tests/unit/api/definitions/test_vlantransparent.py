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

from neutron_lib.api.definitions import vlantransparent
from neutron_lib.tests.unit.api.definitions import base


class VlantransparentDefinitionTestCase(base.DefinitionBaseTestCase):
    extension_module = vlantransparent
    extension_resources = ()
    extension_attributes = (vlantransparent.VLANTRANSPARENT,)

    def test_get_vlan_transparent(self):
        self.assertTrue(vlantransparent.get_vlan_transparent(
            {vlantransparent.VLANTRANSPARENT: True, 'vlan': '1'}))

    def test_get_vlan_transparent_not_set(self):
        self.assertFalse(vlantransparent.get_vlan_transparent(
            {'vlanxtx': True, 'vlan': '1'}))
