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

On VXLAN VNI
============

VXLAN is one option among others that could be used for BGP E-VPNs.
When VXLAN is used on a hardware platform the use of a locally-assigned id
may not be always possible which introduces the need to configure a
globally-assigned VXLAN VNI.

The optional ``vni`` attribute is an admin-only parameter and allows the
admin to enforce the use of a chosen globally-assigned VXLAN VNI for the
said BGPVPN.

The default when no VNI is specified and the VXLAN encapsulation is used, is
to let the backend choose the VNI in advertised routes, and use the VNI in
received routes for transmitted traffic. The backend will conform to
E-VPN overlay specs.

Valid range for the ``vni`` attribute is [1, 2\ :sup:`24`\ -1].

Control of routes advertised to BGPVPNs
=======================================

With the ``bgpvpn`` extension, when associations between networks or routers
and BGVPNs are defined, the routes corresponding to fixed IPs of neutron ports
will be advertised to BGPVPNs.  For router associations, extra routes of the
router ('routes' attribute of a ``router`` resource) may also be advertised
to BGPVPNs.

To provide more flexibility, the ``bgpvpn-routes-control`` extension provides
a way to:

- advertise other routes to a BGPVPN, for instances a prefix that is reachable
  via a neutron port, or routes leaked from another BGPVPN; this is implemented
  thanks to the ``routes`` attribute of a BGPVPN port association

- not advertise the fixed IPs of a neutron port to a BGPVPN, which can be
  particularly relevant when other IP prefixes are reachable via the port; this
  is implemented thanks to the ``advertise_fixed_ips`` attribute of a BGPVPN
  port association

- explicitly control whether extra routes of a router are to be advertised
  to a BGPVPN; this is implemented thanks to the ``advertise_extra_routes``
  attribute of a BGPVPN router association.

  .. note:: This feature is under development for the Rocky release

- optionally control the value of the LOCAL_PREF BGP attribute of advertised
  routes, for all routes of a BGPVPN (thanks to the ``local_pref`` attribute
  of a BGPVPN resource) and/or per route (thanks to the ``local_pref``
  in a port association route)

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

Connectivity Impact inside OpenStack Neutron
============================================

Creating two BGP VPNs with RTs resulting in both VPNs to exchange
routes, and then associating these two BGP VPNs to two networks, will
result in establishing interconnectivity between these two networks,
this simply being the result of applying BGP VPN Route Target semantics
(i.e. without making prefixes to OpenStack networks a particular case).

This similarly applies to router associations.

