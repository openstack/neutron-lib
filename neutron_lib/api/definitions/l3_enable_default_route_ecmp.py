# Copyright 2023 Canonical Ltd.
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

from neutron_lib.api import converters
from neutron_lib.api.definitions import l3
from neutron_lib.api.definitions import l3_ext_gw_multihoming
from neutron_lib import constants

ENABLE_DEFAULT_ROUTE_ECMP = 'enable_default_route_ecmp'

ALIAS = constants.L3_ENABLE_DEFAULT_ROUTE_ECMP_ALIAS
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Enable Default Route ECMP'
API_PREFIX = ''
DESCRIPTION = 'Enables configurable ECMP behavior for default routes'
UPDATED_TIMESTAMP = '2023-02-27T00:00:00-00:00'
RESOURCE_NAME = l3.ROUTER
COLLECTION_NAME = l3.ROUTERS
RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        ENABLE_DEFAULT_ROUTE_ECMP: {
            'allow_post': True,
            'allow_put': True,
            'default': None,
            'is_visible': True,
            'enforce_policy': True,
            'convert_to': converters.convert_to_boolean_if_not_none,
        }
    }
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = [l3.ALIAS, l3_ext_gw_multihoming.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
