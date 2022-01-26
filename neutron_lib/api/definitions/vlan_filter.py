# Copyright (C) 2018 AT&T
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#

from neutron_lib.api.definitions import taas as taas_api_def

ALIAS = 'taas-vlan-filter'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = "VLAN filtering for Neutron Tap as a Service"
DESCRIPTION = "Neutron Tap as a Service Extension for filtering VLANs."
UPDATED_TIMESTAMP = "2018-01-14T10:00:00-00:00"
API_PREFIX = '/taas'
RESOURCE_NAME = 'tap_service'
COLLECTION_NAME = 'tap_services'
TAP_FLOW = 'tap_flow'
TAP_FLOWS = 'tap_flows'

# Regex for a comma-seperate list of integer values (VLANs)
# For ex. "9,18,27-36,45-54" or "0-4095" or "9,18,27,36"
RANGE_REGEX = r"^([0-9]+(-[0-9]+)?)(,([0-9]+(-[0-9]+)?))*$"

RESOURCE_ATTRIBUTE_MAP = {
    taas_api_def.TAP_FLOWS: {
        'vlan_filter': {'allow_post': True, 'allow_put': False,
                        'validate': {'type:regex_or_none': RANGE_REGEX},
                        'is_visible': True, 'default': None}
    }
}
SUB_RESOURCE_ATTRIBUTE_MAP = None
ACTION_MAP = {}
ACTION_STATUS = {}
REQUIRED_EXTENSIONS = [taas_api_def.ALIAS]
OPTIONAL_EXTENSIONS = []
