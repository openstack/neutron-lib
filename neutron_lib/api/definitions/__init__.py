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

from neutron_lib.api.definitions import address_scope
from neutron_lib.api.definitions import agent
from neutron_lib.api.definitions import auto_allocated_topology
from neutron_lib.api.definitions import bgpvpn
from neutron_lib.api.definitions import bgpvpn_routes_control
from neutron_lib.api.definitions import data_plane_status
from neutron_lib.api.definitions import dns
from neutron_lib.api.definitions import dns_domain_ports
from neutron_lib.api.definitions import extra_dhcp_opt
from neutron_lib.api.definitions import fip64
from neutron_lib.api.definitions import firewall
from neutron_lib.api.definitions import firewall_v2
from neutron_lib.api.definitions import firewallrouterinsertion
from neutron_lib.api.definitions import l3
from neutron_lib.api.definitions import logging
from neutron_lib.api.definitions import logging_resource
from neutron_lib.api.definitions import network
from neutron_lib.api.definitions import network_mtu
from neutron_lib.api.definitions import port
from neutron_lib.api.definitions import port_security
from neutron_lib.api.definitions import portbindings
from neutron_lib.api.definitions import provider_net
from neutron_lib.api.definitions import router_interface_fip
from neutron_lib.api.definitions import subnet
from neutron_lib.api.definitions import subnetpool
from neutron_lib.api.definitions import trunk
from neutron_lib.api.definitions import trunk_details


_ALL_API_DEFINITIONS = {
    address_scope,
    agent,
    auto_allocated_topology,
    bgpvpn,
    bgpvpn_routes_control,
    data_plane_status,
    dns,
    dns_domain_ports,
    extra_dhcp_opt,
    fip64,
    firewall,
    firewall_v2,
    firewallrouterinsertion,
    l3,
    logging,
    logging_resource,
    network,
    network_mtu,
    port,
    port_security,
    portbindings,
    provider_net,
    router_interface_fip,
    subnet,
    subnetpool,
    trunk,
    trunk_details
}
