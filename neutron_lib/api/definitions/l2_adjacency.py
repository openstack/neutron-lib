# Copyright (c) 2016 NEC Technologies Ltd.
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

from neutron_lib.api.definitions import network


L2_ADJACENCY = 'l2_adjacency'

ALIAS = L2_ADJACENCY
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'L2 Adjacency'
API_PREFIX = ''
DESCRIPTION = 'Display L2 Adjacency for Neutron Networks.'
UPDATED_TIMESTAMP = '2016-04-12T16:00:00-00:00'
RESOURCE_NAME = network.RESOURCE_NAME
COLLECTION_NAME = network.COLLECTION_NAME
RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        L2_ADJACENCY: {
            'allow_post': False,
            'allow_put': False,
            'is_visible': True
        }
    }
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = []
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
