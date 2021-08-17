# Copyright (c) 2021 China Unicom Cloud Data Co.,Ltd.
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

import copy

from neutron_lib.api import converters
from neutron_lib.api.definitions import qos as qos_apidef
from neutron_lib.api.definitions import qos_bw_minimum_ingress
from neutron_lib import constants
from neutron_lib.db import constants as db_const
from neutron_lib.services.qos import constants as qos_const


ALIAS = 'qos-pps'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'QoS Rule Type Packet per Second Extension'
API_PREFIX = ''
DESCRIPTION = 'Add QoS Rule Type Packet per Second'
UPDATED_TIMESTAMP = '2021-05-12T10:00:00-00:00'
RESOURCE_ATTRIBUTE_MAP = {}
PACKET_RATE_LIMIT_RULES = 'packet_rate_limit_rules'
RESOURCE_NAME = 'packet_rate_limit_rule'
SUB_RES_ATTR_MAP = copy.deepcopy(
    qos_apidef.SUB_RESOURCE_ATTRIBUTE_MAP)
SUB_RES_ATTR_MAP.update({
    PACKET_RATE_LIMIT_RULES: {
        'parent': qos_apidef._PARENT,
        'parameters': dict(
            qos_apidef._QOS_RULE_COMMON_FIELDS,
            **{qos_const.MAX_KPPS: {
                'allow_post': True, 'allow_put': True,
                'convert_to': converters.convert_to_int,
                'is_visible': True,
                'is_filter': True,
                'is_sort_key': True,
                'validate': {
                    'type:range': [0, db_const.DB_INTEGER_MAX_VALUE]}
              },
              qos_const.MAX_BURST_KPPS: {
                'allow_post': True, 'allow_put': True,
                'is_visible': True, 'default': 0,
                'is_filter': True,
                'is_sort_key': True,
                'convert_to': converters.convert_to_int,
                'validate': {
                    'type:range': [0, db_const.DB_INTEGER_MAX_VALUE]}
              },
              qos_const.DIRECTION: {
                'allow_post': True,
                'allow_put': True,
                'is_visible': True,
                'is_filter': True,
                'is_sort_key': True,
                'default': constants.EGRESS_DIRECTION,
                'validate': {
                    'type:values': constants.VALID_DIRECTIONS}
              }
            }),
    }
})
SUB_RES_ATTR_MAP.update(
    qos_bw_minimum_ingress.SUB_RESOURCE_ATTRIBUTE_MAP)
SUB_RESOURCE_ATTRIBUTE_MAP = SUB_RES_ATTR_MAP
ACTION_MAP = {}
REQUIRED_EXTENSIONS = [qos_apidef.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
