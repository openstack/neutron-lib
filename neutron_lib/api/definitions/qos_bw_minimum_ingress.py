# Copyright (c) 2018 Ericsson
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

from neutron_lib.api.definitions import qos as qos_apidef
from neutron_lib import constants
from neutron_lib.services.qos import constants as qos_constants


ALIAS = 'qos-bw-minimum-ingress'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Ingress direction for QoS minimum bandwidth rule'
DESCRIPTION = ("Allow to configure QoS minumum bandwidth rule with ingress "
               "direction.")
UPDATED_TIMESTAMP = '2018-07-09T10:00:00-00:00'
RESOURCE_ATTRIBUTE_MAP = {}
SUB_RESOURCE_ATTRIBUTE_MAP = {
    qos_apidef.MIN_BANDWIDTH_RULES: {
        'parameters': {
            qos_constants.DIRECTION: {
                'allow_post': True, 'allow_put': True,
                'is_visible': True, 'default': constants.EGRESS_DIRECTION,
                'is_filter': True,
                'is_sort_key': True,
                'validate': {
                    'type:values': constants.VALID_DIRECTIONS
                }
            }
        }
    }
}

ACTION_MAP = {}
REQUIRED_EXTENSIONS = [qos_apidef.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
