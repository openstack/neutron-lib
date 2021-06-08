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
from neutron_lib.db import constants as db_const

# Regular expression to validate 32 bits unsigned int
UINT32_REGEX = (r'(0|[1-9]\d{0,8}|[1-3]\d{9}|4[01]\d{8}|42[0-8]\d{7}'
                r'|429[0-3]\d{6}|4294[0-8]\d{5}|42949[0-5]\d{4}'
                r'|429496[0-6]\d{3}|4294967[0-1]\d{2}|42949672[0-8]\d'
                r'|429496729[0-5])')
# Regular expression  to validate 16 bits unsigned int
UINT16_REGEX = (r'(0|[1-9]\d{0,3}|[1-5]\d{4}|6[0-4]\d{3}|65[0-4]\d{2}'
                r'|655[0-2]\d|6553[0-5])')
# Regular expression to validate 8 bits unsigned int
UINT8_REGEX = (r'(0|[1-9]\d{0,1}|1\d{2}|2[0-4]\d|25[0-5])')
# Regular expression to validate IPv4 address
IP4_REGEX = (r'(%s\.%s\.%s\.%s)') % (UINT8_REGEX, UINT8_REGEX, UINT8_REGEX,
                                     UINT8_REGEX)
# Regular expression to validate Route Target list format
# Support of the Type 0, Type 1 and Type 2, cf. chapter 4.2 in RFC 4364
# Also validates Route Distinguisher list format
RTRD_REGEX = (r'^(%s:%s|%s:%s|%s:%s)$') % (UINT16_REGEX, UINT32_REGEX,
                                           IP4_REGEX, UINT16_REGEX,
                                           UINT32_REGEX, UINT16_REGEX)

# The alias of the extension.
ALIAS = 'bgpvpn'

# Whether or not this extension is simply signaling behavior to the user
# or it actively modifies the attribute map.
IS_SHIM_EXTENSION = False

# Whether the extension is marking the adoption of standardattr model for
# legacy resources, or introducing new standardattr attributes. False or
# None if the standardattr model is adopted since the introduction of
# resource extension.
# If this is True, the alias for the extension should be prefixed with
# 'standard-attr-'.
IS_STANDARD_ATTR_EXTENSION = False

# The name of the extension.
NAME = 'BGPVPN Extension'

# The description of the extension.
DESCRIPTION = "Provides support for BGP VPN interconnections"

# A timestamp of when the extension was introduced.
UPDATED_TIMESTAMP = "2014-06-10T17:00:00-00:00"

API_PREFIX = '/bgpvpn'


# The specific resources and/or attributes for the extension (optional).
RESOURCE_NAME = 'bgpvpn'
COLLECTION_NAME = 'bgpvpns'
BGPVPN_L2 = 'l2'
BGPVPN_L3 = 'l3'
BGPVPN_RES = "bgpvpns"
BGPVPN_TYPES = [BGPVPN_L3, BGPVPN_L2]
NETWORK_ASSOCIATION = 'network_association'
NETWORK_ASSOCIATIONS = 'network_associations'
ROUTER_ASSOCIATION = 'router_association'
ROUTER_ASSOCIATIONS = 'router_associations'

# The resource attribute map for the extension.
RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        'id': {'allow_post': False, 'allow_put': False,
               'validate': {'type:uuid': None},
               'is_visible': True,
               'primary_key': True,
               'enforce_policy': True},
        'tenant_id': {'allow_post': True, 'allow_put': False,
                      'validate': {
                          'type:string': db_const.PROJECT_ID_FIELD_SIZE},
                      'required_by_policy': True,
                      'is_visible': True,
                      'enforce_policy': True},
        'name': {'allow_post': True, 'allow_put': True,
                 'default': '',
                 'validate': {'type:string': db_const.NAME_FIELD_SIZE},
                 'is_visible': True,
                 'enforce_policy': True},
        'type': {'allow_post': True, 'allow_put': False,
                 'default': BGPVPN_L3,
                 'validate': {'type:values': BGPVPN_TYPES},
                 'is_visible': True,
                 'enforce_policy': True},
        'route_targets': {'allow_post': True, 'allow_put': True,
                          'default': [],
                          'convert_to': converters.convert_to_list,
                          'validate': {'type:list_of_regex_or_none':
                                       RTRD_REGEX},
                          'is_visible': True,
                          'enforce_policy': True},
        'import_targets': {'allow_post': True, 'allow_put': True,
                           'default': [],
                           'convert_to': converters.convert_to_list,
                           'validate': {'type:list_of_regex_or_none':
                                        RTRD_REGEX},
                           'is_visible': True,
                           'enforce_policy': True},
        'export_targets': {'allow_post': True, 'allow_put': True,
                           'default': [],
                           'convert_to': converters.convert_to_list,
                           'validate': {'type:list_of_regex_or_none':
                                        RTRD_REGEX},
                           'is_visible': True,
                           'enforce_policy': True},
        'route_distinguishers': {'allow_post': True, 'allow_put': True,
                                 'default': [],
                                 'convert_to': converters.convert_to_list,
                                 'validate': {'type:list_of_regex_or_none':
                                              RTRD_REGEX},
                                 'is_visible': True,
                                 'enforce_policy': True},
        'networks': {'allow_post': False, 'allow_put': False,
                     'is_visible': True,
                     'enforce_policy': True},
        'routers': {'allow_post': False, 'allow_put': False,
                    'is_visible': True,
                    'enforce_policy': True},
    },
}

SUB_RESOURCE_ATTRIBUTE_MAP = {
    NETWORK_ASSOCIATIONS: {
        'parent': {'collection_name': COLLECTION_NAME,
                   'member_name': RESOURCE_NAME},
        'parameters': {
            'id': {'allow_post': False, 'allow_put': False,
                   'validate': {'type:uuid': None},
                   'is_visible': True,
                   'primary_key': True},
            'tenant_id': {'allow_post': True, 'allow_put': False,
                          'validate': {
                              'type:string': db_const.PROJECT_ID_FIELD_SIZE},
                          'required_by_policy': True,
                          'is_visible': True,
                          'enforce_policy': True},
            'network_id': {'allow_post': True, 'allow_put': False,
                           'validate': {'type:uuid': None},
                           'is_visible': True,
                           'enforce_policy': True}
        }
    },
    ROUTER_ASSOCIATIONS: {
        'parent': {'collection_name': COLLECTION_NAME,
                   'member_name': RESOURCE_NAME},
        'parameters': {
            'id': {'allow_post': False, 'allow_put': False,
                   'validate': {'type:uuid': None},
                   'is_visible': True,
                   'primary_key': True},
            'tenant_id': {'allow_post': True, 'allow_put': False,
                          'validate': {
                              'type:string': db_const.PROJECT_ID_FIELD_SIZE},
                          'required_by_policy': True,
                          'is_visible': True,
                          'enforce_policy': True},
            'router_id': {'allow_post': True, 'allow_put': False,
                          'validate': {'type:uuid': None},
                          'is_visible': True,
                          'enforce_policy': True}
        }
    }
}

ACTION_MAP = {
}

# The action status.
ACTION_STATUS = {
}

# The list of required extensions.
REQUIRED_EXTENSIONS = [l3.ALIAS]

# The list of optional extensions.
OPTIONAL_EXTENSIONS = [
]
