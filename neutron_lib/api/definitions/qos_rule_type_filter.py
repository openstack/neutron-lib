# Copyright 2022 Red Hat, Inc.
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

from neutron_lib.api import converters
from neutron_lib.api.definitions import qos as qos_apidef
from neutron_lib import constants


ALIAS = 'qos-rule-type-filter'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Allow to filter the list of QoS rule types'
API_PREFIX = ''
DESCRIPTION = ('Allows to filter the QoS rule type list adding two new flags. '
               '"all_rules" prints all implemented QoS rule types.'
               '"all_supported" prints all supported QoS rule types by the '
               'loaded mechanism drivers')
UPDATED_TIMESTAMP = '2022-02-02T10:00:00-00:00'
QOS_RULE_TYPE_ALL_SUPPORTED = 'all_supported'
QOS_RULE_TYPE_ALL_RULES = 'all_rules'
RESOURCE_ATTRIBUTE_MAP = {
    qos_apidef.RULE_TYPES: {
        QOS_RULE_TYPE_ALL_RULES: {
            'allow_post': True, 'allow_put': True,
            'convert_to': converters.convert_to_boolean_if_not_none,
            'default': constants.ATTR_NOT_SPECIFIED,
            'is_filter': True,
            'is_visible': False
        },
        QOS_RULE_TYPE_ALL_SUPPORTED: {
            'allow_post': True, 'allow_put': True,
            'convert_to': converters.convert_to_boolean_if_not_none,
            'default': constants.ATTR_NOT_SPECIFIED,
            'is_filter': True,
            'is_visible': False
        }
    }
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = [qos_apidef.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
