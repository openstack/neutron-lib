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
from neutron_lib.api.definitions import dns_domain_ports
from neutron_lib.api.definitions import subnet

DNS_PUBLISH_FIXED_IP = 'dns_publish_fixed_ip'

# The alias of the extension.
ALIAS = 'subnet-dns-publish-fixed-ip'

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
NAME = 'Subnet DNS publish fixed IP'

# The description of the extension.
DESCRIPTION = 'Support choosing to publish DNS records for IPs from a subnet'

# A timestamp of when the extension was introduced.
UPDATED_TIMESTAMP = "2019-05-24T10:00:00-00:00"

# The name of the resource introduced or being extended.
RESOURCE_NAME = subnet.RESOURCE_NAME

# The plural for the resource introduced or being extended.
COLLECTION_NAME = subnet.COLLECTION_NAME

# The resource attribute map for the extension.
RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        DNS_PUBLISH_FIXED_IP: {
            'allow_post': True, 'allow_put': True,
            'default': False,
            'convert_to': converters.convert_to_boolean,
            'is_visible': True
        }
    }
}

# The subresource attribute map for the extension.
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
    dns_domain_ports.ALIAS,
]

# The list of optional extensions.
OPTIONAL_EXTENSIONS = [
]
