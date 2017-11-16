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

from neutron_lib._i18n import _
from neutron_lib import exceptions
from neutron_lib.exceptions import agent as agent_exc


class InvalidDHCPAgent(agent_exc.AgentNotFound):
    message = _("Agent %(id)s is not a valid DHCP Agent or has been disabled.")


class NetworkHostedByDHCPAgent(exceptions.Conflict):
    message = _("The network %(network_id)s has been already hosted"
                " by the DHCP Agent %(agent_id)s.")


class NetworkNotHostedByDhcpAgent(exceptions.Conflict):
    message = _("The network %(network_id)s is not hosted"
                " by the DHCP Agent %(agent_id)s.")
