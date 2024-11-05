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

from neutron_lib.api.definitions import bgpvpn
from neutron_lib.api import validators
from neutron_lib.tests.unit.api.definitions import base


class BgpvpnDefinitionTestCase(base.DefinitionBaseTestCase):
    extension_module = bgpvpn
    extension_resources = (bgpvpn.COLLECTION_NAME,)
    extension_attributes = ('type', 'route_targets', 'import_targets',
                            'export_targets', 'route_distinguishers',
                            'networks', 'routers', 'router_id', 'network_id')
    extension_subresources = ('network_associations', 'router_associations')

    def _data_for_invalid_rtdt(self):
        values = [[':1'],
                  ['1:'],
                  ['42'],
                  ['65536:123456'],
                  ['123.456.789.123:65535'],
                  ['4294967296:65535'],
                  ['1.1.1.1:655351'],
                  ['4294967295:65536'],
                  [''],
                  ]
        yield from values

    def _data_for_valid_rtdt(self):
        values = [['1:1'],
                  ['1:4294967295'],
                  ['65535:0'],
                  ['65535:4294967295'],
                  ['1.1.1.1:1'],
                  ['1.1.1.1:65535'],
                  ['4294967295:0'],
                  ['65536:65535'],
                  ['4294967295:65535'],
                  ]
        yield from values

    def test_valid_rtrd(self):
        for rtrd in self._data_for_valid_rtdt():
            msg = validators.validate_list_of_regex_or_none(
                rtrd,
                bgpvpn.RTRD_REGEX)
            self.assertIsNone(msg)

    def test_invalid_rtrd(self):
        for rtrd in self._data_for_invalid_rtdt():
            msg = validators.validate_list_of_regex_or_none(
                rtrd,
                bgpvpn.RTRD_REGEX)
            self.assertIsNotNone(msg)
