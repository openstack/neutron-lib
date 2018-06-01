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


NAME = 'Neutron L3 Subnet Pool'
ALIAS = 'subnetpool'
DESCRIPTION = "Layer 3 subnet pool abstraction"

UPDATED_TIMESTAMP = "2012-01-01T10:00:00-00:00"

RESOURCE_NAME = 'subnetpool'
COLLECTION_NAME = 'subnetpools'

RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        'id': {'allow_post': False,
               'allow_put': False,
               'validate': {'type:uuid': None},
               'is_visible': True,
               'is_filter': True,
               'is_sort_key': True,
               'primary_key': True},
        'name': {'allow_post': True,
                 'allow_put': True,
                 'validate': {'type:not_empty_string': None},
                 'is_filter': True,
                 'is_sort_key': True,
                 'is_visible': True},
        'tenant_id': {'allow_post': True,
                      'allow_put': False,
                      'validate': {
                          'type:string': db_const.PROJECT_ID_FIELD_SIZE},
                      'required_by_policy': True,
                      'is_filter': True,
                      'is_sort_key': True,
                      'is_visible': True},
        'prefixes': {'allow_post': True,
                     'allow_put': True,
                     'validate': {'type:subnet_list': None},
                     'is_visible': True},
        'default_quota': {'allow_post': True,
                          'allow_put': True,
                          'validate': {'type:non_negative': None},
                          'convert_to': converters.convert_to_int,
                          'default': constants.ATTR_NOT_SPECIFIED,
                          'is_filter': True,
                          'is_sort_key': True,
                          'is_visible': True},
        'ip_version': {'allow_post': False,
                       'allow_put': False,
                       'is_filter': True,
                       'is_sort_key': True,
                       'is_visible': True},
        'default_prefixlen': {'allow_post': True,
                              'allow_put': True,
                              'validate': {'type:non_negative': None},
                              'convert_to': converters.convert_to_int,
                              'default': constants.ATTR_NOT_SPECIFIED,
                              'is_filter': True,
                              'is_sort_key': True,
                              'is_visible': True},
        'min_prefixlen': {'allow_post': True,
                          'allow_put': True,
                          'default': constants.ATTR_NOT_SPECIFIED,
                          'validate': {'type:non_negative': None},
                          'convert_to': converters.convert_to_int,
                          'is_filter': True,
                          'is_sort_key': True,
                          'is_visible': True},
        'max_prefixlen': {'allow_post': True,
                          'allow_put': True,
                          'default': constants.ATTR_NOT_SPECIFIED,
                          'validate': {'type:non_negative': None},
                          'convert_to': converters.convert_to_int,
                          'is_filter': True,
                          'is_sort_key': True,
                          'is_visible': True},
        'is_default': {'allow_post': True,
                       'allow_put': True,
                       'default': False,
                       'convert_to': converters.convert_to_boolean,
                       'is_visible': True,
                       'is_filter': True,
                       'is_sort_key': True,
                       'required_by_policy': True,
                       'enforce_policy': True},
        constants.SHARED: {
            'allow_post': True,
            'allow_put': False,
            'default': False,
            'convert_to': converters.convert_to_boolean,
            'is_visible': True,
            'is_filter': True,
            'is_sort_key': True,
            'required_by_policy': True,
            'enforce_policy': True
        }
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
