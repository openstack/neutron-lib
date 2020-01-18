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

import abc

from neutron_lib.agent import extension


class L3AgentExtension(extension.AgentExtension, metaclass=abc.ABCMeta):
    """Define stable abstract interface for l3 agent extensions.

    An agent extension extends the agent core functionality.
    """

    @abc.abstractmethod
    def add_router(self, context, data):
        """Handle a router add event.

        Called on router create.

        :param context: RPC context.
        :param data: Router data.
        """

    @abc.abstractmethod
    def update_router(self, context, data):
        """Handle a router update event.

        Called on router update.

        :param context: RPC context.
        :param data: Router data.
        """

    @abc.abstractmethod
    def delete_router(self, context, data):
        """Handle a router delete event.

        :param context: RPC context.
        :param data: Router data.
        """

    @abc.abstractmethod
    def ha_state_change(self, context, data):
        """Change router state from agent extension.

        Called on HA router state change.

        :param context: rpc context
        :param data: dict of router_id and new state
        """
