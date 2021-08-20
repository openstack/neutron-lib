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
from neutron_lib.api.definitions import qos as qos_apidef
from neutron_lib import constants
from neutron_lib.db import constants as db_const
from neutron_lib.services.qos import constants as qos_constants


ALIAS = 'qos-pps-minimum'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
RESOURCE_NAME = 'minimum_packet_rate_rule'
COLLECTION_NAME = RESOURCE_NAME + 's'
NAME = 'QoS minimum packet rate rule'
API_PREFIX = '/' + qos_apidef.ALIAS
DESCRIPTION = ("Allow to configure QoS minimum packet rate rule.")
UPDATED_TIMESTAMP = '2021-07-14T10:00:00-00:00'
RESOURCE_ATTRIBUTE_MAP = {}
SUB_RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        'parent': qos_apidef._PARENT,
        'parameters': {
            **qos_apidef._QOS_RULE_COMMON_FIELDS,
            qos_constants.MIN_KPPS: {
                'allow_post': True,
                'allow_put': True,
                'convert_to': converters.convert_to_int,
                'is_visible': True,
                'is_filter': True,
                'is_sort_key': True,
                'validate': {
                    'type:range': [0, db_const.DB_INTEGER_MAX_VALUE]}
            },
            qos_constants.DIRECTION: {
                'allow_post': True,
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
}

ACTION_MAP = {}
REQUIRED_EXTENSIONS = [qos_apidef.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
