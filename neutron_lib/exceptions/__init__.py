# Copyright 2011 VMware, Inc, 2015 A10 Networks, Inc
# All Rights Reserved.
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

"""
Neutron base exception handling.
"""

from oslo_utils import excutils

from neutron_lib._i18n import _


class NeutronException(Exception):
    """Base Neutron Exception.

    To correctly use this class, inherit from it and define
    a 'message' property. That message will get printf'd
    with the keyword arguments provided to the constructor.
    """
    message = _("An unknown exception occurred.")

    def __init__(self, **kwargs):
        try:
            super().__init__(self.message % kwargs)
            self.msg = self.message % kwargs
        except Exception:
            with excutils.save_and_reraise_exception() as ctxt:
                if not self.use_fatal_exceptions():
                    ctxt.reraise = False
                    # at least get the core message out if something happened
                    super().__init__(self.message)

    def __str__(self):
        return self.msg

    def use_fatal_exceptions(self):
        """Is the instance using fatal exceptions.

        :returns: Always returns False.
        """
        return False


class BadRequest(NeutronException):
    """An exception indicating a generic bad request for a said resource.

    A generic exception indicating a bad request for a specified resource.

    :param resource: The resource requested.
    :param msg: A message indicating why the request is bad.
    """
    message = _('Bad %(resource)s request: %(msg)s.')


class NotFound(NeutronException):
    """A generic not found exception."""
    pass


class Conflict(NeutronException):
    """A generic conflict exception."""
    pass


class NotAuthorized(NeutronException):
    """A generic not authorized exception."""
    message = _("Not authorized.")


class ServiceUnavailable(NeutronException):
    """A generic service unavailable exception."""
    message = _("The service is unavailable.")


class AdminRequired(NotAuthorized):
    """A not authorized exception indicating an admin is required.

    A specialization of the NotAuthorized exception that indicates and admin
    is required to carry out the operation or access a resource.

    :param reason: A message indicating additional details on why admin is
        required for the operation access.
    """
    message = _("User does not have admin privileges: %(reason)s.")


class ObjectNotFound(NotFound):
    """A not found exception indicating an identifiable object isn't found.

    A specialization of the NotFound exception indicating an object with a said
    ID doesn't exist.

    :param id: The ID of the (not found) object.
    """
    message = _("Object %(id)s not found.")


class NetworkNotFound(NotFound):
    """An exception indicating a network was not found.

    A specialization of the NotFound exception indicating a requested network
    could not be found.

    :param net_id: The UUID of the (not found) network requested.
    """
    message = _("Network %(net_id)s could not be found.")


class SubnetNotFound(NotFound):
    """An exception for a requested subnet that's not found.

    A specialization of the NotFound exception indicating a requested subnet
    could not be found.

    :param subnet_id: The UUID of the (not found) subnet that was requested.
    """
    message = _("Subnet %(subnet_id)s could not be found.")


class PortNotFound(NotFound):
    """An exception for a requested port that's not found.

    A specialization of the NotFound exception indicating a requested port
    could not be found.

    :param port_id: The UUID of the (not found) port that was requested.
    """
    message = _("Port %(port_id)s could not be found.")


class PortNotFoundOnNetwork(NotFound):
    """An exception for a requested port on a network that's not found.

    A specialization of the NotFound exception that indicates a specified
    port on a specified network doesn't exist.

    :param port_id: The UUID of the (not found) port that was requested.
    :param net_id: The UUID of the network that was requested for the port.
    """
    message = _("Port %(port_id)s could not be found "
                "on network %(net_id)s.")


class DeviceNotFoundError(NotFound):
    """An exception for a requested device that's not found.

    A specialization of the NotFound exception indicating a requested device
    could not be found.

    :param device_name: The name of the (not found) device that was requested.
    """
    message = _("Device '%(device_name)s' does not exist.")


class InUse(NeutronException):
    """A generic exception indicating a resource is already in use."""
    message = _("The resource is in use.")


class NetworkInUse(InUse):
    """An operational error indicating the network still has ports in use.

    A specialization of the InUse exception indicating a network operation was
    requested, but failed because there are still ports in use on the said
    network.

    :param net_id: The UUID of the network requested.
    """
    message = _("Unable to complete operation on network %(net_id)s. "
                "There are one or more ports still in use on the network.")


class SubnetInUse(InUse):
    """An operational error indicating a subnet is still in use.

    A specialization of the InUse exception indicating an operation failed
    on a subnet because the subnet is still in use.

    :param subnet_id: The UUID of the subnet requested.
    :param reason: Details on why the operation failed. If None, a default
        reason is used indicating one or more ports still have IP allocations
        on the subnet.
    """
    message = _("Unable to complete operation on subnet %(subnet_id)s: "
                "%(reason)s.")

    def __init__(self, **kwargs):
        if 'reason' not in kwargs:
            kwargs['reason'] = _("One or more ports have an IP allocation "
                                 "from this subnet")
        super().__init__(**kwargs)


class SubnetPoolInUse(InUse):
    """An operational error indicating a subnet pool is still in use.

    A specialization of the InUse exception indicating an operation failed
    on a subnet pool because it's still in use.

    :param subnet_pool_id: The UUID of the subnet pool requested.
    :param reason: Details on why the operation failed. If None a default
        reason is used indicating two or more concurrent subnets are allocated.
    """
    message = _("Unable to complete operation on subnet pool "
                "%(subnet_pool_id)s. %(reason)s.")

    def __init__(self, **kwargs):
        if 'reason' not in kwargs:
            kwargs['reason'] = _("Two or more concurrent subnets allocated")
        super().__init__(**kwargs)


class PortInUse(InUse):
    """An operational error indicating a requested port is already attached.

    A specialization of the InUse exception indicating an operation failed on
    a port because it already has an attached device.

    :param port_id: The UUID of the port requested.
    :param net_id: The UUID of the requested port's network.
    :param device_id: The UUID of the device already attached to the port.
    """
    message = _("Unable to complete operation on port %(port_id)s "
                "for network %(net_id)s. Port already has an attached "
                "device %(device_id)s.")


class ServicePortInUse(InUse):
    """An error indicating a service port can't be deleted.

    A specialization of the InUse exception indicating a requested service
    port can't be deleted via the APIs.

    :param port_id: The UUID of the port requested.
    :param reason: Details on why the operation failed.
    """
    message = _("Port %(port_id)s cannot be deleted directly via the "
                "port API: %(reason)s.")


class PortBound(InUse):
    """An operational error indicating a port is already bound.

    A specialization of the InUse exception indicating an operation can't
    complete because the port is already bound.

    :param port_id: The UUID of the port requested.
    :param vif_type: The VIF type associated with the bound port.
    :param old_mac: The old MAC address of the port.
    :param net_mac: The new MAC address of the port.
    """
    message = _("Unable to complete operation on port %(port_id)s, "
                "port is already bound, port type: %(vif_type)s, "
                "old_mac %(old_mac)s, new_mac %(new_mac)s.")


class PortBoundNUMAAffinityPolicy(InUse):
    """An operational error indicating a port is already bound.

    NUMA affinity policy cannot be modified when the port is bound.

    :param port_id: The UUID of the port requested.
    :param host_id: The host ID where the port is bound.
    :param numa_affinity_policy: value passed to be updated.
    """
    message = _("Unable to complete operation on port %(port_id)s, "
                "port is already bound to host %(host_id)s, "
                "numa_affinity_policy value given %(numa_affinity_policy)s.")


class MacAddressInUse(InUse):
    """An network operational error indicating a MAC address is already in use.

    A specialization of the InUse exception indicating an operation failed
    on a network because a specified MAC address is already in use on that
    network.

    :param net_id: The UUID of the network.
    :param mac: The requested MAC address that's already in use.
    """
    message = _("Unable to complete operation for network %(net_id)s. "
                "The mac address %(mac)s is in use.")


class InvalidIpForNetwork(BadRequest):
    """An exception indicating an invalid IP was specified for a network.

    A specialization of the BadRequest exception indicating a specified IP
    address is invalid for a network.

    :param ip_address: The IP address that's invalid on the network.
    """
    message = _("IP address %(ip_address)s is not a valid IP "
                "for any of the subnets on the specified network.")


class InvalidIpForSubnet(BadRequest):
    """An exception indicating an invalid IP was specified for a subnet.

    A specialization of the BadRequest exception indicating a specified IP
    address is invalid for a subnet.

    :param ip_address: The IP address that's invalid on the subnet.
    """
    message = _("IP address %(ip_address)s is not a valid IP "
                "for the specified subnet.")


class IpAddressInUse(InUse):
    """An network operational error indicating an IP address is already in use.

    A specialization of the InUse exception indicating an operation can't
    complete because an IP address is in use.

    :param net_id: The UUID of the network.
    :param ip_address: The IP address that's already in use on the network.
    """
    message = _("Unable to complete operation for network %(net_id)s. "
                "The IP address %(ip_address)s is in use.")


class VlanIdInUse(InUse):
    """A network operational error indicating a VLAN ID is already in use.

    A specialization of the InUse exception indicating network creation failed
    because a specified VLAN is already in use on the physical network.

    :param vlan_id: The VLAN ID.
    :param physical_network: The physical network.
    """
    message = _("Unable to create the network. "
                "The VLAN %(vlan_id)s on physical network "
                "%(physical_network)s is in use.")


class TunnelIdInUse(InUse):
    """A network creation failure due to tunnel ID already in use.

    A specialization of the InUse exception indicating network creation failed
    because a said tunnel ID is already in use.

    :param tunnel_id: The ID of the tunnel that's already in use.
    """
    message = _("Unable to create the network. "
                "The tunnel ID %(tunnel_id)s is in use.")


class ResourceExhausted(ServiceUnavailable):
    """A service unavailable error indicating a resource is exhausted."""
    pass


class NoNetworkAvailable(ResourceExhausted):
    """A failure to create a network due to no tenant networks for allocation.

    A specialization of the ResourceExhausted exception indicating network
    creation failed because no tenant network are available for allocation.
    """
    message = _("Unable to create the network. "
                "No tenant network is available for allocation.")


class SubnetMismatchForPort(BadRequest):
    """A bad request error indicating a specified subnet isn't on a port.

    A specialization of the BadRequest exception indicating a subnet on a port
    doesn't match a specified subnet.

    :param port_id: The UUID of the port.
    :param subnet_id: The UUID of the requested subnet.
    """
    message = _("Subnet on port %(port_id)s does not match "
                "the requested subnet %(subnet_id)s.")


class Invalid(NeutronException):
    """A generic base class for invalid errors."""
    def __init__(self, message=None):
        self.message = message
        super().__init__()


class InvalidInput(BadRequest):
    """A bad request due to invalid input.

    A specialization of the BadRequest error indicating bad input was
    specified.

    :param error_message: Details on the operation that failed due to bad
        input.
    """
    message = _("Invalid input for operation: %(error_message)s.")


class IpAddressGenerationFailure(Conflict):
    """A conflict error due to no more IP addresses on a said network.

    :param net_id: The UUID of the network that has no more IP addresses.
    """
    message = _("No more IP addresses available on network %(net_id)s.")


class PreexistingDeviceFailure(NeutronException):
    """A creation error due to an already existing device.

    An exception indication creation failed due to an already existing
    device.

    :param dev_name: The device name that already exists.
    """
    message = _("Creation failed. %(dev_name)s already exists.")


class OverQuota(Conflict):
    """A error due to exceeding quota limits.

    A specialization of the Conflict exception indicating quota has been
    exceeded.

    :param overs: The resources that have exceeded quota.
    """
    message = _("Quota exceeded for resources: %(overs)s.")


class InvalidContentType(NeutronException):
    """An error due to invalid content type.

    :param content_type: The invalid content type.
    """
    message = _("Invalid content type %(content_type)s.")


class ExternalIpAddressExhausted(BadRequest):
    """An error due to not finding IP addresses on an external network.

    A specialization of the BadRequest exception indicating no IP addresses
    can be found on a network.

    :param net_id: The UUID of the network.
    """
    message = _("Unable to find any IP address on external "
                "network %(net_id)s.")


class InvalidConfigurationOption(NeutronException):
    """An error due to an invalid configuration option value.

    :param opt_name: The name of the configuration option that has an invalid
        value.
    :param opt_value: The value that's invalid for the configuration option.
    """
    message = _("An invalid value was provided for %(opt_name)s: "
                "%(opt_value)s.")


class NetworkTunnelRangeError(NeutronException):
    """An error due to an invalid network tunnel range.

    An exception indicating an invalid network tunnel range was specified.

    :param tunnel_range: The invalid tunnel range. If specified in the
        start:end' format, they will be converted automatically.
    :param error: Additional details on why the range is invalid.
    """
    message = _("Invalid network tunnel range: "
                "'%(tunnel_range)s' - %(error)s.")

    def __init__(self, **kwargs):
        # Convert tunnel_range tuple to 'start:end' format for display
        if isinstance(kwargs['tunnel_range'], tuple):
            kwargs['tunnel_range'] = "%d:%d" % kwargs['tunnel_range']
        super().__init__(**kwargs)


class PolicyInitError(NeutronException):
    """An error due to policy initialization failure.

    :param policy: The policy that failed to initialize.
    :param reason: Details on why the policy failed to initialize.
    """
    message = _("Failed to initialize policy %(policy)s because %(reason)s.")


class PolicyCheckError(NeutronException):
    """An error due to a policy check failure.

    :param policy: The policy that failed to check.
    :param reason: Additional details on the failure.
    """
    message = _("Failed to check policy %(policy)s because %(reason)s.")


class MultipleExceptions(Exception):
    """Container for multiple exceptions encountered.

    The API layer of Neutron will automatically unpack, translate,
    filter, and combine the inner exceptions in any exception derived
    from this class.
    """

    def __init__(self, exceptions, *args, **kwargs):
        """Create a new instance wrapping the exceptions.

        :param exceptions: The inner exceptions this instance is composed of.
        :param args: Passed onto parent constructor.
        :param kwargs: Passed onto parent constructor.
        """
        super().__init__(*args, **kwargs)
        self.inner_exceptions = exceptions


class HostMacAddressGenerationFailure(ServiceUnavailable):
    """MAC address generation failure for a host.

    :param host: The host MAC address generation failed for.
    """
    message = _("Unable to generate unique mac for host %(host)s.")


class NetworkMacAddressGenerationFailure(ServiceUnavailable):
    """An error related to MAC address generation on a network.

        :param net_id: The ID of the network MAC address generation failed on.
        """
    message = _("Unable to generate unique mac on network %(net_id)s.")


class InvalidServiceType(InvalidInput):
    """An error due to an invalid service type.

    :param service_type: The service type that's invalid.
    """
    message = _("Invalid service type: %(service_type)s.")


class NetworkVlanRangeError(NeutronException):
    message = _("Invalid network VLAN range: '%(vlan_range)s' - '%(error)s'.")

    def __init__(self, **kwargs):
        # Convert vlan_range tuple to 'start:end' format for display
        if isinstance(kwargs['vlan_range'], tuple):
            kwargs['vlan_range'] = "%d:%d" % kwargs['vlan_range']
        super().__init__(**kwargs)


class PhysicalNetworkNameError(NeutronException):
    message = _("Empty physical network name.")


class TenantIdProjectIdFilterConflict(BadRequest):
    message = _("Both tenant_id and project_id passed as filters.")


class SubnetPoolNotFound(NotFound):
    message = _("Subnet pool %(subnetpool_id)s could not be found.")


class StateInvalid(BadRequest):
    message = _("Unsupported port state: %(port_state)s.")


class DhcpPortInUse(InUse):
    message = _("Port %(port_id)s is already acquired by another DHCP agent")


class HostRoutesExhausted(BadRequest):
    # NOTE(xchenum): probably make sense to use quota exceeded exception?
    message = _("Unable to complete operation for %(subnet_id)s. "
                "The number of host routes exceeds the limit %(quota)s.")


class DNSNameServersExhausted(BadRequest):
    # NOTE(xchenum): probably make sense to use quota exceeded exception?
    message = _("Unable to complete operation for %(subnet_id)s. "
                "The number of DNS nameservers exceeds the limit %(quota)s.")


class FlatNetworkInUse(InUse):
    message = _("Unable to create the flat network. "
                "Physical network %(physical_network)s is in use.")


class NoNetworkFoundInMaximumAllowedAttempts(ServiceUnavailable):
    message = _("Unable to create the network. "
                "No available network found in maximum allowed attempts.")


class MalformedRequestBody(BadRequest):
    message = _("Malformed request body: %(reason)s.")


class InvalidAllocationPool(BadRequest):
    message = _("The allocation pool %(pool)s is not valid.")


class UnsupportedPortDeviceOwner(Conflict):
    message = _("Operation %(op)s is not supported for device_owner "
                "%(device_owner)s on port %(port_id)s.")


class OverlappingAllocationPools(Conflict):
    message = _("Found overlapping allocation pools: "
                "%(pool_1)s %(pool_2)s for subnet %(subnet_cidr)s.")


class OutOfBoundsAllocationPool(BadRequest):
    message = _("The allocation pool %(pool)s spans "
                "beyond the subnet cidr %(subnet_cidr)s.")


class BridgeDoesNotExist(NeutronException):
    message = _("Bridge %(bridge)s does not exist.")


class QuotaResourceUnknown(NotFound):
    message = _("Unknown quota resources %(unknown)s.")


class QuotaMissingTenant(BadRequest):
    message = _("Tenant-id was missing from quota request.")


class InvalidQuotaValue(Conflict):
    message = _("Change would make usage less than 0 for the following "
                "resources: %(unders)s.")


class InvalidSharedSetting(Conflict):
    message = _("Unable to reconfigure sharing settings for network "
                "%(network)s. Multiple tenants are using it.")


class ExtensionsNotFound(NotFound):
    message = _("Extensions not found: %(extensions)s.")


class GatewayConflictWithAllocationPools(InUse):
    message = _("Gateway ip %(ip_address)s conflicts with "
                "allocation pool %(pool)s.")


class GatewayIpInUse(InUse):
    message = _("Current gateway ip %(ip_address)s already in use "
                "by port %(port_id)s. Unable to update.")


class NetworkVxlanPortRangeError(NeutronException):
    message = _("Invalid network VXLAN port range: '%(vxlan_range)s'.")


class VxlanNetworkUnsupported(NeutronException):
    message = _("VXLAN network unsupported.")


class DuplicatedExtension(NeutronException):
    message = _("Found duplicate extension: %(alias)s.")


class DriverCallError(MultipleExceptions):
    def __init__(self, exc_list=None):
        super().__init__(exc_list or [])


class DeviceIDNotOwnedByTenant(Conflict):
    message = _("The following device_id %(device_id)s is not owned by your "
                "tenant or matches another tenants router.")


class InvalidCIDR(BadRequest):
    message = _("Invalid CIDR %(input)s given as IP prefix.")


class FailToDropPrivilegesExit(SystemExit):
    """Exit exception raised when a drop privileges action fails."""
    code = 99


class NetworkIdOrRouterIdRequiredError(NeutronException):
    message = _('Both network_id and router_id are None. '
                'One must be provided.')


class EmptySubnetPoolPrefixList(BadRequest):
    message = _("Empty subnet pool prefix list.")


class PrefixVersionMismatch(BadRequest):
    message = _("Cannot mix IPv4 and IPv6 prefixes in a subnet pool.")


class UnsupportedMinSubnetPoolPrefix(BadRequest):
    message = _("Prefix '%(prefix)s' not supported in IPv%(version)s pool.")


class IllegalSubnetPoolPrefixBounds(BadRequest):
    message = _("Illegal prefix bounds: %(prefix_type)s=%(prefixlen)s, "
                "%(base_prefix_type)s=%(base_prefixlen)s.")


class IllegalSubnetPoolPrefixUpdate(BadRequest):
    message = _("Illegal update to prefixes: %(msg)s.")


class SubnetAllocationError(NeutronException):
    message = _("Failed to allocate subnet: %(reason)s.")


class AddressScopePrefixConflict(Conflict):
    message = _("Failed to associate address scope: subnetpools "
                "within an address scope must have unique prefixes.")


class IllegalSubnetPoolAssociationToAddressScope(BadRequest):
    message = _("Illegal subnetpool association: subnetpool %(subnetpool_id)s "
                "cannot be associated with address scope "
                "%(address_scope_id)s.")


class IllegalSubnetPoolIpVersionAssociationToAddressScope(BadRequest):
    message = _("Illegal subnetpool association: subnetpool %(subnetpool_id)s "
                "cannot associate with address scope %(address_scope_id)s "
                "because subnetpool ip_version is not %(ip_version)s.")


class IllegalSubnetPoolUpdate(BadRequest):
    message = _("Illegal subnetpool update : %(reason)s.")


class MinPrefixSubnetAllocationError(BadRequest):
    message = _("Unable to allocate subnet with prefix length %(prefixlen)s, "
                "minimum allowed prefix is %(min_prefixlen)s.")


class MaxPrefixSubnetAllocationError(BadRequest):
    message = _("Unable to allocate subnet with prefix length %(prefixlen)s, "
                "maximum allowed prefix is %(max_prefixlen)s.")


class SubnetPoolDeleteError(BadRequest):
    message = _("Unable to delete subnet pool: %(reason)s.")


class SubnetPoolQuotaExceeded(OverQuota):
    message = _("Per-tenant subnet pool prefix quota exceeded.")


class NetworkSubnetPoolAffinityError(BadRequest):
    message = _("Subnets hosted on the same network must be allocated from "
                "the same subnet pool.")


class ObjectActionError(NeutronException):
    message = _('Object action %(action)s failed because: %(reason)s.')


class CTZoneExhaustedError(NeutronException):
    message = _("IPtables conntrack zones exhausted, iptables rules cannot "
                "be applied.")


class TenantQuotaNotFound(NotFound):
    message = _("Quota for tenant %(tenant_id)s could not be found.")


class MultipleFilterIDForIPFound(Conflict):
    message = _("Multiple filter IDs for IP %(ip)s found.")


class FilterIDForIPNotFound(NotFound):
    message = _("Filter ID for IP %(ip)s could not be found.")


class FailedToAddQdiscToDevice(NeutronException):
    message = _("Failed to add %(direction)s qdisc "
                "to device %(device)s.")


class PortBindingNotFound(NotFound):
    message = _("Binding for port %(port_id)s for host %(host)s could not be "
                "found.")


class PortBindingAlreadyActive(Conflict):
    message = _("Binding for port %(port_id)s on host %(host)s is already "
                "active.")


class PortBindingAlreadyExists(Conflict):
    message = _("Binding for port %(port_id)s on host %(host)s already "
                "exists.")


class PortBindingError(NeutronException):
    message = _("Binding for port %(port_id)s on host %(host)s could not be "
                "created or updated.")


class ProcessExecutionError(RuntimeError):
    def __init__(self, message, returncode):
        super().__init__(message)
        self.returncode = returncode


class InvalidSubnetServiceType(InvalidInput):
    message = _("Subnet service type %(service_type)s does not correspond "
                "to a valid device owner.")


class InvalidInputSubnetServiceType(InvalidInput):
    message = _("Subnet service type %(service_type)s is not a string.")
