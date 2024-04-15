.. -*- rst -*-

==========================================
Routers Conntrack Helper (CT) target rules
==========================================

Lists, creates, shows details for, updates, and deletes router conntrack helper
(CT) target rules.

Show conntrack helper
=====================

.. rest_method:: GET /v2.0/routers/{router_id}/conntrack_helpers/{conntrack_helper_id}

Shows information for a router conntrack helper.

.. include:: filtering-show.inc

Normal response codes: 200

Error response codes: 400, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - router_id: router_id
   - conntrack_helper_id: conntrack_helper_id-path
   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - conntrack_helper: conntrack_helper
   - helper: conntrack_helper_helper-body
   - id: conntrack_helper_id-body
   - protocol: conntrack_helper_protocol-body
   - port: conntrack_helper_port-body

Response Example
----------------

.. literalinclude:: samples/conntrack_helpers/conntrack-helper-show-response.json
   :language: javascript

Update a conntrack helper
=========================

.. rest_method:: PUT /v2.0/routers/{router_id}/conntrack_helpers/{conntrack_helper_id}

Updates a router conntrack helper.

Normal response codes: 200

Error response codes: 400, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - router_id: router_id
   - conntrack_helper_id: conntrack_helper_id-path
   - helper: conntrack_helper_helper-update
   - protocol: conntrack_helper_protocol-update
   - port: conntrack_helper_port-update


Request Example
---------------

.. literalinclude:: samples/conntrack_helpers/conntrack-helper-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - conntrack_helper: conntrack_helper
   - id: conntrack_helper_id-body
   - helper: conntrack_helper_helper-body
   - protocol: conntrack_helper_protocol-body
   - port: conntrack_helper_port-body

Response Example
----------------

.. literalinclude:: samples/conntrack_helpers/conntrack-helper-update-response.json
   :language: javascript

Delete a conntrack helper
=========================

.. rest_method:: DELETE /v2.0/routers/{router_id}/conntrack_helpers/{conntrack_helper_id}

Deletes a router conntrack helper.

Normal response codes: 204

Error response codes: 404

Request
-------

.. rest_parameters:: parameters.yaml

   - router_id: router_id
   - conntrack_helper_id: conntrack_helper_id-path

Response
--------

There is no body content for the response of a successful DELETE request.

List router conntrack helpers
=============================

.. rest_method:: GET /v2.0/routers/{router_id}/conntrack_helpers

Lists router conntrack helpers associated with a router.

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: 400, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - router_id: router_id
   - id: id-query
   - helper: conntrack_helper_helper-query
   - protocol: conntrack_helper_protocol-query
   - port: conntrack_helper_port-query
   - sort_key: conntrack_helper-sort_key
   - sort_dir: sort_dir
   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - conntrack_helpers: conntrack_helpers
   - id: conntrack_helper_id-body
   - helper: conntrack_helper_helper-body
   - protocol: conntrack_helper_protocol-body
   - port: conntrack_helper_port-body

Response Example
----------------

.. literalinclude:: samples/conntrack_helpers/conntrack-helper-list-response.json
   :language: javascript

Create conntrack helper
=======================

.. rest_method::  POST /v2.0/routers/{router_id}/conntrack_helpers

Creates a router conntrack helper.

Normal response codes: 201

Error response codes: 400, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - conntrack_helper: conntrack_helper
   - router_id: router_id
   - helper: conntrack_helper_helper-body
   - protocol: conntrack_helper_protocol-body
   - port: conntrack_helper_port-body


Request Example
---------------

.. literalinclude:: samples/conntrack_helpers/conntrack-helper-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - conntrack_helper: conntrack_helper
   - id: conntrack_helper_id-body
   - helper: conntrack_helper_helper-body
   - protocol: conntrack_helper_protocol-body
   - port: conntrack_helper_port-body

Response Example
----------------

.. literalinclude:: samples/conntrack_helpers/conntrack-helper-create-response.json
   :language: javascript
