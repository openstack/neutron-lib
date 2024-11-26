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

import copy

from neutron_lib.api.definitions import port as port_def
from neutron_lib.api.definitions import uplink_status_propagation as usp


ALIAS = 'uplink-status-propagation-updatable'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Uplink status propagation updatable extension'
API_PREFIX = ''
DESCRIPTION = 'Provides ability to update the port uplink status.'
UPDATED_TIMESTAMP = '2024-09-03T18:00:00-00:00'
PROPAGATE_UPLINK_STATUS = usp.PROPAGATE_UPLINK_STATUS
RESOURCE_NAME = port_def.RESOURCE_NAME
COLLECTION_NAME = port_def.COLLECTION_NAME


propagate_uplink_status = copy.deepcopy(
    usp.RESOURCE_ATTRIBUTE_MAP[COLLECTION_NAME][PROPAGATE_UPLINK_STATUS])
propagate_uplink_status['allow_put'] = True

RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {PROPAGATE_UPLINK_STATUS: propagate_uplink_status},
}

SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = [usp.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
