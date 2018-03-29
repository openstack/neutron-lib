# Copyright (c) 2013 OpenStack Foundation.
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

from neutron_lib.api.definitions import agent as agent_apidef
from neutron_lib.api.definitions import network as net_apidef
from neutron_lib import constants


DHCP_NET = 'dhcp-network'
DHCP_NETS = DHCP_NET + 's'
DHCP_AGENT = 'dhcp-agent'
DHCP_AGENTS = DHCP_AGENT + 's'

ALIAS = constants.DHCP_AGENT_SCHEDULER_EXT_ALIAS
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'DHCP Agent Scheduler'
API_PREFIX = ''
DESCRIPTION = 'Schedule networks among dhcp agents'
UPDATED_TIMESTAMP = '2013-02-07T10:00:00-00:00'
RESOURCE_ATTRIBUTE_MAP = {}
SUB_RESOURCE_ATTRIBUTE_MAP = {
    DHCP_NETS: {
        'parent': {
            'collection_name': agent_apidef.COLLECTION_NAME,
            'member_name': agent_apidef.RESOURCE_NAME
        },
        'parameters': {
            'network_id': {
                'allow_post': True, 'allow_put': False,
                'default': constants.ATTR_NOT_SPECIFIED,
                'enforce_policy': True,
                'is_visible': True,
                'validate': {'type:uuid': None}
            }
        }
    },
    DHCP_AGENTS: {
        'parent': {
            'collection_name': net_apidef.COLLECTION_NAME,
            'member_name': net_apidef.RESOURCE_NAME
        },
        # NOTE(boden): the reference implementation only allows the index
        # operation for the agent exposed under the network resource
        'parameters': agent_apidef.RESOURCE_ATTRIBUTE_MAP[
            agent_apidef.COLLECTION_NAME]
    }
}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = [agent_apidef.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
