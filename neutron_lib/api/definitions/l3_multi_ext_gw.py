# Copyright 2021 Ericsson Software Technology
#
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
from neutron_lib.api.definitions import l3_ext_gw_mode


ALIAS = 'multiple-external-gateways'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Neutron L3 Multiple External Gateways'
API_PREFIX = ''
DESCRIPTION = 'Allow more than one External Gateways'
UPDATED_TIMESTAMP = '2021-04-01T00:00:00-00:00'
RESOURCE_NAME = l3.ROUTER
COLLECTION_NAME = l3.ROUTERS
RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        'external_gateways': {
            'allow_post': False,
            'allow_put': False,
            'is_visible': True,
            'default': None,
            'validate': {'type:external_gw_info_list': None},
        },
    },
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = l3.ACTION_MAP
ACTION_MAP[l3.ROUTER].update({
    'add_external_gateways': 'PUT',
    'update_external_gateways': 'PUT',
    'remove_external_gateways': 'PUT',
})
REQUIRED_EXTENSIONS = [l3.ALIAS, l3_ext_gw_mode.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
