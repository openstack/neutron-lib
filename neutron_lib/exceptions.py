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
import six

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
            super(NeutronException, self).__init__(self.message % kwargs)
            self.msg = self.message % kwargs
        except Exception:
            with excutils.save_and_reraise_exception() as ctxt:
                if not self.use_fatal_exceptions():
                    ctxt.reraise = False
                    # at least get the core message out if something happened
                    super(NeutronException, self).__init__(self.message)

    if six.PY2:
        def __unicode__(self):
            return unicode(self.msg)

    def __str__(self):
        return self.msg

    def use_fatal_exceptions(self):
        return False


class BadRequest(NeutronException):
    message = _('Bad %(resource)s request: %(msg)s.')


class NotFound(NeutronException):
    pass


class Conflict(NeutronException):
    pass


class NotAuthorized(NeutronException):
    message = _("Not authorized.")


class ServiceUnavailable(NeutronException):
    message = _("The service is unavailable.")


class AdminRequired(NotAuthorized):
    message = _("User does not have admin privileges: %(reason)s.")


class ObjectNotFound(NotFound):
    message = _("Object %(id)s not found.")


class NetworkNotFound(NotFound):
    message = _("Network %(net_id)s could not be found.")


class SubnetNotFound(NotFound):
    message = _("Subnet %(subnet_id)s could not be found.")


class PortNotFound(NotFound):
    message = _("Port %(port_id)s could not be found.")


class PortNotFoundOnNetwork(NotFound):
    message = _("Port %(port_id)s could not be found "
                "on network %(net_id)s.")


class InUse(NeutronException):
    message = _("The resource is in use.")


class NetworkInUse(InUse):
    message = _("Unable to complete operation on network %(net_id)s. "
                "There are one or more ports still in use on the network.")


class SubnetInUse(InUse):
    message = _("Unable to complete operation on subnet %(subnet_id)s: "
                "%(reason)s.")

    def __init__(self, **kwargs):
        if 'reason' not in kwargs:
            kwargs['reason'] = _("One or more ports have an IP allocation "
                                 "from this subnet")
        super(SubnetInUse, self).__init__(**kwargs)


class SubnetPoolInUse(InUse):
    message = _("Unable to complete operation on subnet pool "
                "%(subnet_pool_id)s. %(reason)s.")

    def __init__(self, **kwargs):
        if 'reason' not in kwargs:
            kwargs['reason'] = _("Two or more concurrent subnets allocated")
        super(SubnetPoolInUse, self).__init__(**kwargs)


class PortInUse(InUse):
    message = _("Unable to complete operation on port %(port_id)s "
                "for network %(net_id)s. Port already has an attached "
                "device %(device_id)s.")


class ServicePortInUse(InUse):
    message = _("Port %(port_id)s cannot be deleted directly via the "
                "port API: %(reason)s.")


class PortBound(InUse):
    message = _("Unable to complete operation on port %(port_id)s, "
                "port is already bound, port type: %(vif_type)s, "
                "old_mac %(old_mac)s, new_mac %(new_mac)s.")


class MacAddressInUse(InUse):
    message = _("Unable to complete operation for network %(net_id)s. "
                "The mac address %(mac)s is in use.")


class InvalidIpForNetwork(BadRequest):
    message = _("IP address %(ip_address)s is not a valid IP "
                "for any of the subnets on the specified network.")


class InvalidIpForSubnet(BadRequest):
    message = _("IP address %(ip_address)s is not a valid IP "
                "for the specified subnet.")


class IpAddressInUse(InUse):
    message = _("Unable to complete operation for network %(net_id)s. "
                "The IP address %(ip_address)s is in use.")


class VlanIdInUse(InUse):
    message = _("Unable to create the network. "
                "The VLAN %(vlan_id)s on physical network "
                "%(physical_network)s is in use.")


class TunnelIdInUse(InUse):
    message = _("Unable to create the network. "
                "The tunnel ID %(tunnel_id)s is in use.")


class ResourceExhausted(ServiceUnavailable):
    pass


class NoNetworkAvailable(ResourceExhausted):
    message = _("Unable to create the network. "
                "No tenant network is available for allocation.")


class SubnetMismatchForPort(BadRequest):
    message = _("Subnet on port %(port_id)s does not match "
                "the requested subnet %(subnet_id)s.")


class Invalid(NeutronException):
    def __init__(self, message=None):
        self.message = message
        super(Invalid, self).__init__()


class InvalidInput(BadRequest):
    message = _("Invalid input for operation: %(error_message)s.")


class IpAddressGenerationFailure(Conflict):
    message = _("No more IP addresses available on network %(net_id)s.")


class PreexistingDeviceFailure(NeutronException):
    message = _("Creation failed. %(dev_name)s already exists.")


class OverQuota(Conflict):
    message = _("Quota exceeded for resources: %(overs)s.")


class InvalidContentType(NeutronException):
    message = _("Invalid content type %(content_type)s.")


class ExternalIpAddressExhausted(BadRequest):
    message = _("Unable to find any IP address on external "
                "network %(net_id)s.")


class TooManyExternalNetworks(NeutronException):
    message = _("More than one external network exists.")


class InvalidConfigurationOption(NeutronException):
    message = _("An invalid value was provided for %(opt_name)s: "
                "%(opt_value)s.")


class NetworkTunnelRangeError(NeutronException):
    message = _("Invalid network tunnel range: "
                "'%(tunnel_range)s' - %(error)s.")

    def __init__(self, **kwargs):
        # Convert tunnel_range tuple to 'start:end' format for display
        if isinstance(kwargs['tunnel_range'], tuple):
            kwargs['tunnel_range'] = "%d:%d" % kwargs['tunnel_range']
        super(NetworkTunnelRangeError, self).__init__(**kwargs)
