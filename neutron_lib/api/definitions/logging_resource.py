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
from neutron_lib.api.definitions import firewall_v2
from neutron_lib.db import constants as db_const


# The alias of the extension.
ALIAS = 'logging-resource'

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
NAME = 'Logging Resource Extension'

# A prefix for API resources. An empty prefix means that the API is going
# to be exposed at the v2/ level as any other core resource.
API_PREFIX = '/logging'

# The description of the extension.
DESCRIPTION = "The logging resource extension."

# A timestamp of when the extension was introduced.
UPDATED_TIMESTAMP = "2016-06-06T10:00:00-00:00"

# The name of the resource.
RESOURCE_NAME = 'logging_resource'

# The plural for the resource.
COLLECTION_NAME = 'logging_resources'

# Attributes
ENABLED = 'enabled'

# Sub resource
FIREWALL_LOGS = 'firewall_logs'


LOGGING_RESOURCE_ID = 'logging_resource_id'
FW_EVENT = 'fw_event'
FIREWALL_ID = 'firewall_id'


FW_EVENT_ACCEPT = 'ACCEPT'
FW_EVENT_DROP = 'DROP'
FW_EVENT_ALL = 'ALL'
FW_EVENTS = [FW_EVENT_ACCEPT, FW_EVENT_DROP, FW_EVENT_ALL]
LOG_COMMON_FIELDS = {
    'id': {'allow_post': False, 'allow_put': False,
           'validate': {'type:uuid': None},
           'is_visible': True, 'primary_key': True},
    'tenant_id': {'allow_post': True, 'allow_put': False,
                  'required_by_policy': True, 'is_visible': True},
    LOGGING_RESOURCE_ID: {'allow_post': False, 'allow_put': False,
                          'is_visible': True}
}

RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        'id': {'allow_post': False, 'allow_put': False,
               'validate': {'type:uuid': None}, 'is_visible': True,
               'primary_key': True},
        'tenant_id': {'allow_post': True, 'allow_put': False,
                      'required_by_policy': True, 'is_visible': True},
        'name': {'allow_post': True, 'allow_put': True,
                 'validate': {'type:string': db_const.NAME_FIELD_SIZE},
                 'default': '', 'is_visible': True},
        'description': {
            'allow_post': True, 'allow_put': True,
            'validate': {'type:string': db_const.LONG_DESCRIPTION_FIELD_SIZE},
            'default': '', 'is_visible': True},
        ENABLED: {'allow_post': True, 'allow_put': True,
                  'is_visible': True, 'default': False,
                  'convert_to': converters.convert_to_boolean},
        FIREWALL_LOGS: {'allow_post': False, 'allow_put': False,
                        'is_visible': True}
    }
}


SUB_RESOURCE_ATTRIBUTE_MAP = {
    FIREWALL_LOGS: {
        'parent': {'collection_name': COLLECTION_NAME,
                   'member_name': RESOURCE_NAME},
        'parameters': dict((LOG_COMMON_FIELDS), **{
            'description': {
                'allow_post': True, 'allow_put': True,
                'validate': {
                    'type:string': db_const.LONG_DESCRIPTION_FIELD_SIZE},
                'default': '', 'is_visible': True},
            FIREWALL_ID: {
                'allow_post': True, 'allow_put': False,
                'is_visible': True,
                'validate': {'type:uuid': None}},
            FW_EVENT: {
                'allow_post': True, 'allow_put': True,
                'is_visible': True,
                'validate': {'type:values': FW_EVENTS},
                'default': FW_EVENT_ALL}
        }),
    },
}

# The action map.
ACTION_MAP = {}

# The action status.
ACTION_STATUS = {
}

# The list of required extensions.
REQUIRED_EXTENSIONS = [
    firewall_v2.ALIAS,
]

# The list of optional extensions.
OPTIONAL_EXTENSIONS = []
