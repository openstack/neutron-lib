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

from neutron_lib.api.definitions import fip_pf_port_range as pf_port_range
from neutron_lib.api.definitions import floating_ip_port_forwarding as fip_pf
from neutron_lib.tests.unit.api.definitions import base


class FipPortForwardingPortRangeTestCase(base.DefinitionBaseTestCase):
    extension_module = pf_port_range
    extension_subresources = (fip_pf.COLLECTION_NAME,)
    extension_attributes = (pf_port_range.EXTERNAL_PORT_RANGE,
                            pf_port_range.INTERNAL_PORT_RANGE,
                            fip_pf.EXTERNAL_PORT,
                            fip_pf.INTERNAL_PORT,)
