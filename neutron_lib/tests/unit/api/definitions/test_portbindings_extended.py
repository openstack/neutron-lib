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

from neutron_lib.api.definitions import portbindings_extended as pbe
from neutron_lib.tests.unit.api.definitions import base


class PortbindingsExtendedDefinitionTestCase(base.DefinitionBaseTestCase):
    extension_module = pbe
    extension_attributes = (pbe.VIF_TYPE,
                            pbe.VIF_DETAILS,
                            pbe.VNIC_TYPE,
                            pbe.HOST,
                            pbe.PROFILE,
                            pbe.STATUS,
                            pbe.PROJECT_ID)
    extension_subresources = (pbe.COLLECTION_NAME,)
