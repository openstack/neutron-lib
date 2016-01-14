# -*- coding: utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
test_exceptions
----------------------------------

Tests for `neutron_lib.exception` module.
"""

import functools

from neutron_lib._i18n import _
import neutron_lib.exceptions as ne
from neutron_lib.tests import _base as base


def _raise(exc_class, **kwargs):
    raise exc_class(**kwargs)


class TestExceptions(base.BaseTestCase):

    def _check_nexc(self, exc_class, expected_msg, **kwargs):
        raise_exc_class = functools.partial(_raise, exc_class)
        e = self.assertRaises(exc_class, raise_exc_class, **kwargs)
        self.assertEqual(expected_msg, str(e))
        self.assertFalse(e.use_fatal_exceptions())

    def test_base(self):
        self._check_nexc(
            ne.NeutronException,
            _('An unknown exception occurred.'))

    def test_not_found(self):
        self._check_nexc(
            ne.NotFound,
            _('An unknown exception occurred.'))

    def test_conflict(self):
        self._check_nexc(
            ne.Conflict,
            _('An unknown exception occurred.'))

    def test_bad_request(self):
        self._check_nexc(
            ne.BadRequest,
            _('Bad A request: B.'),
            resource='A', msg='B')

    def test_bad_request_misused(self):
        try:
            self._check_nexc(
                ne.BadRequest,
                _('Bad A request: B.'),
                bad_resource='A', bad_msg='B')
        except AttributeError:
            pass

    def test_not_authorized(self):
        self._check_nexc(
            ne.NotAuthorized,
            _("Not authorized."))

    def test_service_unavailable(self):
        self._check_nexc(
            ne.ServiceUnavailable,
            _("The service is unavailable."))

    def test_admin_required(self):
        self._check_nexc(
            ne.AdminRequired,
            _("User does not have admin privileges: hoser."),
            reason="hoser")

    def test_object_not_found(self):
        self._check_nexc(
            ne.ObjectNotFound,
            _("Object fallout tato not found."),
            id="fallout tato")

    def test_network_not_found(self):
        self._check_nexc(
            ne.NetworkNotFound,
            _("Network spam could not be found."),
            net_id="spam")

    def test_subnet_not_found(self):
        self._check_nexc(
            ne.SubnetNotFound,
            _("Subnet root could not be found."),
            subnet_id="root")

    def test_port_not_found(self):
        self._check_nexc(
            ne.PortNotFound,
            _("Port harbor could not be found."),
            port_id="harbor")

    def test_port_not_found_on_network(self):
        self._check_nexc(
            ne.PortNotFoundOnNetwork,
            _("Port serial could not be found on network USB."),
            port_id="serial", net_id="USB")

    def test_in_use(self):
        self._check_nexc(
            ne.InUse,
            _("The resource is in use."))

    def test_network_in_use(self):
        self._check_nexc(
            ne.NetworkInUse,
            _("Unable to complete operation on network foo. "
              "There are one or more ports still in use on the network."),
            net_id="foo")

    def test_subnet_in_use(self):
        self._check_nexc(
            ne.SubnetInUse,
            _("Unable to complete operation on subnet garbage: not full."),
            subnet_id="garbage", reason="not full")

    def test_subnet_in_use_no_reason(self):
        self._check_nexc(
            ne.SubnetInUse,
            _("Unable to complete operation on subnet garbage: "
              "One or more ports have an IP allocation from this subnet."),
            subnet_id="garbage")

    def test_subnet_pool_in_use(self):
        self._check_nexc(
            ne.SubnetPoolInUse,
            _("Unable to complete operation on subnet pool ymca. because."),
            subnet_pool_id="ymca", reason="because")

    def test_subnet_pool_in_use_no_reason(self):
        self._check_nexc(
            ne.SubnetPoolInUse,
            _("Unable to complete operation on subnet pool ymca. "
              "Two or more concurrent subnets allocated."),
            subnet_pool_id="ymca")

    def test_port_in_use(self):
        self._check_nexc(
            ne.PortInUse,
            _("Unable to complete operation on port a for network c. "
              "Port already has an attached device b."),
            port_id='a', device_id='b', net_id='c')

    def test_service_port_in_use(self):
        self._check_nexc(
            ne.ServicePortInUse,
            _("Port harbor cannot be deleted directly via the "
              "port API: docking."),
            port_id='harbor', reason='docking')

    def test_port_bound(self):
        self._check_nexc(
            ne.PortBound,
            _("Unable to complete operation on port bigmac, "
              "port is already bound, port type: ketchup, "
              "old_mac onions, new_mac salt."),
            port_id='bigmac', vif_type='ketchup', old_mac='onions',
            new_mac='salt')

    def test_mac_address_in_use(self):
        self._check_nexc(
            ne.MacAddressInUse,
            _("Unable to complete operation for network nutters. "
              "The mac address grill is in use."),
            net_id='nutters', mac='grill')

    def test_invalid_ip_for_network(self):
        self._check_nexc(
            ne.InvalidIpForNetwork,
            _("IP address shazam! is not a valid IP "
              "for any of the subnets on the specified network."),
            ip_address='shazam!')

    def test_invalid_ip_for_subnet(self):
        self._check_nexc(
            ne.InvalidIpForSubnet,
            _("IP address 300.400.500.600 is not a valid IP "
              "for the specified subnet."),
            ip_address='300.400.500.600')

    def test_ip_address_in_use(self):
        self._check_nexc(
            ne.IpAddressInUse,
            _("Unable to complete operation for network boredom. "
              "The IP address crazytown is in use."),
            net_id='boredom', ip_address='crazytown')

    def test_vlan_id_in_use(self):
        self._check_nexc(
            ne.VlanIdInUse,
            _("Unable to create the network. The VLAN virtual on physical "
              "network phys is in use."),
            vlan_id='virtual', physical_network='phys')

    def test_tunnel_id_in_use(self):
        self._check_nexc(
            ne.TunnelIdInUse,
            _("Unable to create the network. The tunnel ID sewer is in use."),
            tunnel_id='sewer')

    def test_resource_exhausted(self):
        self._check_nexc(
            ne.ResourceExhausted,
            _("The service is unavailable."))

    def test_no_network_available(self):
        self._check_nexc(
            ne.NoNetworkAvailable,
            _("Unable to create the network. "
              "No tenant network is available for allocation."))

    def test_subnet_mismatch_for_port(self):
        self._check_nexc(
            ne.SubnetMismatchForPort,
            _("Subnet on port porter does not match "
              "the requested subnet submit."),
            port_id='porter', subnet_id='submit')

    def test_invalid(self):
        try:
            raise ne.Invalid("hello world")
        except ne.Invalid as e:
            self.assertEqual(e.msg, "hello world")

    def test_invalid_input(self):
        self._check_nexc(
            ne.InvalidInput,
            _("Invalid input for operation: warp core breach."),
            error_message='warp core breach')

    def test_ip_address_generation_failure(self):
        self._check_nexc(
            ne.IpAddressGenerationFailure,
            _("No more IP addresses available on network nuke."),
            net_id='nuke')

    def test_preexisting_device_failure(self):
        self._check_nexc(
            ne.PreexistingDeviceFailure,
            _("Creation failed. hal9000 already exists."),
            dev_name='hal9000')

    def test_over_quota(self):
        self._check_nexc(
            ne.OverQuota,
            _("Quota exceeded for resources: tube socks."),
            overs='tube socks')

    def test_invalid_content_type(self):
        self._check_nexc(
            ne.InvalidContentType,
            _("Invalid content type porn."),
            content_type='porn')

    def test_external_ip_address_exhausted(self):
        self._check_nexc(
            ne.ExternalIpAddressExhausted,
            _("Unable to find any IP address on external network darpanet."),
            net_id='darpanet')

    def test_too_many_external_networks(self):
        self._check_nexc(
            ne.TooManyExternalNetworks,
            _("More than one external network exists."))

    def test_invalid_configuration_option(self):
        self._check_nexc(
            ne.InvalidConfigurationOption,
            _("An invalid value was provided for which muppet: big bird."),
            opt_name='which muppet', opt_value='big bird')

    def test_network_tunnel_range_error(self):
        self._check_nexc(
            ne.NetworkTunnelRangeError,
            _("Invalid network tunnel range: 'rats' - present."),
            tunnel_range='rats', error='present')

    def test_network_tunnel_range_error_tuple(self):
        self._check_nexc(
            ne.NetworkTunnelRangeError,
            _("Invalid network tunnel range: '3:4' - present."),
            tunnel_range=(3, 4), error='present')
