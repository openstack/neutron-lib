# Copyright 2015-2016 Hewlett Packard Enterprise Development Company, LP
#
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
from neutron_lib.api.definitions import constants
from neutron_lib.api.definitions import l3
from neutron_lib.api.definitions import network

ALIAS = 'auto-allocated-topology'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Auto Allocated Topology Services'
API_PREFIX = ''
DESCRIPTION = 'Auto Allocated Topology Services.'
UPDATED_TIMESTAMP = '2016-01-01T00:00:00-00:00'
RESOURCE_NAME = 'auto_allocated_topology'
COLLECTION_NAME = 'auto_allocated_topologies'
RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        'id': {'allow_post': False, 'allow_put': False,
               'validate': {'type:uuid': None},
               'is_visible': True},
        'tenant_id': {'allow_post': False, 'allow_put': False,
                      'validate': {'type:uuid': None},
                      'is_visible': True},
    },
    network.COLLECTION_NAME: {
        constants.IS_DEFAULT: {
            'allow_post': True,
            'allow_put': True,
            'default': False,
            'is_filter': True,
            'is_visible': True,
            'convert_to': converters.convert_to_boolean,
            'enforce_policy': True,
            'required_by_policy': True}},
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = [l3.ALIAS, 'subnet_allocation', 'external-net']
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
