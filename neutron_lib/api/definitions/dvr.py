# Copyright (c) 2014 OpenStack Foundation.  All rights reserved.
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
from neutron_lib.api.definitions import l3
from neutron_lib import constants

DISTRIBUTED = 'distributed'

ALIAS = constants.L3_DISTRIBUTED_EXT_ALIAS
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Distributed Virtual Router'
API_PREFIX = ''
DESCRIPTION = 'Enables configuration of Distributed Virtual Routers.'
UPDATED_TIMESTAMP = '2014-06-1T10:00:00-00:00'
RESOURCE_NAME = l3.ROUTER
COLLECTION_NAME = l3.ROUTERS
RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        DISTRIBUTED: {'allow_post': True,
                      'allow_put': True,
                      'is_visible': True,
                      'default': constants.ATTR_NOT_SPECIFIED,
                      'convert_to': converters.convert_to_boolean_if_not_none,
                      'enforce_policy': True},
    }
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = [l3.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
