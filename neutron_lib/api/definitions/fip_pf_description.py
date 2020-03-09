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

from neutron_lib.api.definitions import floating_ip_port_forwarding as pfw
from neutron_lib.db import constants as db_const

DESCRIPTION_FIELD = "description"

ALIAS = 'floating-ip-port-forwarding-description'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Floating IP Port Forwarding new attribute description'
DESCRIPTION = 'Add a description field to Port Forwarding rules'
UPDATED_TIMESTAMP = '2019-11-01T10:00:00-00:00'
RESOURCE_ATTRIBUTE_MAP = {}
SUB_RESOURCE_ATTRIBUTE_MAP = {
    pfw.COLLECTION_NAME: {
        'parameters': {
            DESCRIPTION_FIELD: {
                'allow_post': True,
                'allow_put': True,
                'validate': {
                    'type:string':
                        db_const.LONG_DESCRIPTION_FIELD_SIZE},
                'is_visible': True,
                'is_sort_key': False,
                'is_filter': True,
                'default': ''
            }
        }
    }
}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = [pfw.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
