.. -*- rst -*-

=================
Routers (routers)
=================

A ``router`` is a logical entity for forwarding packets across
internal subnets and NATting them on external networks through an
appropriate external gateway.

This resource is provided when ``router`` extension is enabled.

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
   - network_id: router-network_id
   - enable_snat: router-enable_snat
   - external_fixed_ips: router-external_fixed_ips
   - revision_number: revision_number
   - routes: router-routes
   - destination: router-destination
   - nexthop: router-nexthop
   - distributed: router-distributed
   - ha: router-ha
   - availability_zone_hints: router-availability_zone_hints
   - availability_zones: router-availability_zones

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
   - network_id: router-network_id
   - enable_snat: router-enable_snat-request
   - external_fixed_ips: router-external_fixed_ips-request
   - distributed: router-distributed-request
   - ha: router-ha-request
   - availability_zone_hints: router-availability_zone_hints-request

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
   - network_id: router-network_id
   - enable_snat: router-enable_snat
   - external_fixed_ips: router-external_fixed_ips
   - revision_number: revision_number
   - routes: router-routes
   - destination: router-destination
   - nexthop: router-nexthop
   - distributed: router-distributed
   - ha: router-ha
   - availability_zone_hints: router-availability_zone_hints
   - availability_zones: router-availability_zones

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
   - network_id: router-network_id
   - enable_snat: router-enable_snat
   - external_fixed_ips: router-external_fixed_ips
   - revision_number: revision_number
   - routes: router-routes
   - destination: router-destination
   - nexthop: router-nexthop
   - distributed: router-distributed
   - ha: router-ha
   - availability_zone_hints: router-availability_zone_hints
   - availability_zones: router-availability_zones

Response Example
----------------

.. literalinclude:: samples/routers/router-show-response.json
   :language: javascript

Update router
=============

.. rest_method::  PUT /v2.0/routers/{router_id}

Updates a logical router.

This operation does not enable the update of router interfaces.
To update a router intreface, use the add router interface and
remove router interface operations.

Normal response codes: 200

Error response codes: 400, 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - router: router
   - external_gateway_info: router-external_gateway_info
   - enable_snat: router-enable_snat
   - name: name
   - admin_state_up: admin_state_up
   - external_fixed_ips: router-external_fixed_ips
   - router_id: router_id
   - description: description-request

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
   - network_id: router-network_id
   - enable_snat: router-enable_snat
   - external_fixed_ips: router-external_fixed_ips
   - revision_number: revision_number
   - routes: router-routes
   - destination: router-destination
   - nexthop: router-nexthop
   - distributed: router-distributed
   - ha: router-ha
   - availability_zone_hints: router-availability_zone_hints
   - availability_zones: router-availability_zones

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

Error response codes: 401, 404, 409

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

Response Example
----------------

.. literalinclude:: samples/routers/router-remove-interface-response.json
   :language: javascript

