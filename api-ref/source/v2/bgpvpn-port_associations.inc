=================
Port Associations
=================

Port associations are available if the ``bgpvpn-routes-control`` extension
is available.

Associating or disassociating a BGPVPN to a Port is done by manipulating a
Port association API resource as a sub-resource of the BGPVPN resource.

The semantic behind this API call is a form of policy-based routing: the
traffic from the given Port will be processed according to dataplane lookups
specific to this Port. This means, in particular that Ports belonging to a
given neutron network will possibly see a different L2 or L3 connectivity if
they have different BGPVPN associations.

When, a port association is defined for a given port, and at the same time,
a network association is defined for the port's network, both associations are
considered simultaneously active and the connectivity will be established
between the port and the BGPVPNs in both associations. This is true also in
the case where multiple associations are made, and for a router associations
of a router connected to the port's network.

Port routes
===========

Additionally to providing Port-level granularity in the definition of BGPVPN
connectivity, port associations also provide a way to control the
advertisement of routes other than only the fixed IPs of neutron ports.

So-called static routes are defined as follows: to indicate that prefix
20.1.0.0/16 is reachable via port A and should be advertised
accordingly in BGPVPN X,  a port association is defined between port A
and BGPVPN X, with the ``routes`` attribute set to ``[ {'type': 'prefix',
'prefix': '20.1.0.0/16'} ]``.

Route leaking of the routes of a given BGPVPN into another BGPVPN belonging
to the same tenant, is supported similarily: to indicate that all the prefixes
advertised to BGPVPN Y are reachable via port A (i.e. the routes tagged with at
least an RT belonging to ``route_targets`` or ``import_targets`` of BGPVPN Y),
and that they should be leaked into BGPVPN X, a port association is defined
between port A and BGPVPN X, with the ``routes`` attribute set to
``[ {'type': 'bgpvpn', 'bgpvpn_id': <uuid of BGPVPN Y>} ]``.

Control of BGP LOCAL_PREF attribute
===================================

The BGP LOCAL_PREF for a specific route can be controlled to take a different
value than the one defined in the BGPVPN ``local_pref`` attribute, by
adding a ``'local_pref': VALUE`` in a route in the ``routes`` attribute (see
example in port association Update request).

List Port Associations
======================

.. rest_method::  GET /v2.0/bgpvpn/bgpvpns/{bgpvpn_id}/port_associations

Lists port associations for a given BGP VPN.

Use the ``fields`` query parameter to control which fields are
returned in the response body. Additionally, you can filter results
by using query string parameters. For information, see `Filtering
and Column Selection <https://wiki.openstack.org/wiki/Neutron/APIv2
-specification#Filtering_and_Column_Selection>`__.

Normal response codes: 200

Error response codes: 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - bgpvpn_id: bgpvpn-id-path
   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - port_associations: bgpvpn-port_associations
   - id: bgpvpn-port_association_id
   - port_id: bgpvpn-port_id
   - project_id: project_id
   - routes: bgpvpn-routes
   - advertise_fixed_ips: bgpvpn-advertise_fixed_ips

Response Example
----------------

.. literalinclude:: samples/bgpvpn/port_associations/port_association-list-response.json
   :language: javascript

Create Port Association
=======================

.. rest_method::  POST /v2.0/bgpvpn/bgpvpns/{bgpvpn_id}/port_associations

Creates a port association for a given BGP VPN

Normal response codes: 201

Error response codes: 400, 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - bgpvpn_id: bgpvpn-id-path
   - port_association: bgpvpn-port_association
   - port_id: bgpvpn-port_id
   - routes: bgpvpn-routes-request
   - advertise_fixed_ips: bgpvpn-advertise_fixed_ips-request

Request Example
---------------

.. literalinclude:: samples/bgpvpn/port_associations/port_association-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - port_association: bgpvpn-port_association
   - id: bgpvpn-port_association_id
   - port_id: bgpvpn-port_id
   - project_id: project_id
   - routes: bgpvpn-routes
   - advertise_fixed_ips: bgpvpn-advertise_fixed_ips

Response Example
----------------

.. literalinclude:: samples/bgpvpn/port_associations/port_association-create-response.json
   :language: javascript

Show Port Association details
=============================

.. rest_method::  GET /v2.0/bgpvpn/bgpvpns/{bgpvpn_id}/port_associations/{port_association_id}

Shows details for a port association.

Normal response codes: 200

Error response codes: 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - bgpvpn_id: bgpvpn-id-path
   - port_association_id: bgpvpn-port_association_id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - port_association: bgpvpn-port_association
   - id: bgpvpn-port_association_id
   - port_id: bgpvpn-port_id
   - project_id: project_id
   - routes: bgpvpn-routes
   - advertise_fixed_ips: bgpvpn-advertise_fixed_ips

Response Example
----------------

.. literalinclude:: samples/bgpvpn/port_associations/port_association-show-response.json
   :language: javascript

Update a Port Association
=========================

.. rest_method::  PUT /v2.0/bgpvpn/bgpvpns/{bgpvpn_id}/port_associations/{port_association_id}

Updates a port Association.

Normal response codes: 201

Error response codes: 400, 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - bgpvpn_id: bgpvpn-id-path
   - port_association_id: bgpvpn-port_association_id-path
   - port_association: bgpvpn-port_association
   - routes: bgpvpn-routes-request
   - advertise_fixed_ips: bgpvpn-advertise_fixed_ips-request

Request Example
---------------

.. literalinclude:: samples/bgpvpn/port_associations/port_association-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - port_association: bgpvpn-port_association
   - id: bgpvpn-port_association_id
   - port_id: bgpvpn-port_id
   - project_id: project_id
   - routes: bgpvpn-routes
   - advertise_fixed_ips: bgpvpn-advertise_fixed_ips

Response Example
----------------

.. literalinclude:: samples/bgpvpn/port_associations/port_association-update-response.json
   :language: javascript


Delete Port Association
=======================

.. rest_method::  DELETE /v2.0/bgpvpn/bgpvpns/{bgpvpn_id}/port_associations/{port_association_id}

Deletes a port association.

Normal response codes: 204

Error response codes: 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - bgpvpn_id: bgpvpn-id-path
   - port_association_id: bgpvpn-port_association_id-path

Response
--------

There is no body content for the response of a successful DELETE request.
