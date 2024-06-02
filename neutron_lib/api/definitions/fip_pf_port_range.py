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

from neutron_lib.api.definitions import fip_pf_description as pfw_desc
from neutron_lib.api.definitions import floating_ip_port_forwarding as pfw

ALIAS = 'floating-ip-port-forwarding-port-ranges'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Floating IP Port Forwarding support port ranges'
DESCRIPTION = 'Add support to port ranges'
UPDATED_TIMESTAMP = '2020-07-01T10:00:00-00:00'
EXTERNAL_PORT_RANGE = 'external_port_range'
INTERNAL_PORT_RANGE = 'internal_port_range'
RESOURCE_ATTRIBUTE_MAP = {}
SUB_RESOURCE_ATTRIBUTE_MAP = {
    pfw.COLLECTION_NAME: {
        'parameters': {
            EXTERNAL_PORT_RANGE: {
                'allow_post': True, 'allow_put': True,
                'validate': {'type:port_range': [1, 65535]},
                'is_visible': True,
                'is_sort_key': True,
                'is_filter': True,
                'default': None},
            INTERNAL_PORT_RANGE: {
                'allow_post': True, 'allow_put': True,
                'validate': {'type:port_range': [1, 65535]},
                'is_visible': True,
                'default': None},
            pfw.EXTERNAL_PORT: {
                'allow_post': True, 'allow_put': True,
                'validate': {'type:range_or_none': [1, 65535]},
                'is_visible': True,
                'is_sort_key': True,
                'is_filter': True,
                'default': None},
            pfw.INTERNAL_PORT: {
                'allow_post': True, 'allow_put': True,
                'validate': {'type:range_or_none': [1, 65535]},
                'is_visible': True,
                'default': None},
        }
    }
}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = [pfw.ALIAS]
OPTIONAL_EXTENSIONS = [pfw_desc.ALIAS]
ACTION_STATUS = {}
