.. -*- rst -*-

================
Tap As A Service
================

TaaS plugin provides a mechanism to mirror certain traffic
(for example tagged with specific VLANs) from a source VM to any traffic analyzer VM.
When packet will be forwarded, the original value of source and target ip/ports
information will not be altered and the system administrator will be able to run,
for ex. ``tcpdump``, on the target VM to trace these packets.

TaaS plugin mainly consists of ``tap service`` and ``tap flow``.

VLAN filter
===========

The ``VLAN filtering`` for Neutron Tap as a Service allows to filter
traffic comming from ``tap-flows`` by VLAN id in case of mirroring SRIOV
ports.

Tap Service
===========

TapService represents the port to which the mirrored traffic is delivered.

List Tap Services
=================

.. rest_method:: GET /v2.0/taas/tap_services

List tap services that belong to a given project.

The list might be empty.

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: 401

Request Parameters
------------------

.. rest_parameters:: parameters.yaml

   - project: project_id-query
   - project-domain: project-domain_taas

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - id: tas_id
   - tenant_id: project_id
   - port: mirror_port_tas
   - status: status_tas

Response Example
----------------

.. literalinclude:: samples/taas/tas-list-response.json
   :language: javascript

Create Tap Service
==================

.. rest_method:: POST /v2.0/taas/tap_services

Create a Tap Service by passing the following JSON-encoded data.
``name``, ``monitoring port`` as mandatory parameters and
``description`` as optional parameter.

Normal response codes: 201

Error response codes: 401, 403, 404, 409

Request Parameters
------------------

.. rest_parameters:: parameters.yaml

   - project: project_id-query
   - project-domain: project-domain_taas
   - tenant_id: project_id-query
   - name: tas_name-query
   - port: mirror_port_tas-query
   - description: description_tas-query

Request Example
---------------

.. literalinclude:: samples/taas/tas-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - id: tas_id
   - tenant_id: project_id
   - name: tas_name
   - port: mirror_port_tas
   - status: status_tas
   - description: description_tas
   - project_id: project_id

Response Example
----------------

.. literalinclude:: samples/taas/tas-create-response.json
   :language: javascript

Update Tap Service
==================

.. rest_method:: PUT /v2.0/taas/tap_services/{tap_service_id/name}

Update Tap Service by passing tap service ``name`` or ``id`` as JSON-encoded data.
Name or description or both can only be updated.

Normal response codes: 200

Error response codes: 400, 401, 404, 412

Request Parameters
------------------

.. rest_parameters:: parameters.yaml

   - name: tas_name-query
   - description: description_tas-query

Request Example
---------------

.. literalinclude:: samples/taas/tas-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - id: tas_id
   - name: tas_name
   - port: mirror_port_tas
   - status: status_tas
   - description: description_tas
   - project_id: project_id

Response Example
----------------

.. literalinclude:: samples/taas/tas-update-response.json
   :language: javascript

Delete Tap Service
==================

.. rest_method:: DELETE /v2.0/taas/tap_services/{tap_service_id/name}

Delete Tap Service by passing tap service ``name`` or ``id`` as JSON-encoded data.

Normal response codes: 204

Error response codes: 400, 401, 404, 412

Request Parameters
------------------

.. rest_parameters:: parameters.yaml

   - name: tas_name-query
   - id: tas_id-query

Response Parameters
-------------------

There is no body content for the response of a successful DELETE request.

Show Tap Service
================

.. rest_method:: GET /v2.0/taas/tap_services/{tap_service_id/name}

Show details for a tap service by passing tap service ``name`` or ``id`` as JSON-encoded data.

.. include:: filtering-show.inc

Normal response codes: 200

Error response codes: 401, 404

Request Parameters
------------------

.. rest_parameters:: parameters.yaml

   - project: project_id-query
   - project-domain: project-domain_taas
   - name: tas_name-query

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - id: tas_id
   - name: tas_name
   - port: mirror_port_tas
   - status: status_tas
   - description: description_tas
   - project_id: project_id
   - tenant_id: project_id

Response Example
----------------

.. literalinclude:: samples/taas/tas-show-response.json
   :language: javascript


Tap Flow
========

TapFlow represents the port from which the traffic needs to be mirrored.
It can be a port associated with VM on another cloud network.

List Tap Flow
=============

.. rest_method:: GET /v2.0/taas/tap_flows

List tap flow that belong to a given tenant.

The list might be empty.

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: 401

Request Parameters
------------------

.. rest_parameters:: parameters.yaml

   - project: project_id-query
   - project-domain: project-domain_taas

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - id: taf_id
   - port: source_port_taf
   - status: status_tas

Response Example
----------------

.. literalinclude:: samples/taas/taf-list-response.json
   :language: javascript

Create Tap Flow
===============

.. rest_method:: POST /v2.0/taas/tap_flows

Create a Tap Flow by passing the following JSON-encoded data.
``name``, ``source port``, ``direction`` as ``IN/OUT/BOTH``
``tap_service`` as mandatory parameters and
``description`` as optional parameter.

Normal response codes: 201

Error response codes: 401, 403, 404, 409

Request Parameters
------------------

.. rest_parameters:: parameters.yaml

   - project: project_id-query
   - project-domain: project-domain_taas
   - tenant_id: project_id-query
   - name: taf_name-query
   - port: source_port_taf-query
   - tap_service: tap_service_id-query
   - vlan_filter: vlan-filter_taf-query
   - direction: direction_taf-query
   - description: description_taf-query

Request Example
---------------

.. literalinclude:: samples/taas/taf-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - id: taf_id
   - name: taf_name
   - port: source_port_taf
   - status: status_taf
   - tap_service: tap_service_id
   - direction: description_taf
   - project_id: project_id
   - tenant_id: project_id

Response Example
----------------

.. literalinclude:: samples/taas/taf-create-response.json
   :language: javascript

Update Tap Flow
===============

.. rest_method:: PUT /v2.0/taas/tap_flows/{taf_service_id/name}

Update Tap Flow by passing tap flow ``name`` or ``id`` as JSON-encoded data.
Name or description or both can only be updated.

Normal response codes: 200

Error response codes: 400, 401, 404, 412

Request Parameters
------------------

.. rest_parameters:: parameters.yaml

   - name: taf_name-query
   - description: description_taf-query

Request Example
---------------

.. literalinclude:: samples/taas/taf-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - id: taf_id
   - name: taf_name
   - port: source_port_taf
   - status: status_tas
   - tap_service: tap_service_id
   - direction: description_taf
   - project_id: project_id
   - tenant_id: project_id

Response Example
----------------

.. literalinclude:: samples/taas/taf-update-response.json
   :language: javascript

Delete Tap Flow
===============

.. rest_method:: DELETE /v2.0/taas/tap_flows/{tap_service_id/name}

Delete Tap Flow by passing tap flow ``name`` or ``id`` as JSON-encoded data.

Normal response codes: 204

Error response codes: 400, 401, 404, 412

Request Parameters
------------------

.. rest_parameters:: parameters.yaml

   - id: taf_id-query
   - name: taf_name-query

Response Parameters
-------------------

On successful ``DELETE`` request ``Tap flow {tap_flow_id} deleted.``
message will be displayed.

Show Tap Flow
=============

.. rest_method:: GET /v2.0/taas/tap_flows/{tap_flows_id/name}

Show details for a tap flow by passing tap flow ``name`` or ``id`` as JSON-encoded data.

.. include:: filtering-show.inc

Normal response codes: 200

Error response codes: 401, 404

Request Parameters
------------------

.. rest_parameters:: parameters.yaml

   - project: project_id-query
   - project-domain: project-domain_taas
   - tenant_id: project_id-query
   - id: taf_id-query
   - name: taf_name-query

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - id: taf_id
   - name: taf_name
   - port: source_port_taf
   - status: status_taf
   - tap_service: tap_service_id
   - direction: description_taf
   - project_id: project_id
   - tenant_id: project_id

Response Example
----------------

.. literalinclude:: samples/taas/taf-show-response.json
   :language: javascript
