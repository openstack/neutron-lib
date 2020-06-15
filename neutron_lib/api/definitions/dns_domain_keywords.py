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

from neutron_lib.api.definitions import dns

# The alias of the extension.
ALIAS = 'dns-integration-domain-keywords'

# Whether or not this extension is simply signaling behavior to the user
# or it actively modifies the attribute map (mandatory).
IS_SHIM_EXTENSION = True

# Whether the extension is marking the adoption of standardattr model for
# legacy resources, or introducing new standardattr attributes. False or
# None if the standardattr model is adopted since the introduction of
# resource extension (mandatory).
# If this is True, the alias for the extension should be prefixed with
# 'standard-attr-'.
IS_STANDARD_ATTR_EXTENSION = False

# The name of the extension (mandatory).
NAME = 'DNS domain names with keywords allowed'

# A prefix for API resources. An empty prefix means that the API is going
# to be exposed at the v2/ level as any other core resource (mandatory).
API_PREFIX = ''

# The description of the extension (mandatory).
DESCRIPTION = ("Allows to use keywords like <project_id>, <project_name>, "
               "<user_id> and <user_name> as DNS domain name")

# A timestamp of when the extension was introduced (mandatory).
UPDATED_TIMESTAMP = "2020-06-15T18:00:00-00:00"

# The resource attribute map for the extension. It is effectively the
# bulk of the API contract alongside ACTION_MAP (mandatory).
RESOURCE_ATTRIBUTE_MAP = {}

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
REQUIRED_EXTENSIONS = [dns.ALIAS]

# The list of optional extensions (mandatory).
OPTIONAL_EXTENSIONS = []
