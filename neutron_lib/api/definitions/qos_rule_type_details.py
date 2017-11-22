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


DRIVERS = 'drivers'

ALIAS = 'qos-rule-type-details'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Details of QoS rule types'
API_PREFIX = ''
DESCRIPTION = ("Expose details about QoS rule types supported by loaded "
               "backend drivers")
UPDATED_TIMESTAMP = '2017-06-22T10:00:00-00:00'
RESOURCE_ATTRIBUTE_MAP = {
    qos_apidef.RULE_TYPES: {
        DRIVERS: {
            'allow_post': False,
            'allow_put': False,
            'is_visible': True
        }
    }
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = [qos_apidef.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
