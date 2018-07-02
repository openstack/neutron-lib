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
from neutron_lib.db import constants

# The alias of the extension.
ALIAS = 'router'

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
NAME = 'Neutron L3 Router'

# A prefix for API resources. An empty prefix means that the API is going
# to be exposed at the v2/ level as any other core resource.
API_PREFIX = ''

# The description of the extension.
DESCRIPTION = ("Router abstraction for basic L3 forwarding "
               "between L2 Neutron networks and access to external "
               "networks via a NAT gateway.")

# A timestamp of when the extension was introduced.
UPDATED_TIMESTAMP = "2012-07-20T10:00:00-00:00"


FLOATING_IP_ADDRESS = 'floating_ip_address'
FLOATING_NETWORK_ID = 'floating_network_id'
FLOATINGIP = 'floatingip'
FLOATINGIPS = 'floatingips'
ROUTERS = 'routers'
ROUTER = 'router'
SUBNET_ID = 'subnet_id'
ROUTER_ID = 'router_id'
PORT_ID = 'port_id'
FIXED_IP_ADDRESS = 'fixed_ip_address'
EXTERNAL_GW_INFO = 'external_gateway_info'


RESOURCE_ATTRIBUTE_MAP = {
    ROUTERS: {
        'id': {'allow_post': False, 'allow_put': False,
               'validate': {'type:uuid': None},
               'is_visible': True,
               'is_filter': True,
               'is_sort_key': True,
               'primary_key': True},
        'name': {'allow_post': True, 'allow_put': True,
                 'validate': {'type:string': constants.NAME_FIELD_SIZE},
                 'is_filter': True,
                 'is_sort_key': True,
                 'is_visible': True, 'default': ''},
        'admin_state_up': {'allow_post': True, 'allow_put': True,
                           'default': True,
                           'convert_to': converters.convert_to_boolean,
                           'is_filter': True,
                           'is_sort_key': True,
                           'is_visible': True},
        'status': {'allow_post': False, 'allow_put': False,
                   'is_sort_key': True,
                   'is_visible': True},
        'tenant_id': {'allow_post': True, 'allow_put': False,
                      'required_by_policy': True,
                      'validate': {
                          'type:string': constants.PROJECT_ID_FIELD_SIZE},
                      'is_filter': True,
                      'is_sort_key': True,
                      'is_visible': True},
        EXTERNAL_GW_INFO: {'allow_post': True, 'allow_put': True,
                           'is_visible': True, 'default': None,
                           'enforce_policy': True,
                           'validate': {
                               'type:dict_or_nodata': {
                                   'network_id': {'type:uuid': None,
                                                  'required': True},
                                   'external_fixed_ips': {
                                       'type:fixed_ips': None,
                                       'required': False,
                                   }
                               }
                           }}
    },
    FLOATINGIPS: {
        'id': {'allow_post': False, 'allow_put': False,
               'validate': {'type:uuid': None},
               'is_visible': True,
               'is_filter': True,
               'is_sort_key': True,
               'primary_key': True},
        'floating_ip_address': {'allow_post': True, 'allow_put': False,
                                'validate': {'type:ip_address_or_none': None},
                                'is_sort_key': True, 'is_filter': True,
                                'is_visible': True, 'default': None,
                                'enforce_policy': True},
        'subnet_id': {'allow_post': True, 'allow_put': False,
                      'validate': {'type:uuid_or_none': None},
                      'is_visible': False,  # Use False for input only attr
                      'default': None},
        'floating_network_id': {'allow_post': True, 'allow_put': False,
                                'validate': {'type:uuid': None},
                                'is_filter': True, 'is_sort_key': True,
                                'is_visible': True},
        'router_id': {'allow_post': False, 'allow_put': False,
                      'validate': {'type:uuid_or_none': None},
                      'is_filter': True, 'is_sort_key': True,
                      'is_visible': True, 'default': None},
        'port_id': {'allow_post': True, 'allow_put': True,
                    'validate': {'type:uuid_or_none': None},
                    'is_filter': True,
                    'is_visible': True, 'default': None,
                    'required_by_policy': True},
        'fixed_ip_address': {'allow_post': True, 'allow_put': True,
                             'validate': {'type:ip_address_or_none': None},
                             'is_filter': True, 'is_sort_key': True,
                             'is_visible': True, 'default': None},
        'tenant_id': {'allow_post': True, 'allow_put': False,
                      'required_by_policy': True,
                      'validate': {
                          'type:string': constants.PROJECT_ID_FIELD_SIZE},
                      'is_filter': True, 'is_sort_key': True,
                      'is_visible': True},
        'status': {'allow_post': False, 'allow_put': False,
                   'is_filter': True, 'is_sort_key': True,
                   'is_visible': True},
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
    ROUTER: {
        'add_router_interface': 'PUT',
        'remove_router_interface': 'PUT'
    }
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
