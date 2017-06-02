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

###################################
# Agent extension related constants
###################################
# Extension driver type for Open vSwitch mech driver
OVS_EXTENSION_DRIVER = 'ovs'
# Extension driver type for Linux Bridge mech driver
LB_EXTENSION_DRIVER = 'linuxbridge'
# Extension driver type for macvtap mech driver
MACVTAP_EXTENSION_DRIVER = 'macvtap'
# Extension driver type for SR-IOV mech driver
SRIOV_EXTENSION_DRIVER = 'sriov'


# Agent states as detected by server, used to reply on agent's state report
# agent has just been registered
AGENT_NEW = 'new'
# agent is alive
AGENT_ALIVE = 'alive'
# agent has just returned to alive after being dead
AGENT_REVIVED = 'revived'
