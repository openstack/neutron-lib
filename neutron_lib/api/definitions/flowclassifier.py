# Copyright 2015 Futurewei. All rights reserved.
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
from neutron_lib import constants
from neutron_lib.db import constants as db_const

# The alias of the extension.
ALIAS = 'flow_classifier'

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
NAME = 'Flow Classifier'

# A prefix for API resources. An empty prefix means that the API is going
# to be exposed at the v2/ level as any other core resource.
API_PREFIX = '/sfc'

# The description of the extension.
DESCRIPTION = ("API for selection of packets to direct through service "
               "function chains")

# A timestamp of when the extension was last updated.
UPDATED_TIMESTAMP = "2015-10-05T10:00:00-00:00"


FC_SUPPORTED_ETHERTYPES = [constants.IPv4, constants.IPv6]


RESOURCE_NAME = 'flow_classifier'
COLLECTION_NAME = 'flow_classifiers'


# Attribute Map
RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        'id': {
            'allow_post': False, 'allow_put': False,
            'is_visible': True,
            'validate': {'type:uuid': None},
            'primary_key': True},
        'name': {
            'allow_post': True, 'allow_put': True,
            'is_visible': True, 'default': None,
            'validate': {'type:string': db_const.NAME_FIELD_SIZE},
            'convert_to': converters.convert_none_to_empty_string},
        'description': {
            'allow_post': True, 'allow_put': True,
            'is_visible': True, 'default': None,
            'validate': {'type:string': db_const.DESCRIPTION_FIELD_SIZE},
            'convert_to': converters.convert_none_to_empty_string},
        'tenant_id': {
            'allow_post': True, 'allow_put': False,
            'is_visible': True,
            'validate': {'type:string': db_const.PROJECT_ID_FIELD_SIZE},
            'required_by_policy': True},
        'ethertype': {
            'allow_post': True, 'allow_put': False,
            'is_visible': True, 'default': "IPv4",
            'default_overrides_none': True,
            'validate': {'type:values': FC_SUPPORTED_ETHERTYPES},
            'convert_to': converters.convert_uppercase_ip},
        'protocol': {
            'allow_post': True, 'allow_put': False,
            'is_visible': True, 'default': None,
            'convert_to': converters.convert_to_protocol},
        'source_port_range_min': {
            'allow_post': True, 'allow_put': False,
            'is_visible': True, 'default': None,
            'convert_to': converters.convert_to_int_if_not_none,
            'validate': {'type:range_or_none': [0, constants.PORT_MAX]}},
        'source_port_range_max': {
            'allow_post': True, 'allow_put': False,
            'is_visible': True, 'default': None,
            'convert_to': converters.convert_to_int_if_not_none,
            'validate': {'type:range_or_none': [0, constants.PORT_MAX]}},
        'destination_port_range_min': {
            'allow_post': True, 'allow_put': False,
            'is_visible': True, 'default': None,
            'convert_to': converters.convert_to_int_if_not_none,
            'validate': {'type:range_or_none': [0, constants.PORT_MAX]}},
        'destination_port_range_max': {
            'allow_post': True, 'allow_put': False,
            'is_visible': True, 'default': None,
            'convert_to': converters.convert_to_int_if_not_none,
            'validate': {'type:range_or_none': [0, constants.PORT_MAX]}},
        'source_ip_prefix': {
            'allow_post': True, 'allow_put': False,
            'is_visible': True, 'default': None,
            'validate': {'type:subnet_or_none': None}},
        'destination_ip_prefix': {
            'allow_post': True, 'allow_put': False,
            'is_visible': True, 'default': None,
            'validate': {'type:subnet_or_none': None}},
        'logical_source_port': {
            'allow_post': True, 'allow_put': False,
            'is_visible': True, 'default': None,
            'validate': {'type:uuid_or_none': None}},
        'logical_destination_port': {
            'allow_post': True, 'allow_put': False,
            'is_visible': True, 'default': None,
            'validate': {'type:uuid_or_none': None}},
        'l7_parameters': {
            # NOTE(tmorin): at this point, there is no clean way to extend
            # this attribute; it seems only used by GBP (by monkeypatching it
            # at runtime, see
            # http://codesearch.openstack.org/?q=AIM_FLC_L7_PARAMS)
            # So let's support the GBP fields by now, but consider that
            # future additions will need to happen via proper API extensions
            'allow_post': True, 'allow_put': False,
            'is_visible': True,
            'default': {}, 'default_overrides_none': True,
            'convert_to': converters.convert_none_to_empty_dict,
            'validate': {
                'type:dict': {
                    'logical_source_network': {
                        'default': None,
                        'type:uuid_or_none': None
                    },
                    'logical_destination_network': {
                        'default': None,
                        'type:uuid_or_none': None
                    }
                }
            }
        }
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
