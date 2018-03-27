#    (c) Copyright 2015 NEC Corporation, All Rights Reserved.
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
from neutron_lib.api.definitions import vpn
from neutron_lib.db import constants as db_const

# VPN Endpoint type constants
VPN_ENDPOINT_TYPE_CIDR = 'cidr'
VPN_ENDPOINT_TYPE_NETWORK = 'network'
VPN_ENDPOINT_TYPE_ROUTER = 'router'
VPN_ENDPOINT_TYPE_SUBNET = 'subnet'
VPN_ENDPOINT_TYPE_VLAN = 'vlan'

VPN_SUPPORTED_ENDPOINT_TYPES = [
    VPN_ENDPOINT_TYPE_CIDR, VPN_ENDPOINT_TYPE_NETWORK,
    VPN_ENDPOINT_TYPE_ROUTER, VPN_ENDPOINT_TYPE_SUBNET, VPN_ENDPOINT_TYPE_VLAN,
]

ALIAS = 'vpn-endpoint-groups'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'VPN Endpoint Groups'
DESCRIPTION = 'VPN endpoint groups support'
UPDATED_TIMESTAMP = '2015-08-04T10:00:00-00:00'
API_PREFIX = '/vpn'
RESOURCE_ATTRIBUTE_MAP = {
    'endpoint_groups': {
        'id': {'allow_post': False, 'allow_put': False,
               'validate': {'type:uuid': None},
               'is_visible': True,
               'primary_key': True},
        'tenant_id': {'allow_post': True, 'allow_put': False,
                      'validate': {
                          'type:string': db_const.PROJECT_ID_FIELD_SIZE},
                      'required_by_policy': True,
                      'is_visible': True},
        'name': {'allow_post': True, 'allow_put': True,
                 'validate': {'type:string': db_const.NAME_FIELD_SIZE},
                 'is_visible': True, 'default': ''},
        'description': {'allow_post': True, 'allow_put': True,
                        'validate': {
                            'type:string': db_const.DESCRIPTION_FIELD_SIZE},
                        'is_visible': True, 'default': ''},
        'type': {'allow_post': True, 'allow_put': False,
                 'validate': {'type:values': VPN_SUPPORTED_ENDPOINT_TYPES},
                 'is_visible': True},
        'endpoints': {'allow_post': True, 'allow_put': False,
                      'convert_to': converters.convert_to_list,
                      'is_visible': True,
                      'default': []},
    },
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = [vpn.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
