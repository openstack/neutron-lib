# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from neutron_lib.api.definitions import l3
from neutron_lib import constants


FLAVOR_ID = 'flavor_id'

ALIAS = 'l3-flavors'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Router Flavor Extension'
API_PREFIX = ''
DESCRIPTION = 'Flavor support for routers.'
UPDATED_TIMESTAMP = '2016-05-17T00:00:00-00:00'
RESOURCE_NAME = l3.ROUTER
COLLECTION_NAME = l3.ROUTERS
RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        FLAVOR_ID: {
            'allow_post': True, 'allow_put': False,
            'default': constants.ATTR_NOT_SPECIFIED,
            'is_sort_key': True,
            'is_visible': True, 'enforce_policy': True
        }
    }
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = ['flavors', l3.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
