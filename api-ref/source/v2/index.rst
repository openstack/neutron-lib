:tocdepth: 2


###################
Networking API v2.0
###################

.. rest_expand_all::

####################
General API Overview
####################
.. include:: intro.inc
.. include:: versions.inc
.. include:: extensions.inc
##################
Layer 2 Networking
##################
.. include:: networks.inc
.. include:: network_segment_ranges.inc
.. include:: ports.inc
.. include:: segments.inc
.. include:: trunk.inc
.. include:: trunk-details.inc
##################
Layer 3 Networking
##################
.. include:: address-scopes.inc
.. include:: l3-conntrack-helper.inc
.. include:: floatingips.inc
.. include:: floatingippools.inc
.. include:: fip-port-forwarding.inc
.. include:: routers.inc
.. include:: subnetpools.inc
.. include:: subnetpool_prefix_ops.inc
.. include:: subnets.inc
########
Security
########
.. include:: fwaas-v2.inc
.. include:: rbac-policy.inc
.. include:: security-group-rules.inc
.. include:: security-groups.inc
.. include:: vpnaas.inc
###################
Resource Management
###################
.. include:: flavors.inc
.. include:: metering.inc
.. include:: network-ip-availability.inc
.. include:: quotas.inc
.. include:: quota_details.inc
.. include:: service-providers.inc
.. include:: tags.inc
##################
Quality of Service
##################
.. include:: qos.inc
###########################################
Load Balancer as a Service 2.0 (DEPRECATED)
###########################################

Neutron-lbaas is deprecated as of Queens. Load-Balancer-as-a-Service
(LBaaS v2) is now provided by the `Octavia project
<https://docs.openstack.org/octavia/latest/>`_. The `Octavia API v2
<https://developer.openstack.org/api-ref/load-balancer/v2/index.html>`_ is
backwards compatible with the neutron-lbaas implementation of the LBaaS 2.0
API.

Please see the FAQ at https://wiki.openstack.org/wiki/Neutron/LBaaS/Deprecation

#####################################
Logging Resource (networking-midonet)
#####################################
.. include:: logging_resource.inc
.. include:: firewall_log.inc
#################################################
Router interface floating IP (networking-midonet)
#################################################
.. include:: router-interface-fip.inc
##########################
FIP64 (networking-midonet)
##########################
.. include:: fip64.inc
############################
BGP/MPLS VPN Interconnection
############################
.. include:: bgpvpn-overview.inc
.. include:: bgpvpn-bgpvpns.inc
.. include:: bgpvpn-network_associations.inc
.. include:: bgpvpn-router_associations.inc
.. include:: bgpvpn-port_associations.inc
#######
Logging
#######
.. include:: logging.inc
#################
Networking Agents
#################
.. include:: agents.inc
.. include:: availability_zones.inc
.. include:: l3-agent-scheduler.inc
.. include:: dhcp-agent-scheduler.inc
#######################
Auto Allocated Topology
#######################
.. include:: auto-topology.inc
