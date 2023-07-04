# Copyright (c) 2023 Red Hat, Inc.
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
from neutron_lib.api.definitions import port
from neutron_lib import constants


ALIAS = 'port-hardware-offload-type'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Port hardware offload'
DESCRIPTION = "Expose port hardware offload extension"
UPDATED_TIMESTAMP = "2023-05-09T10:00:00-00:00"
RESOURCE_NAME = port.RESOURCE_NAME
COLLECTION_NAME = port.COLLECTION_NAME
HARDWARE_OFFLOAD_TYPE = 'hardware_offload_type'

RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        HARDWARE_OFFLOAD_TYPE: {
            'allow_post': True,
            'allow_put': False,
            'convert_to': converters.convert_to_string,
            'enforce_policy': True,
            'required_by_policy': False,
            'default': constants.ATTR_NOT_SPECIFIED,
            'is_visible': True,
            'validate': {
                'type:values': constants.VALID_HWOL_TYPES}
            }
    },
}

SUB_RESOURCE_ATTRIBUTE_MAP = None
ACTION_MAP = {}
ACTION_STATUS = {}
REQUIRED_EXTENSIONS = []
OPTIONAL_EXTENSIONS = []
