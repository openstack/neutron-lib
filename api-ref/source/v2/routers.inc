.. -*- rst -*-

=================
Routers (routers)
=================

A ``router`` is a logical entity for forwarding packets across
internal subnets and NATting them on external networks through an
appropriate external gateway.

This resource is provided when ``router`` extension is enabled.

Distributed virtual router extension
====================================

The ``dvr`` extension enables the functionality of configuring a router as a
distributed virtual router, adding ``distributed`` parameter.

Extra routes extension
======================

The extra route extension (``extraroute``) extends ``router`` resources adding
a ``routes`` attribute that contains an array of route objects. Each route
object has a ``destination`` and ``nexthop`` attribute representing the route.
When the ``extraroute-atomic`` extension is also available you can add
or remove a set of extra routes atomically on the server side. For details
please see below.

.. warning::

    By default in a router there is one route for each attached subnet. If you
    add an extra route that matches one of the default routes for a subnet,
    the existing subnet route will be overwritten.
    If the Neutron route is removed, the corresponding route will be removed
    as well. The affected subnet will subsequently lose connectivity to this
    router.

Extra routes (atomic) extension
===============================

The extra route atomic extension (``extraroute-atomic``) extends the
``router`` resource by adding two member actions (``add_extraroutes`` /
``remove_extraroutes``) to edit the set of extra routes atomically on
the server side.

.. warning::

    By default in a router there is one route for each attached subnet. If you
    add an extra route that matches one of the default routes for a subnet,
    the existing subnet route will be overwritten.
    If the Neutron route is removed, the corresponding route will be removed
    as well. The affected subnet will subsequently lose connectivity to this
    router.

HA capability for router extension (``l3-ha``)
=======================================================

The L3 HA extension ``l3-ha``, adds the ``ha`` attribute which enables
HA capability to routers when set to ``true``.

L3 external gateway mode extension (``ext-gw-mode``)
=======================================================

The ``ext-gw-mode`` extension of the router abstraction for specifying whether
SNAT should occur on the external gateway.
The ``ext-gw-mode`` extension allows enabling configurable external gateway
modes, adds the ``external_gateway_info`` attribute to ``routers``
and allows definitions for ``network_id``, ``enable_snat`` and
``external_fixed_ips``.

L3 flavors extension (``l3-flavors``)
=====================================

The router flavor extension (``l3-flavors``) adds the ``flavor_id`` attribute
to routers, allowing requests to be dispatched to different drivers depending
on the flavor associated with a given router.

Resource timestamps
===================

The ``standard-attr-timestamp`` extension adds the ``created_at`` and
``updated_at`` attributes to all resources that have standard attributes.

Router admin state down before update extension
===============================================

The ``router-admin-state-down-before-update`` extension adds the requirement
that the administrative state of a distributed virtual router (DVR) be set to
DOWN (``admin_state_up=False``) prior to modifying the ``distributed``
parameter of the router. The API will return an error response code of 400 if
the router's ``distributed`` attribute is modified without first setting the
router's ``admin_state_up=False``.
This extension requires the ``dvr`` extension.

Router availability zone extension
==================================

The ``router_availability_zone`` extension adds the ``availability_zones``
and ``availability_zone_hints`` attributes to ``routers``, allowing scheduling
based on availability zones and hints.
This extension requires ``router`` and ``availability_zone`` extensions.

Router service type extension (``router-service-type``)
=======================================================

The ``router-service-type`` extension enables associating a service type with a
router by introducing the ``service_type_id`` parameter that can be
used to associate the router with an existing ``service-provider``,
see `Service providers`_.

Tag extension
=============

The ``standard-attr-tag`` adds Tag support for resources with
standard attributes by adding the ``tags`` attribute
allowing consumers to associate tags with resources.

L3 conntrack helpers extension (``expose-l3-conntrack-helper``)
===============================================================

The router conntrack helper extension (``expose-l3-conntrack-helper``) adds the
``conntrack_helpers`` field to routers, allowing configurable netfilter CT
target rules for ``routers``.


List routers
============

.. rest_method::  GET /v2.0/routers

Lists logical routers that the project who submits the request can access.

Default policy settings return only those routers that the project
who submits the request owns, unless an administrative user submits
the request.

Use the ``fields`` query parameter to control which fields are
returned in the response body. Additionally, you can filter results
by using query string parameters. For information, see `Filtering
and Column Selection <https://wiki.openstack.org/wiki/Neutron/APIv2
-specification#Filtering_and_Column_Selection>`__.

Normal response codes: 200

Error response codes: 401

Request
-------

.. rest_parameters:: parameters.yaml

   - id: id-query
   - tenant_id: project_id-query
   - project_id: project_id-query
   - name: name-query
   - description: description-query
   - admin_state_up: admin_state_up-query
   - revision_number: revision_number-query
   - sort_dir: sort_dir
   - sort_key: router-sort_key
   - tags: tags-query
   - tags-any: tags-any-query
   - not-tags: not-tags-query
   - not-tags-any: not-tags-any-query
   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - routers: routers
   - id: router-id-body
   - tenant_id: project_id
   - project_id: project_id
   - name: name
   - description: description
   - admin_state_up: admin_state_up
   - status: router-status
   - external_gateway_info: router-external_gateway_info
   - revision_number: revision_number
   - routes: router-routes
   - destination: router-destination
   - nexthop: router-nexthop
   - distributed: router-distributed
   - ha: router-ha
   - availability_zone_hints: router-availability_zone_hints
   - availability_zones: router-availability_zones
   - service_type_id: router-service_type_id
   - flavor_id: router-flavor_id
   - created_at: created_at_resource
   - updated_at: updated_at_resource
   - tags: tags
   - conntrack_helpers: router-conntrack_helpers

Response Example
----------------

.. literalinclude:: samples/routers/routers-list-response.json
   :language: javascript

Create router
=============

.. rest_method::  POST /v2.0/routers

Creates a logical router.

This operation creates a logical router. The logical router does
not have any internal interface and it is not associated with any
subnet. You can optionally specify an external gateway for a router
at create time. The external gateway for the router must be plugged
into an external network. An external network has its
``router:external`` extended field set to ``true``. To specify an
external gateway, the ID of the external network must be passed
in the ``network_id`` parameter of the ``external_gateway_info``
attribute in the request body.

Normal response codes: 201

Error response codes: 400, 401

Request
-------

.. rest_parameters:: parameters.yaml

   - router: router
   - tenant_id: project_id-request
   - project_id: project_id-request
   - name: name-request
   - description: description-request
   - admin_state_up: admin_state_up-request
   - external_gateway_info: router-external_gateway_info-request
   - distributed: router-distributed-request
   - ha: router-ha-request
   - availability_zone_hints: router-availability_zone_hints-request
   - service_type_id: router-service_type_id-request
   - flavor_id: router-flavor_id-optional

Request Example
---------------

.. literalinclude:: samples/routers/router-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - router: router
   - id: router-id-body
   - tenant_id: project_id
   - project_id: project_id
   - name: name
   - description: description
   - admin_state_up: admin_state_up
   - status: router-status
   - external_gateway_info: router-external_gateway_info
   - revision_number: revision_number
   - routes: router-routes
   - destination: router-destination
   - nexthop: router-nexthop
   - distributed: router-distributed
   - ha: router-ha
   - availability_zone_hints: router-availability_zone_hints
   - availability_zones: router-availability_zones
   - service_type_id: router-service_type_id
   - flavor_id: router-flavor_id
   - created_at: created_at_resource
   - updated_at: updated_at_resource
   - tags: tags
   - conntrack_helpers: router-conntrack_helpers

Response Example
----------------

.. literalinclude:: samples/routers/router-create-response.json
   :language: javascript

Show router details
===================

.. rest_method::  GET /v2.0/routers/{router_id}

Shows details for a router.

Use the ``fields`` query parameter to control which fields are
returned in the response body. For information, see `Filtering and
Column Selection <http://specs.openstack.org/openstack/neutron-
specs/specs/api/networking_general_api_information.html#filtering-
and-column-selection>`__.

Normal response codes: 200

Error response codes: 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - router_id: router_id
   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - router: router
   - id: router-id-body
   - tenant_id: project_id
   - project_id: project_id
   - name: name
   - description: description
   - admin_state_up: admin_state_up
   - status: router-status
   - external_gateway_info: router-external_gateway_info
   - revision_number: revision_number
   - routes: router-routes
   - destination: router-destination
   - nexthop: router-nexthop
   - distributed: router-distributed
   - ha: router-ha
   - availability_zone_hints: router-availability_zone_hints
   - availability_zones: router-availability_zones
   - service_type_id: router-service_type_id
   - flavor_id: router-flavor_id
   - created_at: created_at_resource
   - updated_at: updated_at_resource
   - tags: tags
   - conntrack_helpers: router-conntrack_helpers

Response Example
----------------

.. literalinclude:: samples/routers/router-show-response.json
   :language: javascript

Update router
=============

.. rest_method::  PUT /v2.0/routers/{router_id}

Updates a logical router.

This operation does not enable the update of router interfaces.
To update a router interface, use the add router interface and
remove router interface operations.

Normal response codes: 200

Error response codes: 400, 401, 404, 412

Request
-------

.. rest_parameters:: parameters.yaml

   - router: router
   - external_gateway_info: router-external_gateway_info-request
   - ha: router-ha-request
   - name: name
   - admin_state_up: admin_state_up
   - router_id: router_id
   - description: description-request
   - routes: router-routes-request
   - distributed: router-distributed-request

Request Example
---------------

.. literalinclude:: samples/routers/router-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - router: router
   - id: router-id-body
   - tenant_id: project_id
   - project_id: project_id
   - name: name
   - description: description
   - admin_state_up: admin_state_up
   - status: router-status
   - external_gateway_info: router-external_gateway_info
   - revision_number: revision_number
   - routes: router-routes
   - destination: router-destination
   - nexthop: router-nexthop
   - distributed: router-distributed
   - ha: router-ha
   - availability_zone_hints: router-availability_zone_hints
   - availability_zones: router-availability_zones
   - service_type_id: router-service_type_id
   - flavor_id: router-flavor_id
   - created_at: created_at_resource
   - updated_at: updated_at_resource
   - tags: tags
   - conntrack_helpers: router-conntrack_helpers

Response Example
----------------

.. literalinclude:: samples/routers/router-update-response.json
   :language: javascript

Delete router
=============

.. rest_method::  DELETE /v2.0/routers/{router_id}

Deletes a logical router and, if present, its external gateway interface.

This operation fails if the router has attached interfaces.
Use the remove router interface operation to remove all router
interfaces before you delete the router.

Normal response codes: 204

Error response codes: 401, 404, 409, 412

Request
-------

.. rest_parameters:: parameters.yaml

   - router_id: router_id

Response
--------

There is no body content for the response of a successful DELETE request.

Add interface to router
=======================

.. rest_method::  PUT /v2.0/routers/{router_id}/add_router_interface

Adds an internal interface to a logical router.
This means a specified subnet is attached to a router
as an internal router interface.

Specify the ID of a subnet or port in the request body:

- Subnet ID. The gateway IP address for the subnet is used as
  an IP address of the created router interface.

- Port ID. The IP address associated with the port is used as
  an IP address of the created router interface.

When you specify an IPv6 subnet, this operation adds the subnet to
an existing internal port with same network ID, on the router. If
a port with the same network ID does not exist, this operation
creates a port on the router for that subnet.

The limitation of one IPv4 subnet per router port remains, though a
port can contain any number of IPv6 subnets that belong to the same
network ID.

When you use the ``port-create`` command to add a port and then
call ``router-interface-add`` with this port ID, this operation
adds the port to the router if the following conditions are met:

- The port has no more than one IPv4 subnet.
- The IPv6 subnets, if any, on the port do not have same network
  ID as the network ID of IPv6 subnets on any other ports.

If you specify both subnet ID and port ID,
this operation returns the ``Bad Request (400)`` response code.

If the port is already in use, this operation returns the
``Conflict (409)`` response code.

This operation returns a port ID that is either:

- The same ID that is passed in the request body
  when a port is specified.
- The ID of a port that this operation creates to attach the
  subnet to the router.

After you run this operation, the operation sets:

- The ``device_id`` attribute of this port to the router ID
- The ``device_owner`` attribute to ``network:router_interface``

Normal response codes: 200

Error response codes: 400, 401, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - router_id: router_id
   - subnet_id: router-subnet_id-request
   - port_id: router-port_id-request

Request Example
---------------

.. literalinclude:: samples/routers/router-add-interface-request.json
   :language: javascript

or

.. literalinclude:: samples/routers/router-add-interface-request-with-port.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - id: router-id-body
   - subnet_id: router-subnet_id
   - subnet_ids: router-subnet_ids
   - tenant_id: router-project_id-interface
   - project_id: router-project_id-interface
   - port_id: router-port_id
   - network_id: router-network_id-interface
   - tags: tags

Response Example
----------------

.. literalinclude:: samples/routers/router-add-interface-response.json
   :language: javascript

Remove interface from router
============================

.. rest_method::  PUT /v2.0/routers/{router_id}/remove_router_interface

Deletes an internal interface from a logical router.

This operation deletes an internal router interface, which detaches
a subnet from the router. If this subnet ID is the last subnet on
the port, this operation deletes the port itself. You must specify
either a subnet ID or port ID in the request body; the
operation uses this value to identify which router interface to
deletes.

You can also specify both a subnet ID and port ID. If you
specify both IDs, the subnet ID must correspond to the subnet
ID of the first IP address on the port. Otherwise, this operation
returns the ``Conflict (409)`` response code with information about
the affected router and interface.

If you try to delete the router interface for subnets that are used
by one or more ``routes``, this operation returns the ``Conflict (409)``
response. In this case, you first need to delete such routes from
the router.

If the router or the subnet and port do not exist or are not
visible to you, this operation returns the ``Not Found (404)``
response code. As a consequence of this operation, the operation
removes the port connecting the router with the subnet from the
subnet for the network.

Normal response codes: 200

Error response codes: 400, 401, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - router_id: router_id
   - subnet_id: router-subnet_id-request
   - port_id: router-port_id-request

Request Example
---------------

.. literalinclude:: samples/routers/router-remove-interface-request.json
   :language: javascript

or

.. literalinclude:: samples/routers/router-remove-interface-request-with-port.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - id: router-id-body
   - subnet_id: router-subnet_id
   - subnet_ids: router-subnet_ids
   - tenant_id: router-project_id-interface
   - project_id: router-project_id-interface
   - port_id: router-port_id
   - network_id: router-network_id-interface
   - tags: tags

Response Example
----------------

.. literalinclude:: samples/routers/router-remove-interface-response.json
   :language: javascript

Add extra routes to router
==========================

.. rest_method::  PUT /v2.0/routers/{router_id}/add_extraroutes

Atomically adds a set of extra routes to the router's already existing
extra routes.

This operation is a variation on updating the router's ``routes``
parameter.  In all ways it works the same, except the extra routes sent
in the request body do not replace the existing set of extra routes.
Instead the extra routes sent are added to the existing set of
extra routes.

The use of the add_extraroutes/remove_extraroutes member actions
is preferred to updating the ``routes`` attribute in all cases when
concurrent updates to the set of extra routes are possible.

The addition's corner cases behave the following way:

* When (destinationA, nexthopA) is to be added but it is already present
  that is accepted and the request succeeds.

* Two or more routes with the same destination but with different
  nexthops are all accepted.

* A route whose destination overlaps the destination of existing routes
  (e.g. ``192.168.1.0/24`` and ``192.168.1.0/22``) can be added and
  existing routes are left untouched.

The format of the request body is the same as the format of a PUT
request to the router changing the ``routes`` parameter only.

The response codes and response body are the same as to the update of
the ``routes`` parameter. That is the whole router object is returned
including the ``routes`` parameter which represents the result of the
addition.

Normal response codes: 200

Error response codes: 400, 401, 404, 412

Request
-------

.. rest_parameters:: parameters.yaml

   - router_id: router_id
   - routes: router-routes

Request Example
---------------

.. literalinclude:: samples/routers/router-add-extraroutes-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - id: router-id-body
   - name: router_name
   - routes: router-routes

Response Example
----------------

.. literalinclude:: samples/routers/router-add-extraroutes-response.json
   :language: javascript

Remove extra routes from router
===============================

.. rest_method::  PUT /v2.0/routers/{router_id}/remove_extraroutes

Atomically removes a set of extra routes from the router's already
existing extra routes.

This operation is a variation on updating the router's ``routes``
parameter.  In all ways it works the same, except the extra routes sent
in the request body do not replace the existing set of extra routes.
Instead the the extra routes sent are removed from the existing set of
extra routes.

The use of the add_extraroutes/remove_extraroutes member actions
is preferred to updating the ``routes`` attribute in all cases when
concurrent updates to the set of extra routes are possible.

The removal's corner cases behave the following way:

* An extra route is only removed if there is an exact match (including the
  ``destination`` and ``nexthop``) between the route sent and the route
  already present.

* When (destinationA, nexthopA) is to be removed but it is already missing
  that is accepted and the request succeeds.

The format of the request body is the same as the format of a PUT
request to the router changing the ``routes`` parameter only. However
the routes sent are not meant to overwrite the whole ``routes``
parameter, but they are meant to be removed from the existing set.

The response codes and response body are the same as to the update of
the ``routes`` parameter. That is the whole router object is returned
including the ``routes`` parameter which represents the result of the
removal.

Normal response codes: 200

Error response codes: 400, 401, 404, 412

Request
-------

.. rest_parameters:: parameters.yaml

   - router_id: router_id
   - routes: router-routes

Request Example
---------------

.. literalinclude:: samples/routers/router-remove-extraroutes-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - id: router-id-body
   - name: router_name
   - routes: router-routes

Response Example
----------------

.. literalinclude:: samples/routers/router-remove-extraroutes-response.json
   :language: javascript
