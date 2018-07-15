==========================
Floating IPs (floatingips)
==========================

DNS integration
===============

The ``dns-integration`` extension adds the ``dns_name`` and ``dns_domain``
attributes to floating IPs allowing them to be specified at creation time.
The data in these attributes will be published in an external DNS service
when Neutron is configured to integrate with such a service.

Floating IP port details
========================

The ``fip-port-details`` extension adds the ``port_details`` attribute to
floating IPs. The value of this attribute contains information of the
associated port.

Floating IP port forwardings
============================

The ``expose-port-forwarding-in-fip`` extension adds the ``port_forwardings``
attribute to floating IPs. The value of this attribute contains the
information of associated port forwarding resources.

Resource timestamps
===================

The ``standard-attr-timestamp`` extension adds the ``created_at`` and
``updated_at`` attributes to all resources that have standard attributes.

Tag extension
=============

The ``standard-attr-tag`` adds Tag support for resources with
standard attributes by adding the ``tags`` attribute
allowing consumers to associate tags with resources.

List floating IPs
=================

.. rest_method::  GET /v2.0/floatingips

Lists floating IPs visible to the user.

Default policy settings return only the floating IPs owned by the user's
project, unless the user has admin role.

This example request lists floating IPs in JSON format:

::

   GET /v2.0/floatingips
   Accept: application/json

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
   - router_id: floatingip-router_id-query
   - status: floatingip-status-query
   - tenant_id: project_id-query
   - project_id: project_id-query
   - revision_number: revision_number-query
   - description: description-query
   - floating_network_id: floating_network_id-query
   - fixed_ip_address: floatingip-fixed_ip_address-query
   - floating_ip_address: floating_ip_address-query
   - port_id: floatingip-port_id-query
   - sort_dir: sort_dir
   - sort_key: floatingip-sort_key
   - tags: tags-query
   - tags-any: tags-any-query
   - not-tags: not-tags-query
   - not-tags-any: not-tags-any-query
   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - floatingips: floatingips
   - id: floatingip-id
   - router_id: floatingip-router_id
   - status: floatingip-status
   - tenant_id: project_id
   - project_id: project_id
   - created_at: created_at_resource
   - updated_at: updated_at_resource
   - revision_number: revision_number
   - description: description
   - dns_domain: dns_domain
   - dns_name: dns_name
   - port_details: floating_port_details
   - floating_network_id: floating_network_id
   - fixed_ip_address: floatingip-fixed_ip_address
   - floating_ip_address: floating_ip_address
   - port_id: floatingip-port_id
   - tags: tags
   - port_forwardings: floatingip-port_forwardings

Response Example
----------------

.. literalinclude:: samples/floatingips/floating-ips-list-response.json
   :language: javascript

Create floating IP
==================

.. rest_method::  POST /v2.0/floatingips

Creates a floating IP, and, if you specify port information, associates the floating IP with an internal port.

To associate the floating IP with an internal port, specify the
port ID attribute in the request body. If you do not specify a
port ID in the request, you can issue a PUT request instead of a
POST request.

Default policy settings enable only administrative users to set
floating IP addresses and some non-administrative users might
require a floating IP address. If you do not specify a floating IP
address in the request, the operation automatically allocates one.

By default, this operation associates the floating IP address with
a single fixed IP address that is configured on an OpenStack
Networking port. If a port has multiple IP addresses, you must
specify the ``fixed_ip_address`` attribute in the request body to
associate a fixed IP address with the floating IP address.

You can create floating IPs on only external networks. When you
create a floating IP, you must specify the ID of the network on
which you want to create the floating IP. Alternatively, you can
create a floating IP on a subnet in the external network, based on
the costs and quality of that subnet.

You must configure an IP address with the internal OpenStack
Networking port that is associated with the floating IP address.

The operation returns the ``Bad Request (400)`` response code for one of
reasons:

  - The network is not external, such as ``router:external=False``.

  - The internal OpenStack Networking port is not associated with the
    floating IP address.

  - The requested floating IP address does not fall in the subnet
    range for the external network.

  - The fixed IP address is not valid.

If the port ID is not valid, this operation returns ``404`` response code.

The operation returns the ``Conflict (409)`` response code for one of
reasons:

  - The requested floating IP address is already in use.

  - The internal OpenStack Networking port and fixed IP address are
    already associated with another floating IP.

Normal response codes: 201

Error response codes: 400, 401, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - floatingip: floatingip
   - tenant_id: project_id
   - project_id: project_id
   - floating_network_id: floating_network_id
   - fixed_ip_address: floatingip-fixed_ip_address-request
   - floating_ip_address: floating_ip_address-request
   - port_id: floatingip-port_id-post-request
   - subnet_id: floatingip-subnet_id
   - description: description-request
   - dns_domain: dns_domain-request
   - dns_name: dns_name-request

Request Example
---------------

.. literalinclude:: samples/floatingips/floatingip-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - floatingip: floatingip
   - router_id: floatingip-router_id
   - status: floatingip-status
   - description: description
   - dns_domain: dns_domain
   - dns_name: dns_name
   - port_details: floating_port_details
   - tenant_id: project_id
   - created_at: created_at_resource
   - updated_at: updated_at_resource
   - revision_number: revision_number
   - project_id: project_id
   - floating_network_id: floating_network_id
   - fixed_ip_address: floatingip-fixed_ip_address
   - floating_ip_address: floating_ip_address
   - port_id: floatingip-port_id
   - id: floatingip-id
   - tags: tags
   - port_forwardings: floatingip-port_forwardings

Response Example
----------------

.. literalinclude:: samples/floatingips/floatingip-create-response.json
   :language: javascript

Show floating IP details
========================

.. rest_method::  GET /v2.0/floatingips/{floatingip_id}

Shows details for a floating IP.

Use the ``fields`` query parameter to control which fields are
returned in the response body. For information, see `Filtering and
Column Selection <http://specs.openstack.org/openstack /neutron-
specs/specs/api/networking_general_api_information.html #filtering-
and-column-selection>`__.

This example request shows details for a floating IP in JSON
format. This example also filters the result by the
``fixed_ip_address`` and ``floating_ip_address`` fields.

::

   GET /v2.0/floatingips/{floatingip_id}?fields=fixed_ip_address
   &
   fields=floating_ip_address
   Accept: application/json

Normal response codes: 200

Error response codes: 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - floatingip_id: floatingip-id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - floatingip: floatingip
   - router_id: floatingip-router_id
   - status: floatingip-status
   - description: description
   - dns_domain: dns_domain
   - dns_name: dns_name
   - port_details: floating_port_details
   - tenant_id: project_id
   - created_at: created_at_resource
   - updated_at: updated_at_resource
   - revision_number: revision_number
   - project_id: project_id
   - floating_network_id: floating_network_id
   - fixed_ip_address: floatingip-fixed_ip_address
   - floating_ip_address: floating_ip_address
   - port_id: floatingip-port_id
   - id: floatingip-id
   - tags: tags
   - port_forwardings: floatingip-port_forwardings

Response Example
----------------

.. literalinclude:: samples/floatingips/floatingip-show-response.json
   :language: javascript

Update floating IP
==================

.. rest_method::  PUT /v2.0/floatingips/{floatingip_id}

Updates a floating IP and its association with an internal port.

The association process is the same as the process for the create
floating IP operation.

To disassociate a floating IP from a port, set the ``port_id``
attribute to null or omit it from the request body.

This example updates a floating IP:

::

   PUT /v2.0/floatingips/{floatingip_id} Accept: application/json

Depending on the request body that you submit, this request
associates a port with or disassociates a port from a floating IP.

Normal response codes: 200

Error response codes: 400, 401, 404, 409, 412

Request
-------

.. rest_parameters:: parameters.yaml

   - floatingip: floatingip
   - floatingip_id: floatingip-id-path
   - port_id: floatingip-port_id-put-request
   - fixed_ip_address: floatingip-fixed_ip_address-request
   - description: description-request

Request Example
---------------

.. literalinclude:: samples/floatingips/floatingip-update-request.json
   :language: javascript

Request Example (disassociate)
------------------------------

.. literalinclude:: samples/floatingips/floatingip-disassociate-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - floatingip: floatingip
   - router_id: floatingip-router_id
   - status: floatingip-status
   - tenant_id: project_id
   - project_id: project_id
   - floating_network_id: floating_network_id
   - fixed_ip_address: floatingip-fixed_ip_address
   - floating_ip_address: floating_ip_address
   - port_id: floatingip-port_id
   - id: floatingip-id
   - created_at: created_at_resource
   - updated_at: updated_at_resource
   - revision_number: revision_number
   - description: description
   - dns_domain: dns_domain
   - dns_name: dns_name
   - port_details: floating_port_details
   - tags: tags
   - port_forwardings: floatingip-port_forwardings

Response Example
----------------

.. literalinclude:: samples/floatingips/floatingip-update-response.json
   :language: javascript

Response Example (disassociate)
-------------------------------

.. literalinclude:: samples/floatingips/floatingip-disassociate-response.json
   :language: javascript

Delete floating IP
==================

.. rest_method::  DELETE /v2.0/floatingips/{floatingip_id}

Deletes a floating IP and, if present, its associated port.

This example deletes a floating IP:

::

   DELETE /v2.0/floatingips/{floatingip_id} Accept: application/json

Normal response codes: 204

Error response codes: 401, 404, 412

Request
-------

.. rest_parameters:: parameters.yaml

   - floatingip_id: floatingip-id-path

Response
--------

There is no body content for the response of a successful DELETE request.
