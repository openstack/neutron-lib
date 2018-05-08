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

from neutron_lib.api.definitions import port


IP_ALLOCATION = 'ip_allocation'
IP_ALLOCATION_IMMEDIATE = 'immediate'
IP_ALLOCATION_DEFERRED = 'deferred'
IP_ALLOCATION_NONE = 'none'

ALIAS = 'ip_allocation'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'IP Allocation'
API_PREFIX = ''
DESCRIPTION = 'IP allocation extension.'
UPDATED_TIMESTAMP = '2016-06-10T23:00:00-00:00'
RESOURCE_NAME = port.RESOURCE_NAME
COLLECTION_NAME = port.COLLECTION_NAME
RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        IP_ALLOCATION: {
            'allow_post': False,
            'allow_put': False,
            'is_filter': True,
            'is_sort_key': True,
            'is_visible': True
        }
    }
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = []
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
