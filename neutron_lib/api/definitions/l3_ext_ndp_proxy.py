# Copyright (c) 2020 Troila.
# All rights reserved.
#
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
from neutron_lib.api.definitions import l3
from neutron_lib.api.definitions import l3_ext_gw_mode
from neutron_lib import constants


ALIAS = 'l3-ext-ndp-proxy'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Router support to enable NDP proxy'
API_PREFIX = ''
DESCRIPTION = 'Router extension to enable ndp proxy'
UPDATED_TIMESTAMP = '2020-08-25T00:00:00-00:00'
RESOURCE_NAME = l3.ROUTER
COLLECTION_NAME = l3.ROUTERS
ENABLE_NDP_PROXY = 'enable_ndp_proxy'
RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        ENABLE_NDP_PROXY: {
            'allow_post': True,
            'allow_put': True,
            'convert_to': converters.convert_to_boolean_if_not_none,
            'default': constants.ATTR_NOT_SPECIFIED,
            'is_visible': True,
            'is_filter': True
        }
    }
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = [l3.ALIAS, l3_ext_gw_mode.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
