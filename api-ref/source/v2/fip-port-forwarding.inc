.. -*- rst -*-

============================
Floating IPs port forwarding
============================

Lists, creates, shows details for, updates, and deletes floating IPs port
forwardings.


Port forwarding with port ranges
=========================================

The ``floating-ip-port-forwarding-port-ranges`` extension adds the new
attributes ``internal_port_range`` and ``external_port_range`` to the
floating IP port forwardings. The value of these new attributes should be
a string that represents a colon separated port range. You can not use the
attributes ``internal_port_range`` and ``external_port_range`` with the
attributes ``internal_port`` and ``external_port`` in the same request.

Port forwarding rule description
=========================================

The ``floating-ip-port-forwarding-description`` extension adds the
``description`` attribute to the floating IP port forwardings.
The value of the ``description`` attribute contains a text describing the rule,
which helps users to manage/find easily theirs rules.

Show port forwarding
====================

.. rest_method::  GET /v2.0/floatingips/{floatingip_id}/port_forwardings/{port_forwarding_id}

Shows information for a floating IP port forwarding.

.. include:: filtering-show.inc

Normal response codes: 200

Error response codes: 400, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - floatingip_id: floatingip-id-path
   - port_forwarding_id: fip_port_forwarding_id-path
   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - port_forwarding: fip_port_forwarding
   - id: fip_port_forwarding_id-body
   - internal_port_id: internal_port_id
   - internal_ip_address: internal_ip_address-response
   - internal_port: internal_port
   - internal_port_range: internal_port_range
   - external_port: external_port
   - external_port_range: external_port_range
   - protocol: fip_port_forwarding_protocol-body
   - description: fip_port_forwarding-description

Response Example
----------------

.. literalinclude:: samples/port_forwardings/port-fowarding-show-response.json
   :language: javascript


Update a port forwarding
========================

.. rest_method::  PUT /v2.0/floatingips/{floatingip_id}/port_forwardings/{port_forwarding_id}

Updates a floating IP port forwarding.

Normal response codes: 200

Error response codes: 400, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - floatingip_id: floatingip-id-path
   - port_forwarding_id: fip_port_forwarding_id-path
   - port_forwarding: fip_port_forwarding
   - internal_port_id: internal_port_id-update
   - internal_ip_address: internal_ip_address
   - internal_port: internal_port-update
   - internal_port_range: internal_port_range
   - external_port: external_port-update
   - external_port_range: external_port_range
   - protocol: fip_port_forwarding_protocol-update

Request Example
---------------

.. literalinclude:: samples/port_forwardings/port-fowarding-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - port_forwarding: fip_port_forwarding
   - id: fip_port_forwarding_id-body
   - internal_port_id: internal_port_id
   - internal_ip_address: internal_ip_address-response
   - internal_port: internal_port
   - internal_port_range: internal_port_range
   - external_port: external_port
   - external_port_range: external_port_range
   - protocol: fip_port_forwarding_protocol-body
   - description: fip_port_forwarding-description

Response Example
----------------

.. literalinclude:: samples/port_forwardings/port-fowarding-update-response.json
   :language: javascript

Delete a floating IP port forwarding
====================================

.. rest_method::  DELETE /v2.0/floatingips/{floatingip_id}/port_forwardings/{port_forwarding_id}

Deletes a floating IP port forwarding.

Normal response codes: 204

Error response codes: 404

Request
-------

.. rest_parameters:: parameters.yaml

   - floatingip_id: floatingip-id-path
   - port_forwarding_id: fip_port_forwarding_id-path

Response
--------

There is no body content for the response of a successful DELETE request.

List floating IP port forwardings
=================================

.. rest_method::  GET /v2.0/floatingips/{floatingip_id}/port_forwardings

Lists floating IP port forwardings that the project has access to.

Default policy settings return only the port forwardings associated to floating
IPs owned by the project of the user submitting the request, unless the
user has administrative role.

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: 400, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - floatingip_id: floatingip-id-path
   - id: id-query
   - internal_port_id: internal_port_id-query
   - external_port: external_port-query
   - external_port_range: external_port_range-query
   - protocol: fip_port_forwarding_protocol-query
   - sort_key: fip_port_forwarding-sort_key
   - sort_dir: sort_dir
   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - port_forwardings: fip_port_forwardings
   - id: fip_port_forwarding_id-body
   - internal_port_id: internal_port_id
   - internal_ip_address: internal_ip_address-response
   - internal_port: internal_port
   - internal_port_range: internal_port_range
   - external_port: external_port
   - external_port_range: external_port_range
   - protocol: fip_port_forwarding_protocol-body
   - description: fip_port_forwarding-description

Response Example
----------------

.. literalinclude:: samples/port_forwardings/port-fowarding-list-response.json
   :language: javascript

Create port forwarding
======================

.. rest_method::  POST /v2.0/floatingips/{floatingip_id}/port_forwardings

Creates a floating IP port forwarding.

Normal response codes: 201

Error response codes: 400, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - floatingip_id: floatingip-id-path
   - port_forwarding: fip_port_forwarding
   - internal_port_id: internal_port_id
   - internal_ip_address: internal_ip_address
   - internal_port: internal_port
   - internal_port_range: internal_port_range
   - external_port: external_port
   - external_port_range: external_port_range
   - protocol: fip_port_forwarding_protocol-body
   - description: fip_port_forwarding-description

Request Example
---------------

.. literalinclude:: samples/port_forwardings/port-fowarding-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - port_forwarding: fip_port_forwarding
   - id: fip_port_forwarding_id-body
   - internal_port_id: internal_port_id
   - internal_ip_address: internal_ip_address-response
   - internal_port: internal_port
   - internal_port_range: internal_port_range
   - external_port: external_port
   - external_port_range: external_port_range
   - protocol: fip_port_forwarding_protocol-body
   - description: fip_port_forwarding-description

Response Example
----------------

.. literalinclude:: samples/port_forwardings/port-fowarding-create-response.json
   :language: javascript
