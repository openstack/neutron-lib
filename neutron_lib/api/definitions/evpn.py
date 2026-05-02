# Copyright 2026 Red Hat, LLC
# All Rights Reserved.
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
from neutron_lib import constants


ALIAS = 'evpn'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'EVPN'
API_PREFIX = ''
DESCRIPTION = 'Router extension to support EVPN Type-5 route advertisement'
UPDATED_TIMESTAMP = '2026-04-28T00:00:00-00:00'
RESOURCE_NAME = l3.ROUTER
COLLECTION_NAME = l3.ROUTERS

EVPN_VNI = 'evpn_vni'
ADVERTISE_HOST = 'advertise_host'

RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        EVPN_VNI: {
            'allow_post': True,
            'allow_put': False,
            'convert_to': converters.convert_to_int_if_not_none,
            'default': None,
            'is_visible': True,
            'is_filter': True,
            'is_sort_key': True,
            'enforce_policy': True,
            'validate': {'type:range_or_none':
                         [0, constants.MAX_VXLAN_VNI]},
        },
    },
}

SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = [l3.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
