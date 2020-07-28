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


ALIAS = 'security-groups-normalized-cidr'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Normalized CIDR field for security group rules'
DESCRIPTION = 'Add new field with normalized remote_ip_prefix cidr in SG rule'
UPDATED_TIMESTAMP = '2020-07-28T10:00:00-00:00'

RESOURCE_ATTRIBUTE_MAP = {
    'security_group_rules': {
        'normalized_cidr': {
            'allow_post': False, 'allow_put': False,
            'validate': {'type:subnet_or_none': None},
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
    'security-group'
]

OPTIONAL_EXTENSIONS = [
]
