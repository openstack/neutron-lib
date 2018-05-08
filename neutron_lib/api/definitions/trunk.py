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
from neutron_lib.db import constants as db_const


# The alias of the extension.
ALIAS = 'trunk'

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
NAME = 'Trunk Extension'

# The description of the extension.
DESCRIPTION = "Provides support for trunk ports"

# A timestamp of when the extension was introduced.
UPDATED_TIMESTAMP = "2016-01-01T10:00:00-00:00"

# The specific resources and/or attributes for the extension (optional).
TRUNK = 'trunk'
TRUNKS = 'trunks'
SUB_PORTS = 'sub_ports'

# The resource attribute map for the extension.
RESOURCE_ATTRIBUTE_MAP = {
    TRUNKS: {
        'admin_state_up': {'allow_post': True, 'allow_put': True,
                           'default': True,
                           'convert_to': converters.convert_to_boolean,
                           'is_filter': True,
                           'is_sort_key': True,
                           'is_visible': True},
        'id': {'allow_post': False, 'allow_put': False,
               'validate': {'type:uuid': None},
               'is_filter': True,
               'is_sort_key': True,
               'is_visible': True, 'primary_key': True},
        'name': {'allow_post': True, 'allow_put': True,
                 'validate': {'type:string': db_const.NAME_FIELD_SIZE},
                 'is_filter': True,
                 'is_sort_key': True,
                 'default': '', 'is_visible': True},
        'tenant_id': {'allow_post': True, 'allow_put': False,
                      'required_by_policy': True,
                      'validate':
                          {'type:string': db_const.PROJECT_ID_FIELD_SIZE},
                      'is_filter': True,
                      'is_sort_key': True,
                      'is_visible': True},
        'port_id': {'allow_post': True, 'allow_put': False,
                    'required_by_policy': True,
                    'validate': {'type:uuid': None},
                    'is_filter': True,
                    'is_sort_key': True,
                    'is_visible': True},
        'status': {'allow_post': False, 'allow_put': False,
                   'is_sort_key': True,
                   'is_visible': True},
        SUB_PORTS: {'allow_post': True, 'allow_put': False,
                    'default': [],
                    'convert_list_to': converters.convert_kvp_list_to_dict,
                    'validate': {'type:subports': None},
                    'enforce_policy': True,
                    'is_visible': True}
    },
}

# The subresource attribute map for the extension.
SUB_RESOURCE_ATTRIBUTE_MAP = None

# The action map.
ACTION_MAP = {
    TRUNK: {
        'add_subports': 'PUT',
        'remove_subports': 'PUT',
        'get_subports': 'GET'
    }
}

# The action status.
ACTION_STATUS = {
}

# The list of required extensions.
REQUIRED_EXTENSIONS = [
    "binding",
]

# The list of optional extensions.
OPTIONAL_EXTENSIONS = [
    "provider",  # needed to learn about network segmentation details.
]

# TODO(armax): add support for modeling custom queries
