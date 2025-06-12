.. -*- rst -*-

=======
Subnets
=======

Lists, shows details for, creates, updates, and deletes subnet
resources.

Default subnetpool extension
============================

The default subnetpool extension (``default-subnetpools``) allows
administrative users to specify default subnetpools (one per
IP version). Then users can specify the ``use_default_subnetpool``
attribute when creating a subnet, instead of having to specify the
``subnetpool_id`` attribute referencing the default subnetpool.

Resource timestamps
===================

The ``standard-attr-timestamp`` extension adds the ``created_at`` and
``updated_at`` attributes to all resources that have standard attributes.

Subnet allocation extension
===========================

Subnet allocation extension (``subnet_allocation``) enables allocation of
subnets from a subnet pool.

Subnet DNS publish fixed IP extension
=====================================

The ``subnet-dns-publish-fixed-ip`` extension adds the ``dns_publish_fixed_ip``
attribute to subnets. It allows to select per subnet whether DNS records
for fixed IPs are to be published in an external DNS service.

Segment extension
=================

The `Segments`_ (``segment``) extension makes it possible to associate a
subnet with a specific L2 segment on the network, instead of spanning all the
segments in the network. The association between network and subnet remains,
but an optional ``segment_id`` field is added to the subnet so that it can be
associated with a particular segment on the network. With multiple subnets on a
network the ``segment_id`` is used to determine if the subnets are l2-adjacent
or not. Subnets within a network are either all associated to segments, or
none of them are associated to segments.

Subnet segment_id writable extension
====================================

The subnet segment_id writable (``subnet-segmentid-writable``) extension
enhances the `Segments`_ (``segment``) extension in that now the ``segment_id``
attribute is also available for write when a subnet is updated.

Segment peer subnet host routes extension
=========================================

The segment peer subnet host routes extension (
``segments-peer-subnet-host-routes``) extension enhances the `Segments`_
(``segment``) extension in that now the ``host_routes`` property of the
different `Subnets`_ (``subnets``) in a routed network gets routes to the peer
subnets on different segments added automatically. This ensures that traffic
within an L3 routed network stays within the network even when the default
route is on a different host interface.

Subnet service types extension
==============================

Subnet service types extension (``subnet-service-types``) allows administrative
users to set the desired port types for a subnet by adding the
``service_types`` attributes to ``subnets``.
(For example, the ``network:floatingip_agent_gateway`` service type enables
DVR floating IP agent gateway ports to use the subnet to minimize public
IP address consumption).

Tag extension
=============

The ``standard-attr-tag`` adds Tag support for resources with
standard attributes by adding the ``tags`` attribute
allowing consumers to associate tags with resources.


List subnets
============

.. rest_method::  GET /v2.0/subnets

Lists subnets that the project has access to.

Default policy settings return only subnets owned by the
project of the user submitting the request, unless the
user has administrative role. You can control which attributes
are returned by using the fields query parameter. You can filter
results by using query string parameters.

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: 401

Request
-------

.. rest_parameters:: parameters.yaml

   - id: id-query
   - tenant_id: project_id-query
   - project_id: project_id-query
   - name: name-query
   - enable_dhcp: subnet-enable_dhcp-query
   - network_id: subnet-network_id-query
   - ip_version: subnet-ip_version-query
   - gateway_ip: subnet-gateway_ip-query
   - cidr: cidr-query
   - description: description-query
   - ipv6_address_mode: subnet-ipv6_address_mode-query
   - ipv6_ra_mode: subnet-ipv6_ra_mode-query
   - revision_number: revision_number-query
   - segment_id: subnet-segment_id-query
   - shared: shared-query
   - sort_dir: sort_dir
   - sort_key: subnet-sort_key
   - subnetpool_id: subnet-subnetpool_id-query
   - tags: tags-query
   - tags-any: tags-any-query
   - not-tags: not-tags-query
   - not-tags-any: not-tags-any-query
   - dns_publish_fixed_ip: subnet-dns_publish_fixed_ip-query
   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - subnets: subnets-obj
   - id: subnet-id-body
   - tenant_id: project_id
   - project_id: project_id
   - name: subnet-name
   - enable_dhcp: subnet-enable_dhcp
   - network_id: subnet-network_id
   - dns_nameservers: subnet-dns_nameservers
   - allocation_pools: subnet-allocation_pools
   - host_routes: subnet-host_routes
   - ip_version: subnet-ip_version
   - gateway_ip: subnet-gateway_ip
   - cidr: cidr
   - created_at: created_at_resource
   - description: description
   - ipv6_address_mode: subnet-ipv6_address_mode
   - ipv6_ra_mode: subnet-ipv6_ra_mode
   - revision_number: revision_number
   - segment_id: subnet-segment_id
   - service_types: subnet-service_types
   - subnetpool_id: subnet-subnetpool_id
   - updated_at: updated_at_resource
   - tags: tags
   - dns_publish_fixed_ip: subnet-dns_publish_fixed_ip
   - router:external: subnet-router:external

Response Example
----------------

.. literalinclude:: samples/subnets/subnets-list-response.json
   :language: javascript

Create subnet
=============

.. rest_method::  POST /v2.0/subnets

Creates a subnet on a network.

OpenStack Networking does not try to derive the correct IP version
from the CIDR. If you do not specify the ``gateway_ip`` attribute,
OpenStack Networking allocates an address from the CIDR for the
gateway for the subnet.

To specify a subnet without a gateway, set the ``gateway_ip``
attribute to ``null`` in the request body. If you do not specify
the ``allocation_pools`` attribute, OpenStack Networking
automatically allocates pools for covering all IP addresses in the
CIDR, excluding the address reserved for the subnet gateway.
Otherwise, you can explicitly specify allocation pools as shown in
the following example.

When you specify both the ``allocation_pools`` and ``gateway_ip``
attributes, you must ensure that the gateway IP does not overlap
with the allocation pools; otherwise, the call returns the
``Conflict (409)`` response code.

A subnet can have one or more name servers and host routes. Hosts
in this subnet use the name servers. Devices with IP addresses from
this subnet, not including the local subnet route, use the host
routes.

Specify the ``ipv6_ra_mode`` and ``ipv6_address_mode`` attributes
to create subnets that support IPv6 configurations, such as
stateless address autoconfiguration (SLAAC), DHCPv6 stateful, and
DHCPv6 stateless configurations.

A subnet can optionally be associated with a network segment when
it is created by specifying the ``segment_id`` of a valid segment
on the specified network. A network with subnets associated in this
way is called a routed network. On any given network, all of the
subnets must be associated with segments or none of them can be.
Neutron enforces this invariant. Currently, routed networks are
only supported for provider networks.

.. note::

   Creating a subnet does not always result in an automatic port update
   for the ports which are already bound on the network.

   For details see:
   https://docs.openstack.org/neutron/latest/admin/config-ipv6.html#address-modes-for-ports

Normal response codes: 201

Error response codes: 400, 401, 403, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - subnet: subnet-obj
   - tenant_id: project_id-request
   - project_id: project_id-request
   - name: subnet-name-request
   - enable_dhcp: subnet-enable_dhcp-request
   - network_id: subnet-network_id
   - dns_nameservers: subnet-dns_nameservers-request
   - allocation_pools: subnet-allocation_pools-request
   - host_routes: subnet-host_routes-request
   - ip_version: subnet-ip_version
   - gateway_ip: subnet-gateway_ip-request
   - cidr: cidr
   - prefixlen: subnet-prefixlen-request
   - description: description-request
   - ipv6_address_mode: subnet-ipv6_address_mode-request
   - ipv6_ra_mode: subnet-ipv6_ra_mode-request
   - segment_id: subnet-segment_id-request
   - subnetpool_id: subnet-subnetpool_id-request
   - use_default_subnetpool: use_default_subnetpool
   - service_types: subnet-service_types-optional
   - dns_publish_fixed_ip: subnet-dns_publish_fixed_ip-request

Request Example
---------------

.. literalinclude:: samples/subnets/subnet-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - subnet: subnet-obj
   - id: subnet-id-body
   - tenant_id: project_id
   - project_id: project_id
   - name: subnet-name
   - enable_dhcp: subnet-enable_dhcp
   - network_id: subnet-network_id
   - dns_nameservers: subnet-dns_nameservers
   - allocation_pools: subnet-allocation_pools
   - host_routes: subnet-host_routes
   - ip_version: subnet-ip_version
   - gateway_ip: subnet-gateway_ip
   - cidr: cidr
   - created_at: created_at_resource
   - description: description
   - ipv6_address_mode: subnet-ipv6_address_mode
   - ipv6_ra_mode: subnet-ipv6_ra_mode
   - revision_number: revision_number
   - service_types: subnet-service_types
   - subnetpool_id: subnet-subnetpool_id
   - segment_id: subnet-segment_id
   - updated_at: updated_at_resource
   - tags: tags
   - dns_publish_fixed_ip: subnet-dns_publish_fixed_ip
   - router:external: subnet-router:external

Response Example
----------------

.. literalinclude:: samples/subnets/subnet-create-response.json
   :language: javascript

Bulk create subnet
==================

.. rest_method::  POST /v2.0/subnets

Creates multiple subnets in a single request. Specify a list of subnets in the request body.

The bulk create operation is always atomic. Either all or no
subnets in the request body are created.

Normal response codes: 201

Error response codes: 400, 401, 403, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - subnets: subnets-obj
   - tenant_id: project_id-request
   - project_id: project_id-request
   - name: subnet-name-request
   - enable_dhcp: subnet-enable_dhcp-request
   - network_id: subnet-network_id
   - dns_nameservers: subnet-dns_nameservers-request
   - allocation_pools: subnet-allocation_pools-request
   - host_routes: subnet-host_routes-request
   - ip_version: subnet-ip_version
   - gateway_ip: subnet-gateway_ip-request
   - cidr: cidr
   - prefixlen: subnet-prefixlen-request
   - description: description-request
   - ipv6_address_mode: subnet-ipv6_address_mode-request
   - ipv6_ra_mode: subnet-ipv6_ra_mode-request
   - segment_id: subnet-segment_id-request
   - subnetpool_id: subnet-subnetpool_id-request
   - use_default_subnetpool: use_default_subnetpool
   - service_types: subnet-service_types-optional
   - dns_publish_fixed_ip: subnet-dns_publish_fixed_ip-request

Request Example
---------------

.. literalinclude:: samples/subnets/subnets-create-bulk-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - subnets: subnets-obj
   - id: subnet-id-body
   - tenant_id: project_id
   - project_id: project_id
   - name: subnet-name
   - enable_dhcp: subnet-enable_dhcp
   - network_id: subnet-network_id
   - dns_nameservers: subnet-dns_nameservers
   - allocation_pools: subnet-allocation_pools
   - host_routes: subnet-host_routes
   - ip_version: subnet-ip_version
   - gateway_ip: subnet-gateway_ip
   - cidr: cidr
   - created_at: created_at_resource
   - description: description
   - ipv6_address_mode: subnet-ipv6_address_mode
   - ipv6_ra_mode: subnet-ipv6_ra_mode
   - revision_number: revision_number
   - segment_id: subnet-segment_id
   - service_types: subnet-service_types
   - subnetpool_id: subnet-subnetpool_id
   - updated_at: updated_at_resource
   - tags: tags
   - dns_publish_fixed_ip: subnet-dns_publish_fixed_ip
   - router:external: subnet-router:external

Response Example
----------------

.. literalinclude:: samples/subnets/subnets-create-bulk-response.json
   :language: javascript

Show subnet details
===================

.. rest_method::  GET /v2.0/subnets/{subnet_id}

Shows details for a subnet.

Use the fields query parameter to filter the results.

.. include:: filtering-show.inc

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - subnet_id: subnet_id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - subnet: subnet-obj
   - id: subnet-id-body
   - tenant_id: project_id
   - project_id: project_id
   - created_at: created_at_resource
   - name: subnet-name
   - enable_dhcp: subnet-enable_dhcp
   - network_id: subnet-network_id
   - dns_nameservers: subnet-dns_nameservers
   - allocation_pools: subnet-allocation_pools
   - host_routes: subnet-host_routes
   - ip_version: subnet-ip_version
   - gateway_ip: subnet-gateway_ip
   - cidr: cidr
   - updated_at: updated_at_resource
   - description: description
   - ipv6_address_mode: subnet-ipv6_address_mode
   - ipv6_ra_mode: subnet-ipv6_ra_mode
   - revision_number: revision_number
   - segment_id: subnet-segment_id
   - service_types: subnet-service_types
   - subnetpool_id: subnet-subnetpool_id
   - tags: tags
   - dns_publish_fixed_ip: subnet-dns_publish_fixed_ip
   - router:external: subnet-router:external

Response Example
----------------

.. literalinclude:: samples/subnets/subnet-show-response.json
   :language: javascript

Update subnet
=============

.. rest_method::  PUT /v2.0/subnets/{subnet_id}

Updates a subnet.

Some attributes, such as IP version (ip_version), CIDR (cidr), and
segment (segment_id) cannot be updated. Attempting to update these
attributes results in a ``400 Bad Request`` error.

Normal response codes: 200

Error response codes: 400, 401, 403, 404, 412

Request
-------

.. rest_parameters:: parameters.yaml

   - subnet_id: subnet_id-path
   - name: subnet-name-update-request
   - enable_dhcp: subnet-enable_dhcp-request
   - dns_nameservers: subnet-dns_nameservers-request
   - allocation_pools: subnet-allocation_pools-request
   - host_routes: subnet-host_routes-request
   - gateway_ip: subnet-gateway_ip-update-request
   - description: description-request
   - service_types: subnet-service_types-optional
   - segment_id: subnet-segment_id-request
   - dns_publish_fixed_ip: subnet-dns_publish_fixed_ip-request

Request Example
---------------

.. literalinclude:: samples/subnets/subnet-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - subnet: subnet-obj
   - id: subnet-id-body
   - tenant_id: project_id
   - project_id: project_id
   - name: subnet-name
   - enable_dhcp: subnet-enable_dhcp
   - network_id: subnet-network_id
   - dns_nameservers: subnet-dns_nameservers
   - allocation_pools: subnet-allocation_pools
   - host_routes: subnet-host_routes
   - ip_version: subnet-ip_version
   - gateway_ip: subnet-gateway_ip
   - cidr: cidr
   - created_at: created_at_resource
   - description: description
   - ipv6_address_mode: subnet-ipv6_address_mode
   - ipv6_ra_mode: subnet-ipv6_ra_mode
   - revision_number: revision_number
   - segment_id: subnet-segment_id
   - service_types: subnet-service_types
   - subnetpool_id: subnet-subnetpool_id
   - updated_at: updated_at_resource
   - tags: tags
   - dns_publish_fixed_ip: subnet-dns_publish_fixed_ip
   - router:external: subnet-router:external

Response Example
----------------

.. literalinclude:: samples/subnets/subnet-update-response.json
   :language: javascript

Delete subnet
=============

.. rest_method::  DELETE /v2.0/subnets/{subnet_id}

Deletes a subnet.

The operation fails if subnet IP addresses are still allocated.

Normal response codes: 204

Error response codes: 401, 404, 412

Request
-------

.. rest_parameters:: parameters.yaml

   - subnet_id: subnet_id-path

Response
--------

There is no body content for the response of a successful DELETE request.

