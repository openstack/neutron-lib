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

from neutron_lib.api.definitions import l3
from neutron_lib.db import constants as db_const


FLOATINGIP_POOLS = 'floatingip_pools'

ALIAS = 'floatingip-pools'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Floating IP Pools Extension'
API_PREFIX = '/floatingip_pools'
DESCRIPTION = 'Provides a floating IP pools API.'
UPDATED_TIMESTAMP = '2018-03-21T10:00:00-00:00'
COLLECTION_NAME = FLOATINGIP_POOLS
RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        'subnet_id': {'allow_post': False, 'allow_put': False,
                      'validate': {'type:uuid': None},
                      'is_visible': True},
        'subnet_name': {'allow_post': False, 'allow_put': False,
                        'validate': {'type:string': db_const.NAME_FIELD_SIZE},
                        'is_visible': True},
        'network_id': {'allow_post': False, 'allow_put': False,
                       'validate': {'type:uuid': None},
                       'is_visible': True},
        'cidr': {'allow_post': False, 'allow_put': False,
                 'validate': {'type:subnet_or_none': None},
                 'is_visible': True},
        'project_id': {'allow_post': False, 'allow_put': False,
                       'validate': {
                           'type:string': db_const.PROJECT_ID_FIELD_SIZE},
                       'is_visible': True},
    },
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = [l3.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
