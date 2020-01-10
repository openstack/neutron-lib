# Copyright (c) 2019 Red Hat Inc.
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

from neutron_lib.api.definitions import port as port_apidef
from neutron_lib.api.definitions import qos as qos_apidef
from neutron_lib.services.qos import constants as qos_const

ALIAS = 'qos-port-network-policy'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'QoS port network policy ID'
DESCRIPTION = 'Adds a the QoS network ID to the port definition'
UPDATED_TIMESTAMP = '2019-11-01T10:00:00-00:00'
RESOURCE_ATTRIBUTE_MAP = {
    port_apidef.COLLECTION_NAME: {
        qos_const.QOS_NETWORK_POLICY_ID: {
            'allow_post': False,
            'allow_put': False,
            'is_visible': True,
            'default': None,
            'validate': {'type:uuid_or_none': None}
        }
    }
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = [qos_apidef.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
