# Copyright 2021 Red Hat, Inc.
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

from neutron_lib.api.definitions import l3 as l3_apidef
from neutron_lib.api.definitions import qos as qos_apidef
from neutron_lib.services.qos import constants as qos_consts

ALIAS = 'qos-fip'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Floating IP QoS'
API_PREFIX = ''
DESCRIPTION = 'The floating IP Quality of Service extension'
UPDATED_TIMESTAMP = '2017-07-20T00:00:00-00:00'
RESOURCE_ATTRIBUTE_MAP = {
    l3_apidef.FLOATINGIPS: {
        qos_consts.QOS_POLICY_ID: {
            'allow_post': True,
            'allow_put': True,
            'is_visible': True,
            'default': None,
            'enforce_policy': True,
            'validate': {'type:uuid_or_none': None}}
    }
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = [l3_apidef.ALIAS, qos_apidef.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
