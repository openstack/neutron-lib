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
from neutron_lib.api.definitions import agent
from neutron_lib import constants


ALIAS = 'l3-agent-scheduler-ha-chassis-priority'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'L3 Agent Scheduler HA Chassis Priority'
API_PREFIX = ''
DESCRIPTION = ('Exposes the HA_Chassis priority in the L3 Agent Scheduler '
               'API responses and allows setting priority when scheduling '
               'a router to a chassis.')
UPDATED_TIMESTAMP = '2026-03-31T00:00:00-00:00'
RESOURCE_NAME = agent.RESOURCE_NAME
COLLECTION_NAME = agent.COLLECTION_NAME
HA_CHASSIS_PRIORITY = 'ha_chassis_priority'

RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        HA_CHASSIS_PRIORITY: {
            'allow_post': True,
            'allow_put': True,
            'default': constants.ATTR_NOT_SPECIFIED,
            'is_visible': True,
            'convert_to': converters.convert_to_int_if_not_none,
            'enforce_policy': True,
        }
    }
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
ACTION_STATUS = {}
REQUIRED_EXTENSIONS = [
    agent.ALIAS,
    constants.L3_AGENT_SCHEDULER_EXT_ALIAS,
]
OPTIONAL_EXTENSIONS = []
