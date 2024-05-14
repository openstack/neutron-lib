# All rights reserved.
#
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
from neutron_lib.db import constants as db_const

FLAVOR = 'flavor'
FLAVORS = FLAVOR + 's'
SERVICE_PROFILES = 'service_profiles'
NEXT_PROVIDERS = 'next_providers'

ALIAS = FLAVORS
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Neutron Service Flavors'
API_PREFIX = ''
DESCRIPTION = 'Flavor specification for Neutron advanced services.'
UPDATED_TIMESTAMP = '2015-09-17T10:00:00-00:00'
RESOURCE_ATTRIBUTE_MAP = {
    FLAVORS: {
        'id': {'allow_post': False, 'allow_put': False,
               'validate': {'type:uuid': None},
               'is_visible': True, 'is_filter': True,
               'is_sort_key': True, 'primary_key': True},
        'name': {'allow_post': True, 'allow_put': True,
                 'validate': {'type:string': db_const.NAME_FIELD_SIZE},
                 'is_filter': True, 'is_sort_key': True,
                 'is_visible': True, 'default': ''},
        'description': {'allow_post': True, 'allow_put': True,
                        'validate': {'type:string_or_none':
                                     db_const.LONG_DESCRIPTION_FIELD_SIZE},
                        'is_filter': True, 'is_sort_key': True,
                        'is_visible': True, 'default': ''},
        'service_type': {'allow_post': True, 'allow_put': False,
                         'validate':
                             {'type:service_plugin_type': None},
                         'is_filter': True, 'is_sort_key': True,
                         'is_visible': True},
        'service_profiles': {'allow_post': True, 'allow_put': True,
                             'validate': {'type:uuid_list': None},
                             'is_visible': True, 'default': []},
        'enabled': {'allow_post': True, 'allow_put': True,
                    'convert_to': converters.convert_to_boolean_if_not_none,
                    'default': True, 'is_filter': True, 'is_sort_key': True,
                    'is_visible': True},
    },
    SERVICE_PROFILES: {
        'id': {'allow_post': False, 'allow_put': False,
               'validate': {'type:uuid': None},
               'is_visible': True, 'is_filter': True,
               'is_sort_key': True, 'primary_key': True},
        'description': {'allow_post': True, 'allow_put': True,
                        'validate': {'type:string_or_none':
                                     db_const.LONG_DESCRIPTION_FIELD_SIZE},
                        'is_filter': True, 'is_sort_key': True,
                        'is_visible': True, 'default': ''},
        'driver': {'allow_post': True, 'allow_put': True,
                   'validate': {'type:string':
                                db_const.LONG_DESCRIPTION_FIELD_SIZE},
                   'is_visible': True, 'is_filter': True,
                   'is_sort_key': True, 'default': ''},
        'metainfo': {'allow_post': True, 'allow_put': True,
                     'is_visible': True, 'is_sort_key': True,
                     'default': ''},
        'enabled': {'allow_post': True, 'allow_put': True,
                    'convert_to': converters.convert_to_boolean_if_not_none,
                    'is_filter': True, 'is_sort_key': True,
                    'is_visible': True, 'default': True},
    },
}
SUB_RESOURCE_ATTRIBUTE_MAP = {
    NEXT_PROVIDERS: {
        'parent': {'collection_name': FLAVORS,
                   'member_name': FLAVOR},
        'parameters': {'provider': {'allow_post': False,
                                    'allow_put': False,
                                    'is_visible': True},
                       'driver': {'allow_post': False,
                                  'allow_put': False,
                                  'is_visible': True},
                       'metainfo': {'allow_post': False,
                                    'allow_put': False,
                                    'is_visible': True}}
    },
    SERVICE_PROFILES: {
        'parent': {'collection_name': FLAVORS,
                   'member_name': FLAVOR},
        'parameters': {'id': {'allow_post': True, 'allow_put': False,
                              'validate': {'type:uuid': None},
                              'is_visible': True}}
    }
}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = []
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
