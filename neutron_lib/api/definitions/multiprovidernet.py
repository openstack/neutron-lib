# Copyright (c) 2013 OpenStack Foundation.
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
from neutron_lib.api.definitions import network
from neutron_lib.api import validators
from neutron_lib.api.validators import multiprovidernet as mp_validator
from neutron_lib import constants
from neutron_lib.exceptions import multiprovidernet as mp_exc


def check_duplicate_segments(segments, is_partial_func=None):
    """Helper function checking duplicate segments.

    If is_partial_funcs is specified and not None, then
    SegmentsContainDuplicateEntry is raised if two segments are identical and
    non partially defined (is_partial_func(segment) == False).
    Otherwise SegmentsContainDuplicateEntry is raised if two segment are
    identical.
    """
    if is_partial_func is not None:
        segments = [s for s in segments if not is_partial_func(s)]
    fully_specifieds = [tuple(sorted(s.items())) for s in segments]
    if len(set(fully_specifieds)) != len(fully_specifieds):
        raise mp_exc.SegmentsContainDuplicateEntry()


validators.add_validator(
    'network_segments', mp_validator.convert_and_validate_segments)

SEGMENTS = 'segments'

ALIAS = 'multi-provider'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Multi Provider Network'
API_PREFIX = ''
DESCRIPTION = ("Expose mapping of virtual networks to multiple physical "
               "networks")
UPDATED_TIMESTAMP = '2013-06-27T10:00:00-00:00'
RESOURCE_NAME = network.RESOURCE_NAME
COLLECTION_NAME = network.COLLECTION_NAME
RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        SEGMENTS: {
            'allow_post': True, 'allow_put': True,
            'validate': {'type:network_segments': None},
            'convert_list_to': converters.convert_kvp_list_to_dict,
            'default': constants.ATTR_NOT_SPECIFIED,
            'enforce_policy': True,
            'is_visible': True
        },
    }
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = []
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
