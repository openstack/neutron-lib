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
from neutron_lib.api.definitions import constants as api_const
from neutron_lib.api.definitions import port
from neutron_lib import constants
from neutron_lib.db import constants as db_const

# The alias of the extension.
ALIAS = 'fwaas_v2'

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
NAME = 'FWaaS v2'

# The description of the extension.
DESCRIPTION = "Provides support for firewall-as-a-service version 2"

# A timestamp of when the extension was introduced.
UPDATED_TIMESTAMP = "2016-10-06T10:00:00-00:00"

# Base for the API calls
API_PREFIX = '/fwaas'

RESOURCE_ATTRIBUTE_MAP = {
    api_const.FIREWALL_RULES: {
        'id': {'allow_post': False, 'allow_put': False,
               'validate': {'type:uuid': None},
               'is_visible': True, 'primary_key': True},
        'tenant_id': {'allow_post': True, 'allow_put': False,
                      'required_by_policy': True,
                      'validate': {'type:string':
                                   db_const.UUID_FIELD_SIZE},
                      'is_visible': True},
        'name': {'allow_post': True, 'allow_put': True,
                 'validate': {'type:string': db_const.NAME_FIELD_SIZE},
                 'is_visible': True, 'default': ''},
        'description': {'allow_post': True, 'allow_put': True,
                        'validate': {'type:string':
                                     db_const.DESCRIPTION_FIELD_SIZE},
                        'is_visible': True, 'default': ''},
        'firewall_policy_id': {'allow_post': False, 'allow_put': False,
                               'validate': {'type:uuid_or_none': None},
                               'is_visible': True},
        constants.SHARED: {
            'allow_post': True, 'allow_put': True,
            'default': False, 'is_visible': True,
            'convert_to': converters.convert_to_boolean,
            'required_by_policy': True, 'enforce_policy': True
        },
        'protocol': {
            'allow_post': True, 'allow_put': True,
            'is_visible': True, 'default': None,
            'convert_to': converters.convert_to_protocol,
            'validate': {'type:values': api_const.FW_PROTOCOL_VALUES}},
        'ip_version': {'allow_post': True, 'allow_put': True,
                       'default': 4, 'convert_to': converters.convert_to_int,
                       'validate': {'type:values': [4, 6]},
                       'is_visible': True},
        'source_ip_address': {'allow_post': True, 'allow_put': True,
                              'validate': {'type:ip_or_subnet_or_none': None},
                              'is_visible': True, 'default': None},
        'destination_ip_address': {'allow_post': True, 'allow_put': True,
                                   'validate': {'type:ip_or_subnet_or_none':
                                                None},
                                   'is_visible': True, 'default': None},
        'source_port': {'allow_post': True, 'allow_put': True,
                        'validate': {'type:port_range': None},
                        'convert_to': converters.convert_to_string,
                        'default': None, 'is_visible': True},
        'destination_port': {'allow_post': True, 'allow_put': True,
                             'validate': {'type:port_range': None},
                             'convert_to': converters.convert_to_string,
                             'default': None, 'is_visible': True},
        'position': {'allow_post': False, 'allow_put': False,
                     'default': None, 'is_visible': True},
        'action': {'allow_post': True, 'allow_put': True,
                   'convert_to': converters.convert_string_to_case_insensitive,
                   'validate': {'type:values':
                                api_const.FW_VALID_ACTION_VALUES},
                   'is_visible': True, 'default': 'deny'},
        'enabled': {'allow_post': True, 'allow_put': True,
                    'convert_to': converters.convert_to_boolean,
                    'default': True, 'is_visible': True},
        'source_firewall_group_id': {'allow_post': True, 'allow_put': True,
                                     'validate': {'type:uuid_or_none': None},
                                     'is_visible': True, 'default': None},
        'destination_firewall_group_id': {'allow_post': True,
                                          'allow_put': True,
                                          'validate':
                                              {'type:uuid_or_none': None},
                                          'is_visible': True, 'default': None},
    },
    api_const.FIREWALL_GROUPS: {
        'id': {'allow_post': False, 'allow_put': False,
               'validate': {'type:uuid': None},
               'is_visible': True,
               'primary_key': True},
        'name': {'allow_post': True, 'allow_put': True,
                 'validate': {'type:string': db_const.NAME_FIELD_SIZE},
                 'is_visible': True, 'default': ''},
        'description': {'allow_post': True, 'allow_put': True,
                        'validate': {'type:string':
                                     db_const.DESCRIPTION_FIELD_SIZE},
                        'is_visible': True, 'default': ''},
        'admin_state_up': {'allow_post': True, 'allow_put': True,
                           'default': True, 'is_visible': True,
                           'convert_to': converters.convert_to_boolean},
        'status': {'allow_post': False, 'allow_put': False,
                   'is_visible': True},
        constants.SHARED: {
            'allow_post': True, 'allow_put': True, 'default': False,
            'convert_to': converters.convert_to_boolean,
            'is_visible': True, 'required_by_policy': True,
            'enforce_policy': True
        },
        port.COLLECTION_NAME: {'allow_post': True, 'allow_put': True,
                               'validate': {'type:uuid_list': None},
                               'convert_to':
                                   converters.convert_none_to_empty_list,
                               'default': None, 'is_visible': True},
        'tenant_id': {'allow_post': True, 'allow_put': False,
                      'required_by_policy': True,
                      'validate': {'type:string':
                                   db_const.UUID_FIELD_SIZE},
                      'is_visible': True},
        'ingress_firewall_policy_id': {'allow_post': True,
                                       'allow_put': True,
                                       'validate': {'type:uuid_or_none':
                                                    None},
                                       'default': None, 'is_visible': True},
        'egress_firewall_policy_id': {'allow_post': True,
                                      'allow_put': True,
                                      'validate': {'type:uuid_or_none':
                                                   None},
                                      'default': None, 'is_visible': True},
    },
    api_const.FIREWALL_POLICIES: {
        'id': {'allow_post': False, 'allow_put': False,
               'validate': {'type:uuid': None},
               'is_visible': True,
               'primary_key': True},
        'tenant_id': {'allow_post': True, 'allow_put': False,
                      'required_by_policy': True,
                      'validate': {'type:string':
                                   db_const.UUID_FIELD_SIZE},
                      'is_visible': True},
        'name': {'allow_post': True, 'allow_put': True,
                 'validate': {'type:string': db_const.NAME_FIELD_SIZE},
                 'is_visible': True, 'default': ''},
        'description': {'allow_post': True, 'allow_put': True,
                        'validate': {'type:string':
                                     db_const.DESCRIPTION_FIELD_SIZE},
                        'is_visible': True, 'default': ''},
        constants.SHARED: {
            'allow_post': True, 'allow_put': True, 'default': False,
            'convert_to': converters.convert_to_boolean,
            'is_visible': True, 'required_by_policy': True,
            'enforce_policy': True
        },
        api_const.FIREWALL_RULES: {'allow_post': True, 'allow_put': True,
                                   'validate': {'type:uuid_list': None},
                                   'convert_to':
                                       converters.convert_none_to_empty_list,
                                   'default': None, 'is_visible': True},
        'audited': {'allow_post': True, 'allow_put': True, 'default': False,
                    'convert_to': converters.convert_to_boolean,
                    'is_visible': True},

    },
}

# The subresource attribute map for the extension.  This extension has only
# top level resources, not child resources, so this is set to an empty dict.
SUB_RESOURCE_ATTRIBUTE_MAP = {
}

# The action map.
ACTION_MAP = {
    'firewall_policy': {'insert_rule': 'PUT', 'remove_rule': 'PUT'},
}

# The action status.
ACTION_STATUS = {
}

# The list of required extensions.
REQUIRED_EXTENSIONS = [
]

# The list of optional extensions.
OPTIONAL_EXTENSIONS = [
]
