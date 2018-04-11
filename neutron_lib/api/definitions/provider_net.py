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
from neutron_lib.api.definitions import network
from neutron_lib import constants

# The alias of the extension.
ALIAS = 'provider'

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
NAME = 'Provider Network'

# A prefix for API resources. An empty prefix means that the API is going
# to be exposed at the v2/ level as any other core resource.
API_PREFIX = ''

# The description of the extension.
DESCRIPTION = "Expose mapping of virtual networks to physical networks"

# A timestamp of when the extension was introduced.
UPDATED_TIMESTAMP = "2012-09-07T10:00:00-00:00"

# The name of the resource.
RESOURCE_NAME = network.RESOURCE_NAME

# The plural for the resource.
COLLECTION_NAME = network.COLLECTION_NAME

NETWORK_TYPE = 'provider:network_type'
PHYSICAL_NETWORK = 'provider:physical_network'
SEGMENTATION_ID = 'provider:segmentation_id'
ATTRIBUTES = (NETWORK_TYPE, PHYSICAL_NETWORK, SEGMENTATION_ID)

# Common definitions for maximum string field length
NETWORK_TYPE_MAX_LEN = 32
PHYSICAL_NETWORK_MAX_LEN = 64

RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        NETWORK_TYPE: {'allow_post': True, 'allow_put': True,
                       'validate': {'type:string': NETWORK_TYPE_MAX_LEN},
                       'default': constants.ATTR_NOT_SPECIFIED,
                       'enforce_policy': True,
                       'is_filter': True,
                       'is_visible': True},
        PHYSICAL_NETWORK: {'allow_post': True, 'allow_put': True,
                           'validate': {'type:string':
                                        PHYSICAL_NETWORK_MAX_LEN},
                           'default': constants.ATTR_NOT_SPECIFIED,
                           'enforce_policy': True,
                           'is_filter': True,
                           'is_visible': True},
        SEGMENTATION_ID: {'allow_post': True, 'allow_put': True,
                          'convert_to': converters.convert_to_int,
                          'enforce_policy': True,
                          'default': constants.ATTR_NOT_SPECIFIED,
                          'is_filter': True,
                          'is_visible': True},
    }
}

# The subresource attribute map for the extension. It adds child resources
# to main extension's resource. The subresource map must have a parent and
# a parameters entry. If an extension does not need such a map, None can
# be specified (mandatory).
SUB_RESOURCE_ATTRIBUTE_MAP = None

# The action map: it associates verbs with methods to be performed on
# the API resource. For example:
#
# ACTION_MAP = {
#     RESOURCE_NAME: {
#        'add_my_foo_bars': 'PUT',
#        'remove_my_foo_bars': 'PUT',
#        'get_my_foo_bars': 'GET'
#    }
# }
ACTION_MAP = {
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
