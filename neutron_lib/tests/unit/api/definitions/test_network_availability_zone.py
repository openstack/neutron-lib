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

from neutron_lib.api.definitions import availability_zone
from neutron_lib.api.definitions import network_availability_zone
from neutron_lib.tests.unit.api.definitions import base


class NetworkAvailabilityZoneDefinitionTestCase(base.DefinitionBaseTestCase):
    extension_module = network_availability_zone
    extension_attributes = (availability_zone.AZ_HINTS,
                            availability_zone.COLLECTION_NAME)
