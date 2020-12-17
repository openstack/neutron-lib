# Copyright (c) 2020 Red Hat, Inc.
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

from neutron_lib.api.definitions import port
from neutron_lib.db import constants


ALIAS = 'port-device-profile'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Port device profile'
DESCRIPTION = "Expose the port device profile (Cyborg)"
UPDATED_TIMESTAMP = "2020-12-17T10:00:00-00:00"
RESOURCE_NAME = port.RESOURCE_NAME
COLLECTION_NAME = port.COLLECTION_NAME
DEVICE_PROFILE = 'device_profile'

RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        DEVICE_PROFILE: {
            'allow_post': True,
            'allow_put': False,
            'validate': {
                'type:string_or_none': constants.DESCRIPTION_FIELD_SIZE},
            'default': None,
            'is_visible': True}
    },
}

SUB_RESOURCE_ATTRIBUTE_MAP = None
ACTION_MAP = {}
ACTION_STATUS = {}
REQUIRED_EXTENSIONS = []
OPTIONAL_EXTENSIONS = []
