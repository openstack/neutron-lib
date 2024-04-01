.. -*- rst -*-
.. needs:method_verification
.. needs:parameter_verification
.. needs:example_verification
.. needs:body_verification

=============================
Service Graph (service_graph)
=============================

Lists, shows information for, creates, updates and deletes Service Graphs.

List Service Graphs
===================

.. rest_method:: GET /v1.0/sfc/service_graphs

Lists service graphs.

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: unauthorized(401), forbidden(403)

Response
--------

.. rest_parameters:: parameters.yaml

  - id: sfc_service_graph_id
  - name: sfc_service_graph_name
  - description: description
  - port_chains: port_chains

Response Example
----------------

**Example List service graphs: JSON response**

.. literalinclude:: samples/sfc-service-graphs/service-graph-list-resp.json
   :language: javascript

Create Service Graph
====================

.. rest_method:: POST /v1.0/sfc/service_graphs

Creates a service graph.

Normal response codes: 200

Error response codes: badRequest(400), unauthorized(401), forbidden(403)

Request
-------

.. rest_parameters:: parameters.yaml

  - name: sfc_service_graph_name
  - description: description
  - port_chains: port_chains

**Example Create service graph: JSON request**

.. literalinclude:: samples/sfc-service-graphs/service-graph-create-req.json
   :language: javascript

Response
--------

.. rest_parameters:: parameters.yaml

  - id: sfc_service_graph_id
  - name: sfc_service_graph_name
  - description: description
  - port_chains: port_chains

Response Example
----------------

**Example Create service graph: JSON response**

.. literalinclude:: samples/sfc-service-graphs/service-graph-create-resp.json
   :language: javascript

Show Service Graph Details
==========================

.. rest_method:: GET /v1.0/sfc/service_graphs/{sfc_service_graph_id-path}

Shows details for a service graph.

.. include:: filtering-show.inc

Normal response codes: 200

Error response codes: badRequest(400), unauthorized(401), forbidden(403), itemNotFound(404)

Request
-------

.. rest_parameters:: parameters.yaml

  - service_graph_id: sfc_service_graph_id-path

Response
--------

.. rest_parameters:: parameters.yaml

  - id: sfc_service_graph_id
  - name: sfc_service_graph_name
  - description: description
  - port_chains: port_chains

Response Example
----------------

**Example Show service graph: JSON response**

.. literalinclude:: samples/sfc-service-graphs/service-graph-get-resp.json
   :language: javascript

Update Service Graph
====================

.. rest_method:: PUT /v1.0/sfc/service_graphs/{sfc_service_graph_id-path}

Updates a service graph.

Normal response codes: 200

Error response codes: badRequest(400), unauthorized(401), forbidden(403), itemNotFound(404)

Request
-------

.. rest_parameters:: parameters.yaml

  - service_graph_id: sfc_service_graph_id-path
  - name: sfc_service_graph_name
  - description: description
  - port_chains: port_chains

Request Example
---------------

**Example Update service graph: JSON request**

.. literalinclude:: samples/sfc-service-graphs/service-graph-update-req.json
   :language: javascript

Response
--------

.. rest_parameters:: parameters.yaml

  - id: sfc_service_graph_id
  - name: sfc_service_graph_name
  - description: description
  - port_chains: port_chains

Response Example
----------------

**Example Update service graph: JSON response**

.. literalinclude:: samples/sfc-service-graphs/service-graph-update-resp.json
   :language: javascript

Delete Service Graph
====================

.. rest_method:: DELETE /v1.0/sfc/service_graphs/{sfc_service_graph_id-path}

Deletes a service graph.

Normal response codes: 202

Error response codes: badRequest(400), unauthorized(401), forbidden(403), itemNotFound(404)

Request
-------

.. rest_parameters:: parameters.yaml

  - service_graph_id: sfc_service_graph_id-path

Response
--------

There is no body content for the response of a successful Delete request.
