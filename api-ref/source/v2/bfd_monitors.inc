.. -*- rst -*-

============
BFD monitors
============

A new BFD (Bidirectional Forwarding Detection) resource is introduced.

.. warning::

    This API extension was merged as experimental to enable parallel
    development of multiple backends. At the moment this API does not have
    a reference implementation and should not be considered final. The
    removal of this warning will mark when the reference implementation
    gets merged and the feauture is ready to be consumed.

List BFD monitors
=================

.. rest_method:: GET /v2.0/bfd_monitors

Lists BFD monitors to which the project has access.

Normal response codes: 200

Error response codes: 400, 401, 403

Request
--------

.. rest_parameters:: parameters.yaml

   - id: id-query
   - project_id: project_id-query
   - name: name-query
   - description: description-query
   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - bfd_monitors: bfd_monitor-obj
   - description: description
   - project_id: project_id
   - name: name
   - id: bfd_monitor_id
   - mode: bfd_monitor_mode
   - dst_ip: bfd_monitor_dst_ip
   - src_ip: bfd_monitor_src_ip
   - min_rx: bfd_monitor_min_rx
   - min_tx: bfd_monitor_min_tx
   - multiplier: bfd_monitor_multiplier
   - status: bfd_monitor_status
   - auth_type: bfd_monitor_auth_type
   - auth_key: bfd_monitor_auth_key

Response Example
----------------

.. literalinclude:: samples/bfd/bfd_monitor-list-response.json
   :language: javascript

Create BFD monitor
==================

.. rest_method::  POST /v2.0/bfd_monitors

Creates a BFD monitor.

Normal response codes: 201

Error response codes: 401, 403, 404, 409

Request
--------

.. rest_parameters:: parameters.yaml

   - name: name
   - description: description
   - project_id: project_id
   - mode: bfd_monitor_mode
   - dst_ip: bfd_monitor_dst_ip
   - src_ip: bfd_monitor_src_ip
   - min_rx: bfd_monitor_min_rx
   - min_tx: bfd_monitor_min_tx
   - multiplier: bfd_monitor_multiplier
   - auth_type: bfd_monitor_auth_type
   - auth_key: bfd_monitor_auth_key

Request Example
---------------

.. literalinclude:: samples/bfd/bfd_monitor-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - bfd_monitors: bfd_monitor-obj
   - description: description
   - project_id: project_id
   - name: name
   - id: bfd_monitor_id
   - mode: bfd_monitor_mode
   - dst_ip: bfd_monitor_dst_ip
   - src_ip: bfd_monitor_src_ip
   - min_rx: bfd_monitor_min_rx
   - min_tx: bfd_monitor_min_tx
   - multiplier: bfd_monitor_multiplier
   - status: bfd_monitor_status
   - auth_type: bfd_monitor_auth_type
   - auth_key: bfd_monitor_auth_key

Response Example
----------------

.. literalinclude:: samples/bfd/bfd_monitor-create-response.json
   :language: javascript

Show BFD monitor details
========================

.. rest_method::  GET /v2.0/bfd_monitors/{monitor_id}

Shows details for a BFD monitor.

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - monitor_id: bfd_monitor_id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - bfd_monitors: bfd_monitor-obj
   - description: description
   - project_id: project_id
   - name: name
   - id: bfd_monitor_id
   - mode: bfd_monitor_mode
   - dst_ip: bfd_monitor_dst_ip
   - src_ip: bfd_monitor_src_ip
   - min_rx: bfd_monitor_min_rx
   - min_tx: bfd_monitor_min_tx
   - multiplier: bfd_monitor_multiplier
   - status: bfd_monitor_status
   - auth_type: bfd_monitor_auth_type
   - auth_key: bfd_monitor_auth_key

Response Example
----------------

.. literalinclude:: samples/bfd/bfd_monitor-show-response.json
   :language: javascript

Update BFD monitor
==================

.. rest_method::  PUT /v2.0/bfd_monitors/{monitor_id}

Updates a BFD monitor.

Normal response codes: 200

Error response codes: 400, 401, 404, 412

Request
-------

.. rest_parameters:: parameters.yaml

   - monitor_id: bfd_monitor_id-path
   - name: name
   - description: description
   - min_rx: bfd_monitor_min_rx
   - min_tx: bfd_monitor_min_tx
   - multiplier: bfd_monitor_multiplier

Request Example
---------------

.. literalinclude:: samples/bfd/bfd_monitor-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - bfd_monitors: bfd_monitor-obj
   - description: description
   - project_id: project_id
   - name: name
   - id: bfd_monitor_id
   - mode: bfd_monitor_mode
   - dst_ip: bfd_monitor_dst_ip
   - src_ip: bfd_monitor_src_ip
   - min_rx: bfd_monitor_min_rx
   - min_tx: bfd_monitor_min_tx
   - multiplier: bfd_monitor_multiplier
   - status: bfd_monitor_status
   - auth_type: bfd_monitor_auth_type
   - auth_key: bfd_monitor_auth_key

Response Example
----------------

.. literalinclude:: samples/bfd/bfd_monitor-update-response.json
   :language: javascript

Delete BFD monitor
==================

.. rest_method::  DELETE /v2.0/bfd_monitors/{monitor_id}

Deletes a BFD monitor.

Normal response codes: 204

Error response codes: 400, 401, 404, 412

Request
-------

.. rest_parameters:: parameters.yaml

   - monitor_id: bfd_monitor_id-path

Response
--------

There is no body content for the response of a successful DELETE request.

Get BFD monitor session status
==============================

.. rest_method::  GET /v2.0/bfd_monitors/{monitor_id}/get_bfd_session_status

Shows BFD monitor's session status.

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - monitor_id: bfd_monitor_id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

    - remotes: bfd_monitor_status_remotes

Response Example
----------------

.. literalinclude:: samples/bfd/bfd_monitor_session_status-response.json
   :language: javascript

Get BFD monitor associations
============================

.. rest_method:: GET /v2.0/bfd_monitors/{monitor_id}/get_bfd_monitor_associations

Shows BFD monitor's associations.

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - monitor_id: bfd_monitor_id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

    - remotes: bfd_monitor_associations_remotes

Response Example
----------------

.. literalinclude:: samples/bfd/bfd_monitor_association-response.json
   :language: javascript