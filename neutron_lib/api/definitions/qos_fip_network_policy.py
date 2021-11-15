# Copyright (c) 2021 Red Hat Inc.
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

from neutron_lib.api.definitions import l3 as l3_apidef
from neutron_lib.api.definitions import qos as qos_apidef
from neutron_lib.api.definitions import qos_fip as qos_fip_apidef
from neutron_lib.services.qos import constants as qos_consts

ALIAS = 'qos-fip-network-policy'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'QoS floating IP network policy ID'
DESCRIPTION = 'Adds a the QoS network ID to the floating IP definition'
UPDATED_TIMESTAMP = '2021-11-15T10:00:00-00:00'
RESOURCE_ATTRIBUTE_MAP = {
    l3_apidef.FLOATINGIPS: {
        qos_consts.QOS_NETWORK_POLICY_ID: {
            'allow_post': False,
            'allow_put': False,
            'is_visible': True,
            'default': None
        }
    }
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = [l3_apidef.ALIAS, qos_apidef.ALIAS, qos_fip_apidef.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
