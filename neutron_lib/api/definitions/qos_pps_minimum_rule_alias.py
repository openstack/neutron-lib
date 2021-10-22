# Copyright (c) 2021 Ericsson Software Technology
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
from neutron_lib.api.definitions import qos
from neutron_lib.api.definitions import qos_pps_minimum_rule
from neutron_lib import constants
from neutron_lib.db import constants as db_const
from neutron_lib.services.qos import constants as qos_constants


MIN_PACKET_RATE_RULES_ALIAS = 'alias_minimum_packet_rate_rules'

ALIAS = 'qos-pps-minimum-rule-alias'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'QoS minimum packet rate rule alias'
API_PREFIX = '/' + qos.ALIAS
DESCRIPTION = ('API to enable GET, PUT and DELETE operations on QoS minimum '
               'packet rate rule without specifying policy ID')
UPDATED_TIMESTAMP = '2021-10-22T10:00:00-00:00'
RESOURCE_ATTRIBUTE_MAP = {
    MIN_PACKET_RATE_RULES_ALIAS: {
        **qos._QOS_RULE_COMMON_FIELDS,
        qos_constants.MIN_KPPS: {
                'allow_post': False,
                'allow_put': True,
                'convert_to': converters.convert_to_int,
                'is_visible': True,
                'is_filter': True,
                'is_sort_key': True,
                'validate': {
                    'type:range': [0, db_const.DB_INTEGER_MAX_VALUE]}
        },
        qos_constants.DIRECTION: {
            'allow_post': False,
            'allow_put': True,
            'is_visible': True,
            'default': constants.EGRESS_DIRECTION,
            'is_filter': True,
            'is_sort_key': True,
            'validate': {
                'type:values': constants.VALID_DIRECTIONS_AND_ANY,
            }
        }
    }
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = [qos.ALIAS, qos_pps_minimum_rule.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
