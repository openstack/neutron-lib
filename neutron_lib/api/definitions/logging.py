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

# The alias of the extension.
ALIAS = 'logging'

# Whether or not this extension is simply signaling behavior to the user
# or it actively modifies the attribute map.
IS_SHIM_EXTENSION = False

# Whether the extension is marking the adoption of standardattr model for
# legacy resources, or introducing new standardattr attributes. False or
# None if the standardattr model is adopted since the introduction of
# resource extension.
# If this is True, the alias for the extension should be prefixed with
# 'standard-attr-'.
IS_STANDARD_ATTR_EXTENSION = False

# The name of the extension.
NAME = 'Logging API Extension'

# A prefix for API resources. An empty prefix means that the API is going
# to be exposed at the v2/ level as any other core resource.
API_PREFIX = '/log'

# The description of the extension.
DESCRIPTION = ("Provides a logging API for resources such as "
               "security group and firewall.")

# A timestamp of when the extension was introduced.
UPDATED_TIMESTAMP = "2017-01-01T10:00:00-00:00"

LOGS = 'logs'
LOG_TYPES = 'loggable_resources'

ACCEPT_EVENT = 'ACCEPT'
DROP_EVENT = 'DROP'
ALL_EVENT = 'ALL'
LOG_EVENTS = [ACCEPT_EVENT, DROP_EVENT, ALL_EVENT]

# Attribute Map
RESOURCE_ATTRIBUTE_MAP = {
    LOGS: {
        'id': {'allow_post': False, 'allow_put': False,
               'validate': {'type:uuid': None},
               'is_visible': True,
               'is_filter': True, 'is_sort_key': True,
               'primary_key': True},
        'project_id': {'allow_post': True, 'allow_put': False,
                       'required_by_policy': True,
                       'validate': {
                           'type:string':
                               db_const.PROJECT_ID_FIELD_SIZE},
                       'is_filter': True, 'is_sort_key': True,
                       'is_visible': True},
        'name': {'allow_post': True, 'allow_put': True,
                 'validate': {'type:string': db_const.NAME_FIELD_SIZE},
                 'is_filter': True, 'is_sort_key': True,
                 'default': '', 'is_visible': True},
        'resource_type': {'allow_post': True, 'allow_put': False,
                          'required_by_policy': True,
                          'validate': {
                              'type:string':
                                  db_const.RESOURCE_TYPE_FIELD_SIZE},
                          'is_filter': True, 'is_sort_key': True,
                          'is_visible': True},
        'resource_id': {'allow_post': True, 'allow_put': False,
                        'validate': {'type:uuid_or_none': None},
                        'is_filter': True, 'is_sort_key': True,
                        'default': None, 'is_visible': True},
        'event': {'allow_post': True, 'allow_put': False,
                  'validate': {'type:values': LOG_EVENTS},
                  'is_filter': True,
                  'default': ALL_EVENT, 'is_visible': True},
        'target_id': {'allow_post': True, 'allow_put': False,
                      'validate': {'type:uuid_or_none': None},
                      'is_filter': True, 'is_sort_key': True,
                      'default': None, 'is_visible': True},
        'enabled': {'allow_post': True, 'allow_put': True,
                    'is_visible': True, 'default': True,
                    'is_filter': True, 'is_sort_key': True,
                    'convert_to': converters.convert_to_boolean},
    },
    LOG_TYPES: {
        'type': {'allow_post': False, 'allow_put': False,
                 'is_visible': True}},
}

# The subresource attribute map for the extension.  This extension has only
# top level resources, not child resources, so this is set to an empty dict.
SUB_RESOURCE_ATTRIBUTE_MAP = {}

# The action map.
ACTION_MAP = {}

# The list of required extensions.
REQUIRED_EXTENSIONS = []

# The action status.
ACTION_STATUS = {}

# The list of optional extensions.
OPTIONAL_EXTENSIONS = ['security-group', 'fwaas_v2']
