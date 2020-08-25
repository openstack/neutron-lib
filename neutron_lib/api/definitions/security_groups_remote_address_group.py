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


REMOTE_ADDRESS_GROUP_ID = 'remote_address_group_id'

ALIAS = 'security-groups-remote-address-group'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Remote address group id field for security group rules'
DESCRIPTION = 'Add new field of remote address group id in SG rules'
UPDATED_TIMESTAMP = '2020-08-25T10:00:00-00:00'

RESOURCE_ATTRIBUTE_MAP = {
    'security_group_rules': {
        REMOTE_ADDRESS_GROUP_ID: {
            'allow_post': True, 'allow_put': False,
            'default': None, 'is_visible': True,
            'is_sort_key': True, 'is_filter': True},
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
