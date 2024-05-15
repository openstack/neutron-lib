# Copyright (c) 2013 OpenStack Foundation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import typing

from neutron_lib.api import converters
from neutron_lib.db import constants

ALIAS = 'agent'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = ALIAS
API_PREFIX = ''
DESCRIPTION = 'The agent management extension.'
UPDATED_TIMESTAMP = '2013-02-03T10:00:00-00:00'
RESOURCE_NAME = ALIAS
COLLECTION_NAME = ALIAS + 's'
RESOURCE_ATTRIBUTE_MAP: dict[str, typing.Any] = {
    COLLECTION_NAME: {
        'id': {'allow_post': False, 'allow_put': False,
               'validate': {'type:uuid': None},
               'is_filter': True,
               'is_visible': True},
        'agent_type': {'allow_post': False, 'allow_put': False,
                       'is_filter': True, 'is_visible': True},
        'binary': {'allow_post': False, 'allow_put': False,
                   'is_filter': True, 'is_visible': True},
        'topic': {'allow_post': False, 'allow_put': False,
                  'is_filter': True, 'is_visible': True},
        'host': {'allow_post': False, 'allow_put': False,
                 'is_filter': True, 'is_visible': True},
        'admin_state_up': {'allow_post': False, 'allow_put': True,
                           'convert_to': converters.convert_to_boolean,
                           'is_filter': True,
                           'is_visible': True},
        'created_at': {'allow_post': False, 'allow_put': False,
                       'is_visible': True},
        'started_at': {'allow_post': False, 'allow_put': False,
                       'is_visible': True},
        'heartbeat_timestamp': {'allow_post': False, 'allow_put': False,
                                'is_visible': True},
        'alive': {'allow_post': False, 'allow_put': False,
                  'is_filter': True, 'is_visible': True},
        'configurations': {'allow_post': False, 'allow_put': False,
                           'is_visible': True},
        'description': {
            'allow_post': False, 'allow_put': True,
            'is_visible': True, 'is_filter': True,
            'validate': {
                'type:string_or_none': constants.DESCRIPTION_FIELD_SIZE}},
    }
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = []
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
