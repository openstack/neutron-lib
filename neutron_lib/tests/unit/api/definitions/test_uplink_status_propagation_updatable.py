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

from neutron_lib.api.definitions import uplink_status_propagation as usp
from neutron_lib.api.definitions import uplink_status_propagation_updatable \
    as apidef
from neutron_lib.tests.unit.api.definitions import base


class UplinkStatusPropagationUpdatableDefinitionTestCase(
        base.DefinitionBaseTestCase):
    extension_module = apidef
    extension_resources = (usp.COLLECTION_NAME,)
    extension_attributes = (apidef.PROPAGATE_UPLINK_STATUS,)
