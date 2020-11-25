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
from neutron_lib import constants
from neutron_lib.db import constants as db_const


NAME = 'Neutron Port'
ALIAS = 'port'
DESCRIPTION = "Network port abstraction"

UPDATED_TIMESTAMP = "2012-01-01T10:00:00-00:00"

RESOURCE_NAME = 'port'
COLLECTION_NAME = 'ports'
COLLECTION_NAME_BULK = 'ports_bulk'

PORT_MAC_ADDRESS = 'mac_address'

RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        'id': {'allow_post': False, 'allow_put': False,
               'validate': {'type:uuid': None},
               'is_filter': True,
               'is_sort_key': True,
               'is_visible': True,
               'primary_key': True},
        'name': {'allow_post': True, 'allow_put': True, 'default': '',
                 'validate': {
                     'type:string': db_const.NAME_FIELD_SIZE},
                 'is_filter': True,
                 'is_sort_key': True,
                 'is_visible': True},
        'network_id': {'allow_post': True, 'allow_put': False,
                       'required_by_policy': True,
                       'validate': {'type:uuid': None},
                       'is_filter': True,
                       'is_sort_key': True,
                       'is_visible': True},
        'admin_state_up': {'allow_post': True, 'allow_put': True,
                           'default': True,
                           'convert_to': converters.convert_to_boolean,
                           'is_filter': True,
                           'is_sort_key': True,
                           'is_visible': True},
        PORT_MAC_ADDRESS: {'allow_post': True, 'allow_put': True,
                           'default': constants.ATTR_NOT_SPECIFIED,
                           'validate': {'type:mac_address': None},
                           'enforce_policy': True,
                           'is_filter': True,
                           'is_sort_key': True,
                           'is_visible': True},
        'fixed_ips': {'allow_post': True, 'allow_put': True,
                      'default': constants.ATTR_NOT_SPECIFIED,
                      'convert_list_to':
                          converters.convert_kvp_list_to_dict,
                      'validate': {'type:fixed_ips': None},
                      'enforce_policy': True,
                      'is_filter': True,
                      'is_visible': True},
        'device_id': {'allow_post': True, 'allow_put': True,
                      'validate': {
                          'type:string': db_const.DEVICE_ID_FIELD_SIZE},
                      'default': '',
                      'is_filter': True,
                      'is_sort_key': True,
                      'is_visible': True},
        'device_owner': {'allow_post': True, 'allow_put': True,
                         'validate': {
                             'type:string': db_const.DEVICE_OWNER_FIELD_SIZE},
                         'default': '', 'enforce_policy': True,
                         'is_filter': True,
                         'is_sort_key': True,
                         'is_visible': True},
        'tenant_id': {'allow_post': True, 'allow_put': False,
                      'validate': {
                          'type:string': db_const.PROJECT_ID_FIELD_SIZE},
                      'required_by_policy': True,
                      'is_filter': True,
                      'is_sort_key': True,
                      'is_visible': True},
        'status': {'allow_post': False, 'allow_put': False,
                   'is_filter': True,
                   'is_sort_key': True,
                   'is_visible': True},
    }
}

# This is a core resource so the following are not applicable.
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = []
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
