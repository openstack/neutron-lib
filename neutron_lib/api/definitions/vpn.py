#    (c) Copyright 2013 Hewlett-Packard Development Company, L.P.
#    All Rights Reserved.
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
from neutron_lib.api import validators
from neutron_lib.db import constants as db_const

# Resource constants
VPNSERVICE = 'vpnservice'
VPNSERVICES = 'vpnservices'
IPSEC_SITE_CONNECTION = 'ipsec_site_connection'
IPSEC_SITE_CONNECTIONS = 'ipsec_site_connections'
IPSEC_POLICY = 'ipsecpolicy'
IPSEC_POLICIES = 'ipsecpolicies'
IKE_POLICY = 'ikepolicy'
IKE_POLICIES = 'ikepolicies'

# VPN initiator constants
VPN_INITIATOR_BI_DIRECTIONAL = 'bi-directional'
VPN_INITIATOR_RESPONSE_ONLY = 'response-only'

VPN_SUPPORTED_INITIATORS = [
    VPN_INITIATOR_BI_DIRECTIONAL, VPN_INITIATOR_RESPONSE_ONLY,
]

# VPN encryption algorithm constants
VPN_ENCRYPTION_ALGORITHM_3DES = '3des'
VPN_ENCRYPTION_ALGORITHM_AES_128 = 'aes-128'
VPN_ENCRYPTION_ALGORITHM_AES_192 = 'aes-192'
VPN_ENCRYPTION_ALGORITHM_AES_256 = 'aes-256'

VPN_SUPPORTED_ENCRYPTION_ALGORITHMS = [
    VPN_ENCRYPTION_ALGORITHM_3DES, VPN_ENCRYPTION_ALGORITHM_AES_128,
    VPN_ENCRYPTION_ALGORITHM_AES_192, VPN_ENCRYPTION_ALGORITHM_AES_256,
]

# VPN DPD action constants
VPN_DPD_ACTION_CLEAR = 'clear'
VPN_DPD_ACTION_DISABLED = 'disabled'
VPN_DPD_ACTION_HOLD = 'hold'
VPN_DPD_ACTION_RESTART = 'restart'
VPN_DPD_ACTION_RESTART_BY_PEER = 'restart-by-peer'

VPN_SUPPORTED_DPD_ACTIONS = [
    VPN_DPD_ACTION_CLEAR, VPN_DPD_ACTION_DISABLED, VPN_DPD_ACTION_HOLD,
    VPN_DPD_ACTION_RESTART, VPN_DPD_ACTION_RESTART_BY_PEER,
]

# VPN transform protocol constants
VPN_TRANSFORM_PROTOCOL_AH = 'ah'
VPN_TRANSFORM_PROTOCOL_AH_ESP = 'ah-esp'
VPN_TRANSFORM_PROTOCOL_ESP = 'esp'

VPN_SUPPORTED_TRANSFORM_PROTOCOLS = [
    VPN_TRANSFORM_PROTOCOL_AH, VPN_TRANSFORM_PROTOCOL_AH_ESP,
    VPN_TRANSFORM_PROTOCOL_ESP,
]

# VPN encapsulation mode constants
VPN_ENCAPSULATION_MODE_TRANSPORT = 'transport'
VPN_ENCAPSULATION_MODE_TUNNEL = 'tunnel'

VPN_SUPPORTED_ENCAPSULATION_MODES = [
    VPN_ENCAPSULATION_MODE_TRANSPORT, VPN_ENCAPSULATION_MODE_TUNNEL,
]

# VPN lifetime unit constants
VPN_LIFETIME_UNIT_SECONDS = 'seconds'

VPN_SUPPORTED_LIFETIME_UNITS = [
    VPN_LIFETIME_UNIT_SECONDS,
]

# VPN PFS group constants
VPN_PFS_GROUP2 = 'group2'
VPN_PFS_GROUP5 = 'group5'
VPN_PFS_GROUP14 = 'group14'

VPN_SUPPORTED_PFSES = [
    VPN_PFS_GROUP2, VPN_PFS_GROUP5, VPN_PFS_GROUP14,
]

# VPN IKE version constants
VPN_IKE_VERSION_V1 = 'v1'
VPN_IKE_VERSION_V2 = 'v2'

VPN_SUPPORTED_IKE_VERSIONS = [
    VPN_IKE_VERSION_V1, VPN_IKE_VERSION_V2,
]

# VPN auth mode constants
VPN_AUTH_MODE_PSK = 'psk'

VPN_SUPPORTED_AUTH_MODES = [
    VPN_AUTH_MODE_PSK,
]

# VPN auth algorithm constants
VPN_AUTH_ALGORITHM_SHA1 = 'sha1'
VPN_AUTH_ALGORITHM_SHA256 = 'sha256'
VPN_AUTH_ALGORITHM_SHA384 = 'sha384'
VPN_AUTH_ALGORITHM_SHA512 = 'sha512'

VPN_SUPPORTED_AUTH_ALGORITHMS = [
    VPN_AUTH_ALGORITHM_SHA1, VPN_AUTH_ALGORITHM_SHA256,
    VPN_AUTH_ALGORITHM_SHA384, VPN_AUTH_ALGORITHM_SHA512,
]

# VPN phase1 negotiation mode constants
VPN_PHASE1_NEGOTIATION_MODE_MAIN = 'main'
VPN_PHASE1_NEGOTIATION_MODE_AGGRESSIVE = 'aggressive'

VPN_SUPPORTED_PHASE1_NEGOTIATION_MODES = [
    VPN_PHASE1_NEGOTIATION_MODE_MAIN,
    VPN_PHASE1_NEGOTIATION_MODE_AGGRESSIVE,
]

# The alias of the extension.
ALIAS = 'vpnaas'

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
NAME = 'VPN service'

# The description of the extension.
DESCRIPTION = "Extension for VPN service"

# A timestamp of when the extension was introduced.
UPDATED_TIMESTAMP = "2013-05-29T10:00:00-00:00"

# Base for the API calls
API_PREFIX = '/vpn'

_vpn_lifetime_limits = (60, validators.UNLIMITED)

RESOURCE_ATTRIBUTE_MAP = {

    VPNSERVICES: {
        'id': {'allow_post': False, 'allow_put': False,
               'validate': {'type:uuid': None},
               'is_visible': True,
               'is_sort_key': True,
               'primary_key': True},
        'tenant_id': {'allow_post': True, 'allow_put': False,
                      'validate': {
                          'type:string': db_const.PROJECT_ID_FIELD_SIZE},
                      'required_by_policy': True,
                      'is_sort_key': True,
                      'is_visible': True},
        'name': {'allow_post': True, 'allow_put': True,
                 'validate': {'type:string': db_const.NAME_FIELD_SIZE},
                 'is_visible': True, 'is_sort_key': True, 'default': ''},
        'description': {'allow_post': True, 'allow_put': True,
                        'validate': {
                            'type:string': db_const.DESCRIPTION_FIELD_SIZE},
                        'is_visible': True, 'default': ''},
        'subnet_id': {'allow_post': True, 'allow_put': False,
                      'validate': {'type:uuid_or_none': None},
                      'is_visible': True, 'default': None},
        'router_id': {'allow_post': True, 'allow_put': False,
                      'validate': {'type:uuid': None},
                      'is_sort_key': True,
                      'is_visible': True},
        'admin_state_up': {'allow_post': True, 'allow_put': True,
                           'default': True,
                           'convert_to': converters.convert_to_boolean,
                           'is_visible': True},
        'external_v4_ip': {'allow_post': False, 'allow_put': False,
                           'is_visible': True},
        'external_v6_ip': {'allow_post': False, 'allow_put': False,
                           'is_visible': True},
        'status': {'allow_post': False, 'allow_put': False,
                   'is_visible': True},
    },

    IPSEC_SITE_CONNECTIONS: {
        'id': {'allow_post': False, 'allow_put': False,
               'validate': {'type:uuid': None},
               'is_visible': True,
               'is_sort_key': True,
               'primary_key': True},
        'tenant_id': {'allow_post': True, 'allow_put': False,
                      'validate': {
                          'type:string': db_const.PROJECT_ID_FIELD_SIZE},
                      'required_by_policy': True,
                      'is_sort_key': True,
                      'is_visible': True},
        'name': {'allow_post': True, 'allow_put': True,
                 'validate': {'type:string': db_const.NAME_FIELD_SIZE},
                 'is_visible': True, 'is_sort_key': True, 'default': ''},
        'description': {'allow_post': True, 'allow_put': True,
                        'validate': {
                            'type:string': db_const.DESCRIPTION_FIELD_SIZE},
                        'is_visible': True, 'default': ''},
        'local_id': {'allow_post': True, 'allow_put': True,
                     'validate': {'type:string': None},
                     'is_visible': True, 'default': ''},
        'peer_address': {'allow_post': True, 'allow_put': True,
                         'validate': {'type:string': None},
                         'is_visible': True},
        'peer_id': {'allow_post': True, 'allow_put': True,
                    'validate': {'type:string': None},
                    'is_visible': True},
        'peer_cidrs': {'allow_post': True, 'allow_put': True,
                       'convert_to': converters.convert_to_list,
                       'validate': {'type:list_of_subnets_or_none': None},
                       'is_visible': True,
                       'default': None},
        'local_ep_group_id': {'allow_post': True, 'allow_put': True,
                              'validate': {'type:uuid_or_none': None},
                              'is_visible': True, 'default': None},
        'peer_ep_group_id': {'allow_post': True, 'allow_put': True,
                             'validate': {'type:uuid_or_none': None},
                             'is_visible': True, 'default': None},
        'route_mode': {'allow_post': False, 'allow_put': False,
                       'is_visible': True},
        'mtu': {'allow_post': True, 'allow_put': True,
                'default': 1500,
                'validate': {'type:non_negative': None},
                'convert_to': converters.convert_to_int,
                'is_visible': True},
        'initiator': {'allow_post': True, 'allow_put': True,
                      'default': VPN_INITIATOR_BI_DIRECTIONAL,
                      'validate': {'type:values': VPN_SUPPORTED_INITIATORS},
                      'is_visible': True},
        'auth_mode': {'allow_post': False, 'allow_put': False,
                      'default': VPN_AUTH_MODE_PSK,
                      'validate': {'type:values': VPN_SUPPORTED_AUTH_MODES},
                      'is_visible': True},
        'psk': {'allow_post': True, 'allow_put': True,
                'validate': {'type:string': None},
                'is_visible': True},
        'dpd': {
            'allow_post': True, 'allow_put': True,
            'convert_to': converters.convert_none_to_empty_dict,
            'is_visible': True,
            'default': {},
            'validate': {
                'type:dict_or_empty': {
                    'action': {'type:values': VPN_SUPPORTED_DPD_ACTIONS},
                    'interval': {'type:non_negative': None},
                    'timeout': {'type:non_negative': None}}}},
        'admin_state_up': {'allow_post': True, 'allow_put': True,
                           'default': True,
                           'convert_to': converters.convert_to_boolean,
                           'is_visible': True},
        'status': {'allow_post': False, 'allow_put': False,
                   'is_visible': True},
        'vpnservice_id': {'allow_post': True, 'allow_put': False,
                          'validate': {'type:uuid': None},
                          'is_visible': True},
        'ikepolicy_id': {'allow_post': True, 'allow_put': False,
                         'validate': {'type:uuid': None},
                         'is_visible': True},
        'ipsecpolicy_id': {'allow_post': True, 'allow_put': False,
                           'validate': {'type:uuid': None},
                           'is_visible': True},
    },

    IPSEC_POLICIES: {
        'id': {'allow_post': False, 'allow_put': False,
               'validate': {'type:uuid': None},
               'is_visible': True,
               'is_sort_key': True,
               'primary_key': True},
        'tenant_id': {'allow_post': True, 'allow_put': False,
                      'validate': {
                          'type:string': db_const.PROJECT_ID_FIELD_SIZE},
                      'required_by_policy': True,
                      'is_sort_key': True,
                      'is_visible': True},
        'name': {'allow_post': True, 'allow_put': True,
                 'validate': {'type:string': db_const.NAME_FIELD_SIZE},
                 'is_visible': True, 'is_sort_key': True, 'default': ''},
        'description': {'allow_post': True, 'allow_put': True,
                        'validate': {
                            'type:string': db_const.DESCRIPTION_FIELD_SIZE},
                        'is_visible': True, 'default': ''},
        'transform_protocol': {
            'allow_post': True,
            'allow_put': True,
            'default': VPN_TRANSFORM_PROTOCOL_ESP,
            'validate': {'type:values': VPN_SUPPORTED_TRANSFORM_PROTOCOLS},
            'is_visible': True},
        'auth_algorithm': {
            'allow_post': True,
            'allow_put': True,
            'default': VPN_AUTH_ALGORITHM_SHA1,
            'validate': {'type:values': VPN_SUPPORTED_AUTH_ALGORITHMS},
            'is_visible': True},
        'encryption_algorithm': {
            'allow_post': True,
            'allow_put': True,
            'default': VPN_ENCRYPTION_ALGORITHM_AES_128,
            'validate': {'type:values': VPN_SUPPORTED_ENCRYPTION_ALGORITHMS},
            'is_visible': True},
        'encapsulation_mode': {
            'allow_post': True,
            'allow_put': True,
            'default': VPN_ENCAPSULATION_MODE_TUNNEL,
            'validate': {'type:values': VPN_SUPPORTED_ENCAPSULATION_MODES},
            'is_visible': True},
        'lifetime': {
            'allow_post': True, 'allow_put': True,
            'convert_to': converters.convert_none_to_empty_dict,
            'default': {},
            'validate': {
                'type:dict_or_empty': {
                    'units': {'type:values': VPN_SUPPORTED_LIFETIME_UNITS},
                    'value': {'type:range': _vpn_lifetime_limits}}},
            'is_visible': True},
        'pfs': {'allow_post': True, 'allow_put': True,
                'default': VPN_PFS_GROUP5,
                'validate': {'type:values': VPN_SUPPORTED_PFSES},
                'is_visible': True},
    },

    IKE_POLICIES: {
        'id': {'allow_post': False, 'allow_put': False,
               'validate': {'type:uuid': None},
               'is_visible': True,
               'is_sort_key': True,
               'primary_key': True},
        'tenant_id': {'allow_post': True, 'allow_put': False,
                      'validate': {
                          'type:string': db_const.PROJECT_ID_FIELD_SIZE},
                      'required_by_policy': True,
                      'is_sort_key': True,
                      'is_visible': True},
        'name': {'allow_post': True, 'allow_put': True,
                 'validate': {'type:string': db_const.NAME_FIELD_SIZE},
                 'is_visible': True, 'is_sort_key': True, 'default': ''},
        'description': {'allow_post': True, 'allow_put': True,
                        'validate': {
                            'type:string': db_const.DESCRIPTION_FIELD_SIZE},
                        'is_visible': True, 'default': ''},
        'auth_algorithm': {
            'allow_post': True, 'allow_put': True,
            'default': VPN_AUTH_ALGORITHM_SHA1,
            'validate': {'type:values': VPN_SUPPORTED_AUTH_ALGORITHMS},
            'is_visible': True},
        'encryption_algorithm': {
            'allow_post': True, 'allow_put': True,
            'default': VPN_ENCRYPTION_ALGORITHM_AES_128,
            'validate': {'type:values': VPN_SUPPORTED_ENCRYPTION_ALGORITHMS},
            'is_visible': True},
        'phase1_negotiation_mode': {
            'allow_post': True, 'allow_put': True,
            'default': VPN_PHASE1_NEGOTIATION_MODE_MAIN,
            'validate': {
                'type:values': VPN_SUPPORTED_PHASE1_NEGOTIATION_MODES},
            'is_visible': True},
        'lifetime': {
            'allow_post': True, 'allow_put': True,
            'convert_to': converters.convert_none_to_empty_dict,
            'default': {},
            'validate': {
                'type:dict_or_empty': {
                    'units': {'type:values': VPN_SUPPORTED_LIFETIME_UNITS},
                    'value': {'type:range': _vpn_lifetime_limits}}},
            'is_visible': True},
        'ike_version': {
            'allow_post': True, 'allow_put': True,
            'default': VPN_IKE_VERSION_V1,
            'validate': {'type:values': VPN_SUPPORTED_IKE_VERSIONS},
            'is_visible': True},
        'pfs': {'allow_post': True, 'allow_put': True,
                'default': VPN_PFS_GROUP5,
                'validate': {'type:values': VPN_SUPPORTED_PFSES},
                'is_visible': True},
    },
}

# The subresource attribute map for the extension.  This extension has only
# top level resources, not child resources, so this is set to an empty dict.
SUB_RESOURCE_ATTRIBUTE_MAP = {
}

# The action map.
ACTION_MAP = {
}

# The action status.
ACTION_STATUS = {
}

# The list of required extensions.
REQUIRED_EXTENSIONS = [
    l3.ALIAS,
]

# The list of optional extensions.
OPTIONAL_EXTENSIONS = [
]
