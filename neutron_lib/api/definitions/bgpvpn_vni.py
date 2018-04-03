#
# Copyright 2017 Ericsson India Global Services Pvt Ltd. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#

from neutron_lib.api import converters as lib_converters
from neutron_lib.api.definitions import bgpvpn
from neutron_lib import constants


VNI = 'vni'

# The alias of the extension.
ALIAS = 'bgpvpn-vni'

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
NAME = 'BGPVPN VXLAN VNI extension'

# A prefix for API resources. An empty prefix means that the API is going
# to be exposed at the v2/ level as any other core resource.
API_PREFIX = ''

# The description of the extension.
DESCRIPTION = "BGPVPN VXLAN VNI extension"

# A timestamp of when the extension was introduced.
UPDATED_TIMESTAMP = "2017-09-12T10:00:00-00:00"


RESOURCE_ATTRIBUTE_MAP = {
    bgpvpn.COLLECTION_NAME: {
        VNI: {'allow_post': True, 'allow_put': False,
              'convert_to': lib_converters.convert_to_int_if_not_none,
              'default': None,
              'validate': {'type:range_or_none': [constants.MIN_VXLAN_VNI,
                                                  constants.MAX_VXLAN_VNI]
                           },
              'is_visible': True, 'enforce_policy': True},
    },
}

# The subresource attribute map for the extension. It adds child resources
# to main extension's resource. The subresource map must have a parent and
# a parameters entry. If an extension does not need such a map, None can
# be specified (mandatory).
SUB_RESOURCE_ATTRIBUTE_MAP = {}

# The action map: it associates verbs with methods to be performed on
# the API resource.
ACTION_MAP = {}

# The action status.
ACTION_STATUS = {
}

# The list of required extensions.
REQUIRED_EXTENSIONS = [bgpvpn.ALIAS]

# The list of optional extensions.
OPTIONAL_EXTENSIONS = []
