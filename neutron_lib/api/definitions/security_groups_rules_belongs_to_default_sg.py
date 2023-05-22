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


ALIAS = 'security-groups-rules-belongs-to-default-sg'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = "Security group rule belongs to the project's default security group"
DESCRIPTION = ("Flag to determine if the security group rule belongs to the "
               "project's default security group")
UPDATED_TIMESTAMP = '2023-05-23T10:00:00-00:00'
BELONGS_TO_DEFAULT_SG = 'belongs_to_default_sg'

RESOURCE_ATTRIBUTE_MAP = {
    'security_group_rules': {
        BELONGS_TO_DEFAULT_SG: {
            'allow_post': False,
            'allow_put': False,
            'convert_to': converters.convert_to_boolean_if_not_none,
            'is_visible': True,
            'is_filter': True,
            'is_sort_key': False,
        },
    }
}

SUB_RESOURCE_ATTRIBUTE_MAP = {
}

ACTION_MAP = {
}

ACTION_STATUS = {
}

REQUIRED_EXTENSIONS = [
    'security-group'
]

OPTIONAL_EXTENSIONS = [
]
