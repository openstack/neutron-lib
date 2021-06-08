#    Copyright (c) 2021 Cloudification GmbH.  All rights reserved.
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
from neutron_lib.api.definitions import bgpvpn
from neutron_lib import constants


ALIAS = 'rbac-bgpvpn'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Add bgpvpn type to RBAC'
DESCRIPTION = 'Add bgpvpn type to RBAC'
UPDATED_TIMESTAMP = '2021-06-07T00:00:00-00:00'
API_PREFIX = bgpvpn.API_PREFIX
RESOURCE_NAME = bgpvpn.RESOURCE_NAME
COLLECTION_NAME = bgpvpn.COLLECTION_NAME
RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        constants.SHARED: {
            'allow_post': False,
            'allow_put': False,
            'default': False,
            'convert_to': converters.convert_to_boolean,
            'is_visible': True,
            'is_filter': True,
            'is_sort_key': True,
            'enforce_policy': True
        }
    },
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = ['rbac-policies', bgpvpn.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
