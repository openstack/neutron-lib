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

from neutron_lib.api import converters
from neutron_lib.api.definitions import port as port_def

PROPAGATE_UPLINK_STATUS = 'propagate_uplink_status'

ALIAS = 'uplink-status-propagation'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Uplink status propagation extension'
API_PREFIX = ''
DESCRIPTION = 'Provides ability to propagate port uplink status.'
UPDATED_TIMESTAMP = '2018-05-31T18:00:00-00:00'
RESOURCE_NAME = port_def.RESOURCE_NAME
COLLECTION_NAME = port_def.COLLECTION_NAME
RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        PROPAGATE_UPLINK_STATUS: {'allow_post': True,
                                  'allow_put': False,
                                  'default': True,
                                  'convert_to': converters.convert_to_boolean,
                                  'is_visible': True},
    },
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = []
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
