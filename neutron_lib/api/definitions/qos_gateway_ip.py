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

from neutron_lib.api.definitions import l3
from neutron_lib.api.definitions import l3_ext_gw_mode
from neutron_lib.api.definitions import qos
from neutron_lib.services.qos import constants as qos_consts


ALIAS = 'qos-gateway-ip'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Router gateway IP QoS'
API_PREFIX = ''
DESCRIPTION = 'The Router gateway IP Quality of Service extension'
UPDATED_TIMESTAMP = '2018-02-24T00:00:00-00:00'
RESOURCE_NAME = l3.ROUTER
COLLECTION_NAME = l3.ROUTERS

routers: typing.Dict[str, typing.Any] = copy.deepcopy(
    l3_ext_gw_mode.RESOURCE_ATTRIBUTE_MAP[COLLECTION_NAME]
)
routers[l3.EXTERNAL_GW_INFO]['validate']['type:dict_or_nodata'][
    qos_consts.QOS_POLICY_ID] = {
    'type:uuid_or_none': None,
    'required': False
}
RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: routers
}

SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = [l3.ALIAS, qos.ALIAS, l3_ext_gw_mode.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
