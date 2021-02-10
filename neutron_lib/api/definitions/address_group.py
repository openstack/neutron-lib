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


ALIAS = 'address-group'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Address group'
DESCRIPTION = 'Support address group'
UPDATED_TIMESTAMP = '2020-07-15T10:00:00-00:00'

RESOURCE_NAME = 'address_group'
COLLECTION_NAME = 'address_groups'

RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        'id': {'allow_post': False, 'allow_put': False,
               'validate': {'type:uuid': None},
               'is_visible': True,
               'is_filter': True,
               'is_sort_key': True,
               'primary_key': True},
        'name': {'allow_post': True, 'allow_put': True, 'default': '',
                 'validate': {
                     'type:string': db_const.NAME_FIELD_SIZE},
                 'is_filter': True,
                 'is_sort_key': True,
                 'is_visible': True},
        'description': {'allow_post': True, 'allow_put': True, 'default': '',
                        'validate': {
                            'type:string':
                                db_const.LONG_DESCRIPTION_FIELD_SIZE},
                        'is_filter': True,
                        'is_sort_key': True,
                        'is_visible': True},
        'project_id': {'allow_post': True,
                       'allow_put': False,
                       'validate': {
                           'type:string': db_const.PROJECT_ID_FIELD_SIZE},
                       'required_by_policy': True,
                       'is_filter': True,
                       'is_sort_key': True,
                       'is_visible': True},
        'addresses': {'allow_post': True, 'allow_put': False,
                      'convert_to':
                          converters.convert_none_to_empty_list,
                      'default': constants.ATTR_NOT_SPECIFIED,
                      'validate': {'type:subnet_list': None},
                      'is_visible': True},
        constants.SHARED: {'allow_post': False,
                           'allow_put': False,
                           'default': False,
                           'convert_to': converters.convert_to_boolean,
                           'is_visible': False,
                           'is_filter': False,
                           'is_sort_key': False},
    }
}

SUB_RESOURCE_ATTRIBUTE_MAP = None

ACTION_MAP = {
    RESOURCE_NAME: {
        'add_addresses': 'PUT',
        'remove_addresses': 'PUT'
    },
}

ACTION_STATUS = {
}

REQUIRED_EXTENSIONS = [
    'security-group'
]

OPTIONAL_EXTENSIONS = [
]
