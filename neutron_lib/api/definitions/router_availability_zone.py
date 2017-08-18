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

from neutron_lib.api.definitions import availability_zone as az
from neutron_lib.api.definitions import l3


ALIAS = 'router_availability_zone'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Router Availability Zone'
API_PREFIX = ''
DESCRIPTION = 'Availability zone support for router.'
UPDATED_TIMESTAMP = '2015-01-01T10:00:00-00:00'
RESOURCE_NAME = l3.ROUTER
COLLECTION_NAME = l3.ROUTERS
RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        az.COLLECTION_NAME: {
            'allow_post': False, 'allow_put': False,
            'is_visible': True
        },
        az.AZ_HINTS: {
            'allow_post': True, 'allow_put': False, 'is_visible': True,
            'validate': {'type:availability_zone_hint_list': None},
            'default': []
        }
    }
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = [l3.ALIAS, az.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
