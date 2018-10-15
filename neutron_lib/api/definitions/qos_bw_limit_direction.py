# Copyright (c) 2017 OVH SAS
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

from neutron_lib.api.definitions import qos as qos_apidef
from neutron_lib import constants
from neutron_lib.services.qos import constants as qos_const


ALIAS = 'qos-bw-limit-direction'
LABEL = ''
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Direction for QoS bandwidth limit rule'
API_PREFIX = ''
DESCRIPTION = ("Allow to configure QoS bandwidth limit rule with specific "
               "direction: ingress or egress")
UPDATED_TIMESTAMP = '2017-04-10T10:00:00-00:00'
RESOURCE_ATTRIBUTE_MAP = {}
SUB_RESOURCE_ATTRIBUTE_MAP = {
    # NOTE(boden): parameters is required here as BANDWIDTH_LIMIT_RULES is a
    # sub-resource extension itself
    qos_apidef.BANDWIDTH_LIMIT_RULES: {
        'parameters': {
            qos_const.DIRECTION: {
                'allow_post': True,
                'allow_put': True,
                'is_visible': True,
                'is_filter': True,
                'is_sort_key': True,
                'default': constants.EGRESS_DIRECTION,
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
