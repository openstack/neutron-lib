# Copyright (c) 2017 NEC Corporation.  All rights reserved.
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

from neutron_lib.api.definitions import port
from neutron_lib import constants


VALID_VALUES = [None, constants.ACTIVE, constants.DOWN]

# The alias of the extension.
ALIAS = 'data-plane-status'

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
NAME = 'Port data plane status extension'

# The description of the extension.
DESCRIPTION = "Expose status of underlying data plane"

# A timestamp of when the extension was introduced.
UPDATED_TIMESTAMP = "2017-01-24T10:00:00-00:00"

# The name of the resource introduced or being extended.
RESOURCE_NAME = port.RESOURCE_NAME

# The plural for the resource introduced or being extended.
COLLECTION_NAME = port.COLLECTION_NAME

# The specific resources and/or attributes for the extension (optional).
DATA_PLANE_STATUS = 'data_plane_status'

# The resource attribute map for the extension.
RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        DATA_PLANE_STATUS: {'allow_post': False, 'allow_put': True,
                            'default': constants.ATTR_NOT_SPECIFIED,
                            'validate': {'type:values': VALID_VALUES},
                            'is_visible': True,
                            'enforce_policy': True, }
    },
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
]

# The list of optional extensions.
OPTIONAL_EXTENSIONS = [
]
