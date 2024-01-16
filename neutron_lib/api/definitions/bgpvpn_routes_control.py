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
from neutron_lib.api.definitions import bgpvpn
from neutron_lib.db import constants as db_const


# The alias of the extension.
ALIAS = 'bgpvpn-routes-control'

# Whether or not this extension is simply signaling behavior to the user
# or it actively modifies the attribute map (mandatory).
IS_SHIM_EXTENSION = False

# Whether the extension is marking the adoption of standardattr model for
# legacy resources, or introducing new standardattr attributes. False or
# None if the standardattr model is adopted since the introduction of
# resource extension (mandatory).
# If this is True, the alias for the extension should be prefixed with
# 'standard-attr-'.
IS_STANDARD_ATTR_EXTENSION = False

# The name of the extension (mandatory).
NAME = 'BGPVPN Routes Control Extension'

# The description of the extension (mandatory).
DESCRIPTION = "Provides support for controlling routes advertised to a BGPVPN"

# A timestamp of when the extension was introduced (mandatory).
UPDATED_TIMESTAMP = "2017-05-20T00:00:00-00:00"

# The specific resources and/or attributes for the extension (optional).
# In case of simple extensions, with single resource, the string constants
# RESOURCE_NAME and COLLECTION_NAME can be used, otherwise string literals
# can be used instead.

# The name of the resource introduced or being extended (later case)
RESOURCE_NAME = bgpvpn.RESOURCE_NAME

# The plural for the resource introduced or being extended (later case)
COLLECTION_NAME = bgpvpn.COLLECTION_NAME

LOCAL_PREF_KEY = 'local_pref'
LOCAL_PREF_RANGE = [0, 2**32 - 1]  # RFC 4271, section 4.3 (p.18)

RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        'ports': {'allow_post': False, 'allow_put': False,
                  'is_visible': True,
                  'enforce_policy': True},
        LOCAL_PREF_KEY: {
            'allow_post': True, 'allow_put': True,
            'is_visible': True,
            'default': None,
            'validate': {'type:range_or_none': LOCAL_PREF_RANGE},
            'enforce_policy': True}
    }
}

PORT_ASSOCIATION = 'port_association'
PORT_ASSOCIATIONS = 'port_associations'

ROUTES = 'routes'

PREFIX_TYPE = 'prefix'
BGPVPN_TYPE = 'bgpvpn'
ROUTE_TYPES = [PREFIX_TYPE, BGPVPN_TYPE]

ADV_FIXED_IPS = 'advertise_fixed_ips'

TYPE = 'type'

PREFIX = 'prefix'
BGPVPN_ID = 'bgpvpn_id'

ADV_EXTRA_ROUTES = 'advertise_extra_routes'

LOCAL_PREF_KEY_SPEC = {'type:range': LOCAL_PREF_RANGE,
                       'required': False}

ROUTE_SPECS = [
    {'type': {'type:values': [PREFIX_TYPE],
              'required': True},
     'prefix': {'type:subnet': None,
                'required': True},
     LOCAL_PREF_KEY: LOCAL_PREF_KEY_SPEC,
     },
    {'type': {'type:values': [BGPVPN_TYPE],
              'required': True},
     'bgpvpn_id': {'type:uuid': None,
                   'required': True},
     LOCAL_PREF_KEY: LOCAL_PREF_KEY_SPEC,
     },
]

SUB_RESOURCE_ATTRIBUTE_MAP = {
    PORT_ASSOCIATIONS: {
        'parent': {
            'collection_name': COLLECTION_NAME,
            'member_name': RESOURCE_NAME},
        'parameters': {
            'id': {'allow_post': False, 'allow_put': False,
                   'validate': {'type:uuid': None},
                   'is_visible': True,
                   'primary_key': True},
            'project_id': {'allow_post': True, 'allow_put': False,
                           'validate': {
                               'type:string': db_const.PROJECT_ID_FIELD_SIZE},
                           'required_by_policy': True,
                           'is_visible': True,
                           'enforce_policy': True},
            'port_id': {'allow_post': True, 'allow_put': False,
                        'validate': {'type:uuid': None},
                        'is_visible': True,
                        'enforce_policy': True},
            ROUTES: {'allow_post': True, 'allow_put': True,
                     'default': [],
                     'convert_list_to': converters.convert_kvp_list_to_dict,
                     'validate': {
                         'type:list_of_any_key_specs_or_none': ROUTE_SPECS
                     },
                     'enforce_policy': True,
                     'is_visible': True},
            ADV_FIXED_IPS: {'allow_post': True, 'allow_put': True,
                            'default': True,
                            'convert_to': converters.convert_to_boolean,
                            'is_visible': True},
        },
    },
    bgpvpn.ROUTER_ASSOCIATIONS: {
        'parent': {'collection_name': COLLECTION_NAME,
                   'member_name': RESOURCE_NAME},
        'parameters': {
            ADV_EXTRA_ROUTES: {'allow_post': True, 'allow_put': True,
                               'default': True,
                               'convert_to': converters.convert_to_boolean,
                               'is_visible': True},
        }
    }
}


ACTION_MAP = {
}

ACTION_STATUS = {}

REQUIRED_EXTENSIONS = [
    bgpvpn.ALIAS
]

OPTIONAL_EXTENSIONS = []
