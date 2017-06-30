# Copyright (c) 2017 IBM
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

from neutron_lib.api import converters as convert
from neutron_lib.api.definitions import dns
from neutron_lib.api.definitions import port
from neutron_lib.db import constants


# The alias of the extension.
ALIAS = 'dns-domain-ports'

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
NAME = 'dns_domain for ports'

# The description of the extension (mandatory).
DESCRIPTION = "Allows the DNS domain to be specified for a network port."

# A timestamp of when the extension was introduced (mandatory).
UPDATED_TIMESTAMP = "2017-04-24T10:00:00-00:00"

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
        dns.DNSDOMAIN: {'allow_post': True, 'allow_put': True,
                        'default': '',
                        'convert_to':
                            convert.convert_string_to_case_insensitive,
                        'validate': {'type:dns_domain_name':
                                     constants.FQDN_FIELD_SIZE},
                        'is_visible': True},
    },
}

# The subresource attribute map for the extension.
SUB_RESOURCE_ATTRIBUTE_MAP = {
}

# The action map
ACTION_MAP = {
}

# The action status
ACTION_STATUS = {
}

# The list of required extensions (mandatory).
REQUIRED_EXTENSIONS = [dns.ALIAS]

# The list of optional extensions (mandatory).
OPTIONAL_EXTENSIONS = [
]
