# Copyright (c) 2026 Red Hat Inc.
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
from neutron_lib.api.definitions import network
from neutron_lib.api.definitions import port
from neutron_lib.services.pvlan import constants as pvlan_const


ALIAS = 'pvlan'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Private VLAN'
DESCRIPTION = 'The Private VLAN semantics extension.'
UPDATED_TIMESTAMP = '2026-02-03T10:00:00-00:00'

RESOURCE_ATTRIBUTE_MAP = {
    network.COLLECTION_NAME: {
        pvlan_const.PVLAN: {
            'allow_post': True,
            'allow_put': True,
            'is_visible': True,
            'default': False,
            'validate': {'type:boolean': None},
            'convert_to': converters.convert_to_boolean}
    },
    port.COLLECTION_NAME: {
        pvlan_const.PVLAN_TYPE: {
            'allow_post': True,
            'allow_put': True,
            'is_filter': True,
            'default': None,
            'is_visible': True,
            'validate': {'type:values': (*pvlan_const.PVLAN_TYPES, None)}
        },
        pvlan_const.PVLAN_COMMUNITY: {
            'allow_post': True,
            'allow_put': True,
            'is_visible': True,
            'default': None,
            'validate': {
                'type:regex_or_none': pvlan_const.COMMUNITY_NAME_REGEX}
        }
    }
}


SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}

ACTION_STATUS = {}
REQUIRED_EXTENSIONS = []
OPTIONAL_EXTENSIONS = []
