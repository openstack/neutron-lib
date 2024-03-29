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
from neutron_lib.api.definitions import vlan_filter
from neutron_lib.tests.unit.api.definitions import base


class TaasVlanFilterDefinitionTestCase(base.DefinitionBaseTestCase):
    extension_module = vlan_filter
    extension_resources = (taas.TAP_FLOWS,)
    extension_attributes = ('vlan_filter',)
