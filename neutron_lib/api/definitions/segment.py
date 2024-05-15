# Copyright (c) 2016 Hewlett Packard Enterprise Development Company, L.P.
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

import typing

from neutron_lib.api import converters
from neutron_lib.api.definitions import provider_net
from neutron_lib.api.definitions import subnet
from neutron_lib import constants
from neutron_lib.db import constants as db_constants


SEGMENT_ID = 'segment_id'
NETWORK_TYPE = 'network_type'
PHYSICAL_NETWORK = 'physical_network'
SEGMENTATION_ID = 'segmentation_id'
NAME_LEN = db_constants.NAME_FIELD_SIZE
DESC_LEN = db_constants.DESCRIPTION_FIELD_SIZE

ALIAS = 'segment'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Segment'
API_PREFIX = ''
DESCRIPTION = 'Segments extension.'
UPDATED_TIMESTAMP = '2016-02-24T17:00:00-00:00'
RESOURCE_NAME = 'segment'
COLLECTION_NAME = RESOURCE_NAME + 's'
RESOURCE_ATTRIBUTE_MAP: dict[str, typing.Any] = {
    COLLECTION_NAME: {
        'id': {
            'allow_post': False,
            'allow_put': False,
            'validate': {
                'type:uuid': None
            },
            'is_filter': True,
            'is_sort_key': True,
            'is_visible': True,
            'primary_key': True
        },
        'tenant_id': {
            'allow_post': True,
            'allow_put': False,
            'validate': {
                'type:string': db_constants.PROJECT_ID_FIELD_SIZE
            },
            'is_visible': False},
        'network_id': {
            'allow_post': True,
            'allow_put': False,
            'validate': {
                'type:uuid': None
            },
            'is_filter': True,
            'is_sort_key': True,
            'is_visible': True
        },
        PHYSICAL_NETWORK: {
            'allow_post': True,
            'allow_put': False,
            'default': constants.ATTR_NOT_SPECIFIED,
            'validate': {
                'type:string': provider_net.PHYSICAL_NETWORK_MAX_LEN
            },
            'is_filter': True,
            'is_sort_key': True,
            'is_visible': True
        },
        NETWORK_TYPE: {
            'allow_post': True,
            'allow_put': False,
            'validate': {
                'type:string': provider_net.NETWORK_TYPE_MAX_LEN
            },
            'is_filter': True,
            'is_sort_key': True,
            'is_visible': True
        },
        SEGMENTATION_ID: {
            'allow_post': True,
            'allow_put': False,
            'default': constants.ATTR_NOT_SPECIFIED,
            'convert_to': converters.convert_to_int,
            'is_sort_key': True,
            'is_visible': True
        },
        'name': {
            'allow_post': True,
            'allow_put': True,
            'default': constants.ATTR_NOT_SPECIFIED,
            'validate': {
                'type:string_or_none': NAME_LEN
            },
            'is_filter': True,
            'is_sort_key': True,
            'is_visible': True
        }
    },
    subnet.COLLECTION_NAME: {
        SEGMENT_ID: {
            'allow_post': True,
            'allow_put': False,
            'default': None,
            'validate': {
                'type:uuid_or_none': None
            },
            'is_filter': True,
            'is_sort_key': True,
            'is_visible': True
        }
    }
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = [
    'standard-attr-description'
]
OPTIONAL_EXTENSIONS = [
    # Use string instead of constant to avoid circulated import
    'standard-attr-segment'
]
ACTION_STATUS = {}
