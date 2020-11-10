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


# L3 Exceptions
class RouterNotFound(exceptions.NotFound):
    message = _("Router %(router_id)s could not be found")


class RouterInUse(exceptions.InUse):
    message = _("Router %(router_id)s %(reason)s")

    def __init__(self, **kwargs):
        if 'reason' not in kwargs:
            kwargs['reason'] = "still has ports"
        super().__init__(**kwargs)


class RouterInterfaceNotFound(exceptions.NotFound):
    message = _("Router %(router_id)s does not have "
                "an interface with id %(port_id)s")


class RouterInterfaceNotFoundForSubnet(exceptions.NotFound):
    message = _("Router %(router_id)s has no interface "
                "on subnet %(subnet_id)s")


class RouterInterfaceInUseByFloatingIP(exceptions.InUse):
    message = _("Router interface for subnet %(subnet_id)s on router "
                "%(router_id)s cannot be deleted, as it is required "
                "by one or more floating IPs.")


class FloatingIPNotFound(exceptions.NotFound):
    message = _("Floating IP %(floatingip_id)s could not be found")


class ExternalGatewayForFloatingIPNotFound(exceptions.NotFound):
    message = _("External network %(external_network_id)s is not reachable "
                "from subnet %(subnet_id)s.  Therefore, cannot associate "
                "Port %(port_id)s with a Floating IP.")


class FloatingIPPortAlreadyAssociated(exceptions.InUse):
    message = _("Cannot associate floating IP %(floating_ip_address)s "
                "(%(fip_id)s) with port %(port_id)s "
                "using fixed IP %(fixed_ip)s, as that fixed IP already "
                "has a floating IP on external network %(net_id)s.")


class RouterExternalGatewayInUseByFloatingIp(exceptions.InUse):
    message = _("Gateway cannot be updated for router %(router_id)s, since a "
                "gateway to external network %(net_id)s is required by one or "
                "more floating IPs.")


class RouterInterfaceAttachmentConflict(exceptions.Conflict):
    message = _("Error %(reason)s while attempting the operation.")


class RouterNotCompatibleWithAgent(exceptions.NeutronException):
    message = _("Router '%(router_id)s' is not compatible with this agent.")


class RouterNotFoundInRouterFactory(exceptions.NeutronException):
    message = _("Router '%(router_id)s' with features '%(features)s' could "
                "not be found in the router factory.")


class FloatingIpSetupException(exceptions.NeutronException):
    def __init__(self, message=None):
        self.message = message
        super().__init__()


class AbortSyncRouters(exceptions.NeutronException):
    message = _("Aborting periodic_sync_routers_task due to an error.")


class IpTablesApplyException(exceptions.NeutronException):
    def __init__(self, message=None):
        self.message = message
        super().__init__()
