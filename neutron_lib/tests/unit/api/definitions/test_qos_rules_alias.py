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

from neutron_lib.api.definitions import qos_rules_alias
from neutron_lib.services.qos import constants as q_const
from neutron_lib.tests.unit.api.definitions import base


class QoSRulesAliasDefinitionTestCase(base.DefinitionBaseTestCase):
    extension_module = qos_rules_alias
    extension_resources = (qos_rules_alias.BANDWIDTH_LIMIT_RULES_ALIAS,
                           qos_rules_alias.DSCP_MARKING_RULES_ALIAS,
                           qos_rules_alias.MIN_BANDWIDTH_RULES_ALIAS)
    extension_attributes = (q_const.DIRECTION,
                            q_const.MAX_BURST,
                            q_const.DSCP_MARK,
                            q_const.MIN_KBPS,
                            q_const.MAX_KBPS)
