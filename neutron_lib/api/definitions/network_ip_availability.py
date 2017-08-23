# Copyright 2016 GoDaddy.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
#  implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

ALIAS = 'network-ip-availability'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Network IP Availability'
API_PREFIX = ''
DESCRIPTION = 'Provides IP availability data for each network and subnet.'
UPDATED_TIMESTAMP = '2015-09-24T00:00:00-00:00'
RESOURCE_NAME = "network_ip_availability"
RESOURCE_PLURAL = "network_ip_availabilities"
COLLECTION_NAME = RESOURCE_PLURAL.replace('_', '-')
RESOURCE_ATTRIBUTE_MAP = {
    RESOURCE_PLURAL: {
        'network_id': {
            'allow_post': False, 'allow_put': False,
            'is_visible': True
        },
        'network_name': {
            'allow_post': False, 'allow_put': False,
            'is_visible': True
        },
        'tenant_id': {
            'allow_post': False, 'allow_put': False,
            'is_visible': True
        },
        'total_ips': {
            'allow_post': False, 'allow_put': False,
            'is_visible': True
        },
        'used_ips': {
            'allow_post': False, 'allow_put': False,
            'is_visible': True
        },
        'subnet_ip_availability': {
            'allow_post': False, 'allow_put': False,
            'is_visible': True
        }
        # TODO(wwriverrat) Make composite attribute for subnet_ip_availability
    }
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = []
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
