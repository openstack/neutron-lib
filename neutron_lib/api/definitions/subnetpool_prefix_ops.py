# (c) Copyright 2019 SUSE LLC
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

from neutron_lib.api.definitions import subnetpool as subnetpool_def
from neutron_lib import constants

ALIAS = "subnetpool-prefix-ops"
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = "Subnet Pool Prefix Operations"
DESCRIPTION = "Provides support for adjusting the prefix list of subnet pools"
UPDATED_TIMESTAMP = "2019-02-08T10:00:00-00:00"


RESOURCE_ATTRIBUTE_MAP = {
}

# The subresource attribute map for the extension.  This extension has only
# top level resources, not child resources, so this is set to an empty dict.
SUB_RESOURCE_ATTRIBUTE_MAP = {
}

# The action map.
ACTION_MAP = {
    subnetpool_def.RESOURCE_NAME: {
        'add_prefixes': 'PUT',
        'remove_prefixes': 'PUT'
    }
}

# The action status.
ACTION_STATUS = {
}

# The list of required extensions.
REQUIRED_EXTENSIONS = [constants.SUBNET_ALLOCATION_EXT_ALIAS]

# The list of optional extensions.
OPTIONAL_EXTENSIONS = [
]
