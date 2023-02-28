# Copyright (c) 2023 Ericsson Software Technology
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

from neutron_lib.api.definitions import port


ALIAS = 'port-hints'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Port hints'
DESCRIPTION = 'Backend specific port hints to allow backend specific tuning'
UPDATED_TIMESTAMP = '2023-01-01T00:00:00-00:00'
RESOURCE_NAME = port.RESOURCE_NAME
COLLECTION_NAME = port.COLLECTION_NAME
HINTS = 'hints'
HINTS_SPEC = {
    'type:dict_or_none': {'openvswitch': {
        'type:dict': {'other_config': {
            'type:dict': {'tx-steering': {
                'type:values': ['thread', 'hash']}}}}}}}

RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        HINTS: {
            'allow_post': True,
            'allow_put': True,
            'default': None,
            'enforce_policy': True,
            'is_visible': True,
            'validate': HINTS_SPEC,
        },
    },
}

SUB_RESOURCE_ATTRIBUTE_MAP = None
ACTION_MAP = {}
ACTION_STATUS = {}
REQUIRED_EXTENSIONS = []
OPTIONAL_EXTENSIONS = []
