# Copyright 2013 VMware, Inc.
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

import copy
import typing

from neutron_lib.api import converters
from neutron_lib.api.definitions import l3


ALIAS = 'ext-gw-mode'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Neutron L3 Configurable external gateway mode'
API_PREFIX = ''
DESCRIPTION = ('Extension of the router abstraction for specifying whether '
               'SNAT should occur on the external gateway')
UPDATED_TIMESTAMP = '2013-03-28T10:00:00-00:00'
RESOURCE_NAME = l3.ROUTER
COLLECTION_NAME = l3.ROUTERS

routers: typing.Dict[str, typing.Any] = copy.deepcopy(
    l3.RESOURCE_ATTRIBUTE_MAP[COLLECTION_NAME]
)
routers[l3.EXTERNAL_GW_INFO]['validate']['type:dict_or_nodata'][
    'enable_snat'] = {
    'type:boolean': None,
    'required': False,
    'convert_to': converters.convert_to_boolean
}
RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: routers
}

SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = [l3.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
