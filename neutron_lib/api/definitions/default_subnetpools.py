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
from neutron_lib.api.definitions import subnet as subnet_def
from neutron_lib import constants

USE_DEFAULT_SUBNETPOOL = 'use_default_subnetpool'

ALIAS = 'default-subnetpools'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Default Subnetpools'
API_PREFIX = ''
DESCRIPTION = 'Provides ability to mark and use a subnetpool as the default.'
UPDATED_TIMESTAMP = '2016-02-18T18:00:00-00:00'
RESOURCE_NAME = subnet_def.RESOURCE_NAME
COLLECTION_NAME = subnet_def.COLLECTION_NAME
RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        USE_DEFAULT_SUBNETPOOL: {'allow_post': True,
                                 'allow_put': False,
                                 'default': False,
                                 'convert_to': converters.convert_to_boolean,
                                 'is_visible': False},
    },
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = [constants.SUBNET_ALLOCATION_EXT_ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
