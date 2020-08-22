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

from neutron_lib.api.definitions import l3_ndp_proxy
from neutron_lib.tests.unit.api.definitions import base


class L3NDPProxyDefinitionTestCase(base.DefinitionBaseTestCase):
    extension_module = l3_ndp_proxy
    extension_resources = (l3_ndp_proxy.COLLECTION_NAME,)
    extension_attributes = (l3_ndp_proxy.ID, l3_ndp_proxy.NAME,
                            l3_ndp_proxy.PROJECT_ID, l3_ndp_proxy.ROUTER_ID,
                            l3_ndp_proxy.PORT_ID, l3_ndp_proxy.IP_ADDRESS,
                            l3_ndp_proxy.DESCRIPTION,)
