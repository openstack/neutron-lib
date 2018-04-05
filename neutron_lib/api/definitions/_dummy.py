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

# A declaration of a dummy neutron extension: this may have a number of
# constants being defined, and their aim is to document as much about
# the extension as possible.

# The alias of the extension.
ALIAS = 'dummy'

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
NAME = 'Foo Extension'

# A prefix for API resources. An empty prefix means that the API is going
# to be exposed at the v2/ level as any other core resource (mandatory).
API_PREFIX = ''

# The description of the extension (mandatory).
DESCRIPTION = "Provides support for foo"

# A timestamp of when the extension was introduced (mandatory).
UPDATED_TIMESTAMP = "2000-00-01T00:00:00-00:00"

# The specific resources and/or attributes for the extension (optional).
# In case of simple extensions, with single resource, the string constants
# RESOURCE_NAME and COLLECTION_NAME can be used, otherwise string literals
# can be used instead.

# The name of the resource introduced or being extended
# (in case it is defined by another extension, or it is
# a core resource).
RESOURCE_NAME = 'foo'

# The plural for the resource introduced or being extended
# (in case it is defined by another extension, or it is a
# core resource).
COLLECTION_NAME = 'fooes'

# The resource attribute map for the extension. It is effectively the
# bulk of the API contract alongside ACTION_MAP (mandatory).
RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        'id': {'allow_post': False, 'allow_put': False,
               'validate': {'type:uuid': None},
               'is_visible': True, 'primary_key': True},
    }
}

# The subresource attribute map for the extension. It adds child resources
# to main extension's resource. The subresource map must have a parent and
# a parameters entry. If an extension does not need such a map, None can
# be specified (mandatory).
# Note that if an existing sub-resource is being extended, the
# existing resources to extend the new extension attributes must be
# defined under the 'parameters' key.
SUB_RESOURCE_ATTRIBUTE_MAP = {
    'subfoo': {
        'parent': {
            'collection_name': COLLECTION_NAME,
            'member_name': RESOURCE_NAME},
        'parameters': {
            'id': {'allow_post': False, 'allow_put': False,
                   'validate': {'type:uuid': None},
                   'is_visible': True,
                   'primary_key': True},
        },
    },
}

# The action map: it associates verbs with methods to be performed on
# the API resource (mandatory). For example:
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

# The action status: it associates response statuses with methods to be
# performed on the API resource (mandatory). For example:
#
# ACTION_STATUS = {
#     'create': 201,
#     'delete': 204
# }
ACTION_STATUS = {
}

# The list of required extensions (mandatory).
REQUIRED_EXTENSIONS = [
]

# The list of optional extensions (mandatory).
OPTIONAL_EXTENSIONS = [
]

# TODO(armax): add support for modeling custom queries
