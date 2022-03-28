# Copyright (c) 2018 Intel Corporation.
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
from neutron_lib.api.definitions import provider_net as providernet
from neutron_lib import constants
from neutron_lib.db import constants as db_const

# The name of the extension.
NAME = 'Neutron Network Segment Range'
# The alias of the extension.
ALIAS = 'network-segment-range'
# The description of the extension.
DESCRIPTION = "Provides support for the network segment range management"

# A timestamp of when the extension was introduced.
UPDATED_TIMESTAMP = "2018-11-29T00:00:00-00:00"

# The name of the resource.
RESOURCE_NAME = 'network_segment_range'
# The plural for the resource.
COLLECTION_NAME = 'network_segment_ranges'

# Min ID for VLAN, VXLAN, GRE and GENEVE all equal to 1; Max ID for them are
# 4094, 2 ** 24 - 1, 2 ** 32 - 1 and 2 ** 24 - 1 respectively.
# Take the largest range: [MIN_GRE_ID, MAX_GRE_ID] as the limit for validation.
NETWORK_SEGMENT_RANGE_LIMIT = [constants.MIN_GRE_ID, constants.MAX_GRE_ID]

RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        'id': {'allow_post': False,
               'allow_put': False,
               'validate': {'type:uuid': None},
               'is_filter': True,
               'is_sort_key': True,
               'primary_key': True,
               'is_visible': True},
        'name': {'allow_post': True,
                 'allow_put': True,
                 'validate': {'type:string': db_const.NAME_FIELD_SIZE},
                 'default': '',
                 'is_filter': True,
                 'is_sort_key': True,
                 'is_visible': True},
        'default': {'allow_post': False,
                    'allow_put': False,
                    'convert_to': converters.convert_to_boolean,
                    'default': False,
                    'is_visible': True},
        constants.SHARED: {'allow_post': True,
                           'allow_put': False,
                           'convert_to': converters.convert_to_boolean,
                           'default': True,
                           'is_visible': True},
        'project_id': {'allow_post': True,
                       'allow_put': False,
                       'validate': {
                           'type:string': db_const.PROJECT_ID_FIELD_SIZE},
                       'required_by_policy': True,
                       'is_filter': True,
                       'is_sort_key': True,
                       'is_visible': True},
        'network_type': {'allow_post': True,
                         'allow_put': False,
                         'validate': {
                             'type:values':
                                 constants.NETWORK_SEGMENT_RANGE_TYPES},
                         'default': constants.ATTR_NOT_SPECIFIED,
                         'is_filter': True,
                         'is_visible': True},
        'physical_network': {'allow_post': True,
                             'allow_put': False,
                             'validate': {
                                 'type:string':
                                     providernet.PHYSICAL_NETWORK_MAX_LEN},
                             'default': constants.ATTR_NOT_SPECIFIED,
                             'is_filter': True,
                             'is_visible': True},
        'minimum': {'allow_post': True,
                    'allow_put': True,
                    'convert_to': converters.convert_to_int,
                    'validate': {'type:range': NETWORK_SEGMENT_RANGE_LIMIT},
                    'is_visible': True},
        'maximum': {'allow_post': True,
                    'allow_put': True,
                    'convert_to': converters.convert_to_int,
                    'validate': {'type:range': NETWORK_SEGMENT_RANGE_LIMIT},
                    'is_visible': True},
        'used': {'allow_post': False,
                 'allow_put': False,
                 'is_visible': True},
        'available': {'allow_post': False,
                      'allow_put': False,
                      'convert_to': converters.convert_none_to_empty_list,
                      'is_visible': True}
    }
}

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

# The subresource attribute map for the extension. It adds child resources
# to main extension's resource. The subresource map must have a parent and
# a parameters entry. If an extension does not need such a map, None can
# be specified (mandatory).
SUB_RESOURCE_ATTRIBUTE_MAP = {}

# The action map: it associates verbs with methods to be performed on
# the API resource.
ACTION_MAP = {}

# The list of required extensions.
REQUIRED_EXTENSIONS = [providernet.ALIAS]

# The list of optional extensions.
OPTIONAL_EXTENSIONS = []

# The action status.
ACTION_STATUS = {}
