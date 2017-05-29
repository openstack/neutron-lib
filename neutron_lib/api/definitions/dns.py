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

from neutron_lib.api import converters as convert
from neutron_lib.api.definitions import l3
from neutron_lib.api.definitions import network
from neutron_lib.api.definitions import port
from neutron_lib.api import validators
from neutron_lib.api.validators import dns as dns_validator
from neutron_lib.db import constants

# The alias of the extension.
ALIAS = 'dns-integration'

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
NAME = 'DNS Integration'

# A prefix for API resources. An empty prefix means that the API is going
# to be exposed at the v2/ level as any other core resource (mandatory).
API_PREFIX = ''

# The description of the extension (mandatory).
DESCRIPTION = "Provides integration with DNS."

# A timestamp of when the extension was introduced (mandatory).
UPDATED_TIMESTAMP = "2015-08-15T18:00:00-00:00"

DNSNAME = 'dns_name'
DNSDOMAIN = 'dns_domain'
DNSASSIGNMENT = 'dns_assignment'

validators.add_validator('dns_host_name', dns_validator.validate_dns_name)
validators.add_validator('fip_dns_host_name',
                         dns_validator.validate_fip_dns_name)
validators.add_validator('dns_domain_name',
                         dns_validator.validate_dns_domain)

# The resource attribute map for the extension. It is effectively the
# bulk of the API contract alongside ACTION_MAP (mandatory).
RESOURCE_ATTRIBUTE_MAP = {
    port.COLLECTION_NAME: {
        DNSNAME: {'allow_post': True, 'allow_put': True,
                  'default': '',
                  'convert_to': convert.convert_string_to_case_insensitive,
                  'validate': {'type:dns_host_name':
                               constants.FQDN_FIELD_SIZE},
                  'is_visible': True},
        DNSASSIGNMENT: {'allow_post': False, 'allow_put': False,
                        'is_visible': True},
    },
    l3.FLOATINGIPS: {
        DNSNAME: {'allow_post': True, 'allow_put': False,
                  'default': '',
                  'convert_to': convert.convert_string_to_case_insensitive,
                  'validate': {'type:fip_dns_host_name':
                               constants.FQDN_FIELD_SIZE},
                  'is_visible': True},
        DNSDOMAIN: {'allow_post': True, 'allow_put': False,
                    'default': '',
                    'convert_to': convert.convert_string_to_case_insensitive,
                    'validate': {'type:dns_domain_name':
                                 constants.FQDN_FIELD_SIZE},
                    'is_visible': True},
    },
    network.COLLECTION_NAME: {
        DNSDOMAIN: {'allow_post': True, 'allow_put': True,
                    'default': '',
                    'convert_to': convert.convert_string_to_case_insensitive,
                    'validate': {'type:dns_domain_name':
                                 constants.FQDN_FIELD_SIZE},
                    'is_visible': True},
    },
}

# The subresource attribute map for the extension. It adds child resources
# to main extension's resource. The subresource map must have a parent and
# a parameters entry. If an extension does not need such a map, None can
# be specified (mandatory). For example:
SUB_RESOURCE_ATTRIBUTE_MAP = {}

# The action map: it associates verbs with methods to be performed on
# the API resource (mandatory).
ACTION_MAP = {}

# The action status: it associates response statuses with methods to be
# performed on the API resource (mandatory).
ACTION_STATUS = {}

# The list of required extensions (mandatory).
REQUIRED_EXTENSIONS = [l3.ALIAS]

# The list of optional extensions (mandatory).
OPTIONAL_EXTENSIONS = []
