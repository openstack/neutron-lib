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
from neutron_lib.api.definitions import bgpvpn
from neutron_lib.api.definitions import evpn
from neutron_lib.api.definitions import network
from neutron_lib import constants
from neutron_lib.types import (
    ActionMap,
    ResourceAttributeMap,
    SubResourceAttributeMap,
)


ALIAS = 'evpn-l2'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'L2 EVPN'
API_PREFIX = ''
DESCRIPTION = 'Network extension to support EVPN Type-2 route advertisement'
UPDATED_TIMESTAMP = '2026-10-29T00:00:00-00:00'
RESOURCE_NAME = network.RESOURCE_NAME
COLLECTION_NAME = network.COLLECTION_NAME

EVPN_VNI = evpn.EVPN_VNI
EVPN_RT = 'evpn_rt'

RESOURCE_ATTRIBUTE_MAP: ResourceAttributeMap = {
    COLLECTION_NAME: {
        EVPN_VNI: {
            'allow_post': True,
            'allow_put': True,
            'convert_to': converters.convert_to_int_if_not_none,
            'default': constants.ATTR_NOT_SPECIFIED,
            'is_visible': True,
            'is_filter': False,
            'is_sort_key': False,
            'enforce_policy': True,
            # Zero requests automatic allocation; None removes the VNI.
            'validate': {'type:range_or_none': (0, constants.MAX_VXLAN_VNI)},
        },
        EVPN_RT: {
            'allow_post': False,
            'allow_put': True,
            'default': constants.ATTR_NOT_SPECIFIED,
            'is_visible': True,
            'is_filter': False,
            'is_sort_key': False,
            'enforce_policy': True,
            'validate': {'type:regex_or_none': bgpvpn.RTRD_REGEX},
        },
    },
}

SUB_RESOURCE_ATTRIBUTE_MAP: SubResourceAttributeMap = {}
ACTION_MAP: ActionMap = {}
REQUIRED_EXTENSIONS = []
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
