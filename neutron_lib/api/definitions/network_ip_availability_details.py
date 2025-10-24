#  Copyright 2025 Samsung SDS. All Rights Reserved
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

from neutron_lib.api.definitions import network_ip_availability


IP_AVAILABILITY_DETAILS = "ip_availability_details"

ALIAS = 'network-ip-availability-details'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Network IP Availability Details Extension'
DESCRIPTION = ('Add ip_availability_details attribute to'
               ' network-ip-availabilities resource.')
UPDATED_TIMESTAMP = '2025-10-31T00:00:00-00:00'

RESOURCE_ATTRIBUTE_MAP = {
    network_ip_availability.RESOURCE_PLURAL: {
        IP_AVAILABILITY_DETAILS: {
            'allow_post': False, 'allow_put': False,
            'is_visible': True
        }
    }
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = [network_ip_availability.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
