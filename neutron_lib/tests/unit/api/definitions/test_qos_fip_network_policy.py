# Copyright (c) 2021 Red Hat Inc.
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

from neutron_lib.api.definitions import l3 as l3_apidef
from neutron_lib.api.definitions import qos_fip_network_policy
from neutron_lib.services.qos import constants as qos_const
from neutron_lib.tests.unit.api.definitions import base


class QosFipNetworkPolicyTestCase(base.DefinitionBaseTestCase):
    extension_module = qos_fip_network_policy
    extension_resources = (l3_apidef.FLOATINGIPS,)
    extension_attributes = (qos_const.QOS_NETWORK_POLICY_ID,)
