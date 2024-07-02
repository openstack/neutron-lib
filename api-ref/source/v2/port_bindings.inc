.. -*- rst -*-

============
Port Binding
============

Expose port bindings of a virtual port to external application.

Port Bindings Extended
======================

The ``Port Bindings Extended`` extension adds extra fields to ``Port Binding``
like ``status`` and ``project id``, and allows the ``activation`` of the
binding.

Show Port Binding of a Port
===========================

.. rest_method:: GET /v2.0/ports/{port_id}/bindings

.. include:: filtering-show.inc

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

    - port_id: port_id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

    - bindings: bindings
    - host: host
    - profile: binding:profile
    - vif_details: binding:vif_details
    - vif_type: binding:vif_type
    - vnic_type: binding:vnic_type

Response Example (Admin user)
-----------------------------

.. literalinclude:: samples/port_bindings/port-binding-list-response.json
   :language: javascript

Create Port binding
===================

.. rest_method:: POST /v2.0/ports/{port_id}/bindings/

Normal response codes: 201

Error response codes: 400, 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - port_id: port_id-path
   - bindings: bindings
   - host: host
   - profile: binding:profile
   - vif_details: binding:vif_details
   - vif_type: binding:vif_type
   - vnic_type: binding:vnic_type

Request Example (Admin user)
----------------------------

.. literalinclude:: samples/port_bindings/port-binding-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - port_id: port_id-path
   - bindings: bindings
   - host: host
   - profile: binding:profile
   - vif_details: binding:vif_details
   - vif_type: binding:vif_type
   - vnic_type: binding:vnic_type

Response Example (admin user)
-----------------------------

.. literalinclude:: samples/port_bindings/port-binding-create-response.json
   :language: javascript

Activate Port binding
=====================

.. rest_method:: PUT /v2.0/ports/{port_id}/bindings/{host}/activate

Normal response codes: 200

Error response codes: 400, 401, 404, 412

Request
-------

.. rest_parameters:: parameters.yaml

   - port_id: port_id-path
   - host: host

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - port_id: port_id-path
   - bindings: bindings
   - host: host
   - profile: binding:profile
   - vif_details: binding:vif_details
   - vif_type: binding:vif_type
   - vnic_type: binding:vnic_type

Response Example (admin user)
-----------------------------

.. literalinclude:: samples/port_bindings/port-binding-activate-response.json
   :language: javascript

Delete Port Binding
===================

.. rest_method:: DELETE /v2.0/ports/{port_id}/bindings/{host}

Normal response codes: 204

Error response codes: 401, 403, 404, 412

Request
-------

.. rest_parameters:: parameters.yaml

   - port_id: port_id-path
   - host: host

Response
--------

There is no body content for the response of a successful DELETE request.

