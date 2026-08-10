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

from neutron_lib.db import constants as db_const
from neutron_lib.types import (
    ActionMap,
    ResourceAttributeMap,
    SubResourceAttributeMap,
)

ALIAS = 'security-groups-name-restrictions'

IS_SHIM_EXTENSION = False

IS_STANDARD_ATTR_EXTENSION = False

NAME = 'Security group name restrictions'
DESCRIPTION = (
    'Enforce printable characters and no leading/trailing whitespace '
    'in security group names, consistent with other Neutron resources'
)

UPDATED_TIMESTAMP = '2026-07-29T10:00:00-00:00'

COLLECTION_NAME = 'security_groups'

RESOURCE_ATTRIBUTE_MAP: ResourceAttributeMap = {
    COLLECTION_NAME: {
        'name': {
            'allow_post': True,
            'allow_put': True,
            'is_visible': True,
            'default': '',
            'is_filter': True,
            'is_sort_key': True,
            'validate': {
                'type:name_string_not_default': db_const.NAME_FIELD_SIZE},
        },
    },
}

SUB_RESOURCE_ATTRIBUTE_MAP: SubResourceAttributeMap = {}

ACTION_MAP: ActionMap = {}

ACTION_STATUS = {}

REQUIRED_EXTENSIONS = [
    'security-group',
]

OPTIONAL_EXTENSIONS = []
