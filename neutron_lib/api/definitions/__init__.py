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
from neutron_lib.api.definitions import allowedaddresspairs
from neutron_lib.api.definitions import auto_allocated_topology
from neutron_lib.api.definitions import availability_zone
from neutron_lib.api.definitions import bgpvpn
from neutron_lib.api.definitions import bgpvpn_routes_control
from neutron_lib.api.definitions import bgpvpn_vni
from neutron_lib.api.definitions import data_plane_status
from neutron_lib.api.definitions import default_subnetpools
from neutron_lib.api.definitions import dns
from neutron_lib.api.definitions import dns_domain_ports
from neutron_lib.api.definitions import dvr
from neutron_lib.api.definitions import external_net
from neutron_lib.api.definitions import extra_dhcp_opt
from neutron_lib.api.definitions import extraroute
from neutron_lib.api.definitions import fip64
from neutron_lib.api.definitions import firewall
from neutron_lib.api.definitions import firewall_v2
from neutron_lib.api.definitions import firewallrouterinsertion
from neutron_lib.api.definitions import flavors
from neutron_lib.api.definitions import ip_allocation
from neutron_lib.api.definitions import ip_substring_port_filtering
from neutron_lib.api.definitions import l2_adjacency
from neutron_lib.api.definitions import l3
from neutron_lib.api.definitions import l3_ext_gw_mode
from neutron_lib.api.definitions import l3_ext_ha_mode
from neutron_lib.api.definitions import l3_flavors
from neutron_lib.api.definitions import logging
from neutron_lib.api.definitions import logging_resource
from neutron_lib.api.definitions import metering
from neutron_lib.api.definitions import multiprovidernet
from neutron_lib.api.definitions import network
from neutron_lib.api.definitions import network_availability_zone
from neutron_lib.api.definitions import network_ip_availability
from neutron_lib.api.definitions import network_mtu
from neutron_lib.api.definitions import network_mtu_writable
from neutron_lib.api.definitions import pagination
from neutron_lib.api.definitions import port
from neutron_lib.api.definitions import port_security
from neutron_lib.api.definitions import portbindings
from neutron_lib.api.definitions import portbindings_extended
from neutron_lib.api.definitions import project_id
from neutron_lib.api.definitions import provider_net
from neutron_lib.api.definitions import qos
from neutron_lib.api.definitions import qos_default
from neutron_lib.api.definitions import qos_rule_type_details
from neutron_lib.api.definitions import revisionifmatch
from neutron_lib.api.definitions import router_availability_zone
from neutron_lib.api.definitions import router_interface_fip
from neutron_lib.api.definitions import routerservicetype
from neutron_lib.api.definitions import segment
from neutron_lib.api.definitions import servicetype
from neutron_lib.api.definitions import sorting
from neutron_lib.api.definitions import subnet
from neutron_lib.api.definitions import subnet_onboard
from neutron_lib.api.definitions import subnetpool
from neutron_lib.api.definitions import trunk
from neutron_lib.api.definitions import trunk_details
from neutron_lib.api.definitions import vlantransparent


_ALL_API_DEFINITIONS = {
    address_scope,
    agent,
    allowedaddresspairs,
    auto_allocated_topology,
    availability_zone,
    bgpvpn,
    bgpvpn_routes_control,
    bgpvpn_vni,
    data_plane_status,
    default_subnetpools,
    dns,
    dns_domain_ports,
    dvr,
    external_net,
    extra_dhcp_opt,
    extraroute,
    fip64,
    firewall,
    firewall_v2,
    firewallrouterinsertion,
    flavors,
    ip_allocation,
    ip_substring_port_filtering,
    l2_adjacency,
    l3,
    l3_ext_gw_mode,
    l3_ext_ha_mode,
    l3_flavors,
    logging,
    logging_resource,
    metering,
    multiprovidernet,
    network,
    network_availability_zone,
    network_ip_availability,
    network_mtu,
    network_mtu_writable,
    pagination,
    port,
    port_security,
    portbindings,
    portbindings_extended,
    project_id,
    provider_net,
    qos,
    qos_default,
    qos_rule_type_details,
    revisionifmatch,
    router_availability_zone,
    router_interface_fip,
    routerservicetype,
    segment,
    servicetype,
    sorting,
    subnet,
    subnet_onboard,
    subnetpool,
    trunk,
    trunk_details,
    vlantransparent
}
