# Copyright (c) 2019 OpenStack Foundation
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
from neutron_lib.api.definitions import l3
from neutron_lib import constants
from neutron_lib.db import constants as db_const

PROTOCOLS = constants.IPTABLES_PROTOCOL_MAP.keys()

# The alias of the extension.
ALIAS = 'l3-conntrack-helper'

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
NAME = 'L3 Conntrack helper'

# A prefix for API resources. An empty prefix means that the API is going
# to be exposed at the v2/ level as any other core resource.
API_PREFIX = '/' + l3.ROUTERS

# The description of the extension.
DESCRIPTION = "Allow adding CT target rules for conntrack helper"

# A timestamp of when the extension was introduced.
UPDATED_TIMESTAMP = "2019-04-04T10:00:00-00:00"

# The name of the resource.
RESOURCE_NAME = 'conntrack_helper'

# The plural for the resource.
COLLECTION_NAME = 'conntrack_helpers'

# parent
PARENT_RESOURCE_NAME = l3.ROUTER
PARENT_COLLECTION_NAME = l3.ROUTERS

ID = 'id'
PROJECT_ID = 'project_id'
PROTOCOL = 'protocol'
PORT = 'port'
HELPER = 'helper'
RESOURCE_ATTRIBUTE_MAP = {}

# The subresource attribute map for the extension. It adds child resources
# to main extension's resource. The subresource map must have a parent and
# a parameters entry. If an extension does not need such a map, None can
# be specified (mandatory).
SUB_RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        'parent': {'collection_name': PARENT_COLLECTION_NAME,
                   'member_name': PARENT_RESOURCE_NAME},
        'parameters': {
            ID: {'allow_post': False,
                 'allow_put': False,
                 'validate': {'type:uuid': None},
                 'is_visible': True,
                 'primary_key': True,
                 'is_sort_key': True,
                 'is_filter': True},
            PROJECT_ID: {'allow_post': True,
                         'allow_put': False,
                         'validate': {
                             'type:string': db_const.PROJECT_ID_FIELD_SIZE},
                         'required_by_policy': True,
                         'is_visible': False},
            PROTOCOL: {'allow_post': True, 'allow_put': True,
                       'validate': {'type:values': PROTOCOLS},
                       'is_visible': True,
                       'convert_to': converters.convert_to_protocol,
                       'is_sort_key': True,
                       'is_filter': True},
            PORT: {'allow_post': True, 'allow_put': True,
                   'convert_to': converters.convert_to_int,
                   'validate': {'type:range': [1, 65535]},
                   'is_visible': True,
                   'is_sort_key': True,
                   'is_filter': True},
            HELPER: {'allow_post': True, 'allow_put': True,
                     'convert_to': converters.convert_to_string,
                     'validate': {'type:string': 64},
                     'is_visible': True,
                     'is_sort_key': True,
                     'is_filter': True},
        }
    }
}

# The action map: it associates verbs with methods to be performed on
# the API resource.
ACTION_MAP = {
}

# The action status.
ACTION_STATUS = {
}

# The list of required extensions.
REQUIRED_EXTENSIONS = [l3.ALIAS]

# The list of optional extensions.
OPTIONAL_EXTENSIONS = [
]
