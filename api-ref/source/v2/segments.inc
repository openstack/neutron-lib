.. -*- rst -*-

========
Segments
========

Lists, shows details for, creates, updates, and deletes segments. The
segments API is admin-only.

Resource timestamps
===================

The ``standard-attr-timestamp`` extension adds the ``created_at`` and
``updated_at`` attributes to all resources that have standard attributes.

Show segment details
====================

.. rest_method::  GET /v2.0/segments/{segment_id}

Shows details for a segment.

.. include:: filtering-show.inc

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - segment_id: segment_id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - id: segment_id
   - network_id: network_id
   - physical_network: provider:physical_network
   - network_type: network_type
   - revision_number: revision_number
   - segmentation_id: provider:segmentation_id
   - name: name
   - description: description
   - created_at: created_at_resource
   - updated_at: updated_at_resource

Response Example
----------------

.. literalinclude:: samples/segments/segment-show-response.json
   :language: javascript

Update segment
==============

.. rest_method::  PUT /v2.0/segments/{segment_id}

Updates a segment.

Normal response codes: 200

Error response codes: 400, 401, 403, 404, 412

Request
-------

.. rest_parameters:: parameters.yaml

   - segment_id: segment_id-path
   - name: name-segment
   - description: description-request

Request Example
---------------

.. literalinclude:: samples/segments/segment-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - id: segment_id
   - network_id: network_id
   - physical_network: provider:physical_network
   - network_type: network_type
   - revision_number: revision_number
   - segmentation_id: provider:segmentation_id
   - name: name
   - description: description
   - created_at: created_at_resource
   - updated_at: updated_at_resource

Response Example
----------------

.. literalinclude:: samples/segments/segment-update-response.json
   :language: javascript

Delete segment
==============

.. rest_method::  DELETE /v2.0/segments/{segment_id}

Deletes a segment and its associated resources.

Normal response codes: 204

Error response codes: 401, 404, 409, 412

Request
-------

.. rest_parameters:: parameters.yaml

   - segment_id: segment_id-path

Response
--------

There is no body content for the response of a successful DELETE request.

List segments
=============

.. rest_method::  GET /v2.0/segments

Lists segments to which the project has access.

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: 401

Request
-------

.. rest_parameters:: parameters.yaml

   - id: id-query
   - network_id: network_id-query
   - physical_network: provider:physical_network-query
   - network_type: provider:network_type-query
   - revision_number: revision_number-query
   - segmentation_id: provider:segmentation_id-query
   - name: name-query
   - description: description-query
   - sort_dir: sort_dir
   - sort_key: segment-sort_key
   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - id: segment_id
   - network_id: network_id
   - physical_network: provider:physical_network
   - network_type: network_type
   - revision_number: revision_number
   - segmentation_id: provider:segmentation_id
   - name: name
   - description: description
   - created_at: created_at_resource
   - updated_at: updated_at_resource

Response Example
----------------

.. literalinclude:: samples/segments/segments-list-response.json
   :language: javascript

Create segment
==============

.. rest_method::  POST /v2.0/segments

Creates a segment.

Normal response codes: 201

Error response codes: 400, 401

Request
-------

.. rest_parameters:: parameters.yaml

   - network_id: network_id
   - physical_network: provider:physical_network
   - network_type: network_type
   - segmentation_id: provider:segmentation_id
   - name: name-segment
   - description: description-request

Request Example
---------------

.. literalinclude:: samples/segments/segment-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - id: segment_id
   - network_id: network_id
   - physical_network: provider:physical_network
   - network_type: network_type
   - revision_number: revision_number
   - segmentation_id: provider:segmentation_id
   - name: name
   - description: description
   - created_at: created_at_resource
   - updated_at: updated_at_resource

Response Example
----------------

.. literalinclude:: samples/segments/segment-create-response.json
   :language: javascript
