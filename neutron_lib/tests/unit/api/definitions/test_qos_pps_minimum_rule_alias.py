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

from neutron_lib.api.definitions import qos_pps_minimum_rule_alias as apidef
from neutron_lib.services.qos import constants as qos_constants
from neutron_lib.tests.unit.api.definitions import base


class QoSPPSMinimumRuleAliasDefinitionTestCase(base.DefinitionBaseTestCase):
    extension_module = apidef

    extension_resources = (apidef.MIN_PACKET_RATE_RULES_ALIAS,)
    extension_attributes = (qos_constants.MIN_KPPS, qos_constants.DIRECTION)
