# Copyright (c) 2013 OpenStack Foundation.
# All Rights Reserved.
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


# For backward compatibility the 'router' prefix is kept.
EXTERNAL = 'router:external'

ALIAS = 'external-net'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Neutron external network'
API_PREFIX = ''
DESCRIPTION = 'Adds external network attribute to network resource.'
UPDATED_TIMESTAMP = '2013-01-14T10:00:00-00:00'
RESOURCE_NAME = network.RESOURCE_NAME
COLLECTION_NAME = network.COLLECTION_NAME
RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        EXTERNAL: {
            'allow_post': True,
            'allow_put': True,
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
REQUIRED_EXTENSIONS = []
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
