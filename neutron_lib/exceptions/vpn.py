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


# VPNaaS Exceptions
class VPNServiceNotFound(exceptions.NotFound):
    message = _("VPNService %(vpnservice_id)s could not be found")


class IPsecSiteConnectionNotFound(exceptions.NotFound):
    message = _("ipsec_site_connection %(ipsec_site_conn_id)s not found")


class IPsecSiteConnectionDpdIntervalValueError(exceptions.InvalidInput):
    message = _("ipsec_site_connection %(attr)s is "
                "equal to or less than dpd_interval")


class IPsecSiteConnectionMtuError(exceptions.InvalidInput):
    message = _("ipsec_site_connection MTU %(mtu)d is too small "
                "for ipv%(version)s")


class IPsecSiteConnectionPeerCidrError(exceptions.InvalidInput):
    message = _("ipsec_site_connection peer cidr %(peer_cidr)s is "
                "invalid CIDR")


class IKEPolicyNotFound(exceptions.NotFound):
    message = _("IKEPolicy %(ikepolicy_id)s could not be found")


class IPsecPolicyNotFound(exceptions.NotFound):
    message = _("IPsecPolicy %(ipsecpolicy_id)s could not be found")


class IKEPolicyInUse(exceptions.InUse):
    message = _("IKEPolicy %(ikepolicy_id)s is in use by existing "
                "IPsecSiteConnection and can't be updated or deleted")


class VPNServiceInUse(exceptions.InUse):
    message = _("VPNService %(vpnservice_id)s is still in use")


class SubnetInUseByVPNService(exceptions.InUse):
    message = _("Subnet %(subnet_id)s is used by VPNService %(vpnservice_id)s")


class SubnetInUseByEndpointGroup(exceptions.InUse):
    message = _("Subnet %(subnet_id)s is used by endpoint group %(group_id)s")


class SubnetInUseByIPsecSiteConnection(exceptions.InUse):
    message = _("Subnet %(subnet_id)s is used by ipsec site connection "
                "%(ipsec_site_connection_id)s")


class VPNStateInvalidToUpdate(exceptions.BadRequest):
    message = _("Invalid state %(state)s of vpnaas resource %(id)s "
                "for updating")


class IPsecPolicyInUse(exceptions.InUse):
    message = _("IPsecPolicy %(ipsecpolicy_id)s is in use by existing "
                "IPsecSiteConnection and can't be updated or deleted")


class DeviceDriverImportError(exceptions.NeutronException):
    message = _("Can not load driver :%(device_driver)s")


class SubnetIsNotConnectedToRouter(exceptions.BadRequest):
    message = _("Subnet %(subnet_id)s is not "
                "connected to Router %(router_id)s")


class RouterIsNotExternal(exceptions.BadRequest):
    message = _("Router %(router_id)s has no external network gateway set")


class VPNPeerAddressNotResolved(exceptions.InvalidInput):
    message = _("Peer address %(peer_address)s cannot be resolved")


class ExternalNetworkHasNoSubnet(exceptions.BadRequest):
    message = _("Router's %(router_id)s external network has "
                "no %(ip_version)s subnet")


# VPN Endpoint Group Exceptions
class VPNEndpointGroupNotFound(exceptions.NotFound):
    message = _("Endpoint group %(endpoint_group_id)s could not be found")


class InvalidEndpointInEndpointGroup(exceptions.InvalidInput):
    message = _("Endpoint '%(endpoint)s' is invalid for group "
                "type '%(group_type)s': %(why)s")


class MissingEndpointForEndpointGroup(exceptions.BadRequest):
    message = _("No endpoints specified for endpoint group '%(group)s'")


class NonExistingSubnetInEndpointGroup(exceptions.InvalidInput):
    message = _("Subnet %(subnet)s in endpoint group does not exist")


class MixedIPVersionsForIPSecEndpoints(exceptions.BadRequest):
    message = _("Endpoints in group %(group)s do not have the same IP "
                "version, as required for IPSec site-to-site connection")


class MixedIPVersionsForPeerCidrs(exceptions.BadRequest):
    message = _("Peer CIDRs do not have the same IP version, as required "
                "for IPSec site-to-site connection")


class MixedIPVersionsForIPSecConnection(exceptions.BadRequest):
    message = _("IP versions are not compatible between peer and local "
                "endpoints")


class InvalidEndpointGroup(exceptions.BadRequest):
    message = _("Endpoint group%(suffix)s %(which)s cannot be specified, "
                "when VPN Service has subnet specified")


class WrongEndpointGroupType(exceptions.BadRequest):
    message = _("Endpoint group %(which)s type is '%(group_type)s' and "
                "should be '%(expected)s'")


class PeerCidrsInvalid(exceptions.BadRequest):
    message = _("Peer CIDRs cannot be specified, when using endpoint "
                "groups")


class MissingPeerCidrs(exceptions.BadRequest):
    message = _("Missing peer CIDRs for IPsec site-to-site connection")


class MissingRequiredEndpointGroup(exceptions.BadRequest):
    message = _("Missing endpoint group%(suffix)s %(which)s for IPSec "
                "site-to-site connection")


class EndpointGroupInUse(exceptions.BadRequest):
    message = _("Endpoint group %(group_id)s is in use and cannot be deleted")


# VPN Flavors Exceptions
class FlavorsPluginNotLoaded(exceptions.NotFound):
    message = _("Flavors plugin not found")


class NoProviderFoundForFlavor(exceptions.NotFound):
    message = _("No service provider found for flavor %(flavor_id)s")


# IPsec Service Driver Validator Exceptions
class IpsecValidationFailure(exceptions.BadRequest):
    message = _("IPSec does not support %(resource)s attribute %(key)s "
                "with value '%(value)s'")


class IkeValidationFailure(exceptions.BadRequest):
    message = _("IKE does not support %(resource)s attribute %(key)s "
                "with value '%(value)s'")


# Cisco Csr Driver Exceptions
class CsrInternalError(exceptions.NeutronException):
    message = _("Fatal - %(reason)s")


# Cisco CSR Driver Validator Exceptions
class CsrValidationFailure(exceptions.BadRequest):
    message = _("Cisco CSR does not support %(resource)s attribute %(key)s "
                "with value '%(value)s'")
