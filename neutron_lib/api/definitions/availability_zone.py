# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from neutron_lib.api.definitions import agent
from neutron_lib.api import validators
from neutron_lib.api.validators import availability_zone as az_validator


validators.add_validator('availability_zone_hint_list',
                         az_validator._validate_availability_zone_hints)

AZ_HINTS = 'availability_zone_hints'

ALIAS = 'availability_zone'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Availability Zone'
API_PREFIX = ''
DESCRIPTION = 'The availability zone extension.'
UPDATED_TIMESTAMP = '2015-01-01T10:00:00-00:00'
RESOURCE_NAME = 'availability_zone'
COLLECTION_NAME = RESOURCE_NAME + 's'
RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        'name': {'is_visible': True, 'is_filter': True},
        'resource': {'is_visible': True, 'is_filter': True},
        'state': {'is_visible': True, 'is_filter': True}
    },
    agent.COLLECTION_NAME: {
        RESOURCE_NAME: {
            'allow_post': False, 'allow_put': False, 'is_filter': True,
            'is_visible': True}
    }
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = [agent.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
