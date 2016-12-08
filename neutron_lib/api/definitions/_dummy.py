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

# The alias of the extension.
ALIAS = 'dummy'

# The label to lookup the plugin in the plugin directory. It can match the
# alias, as required.
LABEL = 'DUMMY'

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
NAME = 'Foo Extension'

# A prefix for API resources. An empty prefix means that the API is going
# to be exposed at the v2/ level as any other core resource.
API_PREFIX = ''

# The description of the extension.
DESCRIPTION = "Provides support for foo"

# A timestamp of when the extension was introduced.
UPDATED_TIMESTAMP = "2000-00-01T00:00:00-00:00"

# The name of the resource.
RESOURCE_NAME = 'foo'

# The plural for the resource.
COLLECTION_NAME = 'fooes'

# The resource attribute map for the extension. It is effectively the
# bulk of the API contract alongside ACTION_MAP
RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        'id': {'allow_post': False, 'allow_put': False,
               'validate': {'type:uuid': None},
               'is_visible': True, 'primary_key': True},
    }
}

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

# The list of required extensions.
REQUIRED_EXTENSIONS = [
]

# The list of optional extensions.
OPTIONAL_EXTENSIONS = [
]

# TODO(armax): add support for modeling custom queries
