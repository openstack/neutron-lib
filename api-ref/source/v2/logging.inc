.. -*- rst -*-

============
Log resource
============

The ``logging`` extension lists, creates, shows information for, and updates
log resource.

Resource timestamps
===================

The ``standard-attr-timestamp`` extension adds the ``created_at`` and
``updated_at`` attributes to all resources that have standard attributes.

List logs
=========

.. rest_method::  GET /v2.0/log/logs

Lists all log resources associated with your project.

.. include:: filtering-list.inc

The list might be empty.

Normal response codes: 200

Error response codes: 401

Request
-------

.. rest_parameters:: parameters.yaml

   - id: id-query
   - name: name-query
   - description: description-query
   - tenant_id: project_id-query
   - project_id: project_id-query
   - event: log_event-query
   - revision_number: revision_number-query
   - resource_type: resource_log_type-query
   - resource_id: resource_log_id-query
   - target_id: resource_target_log_id-query
   - enabled: log_enabled-query
   - sort_dir: sort_dir
   - sort_key: log-sort_key
   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - logs: logs
   - id: log_id
   - name: name
   - created_at: created_at_resource
   - description: description
   - tenant_id: project_id
   - project_id: project_id
   - event: log_event
   - revision_number: revision_number
   - resource_type: resource_log_type
   - resource_id: resource_log_id
   - target_id: resource_target_log_id
   - updated_at: updated_at_resource
   - enabled: log_enabled

Response Example
----------------

.. literalinclude:: samples/logs/log-list-response.json
   :language: javascript

Create log
==========

.. rest_method::  POST /v2.0/log/logs

Creates a log resource.

Creates a log resource by using the configuration that you define in
the request object. A response object is returned. The object
contains a unique ID.

If the caller is not an administrative user, this call returns the
HTTP ``Forbidden (403)`` response code.

Users with an administrative role can create policies on behalf of
other projects by specifying a project ID that is different than
their own.

Normal response codes: 201

Error response codes: 400, 401, 403, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - log: log
   - name: name-request
   - description: description-request
   - tenant_id: project_id-request
   - project_id: project_id-request
   - event: log_event-request
   - resource_type: resource_log_type
   - resource_id: resource_log_id-request
   - target_id: resource_target_log_id-request
   - enabled: log_enabled-request

Request Example
---------------

.. literalinclude:: samples/logs/log-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - log: log
   - id: log_id
   - name: name
   - created_at: created_at_resource
   - description: description
   - tenant_id: project_id
   - project_id: project_id
   - event: log_event
   - revision_number: revision_number
   - resource_type: resource_log_type
   - resource_id: resource_log_id
   - target_id: resource_target_log_id
   - updated_at: updated_at_resource
   - enabled: log_enabled

Request Example
---------------

.. literalinclude:: samples/logs/log-create-response.json
   :language: javascript

Show log
========

.. rest_method::  GET /v2.0/log/logs/{log_id}

Shows details log resource.

.. include:: filtering-show.inc

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - log_id: log_id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - log: log
   - id: log_id
   - name: name
   - created_at: created_at_resource
   - description: description
   - tenant_id: project_id
   - project_id: project_id
   - event: log_event
   - revision_number: revision_number
   - resource_type: resource_log_type
   - resource_id: resource_log_id
   - target_id: resource_target_log_id
   - updated_at: updated_at_resource
   - enabled: log_enabled

Response Example
----------------

.. literalinclude:: samples/logs/log-show-response.json
   :language: javascript

Update log
==========

.. rest_method::  PUT /v2.0/log/logs/{log_id}

Updates a log resource.

Normal response codes: 200

Error response codes: 400, 401, 404, 412

Request
-------

.. rest_parameters:: parameters.yaml

   - log_id: log_id-path
   - log: log
   - name: name-request
   - description: description-request
   - enabled: log_enabled-request-put

Request Example
---------------

.. literalinclude:: samples/logs/log-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - log: log
   - id: log_id
   - name: name
   - created_at: created_at_resource
   - description: description
   - tenant_id: project_id
   - project_id: project_id
   - event: log_event
   - revision_number: revision_number
   - resource_type: resource_log_type
   - resource_id: resource_log_id
   - target_id: resource_target_log_id
   - updated_at: updated_at_resource
   - enabled: log_enabled

Response Example
----------------

.. literalinclude:: samples/logs/log-update-response.json
   :language: javascript

Delete log
==========

.. rest_method::  DELETE /v2.0/log/logs/{log_id}

Deletes a log resource.

Normal response codes: 204

Error response codes: 400, 401, 404, 412

Request
-------

.. rest_parameters:: parameters.yaml

   - log_id: log_id-path

Response
--------

There is no body content for the response of a successful DELETE request.

=================
Loggable resource
=================

List loggable resources
=======================

.. rest_method::  GET /v2.0/log/loggable-resources

Lists all resource log types are supporting.

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: 401

Request
-------

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - loggable_resources: loggable_resources
   - type: resource_log_type

Response Example
----------------

.. literalinclude:: samples/logs/loggable_resources-list-response.json
   :language: javascript
