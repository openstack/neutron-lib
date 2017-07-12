=======================
BGP - MPLS VPN Overview
=======================

The ``bgpvpn`` extension implements the BGP VPN Interconnection API
which provides the ability to associate OpenStack networks and/or
routers with Multiprotocol Label Switching (MPLS) Virtual Private
Networks (VPNs) via Border Gateway Protocol (BGP) peering. BGP-MPLS VPNs
are commonly provided by telecommunications service providers to
customers in addition to or instead of Internet connectivity for Wide
Area Networking. This API enables the interconnection with these
WAN VPNs using *Route Targets* to indicate the desired network(s).

On Route Targets
================

``route_targets``, ``import_targets``, ``export_targets`` attributes

- The set of RTs used for import is the union of ``route_targets`` and ``import_targets``.
- The set of RTs used for export is the union of ``route_targets`` and ``export_targets``.

At least one of ``route_targets``, ``import_targets`` or ``export_targets`` options will
typically be defined, but the API will not enforce that and all lists can be
empty.

For instance, in the very typical use case where the BGP VPN uses a single
Route Target for both import and export, the route_targets parameter alone is
enough and will contain one Route target.

On Route Distinguishers (RDs)
=============================

The ``route_distinguishers`` parameter is optional and provides an
indication of the RDs that shall be used for routes announced for
Neutron networks. The contract is that when a list of RDs is specified,
the backend will use, for a said advertisement of a route, one of these
RDs. The motivation for having a list rather than only one RD is to
allow the support for multihoming a VPN prefix (typically for
resiliency, load balancing or anycast). A backend may or may not
support this behavior, and should report an API error in the latter
case. When not specified, the backend will use automatically-assigned
RDs (for instance <ip>:<number> RDs derived from the Provider Edge (PE) IP).

Valid strings for Route Distinguishers and Route Targets
========================================================

Valid strings for a Route Target or a Route Distinguisher are the following:

- <2-byte AS#>:<32bit-number>
- <4-byte AS#>:<16bit-number>
- <4-byte IPv4>:<16bit-number>

======================
BGP - MPLS VPN Caveats
======================

Association constraints
=======================

A given BGP VPN can be associated to multiple networks and/or multiple
routers.

To avoid any ambiguity on semantics in particular the context of
processing associated to a router (e.g. NAT or FWaaS), if a given subnet
in a network is bound to a router, this API does not allow to both
associate the network to an L3 BGP VPN and the router to the same or to
a distinct L3 BGP VPN.

Moreover, for BGP VPNs of type L3, there are possible cases of IP prefix
overlaps that can't be detected by the service plugin before BGP routes
are received, for which the behavior is left undefined by these
specifications (i.e. which of the overlapping routes is being used) and
will depend on the backend. This applies for both router associations
and network associations in the case where traffic is forwarded by a
router and the destination IP belongs both to a prefix of a BGP VPN
associated with the router or with the network originating the traffic,
and to a prefix of a subnet bound to the router; in such a case whether
the traffic will be delivered to the subnet or to the BGP VPN is not
defined by this API.

Connectivity Impact inside Openstack Neutron
============================================

Creating two BGP VPNs with RTs resulting in both VPNs to exchange
routes, and then associating these two BGP VPNs to two networks, will
result in establishing interconnectivity between these two networks,
this simply being the result of applying BGP VPN Route Target semantics
(i.e. without making prefixes to OpenStack networks a particular case).

This similarly applies to router associations.

