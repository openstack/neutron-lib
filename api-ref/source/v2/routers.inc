.. -*- rst -*-
.. needs:method_verification
.. needs:parameter_verification
.. needs:example_verification
.. needs:body_verification

=================
Routers (routers)
=================

Routes packets between subnets, forwards packets from internal
networks to external ones, and accesses instances from external
networks through floating IPs.

This extension introduces these resources:

- **router**. A logical entity for forwarding packets across
  internal subnets and NATting them on external networks through an
  appropriate external gateway.

- **floatingip**. An external IP address that you map to a port in
  an internal network.

Add interface to router
=======================

.. rest_method::  PUT /v2.0/routers/{router_id}/add_router_interface

Adds an internal interface to a logical router.

Attaches a subnet to an internal router interface.

Specify the UUID of a subnet or port in the request body:

- Subnet UUID. The gateway IP address for the subnet is used to
  create the router interface.

- Port UUID. The IP address associated with the port is used to
  create the router interface.

When you specify an IPv6 subnet, this operation adds the subnet to
an existing internal port with same network UUID, on the router. If
a port with the same network UUID does not exist, this operation
creates a port on the router for that subnet.

The limitation of one IPv4 subnet per router port remains, though a
port can contain any number of IPv6 subnets that belong to the same
network UUID.

When you use the ``port-create`` command to add a port and then
call ``router-interface-add`` with this port UUID, this operation
adds the port to the router if the following conditions are met:

- The port has no more than one IPv4 subnet.

  The IPv6 subnets, if any, on the port do not have same network
  UUID as the network UUID of IPv6 subnets on any other ports.

If you specify both UUIDs, this operation returns the ``Bad Request
(400)`` response code.

If the port is already in use, this operation returns the
``Conflict (409)`` response code.

This operation returns a port UUID that is either:

- The same UUID that is passed in the request body.

- The UUID of a port that this operation creates to attach the
  subnet to the router.

After you run this operation, the operation sets:

- The device UUID of this port to the router UUID.

- The ``device_owner`` attribute to ``network:router_interface``.

Normal response codes: 200

Error response codes: 404,409,401,400

Request
-------

.. rest_parameters:: parameters.yaml

   - subnet_id: subnet_id
   - port_id: port_id
   - router_id: router_id

Request Example
---------------

.. literalinclude:: samples/routers/router-add-interface-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - subnet_id: subnet_id
   - tenant_id: tenant_id
   - port_id: port_id
   - id: id

Response Example
----------------

.. literalinclude:: samples/routers/router-add-interface-response.json
   :language: javascript

Delete interface from router
============================

.. rest_method::  PUT /v2.0/routers/{router_id}/remove_router_interface

Deletes an internal interface from a logical router.

This operation deletes an internal router interface, which detaches
a subnet from the router. If this subnet UUID is the last subnet on
the port, this operation deletes the port itself. You must specify
either a subnet UUID or port UUID in the request body; the
operation uses this value to identify which router interface to
deletes.

You can also specify both a subnet UUID and port UUID. If you
specify both UUIDs, the subnet UUID must correspond to the subnet
UUID of the first IP address on the port. Otherwise, this operation
returns the ``Conflict (409)`` response code with information about
the affected router and interface.

If the router or the subnet and port do not exist or are not
visible to you, this operation returns the ``Not Found (404)``
response code. As a consequence of this operation, the operation
removes the port connecting the router with the subnet from the
subnet for the network.

This example deletes an interface from a router:

::

   PUT /v2.0/routers/{router_id}/remove_router_interface Accept: application/json

Normal response codes: 200

Error response codes: 404,409,401,400

Request
-------

.. rest_parameters:: parameters.yaml

   - subnet_id: subnet_id
   - port_id: port_id
   - router_id: router_id

Request Example
---------------

.. literalinclude:: samples/routers/router-remove-interface-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - subnet_id: subnet_id
   - tenant_id: tenant_id
   - port_id: port_id
   - id: id

Response Example
----------------

.. literalinclude:: samples/routers/router-remove-interface-response.json
   :language: javascript

Show router details
===================

.. rest_method::  GET /v2.0/routers/{router_id}

Shows details for a router.

This example request shows details for a router in JSON format:

::

   GET /v2.0/routers/{router_id} Accept: application/json

Use the ``fields`` query parameter to control which fields are
returned in the response body. For information, see `Filtering and
Column Selection <http://specs.openstack.org/openstack/neutron-
specs/specs/api/networking_general_api_information.html#filtering-
and-column-selection>`__.

Normal response codes: 200

Error response codes: 404,403,401

Request
-------

.. rest_parameters:: parameters.yaml

   - router_id: router_id

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - external_gateway_info: external_gateway_info
   - status: status
   - availability_zone_hints: availability_zone_hints
   - availability_zones: availability_zones
   - name: name
   - admin_state_up: admin_state_up
   - tenant_id: tenant_id
   - distributed: distributed
   - enable_snat: enable_snat
   - routes: routes
   - router: router
   - ha: ha
   - id: id
   - external_fixed_ips: external_fixed_ips

Response Example
----------------

.. literalinclude:: samples/routers/router-show-response.json
   :language: javascript

Update router
=============

.. rest_method::  PUT /v2.0/routers/{router_id}

Updates a logical router.

You can update the name, administrative state, and the external
gateway. For more information about how to set the external gateway
for a router, see the create router operation. This operation does
not enable the update of router interfaces. To update a router, use
the add router interface and remove router interface operations.

This example updates the external gateway information for a router:

::

   PUT /v2.0/routers/{router_id} Accept: application/json

Normal response codes: 200

Error response codes: 404,401,400

Request
-------

.. rest_parameters:: parameters.yaml

   - external_gateway_info: external_gateway_info
   - enable_snat: enable_snat
   - name: name
   - admin_state_up: admin_state_up
   - router: router
   - external_fixed_ips: external_fixed_ips
   - router_id: router_id

Request Example
---------------

.. literalinclude:: samples/routers/router-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - external_gateway_info: external_gateway_info
   - status: status
   - availability_zone_hints: availability_zone_hints
   - availability_zones: availability_zones
   - name: name
   - admin_state_up: admin_state_up
   - tenant_id: tenant_id
   - distributed: distributed
   - enable_snat: enable_snat
   - routes: routes
   - router: router
   - ha: ha
   - id: id
   - external_fixed_ips: external_fixed_ips

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

This example deletes a router:

::

   DELETE /v2.0/routers/{router_id} Accept: application/json

Error response codes: 409,404,204,401

Request
-------

.. rest_parameters:: parameters.yaml

   - router_id: router_id

List routers
============

.. rest_method::  GET /v2.0/routers

Lists logical routers that the tenant who submits the request can access.

Default policy settings return only those routers that the tenant
who submits the request owns, unless an administrative user submits
the request.

This example request lists routers in JSON format:

::

   GET /v2.0/routers Accept: application/json

Use the ``fields`` query parameter to control which fields are
returned in the response body. Additionally, you can filter results
by using query string parameters. For information, see `Filtering
and Column Selection <https://wiki.openstack.org/wiki/Neutron/APIv2
-specification#Filtering_and_Column_Selection>`__.

Normal response codes: 200

Error response codes: 401

Request
-------

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - external_gateway_info: external_gateway_info
   - status: status
   - availability_zone_hints: availability_zone_hints
   - availability_zones: availability_zones
   - name: name
   - admin_state_up: admin_state_up
   - routers: routers
   - distributed: distributed
   - enable_snat: enable_snat
   - tenant_id: tenant_id
   - routes: routes
   - ha: ha
   - id: id
   - external_fixed_ips: external_fixed_ips

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
external gateway, the UUID of the external network must be passed
in the ``external_gateway_info`` attribute in the request body, as
follows:

.. code-block:: json

   {
      "router": {
         "external_gateway_info": {
            "network_id": "8ca37218-28ff-41cb-9b10-039601ea7e6b"
         }
      }
   }

Error response codes: 201,401,400

Request
-------

.. rest_parameters:: parameters.yaml

   - external_gateway_info: external_gateway_info
   - enable_snat: enable_snat
   - name: name
   - admin_state_up: admin_state_up
   - router: router
   - external_fixed_ips: external_fixed_ips

Request Example
---------------

.. literalinclude:: samples/routers/router-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - external_gateway_info: external_gateway_info
   - status: status
   - availability_zone_hints: availability_zone_hints
   - availability_zones: availability_zones
   - name: name
   - admin_state_up: admin_state_up
   - tenant_id: tenant_id
   - distributed: distributed
   - enable_snat: enable_snat
   - routes: routes
   - router: router
   - ha: ha
   - id: id
   - external_fixed_ips: external_fixed_ips

