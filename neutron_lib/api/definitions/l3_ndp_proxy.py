# Copyright (c) 2020 Troila.
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
ALIAS = 'l3-ndp-proxy'

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
NAME = 'L3 NDP Proxy'

# A prefix for API resources. An empty prefix means that the API is going
# to be exposed at the v2/ level as any other core resource.
API_PREFIX = ''

# The description of the extension.
DESCRIPTION = "Router support for L3 NDP proxy."

# A timestamp of when the extension was introduced.
UPDATED_TIMESTAMP = "2021-06-29T10:00:00-00:00"

# The name of the resource.
RESOURCE_NAME = 'ndp_proxy'

# The plural for the resource.
COLLECTION_NAME = 'ndp_proxies'

ID = 'id'
NAME = 'name'
PROJECT_ID = 'project_id'
ROUTER_ID = 'router_id'
PORT_ID = 'port_id'
IP_ADDRESS = 'ip_address'
DESCRIPTION = 'description'

# The resource attribute map for the extension.
RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        ID: {'allow_post': False,
             'allow_put': False,
             'validate': {'type:uuid': None},
             'is_visible': True,
             'is_sort_key': True,
             'primary_key': True},
        NAME: {'allow_post': True,
               'allow_put': True,
               'validate': {'type:string': db_const.NAME_FIELD_SIZE},
               'is_filter': True,
               'is_sort_key': True,
               'is_visible': True, 'default': ''},
        PROJECT_ID: {'allow_post': True,
                     'allow_put': False,
                     'required_by_policy': True,
                     'validate': {
                         'type:string': db_const.PROJECT_ID_FIELD_SIZE},
                     'is_sort_key': True,
                     'is_visible': True},
        ROUTER_ID: {'allow_post': True,
                    'allow_put': False,
                    'validate': {'type:uuid': None},
                    'is_sort_key': True,
                    'is_visible': True},
        PORT_ID: {'allow_post': True,
                  'allow_put': False,
                  'validate': {'type:uuid': None},
                  'is_sort_key': True,
                  'is_visible': True},
        IP_ADDRESS: {'allow_post': True,
                     'allow_put': False,
                     'default': None,
                     'validate': {
                         'type:ip_address_or_none': None},
                     'is_sort_key': True,
                     'is_visible': True},
        DESCRIPTION: {'allow_post': True,
                      'allow_put': True,
                      'default': '',
                      'validate': {'type:string':
                                   db_const.LONG_DESCRIPTION_FIELD_SIZE},
                      'is_visible': True}
    }
}

# The subresource attribute map for the extension. It adds child resources
# to main extension's resource. The subresource map must have a parent and
# a parameters entry. If an extension does not need such a map, None can
# be specified (mandatory).
SUB_RESOURCE_ATTRIBUTE_MAP = {}

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
OPTIONAL_EXTENSIONS = []
