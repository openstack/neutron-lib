.. -*- rst -*-

===================
Router Associations
===================

Associating a BGPVPN to a Router can be done only for BGPVPN of type L3. The
semantic is that all Subnets bound to the Router will be interconnected with
the BGPVPN.

A said Router can be associated with multiple BGPVPNs.

Associating or disassociating a BGPVPN to a Router is done by manipulating a
Router association API resource as a sub-resource of the BGPVPN resource:

Advertising router extra routes to a BGPVPN
===========================================

The ``bgpvpn-routes-control`` API extension allows to control the
re-advertisement of a router extra routes in a BGPVPN ("extra routes" are
routes defined in the ``routes`` attribute of a router when the ``extraroute``
extension is available).

The ``advertise_extra_routes`` attribute can in this case be set on a
router_association:

- ``true``: the extra routes defined in the ``routes`` attribute of
  the router will be advertised to the BGPVPN (default value)
- ``false``: the extra routes defined in the ``routes`` attribute of
  the router will **not** be advertised to the BGPVPN

List Router Associations
=========================

.. rest_method::  GET /v2.0/bgpvpn/bgpvpns/{bgpvpn_id}/router_associations

Lists router associations for a given BGP VPN.

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: 400, 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - bgpvpn_id: bgpvpn-id-path
   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - router_associations: bgpvpn-router_associations
   - id: bgpvpn-router_association_id
   - router_id: bgpvpn-router_id
   - tenant_id: project_id
   - project_id: project_id

Response Example
----------------

.. literalinclude:: samples/bgpvpn/router_associations/router_association-list-response.json
   :language: javascript

Create Router Association
==========================

.. rest_method::  POST /v2.0/bgpvpn/bgpvpns/{bgpvpn_id}/router_associations

Creates a router association for a given BGP VPN

Normal response codes: 201

Error response codes: 400, 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - bgpvpn_id: bgpvpn-id-path
   - router_association: bgpvpn-router_association
   - router_id: bgpvpn-router_id

Request Example
---------------

.. literalinclude:: samples/bgpvpn/router_associations/router_association-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - router_association: bgpvpn-router_association
   - id: bgpvpn-router_association_id
   - router_id: bgpvpn-router_id
   - tenant_id: project_id
   - project_id: project_id

Response Example
----------------

.. literalinclude:: samples/bgpvpn/router_associations/router_association-create-response.json
   :language: javascript

Show Router Association details
================================

.. rest_method::  GET /v2.0/bgpvpn/bgpvpns/{bgpvpn_id}/router_associations/{router_association_id}

Shows details for a router association.

.. include:: filtering-show.inc

Normal response codes: 200

Error response codes: 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - bgpvpn_id: bgpvpn-id-path
   - router_association_id: bgpvpn-router_association_id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - router_association: bgpvpn-router_association
   - id: bgpvpn-router_association_id
   - router_id: bgpvpn-router_id
   - tenant_id: project_id
   - project_id: project_id

Response Example
----------------

.. literalinclude:: samples/bgpvpn/router_associations/router_association-show-response.json
   :language: javascript


Update a Router Association ('bgpvpn-routes-control' extension)
===============================================================

.. note:: This operation is only available when the ``bgpvpn-routes-control``
          API extension is enabled.

.. rest_method::  PUT /v2.0/bgpvpn/bgpvpns/{bgpvpn_id}/router_associations/{router_association_id}

Updates a router association.

Normal response codes: 201

Error response codes: 400, 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - bgpvpn_id: bgpvpn-id-path
   - router_association_id: bgpvpn-router_association_id-path
   - router_association: bgpvpn-router_association
   - advertise_extra_routes: bgpvpn-advertise_extra_routes-request

Request Example
---------------

.. literalinclude:: samples/bgpvpn/router_associations/router_association-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - router_association: bgpvpn-router_association
   - id: bgpvpn-router_association_id
   - router_id: bgpvpn-router_id
   - project_id: project_id
   - advertise_extra_routes: bgpvpn-advertise_extra_routes

Response Example
----------------

.. literalinclude:: samples/bgpvpn/router_associations/router_association-update-response.json
   :language: javascript


Delete Router Association
==========================

.. rest_method::  DELETE /v2.0/bgpvpn/bgpvpns/{bgpvpn_id}/router_associations/{router_association_id}

Deletes a router association.

Normal response codes: 204

Error response codes: 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - bgpvpn_id: bgpvpn-id-path
   - router_association_id: bgpvpn-router_association_id-path

Response
--------

There is no body content for the response of a successful DELETE request.
