# Copyright (c) 2024 Red Hat Inc.
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
from neutron_lib.api.definitions import external_net as extnet_def
from neutron_lib.api.definitions import subnet as subnet_def


ALIAS = 'subnet-external-network'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Subnet belongs to an external network'
API_PREFIX = ''
DESCRIPTION = 'Informs if the subnet belongs to an external network'
UPDATED_TIMESTAMP = '2024-02-05T18:00:00-00:00'
RESOURCE_NAME = extnet_def.EXTERNAL  # 'router:external'

RESOURCE_ATTRIBUTE_MAP = {
    subnet_def.COLLECTION_NAME: {
        RESOURCE_NAME: {
            'allow_post': False,
            'allow_put': False,
            'default': False,
            'is_visible': True,
            'is_filter': True,
            'convert_to': converters.convert_to_boolean,
            'enforce_policy': True,
            'required_by_policy': True
        }
    }
}

SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
ACTION_STATUS = {}
REQUIRED_EXTENSIONS = [extnet_def.ALIAS]
OPTIONAL_EXTENSIONS = []
