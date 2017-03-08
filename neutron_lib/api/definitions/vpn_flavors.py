# Copyright 2017 Eayun, Inc.
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
#

from neutron_lib.api.definitions import flavors
from neutron_lib.api.definitions import vpn

FLAVOR_ID = 'flavor_id'

ALIAS = 'vpn-flavors'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'VPN Service Falvor Extension'
DESCRIPTION = 'Flavor support for vpnservices.'
UPDATED_TIMESTAMP = '2017-04-19T00:00:00-00:00'
API_PREFIX = '/vpn'
RESOURCE_NAME = vpn.VPNSERVICE
COLLECTION_NAME = vpn.VPNSERVICES
RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        FLAVOR_ID: {'allow_post': True, 'allow_put': False,
                    'validate': {'type:uuid_or_none': None},
                    'is_visible': True, 'default': None}
    },
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = [vpn.ALIAS]
OPTIONAL_EXTENSIONS = [flavors.ALIAS]
ACTION_STATUS = {}
