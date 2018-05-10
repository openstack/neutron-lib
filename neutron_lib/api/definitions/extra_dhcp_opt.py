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
from neutron_lib.api.definitions import port


# Common definitions for maximum string field length
DHCP_OPT_NAME_MAX_LEN = 64
VALID_BLANK_EXTRA_DHCP_OPTS = ('router', 'classless-static-route')
DHCP_OPT_VALUE_MAX_LEN = 255


EXTRA_DHCP_OPT_KEY_SPECS = [
    # key spec for opt_name in _VALID_BLANK_EXTRA_DHCP_OPTS
    {'opt_name': {'type:values': VALID_BLANK_EXTRA_DHCP_OPTS,
                  'required': True},
     'opt_value': {'type:string_or_none':
                   DHCP_OPT_VALUE_MAX_LEN,
                   'required': True},
     'ip_version': {'convert_to': converters.convert_to_int,
                    'type:values': [4, 6],
                    'required': False}},
    # key spec if opt_name not in _VALID_BLANK_EXTRA_DHCP_OPTS
    {'opt_name': {'type:not_empty_string': DHCP_OPT_NAME_MAX_LEN,
                  'required': True},
     'opt_value': {'type:not_empty_string_or_none':
                   DHCP_OPT_VALUE_MAX_LEN,
                   'required': True},
     'ip_version': {'convert_to': converters.convert_to_int,
                    'type:values': [4, 6],
                    'required': False}}
]

EXTRADHCPOPTS = 'extra_dhcp_opts'
DHCP_OPT_CLIENT_ID = "client-id"

# client-id option value as defined in RFC 4776
DHCP_OPT_CLIENT_ID_NUM = 61

# The alias of the extension.
ALIAS = 'extra_dhcp_opt'

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
NAME = 'Neutron Extra DHCP options'

# A prefix for API resources. An empty prefix means that the API is going
# to be exposed at the v2/ level as any other core resource (mandatory).
API_PREFIX = ''

# The description of the extension (mandatory).
DESCRIPTION = ("Extra options configuration for DHCP. "
               "For example PXE boot options to DHCP clients can "
               "be specified (e.g. tftp-server, server-ip-address, "
               "bootfile-name)")

# A timestamp of when the extension was introduced (mandatory).
UPDATED_TIMESTAMP = "2013-03-17T12:00:00-00:00"

# The specific resources and/or attributes for the extension (optional).
# In case of simple extensions, with single resource, the string constants
# RESOURCE_NAME and COLLECTION_NAME can be used, otherwise string literals
# can be used instead.

# The name of the resource introduced or being extended
# (in case it is defined by another extension, or it is
# a core resource).
RESOURCE_NAME = port.RESOURCE_NAME

# The plural for the resource introduced or being extended
# (in case it is defined by another extension, or it is a
# core resource).
COLLECTION_NAME = port.COLLECTION_NAME

# The resource attribute map for the extension. It is effectively the
# bulk of the API contract alongside ACTION_MAP (mandatory).
RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        EXTRADHCPOPTS: {
            'allow_post': True,
            'allow_put': True,
            'is_visible': True,
            'default': None,
            'validate': {
                'type:list_of_any_key_specs_or_none': EXTRA_DHCP_OPT_KEY_SPECS
            }
        }
    }
}

# The subresource attribute map for the extension. It adds child resources
# to main extension's resource. The subresource map must have a parent and
# a parameters entry. If an extension does not need such a map, None can
# be specified (mandatory).
SUB_RESOURCE_ATTRIBUTE_MAP = {}

# The action map: it associates verbs with methods to be performed on
# the API resource (mandatory).
ACTION_MAP = {}

# The list of required extensions (mandatory).
REQUIRED_EXTENSIONS = []

# The list of optional extensions (mandatory).
OPTIONAL_EXTENSIONS = []

ACTION_STATUS = {}
