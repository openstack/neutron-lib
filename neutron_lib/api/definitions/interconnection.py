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

from neutron_lib.api.definitions import l3
from neutron_lib.db import constants as db_const

# The alias of the extension.
ALIAS = 'interconnection'

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
NAME = 'Neutron-Neutron Interconnection'

# The description of the extension.
DESCRIPTION = "Provides support for Neutron-Neutron Interconnections"

# A timestamp of when the extension was introduced.
UPDATED_TIMESTAMP = "2019-01-14T16:30:00-00:00"

API_PREFIX = 'interconnection'

# The specific resources and/or attributes for the extension (optional).
RESOURCE_NAME = 'interconnection'
COLLECTION_NAME = 'interconnections'

NETWORK_L2 = 'network_l2'
NETWORK_L3 = 'network_l3'
VALID_TYPES = [l3.ROUTER, NETWORK_L2, NETWORK_L3]

# The resource attribute map for the extension.
RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        'id': {'allow_post': False, 'allow_put': False,
               'validate': {'type:uuid': None},
               'is_filter': True, 'is_sort_key': True,
               'is_visible': True,
               'primary_key': True},
        'project_id': {'allow_post': True, 'allow_put': False,
                       'validate': {
                           'type:string': db_const.PROJECT_ID_FIELD_SIZE},
                       'required_by_policy': True,
                       'is_filter': True, 'is_sort_key': True,
                       'is_visible': True},
        'name': {'allow_post': True, 'allow_put': True,
                 'default': '',
                 'validate': {'type:string': db_const.NAME_FIELD_SIZE},
                 'is_filter': True, 'is_sort_key': True,
                 'is_visible': True},
        'type': {'allow_post': True, 'allow_put': False,
                 'validate': {'type:values': VALID_TYPES},
                 'is_filter': True, 'is_sort_key': True,
                 'is_visible': True},
        'state': {'allow_post': False, 'allow_put': False,
                  'is_filter': True, 'is_sort_key': True,
                  'is_visible': True},
        'local_resource_id': {'allow_post': True, 'allow_put': False,
                              'validate': {'type:uuid': None},
                              'is_visible': True},
        'remote_resource_id': {'allow_post': True, 'allow_put': False,
                               'validate': {'type:uuid': None},
                               'is_visible': True},
        'remote_keystone': {'allow_post': True, 'allow_put': False,
                            'validate': {'type:string_or_none': None},
                            'is_visible': True},
        'remote_region': {'allow_post': True, 'allow_put': False,
                          'validate': {'type:string_or_none': None},
                          'is_visible': True},
        'remote_interconnection_id': {'allow_post': False, 'allow_put': False,
                                      'validate': {'type:uuid_or_none': None},
                                      'is_visible': True},
        'local_parameters': {'allow_post': False, 'allow_put': False,
                             'is_visible': True},
        'remote_parameters': {'allow_post': False, 'allow_put': False,
                              'is_visible': True}
    },
}

# The subresource attribute map for the extension. It adds child resources
# to main extension's resource. The subresource map must have a parent and
# a parameters entry. If an extension does not need such a map, None can
# be specified (mandatory).
SUB_RESOURCE_ATTRIBUTE_MAP = None

# The action map: it associates verbs with methods to be performed on
# the API resource.
ACTION_MAP = {
    RESOURCE_NAME: {
        'refresh': 'PUT'
    }
}

# The action status.
ACTION_STATUS = {
}

# The list of required extensions.
REQUIRED_EXTENSIONS = [
    l3.ALIAS
]

# The list of optional extensions.
OPTIONAL_EXTENSIONS = [
]
