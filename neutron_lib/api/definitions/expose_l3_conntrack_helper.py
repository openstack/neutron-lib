# Copyright (c) 2019 OpenStack Foundation
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

from neutron_lib.api.definitions import l3
from neutron_lib.api.definitions import l3_conntrack_helper

ALIAS = "expose-l3-conntrack-helper"
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Expose CT target rules for conntrack helper'
API_PREFIX = ''
DESCRIPTION = 'Expose allow adding CT target rules for conntrack helper'
UPDATED_TIMESTAMP = '2019-04-04T10:00:00-00:00'
RESOURCE_NAME = l3.ROUTER
COLLECTION_NAME = l3.ROUTERS
RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        l3_conntrack_helper.COLLECTION_NAME: {
            'allow_post': False,
            'allow_put': False,
            'is_visible': True,
            'default': None
        }
    }
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = [l3.ALIAS, l3_conntrack_helper.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
