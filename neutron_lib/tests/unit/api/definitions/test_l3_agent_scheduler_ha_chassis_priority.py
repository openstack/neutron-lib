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

from neutron_lib.api.definitions import l3_agent_scheduler_ha_chassis_priority
from neutron_lib.tests.unit.api.definitions import test_agent as base


class L3AgentSchedulerHaPriorityDefinitionTestCase(
        base.AgentDefinitionTestCase):
    extension_module = l3_agent_scheduler_ha_chassis_priority
    extension_attributes: tuple[str, ...] = (
        l3_agent_scheduler_ha_chassis_priority.HA_CHASSIS_PRIORITY,
    )
