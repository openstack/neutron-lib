#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

from neutron_lib.api import converters
from neutron_lib.api.definitions import stateful_security_group
from neutron_lib.db import constants as db_const

ALIAS = 'security-groups-default-statefulness'

IS_SHIM_EXTENSION = False

IS_STANDARD_ATTR_EXTENSION = False

NAME = 'Security Groups Default Statefulness'

DESCRIPTION = (
    "Allows configuring the default value of the 'stateful' attribute "
    "for new security groups, on a per-project or system-wide basis")

UPDATED_TIMESTAMP = '2026-04-13T00:00:00-00:00'

RESOURCE_NAME = 'security_groups_default_statefulness'
COLLECTION_NAME = 'security_groups_default_statefulness'

ID = 'id'
PROJECT_ID = 'project_id'
STATEFUL = 'stateful'

RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        ID: {'allow_post': False,
             'allow_put': False,
             'validate': {'type:uuid': None},
             'is_visible': True,
             'primary_key': True,
             'is_sort_key': True,
             'is_filter': True},
        PROJECT_ID: {
            'allow_post': True,
            'allow_put': False,
            'validate': {
                'type:string_or_none':
                    db_const.PROJECT_ID_FIELD_SIZE},
            'is_visible': True,
            'required_by_policy': True,
            'default': None,
            'is_sort_key': True,
            'is_filter': True},
        STATEFUL: {
            'allow_post': True,
            'allow_put': True,
            'convert_to': converters.convert_to_boolean,
            'default': True,
            'is_visible': True,
            'is_filter': True,
            'is_sort_key': True},
    }
}

SUB_RESOURCE_ATTRIBUTE_MAP = {
}

ACTION_MAP = {
}

ACTION_STATUS = {
}

REQUIRED_EXTENSIONS = [
    'security-group',
    stateful_security_group.ALIAS,
]

OPTIONAL_EXTENSIONS = [
]
