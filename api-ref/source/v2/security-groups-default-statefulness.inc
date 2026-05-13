.. -*- rst -*-

.. _security_groups_default_statefulness:

==============================================================================
Security groups default statefulness (security-groups-default-statefulness)
==============================================================================

Lists, creates, shows information for, updates, and deletes the default
statefulness configuration for security groups.

This resource allows configuring the default value of the ``stateful``
attribute for newly created security groups, either system-wide (when no
``project_id`` is specified) or on a per-project basis.

List security groups default statefulness
=========================================

.. rest_method::  GET /v2.0/security-groups-default-statefulness

Lists all security groups default statefulness configurations.

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: 401

Request
-------

.. rest_parameters:: parameters.yaml

   - id: id-query
   - project_id: project_id-query
   - stateful: sg_default_statefulness-stateful-query
   - sort_dir: sort_dir
   - sort_key: sg_default_statefulness-sort_key
   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - security_groups_default_statefulness: sg_default_statefulness-list
   - id: sg_default_statefulness-id
   - project_id: sg_default_statefulness-project_id
   - stateful: sg_default_statefulness-stateful

Response Example
----------------

.. literalinclude:: samples/security-groups-default-statefulness/security-groups-default-statefulness-list-response.json
   :language: javascript

Create security groups default statefulness
===========================================

.. rest_method::  POST /v2.0/security-groups-default-statefulness

Creates a security groups default statefulness configuration.

Normal response codes: 201

Error response codes: 400, 401, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - security_groups_default_statefulness: sg_default_statefulness-obj
   - project_id: sg_default_statefulness-project_id-request
   - stateful: sg_default_statefulness-stateful-request

Request Example
---------------

.. literalinclude:: samples/security-groups-default-statefulness/security-groups-default-statefulness-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - security_groups_default_statefulness: sg_default_statefulness-obj
   - id: sg_default_statefulness-id
   - project_id: sg_default_statefulness-project_id
   - stateful: sg_default_statefulness-stateful

Response Example
----------------

.. literalinclude:: samples/security-groups-default-statefulness/security-groups-default-statefulness-create-response.json
   :language: javascript

Show security groups default statefulness
=========================================

.. rest_method::  GET /v2.0/security-groups-default-statefulness/{security_groups_default_statefulness_id}

Shows details for a security groups default statefulness configuration.

.. include:: filtering-show.inc

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - security_groups_default_statefulness_id: sg_default_statefulness-id-path
   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - security_groups_default_statefulness: sg_default_statefulness-obj
   - id: sg_default_statefulness-id
   - project_id: sg_default_statefulness-project_id
   - stateful: sg_default_statefulness-stateful

Response Example
----------------

.. literalinclude:: samples/security-groups-default-statefulness/security-groups-default-statefulness-show-response.json
   :language: javascript

Update security groups default statefulness
===========================================

.. rest_method::  PUT /v2.0/security-groups-default-statefulness/{security_groups_default_statefulness_id}

Updates a security groups default statefulness configuration.

Normal response codes: 200

Error response codes: 400, 401, 404, 412

Request
-------

.. rest_parameters:: parameters.yaml

   - security_groups_default_statefulness_id: sg_default_statefulness-id-path
   - security_groups_default_statefulness: sg_default_statefulness-obj
   - stateful: sg_default_statefulness-stateful-request

Request Example
---------------

.. literalinclude:: samples/security-groups-default-statefulness/security-groups-default-statefulness-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - security_groups_default_statefulness: sg_default_statefulness-obj
   - id: sg_default_statefulness-id
   - project_id: sg_default_statefulness-project_id
   - stateful: sg_default_statefulness-stateful

Response Example
----------------

.. literalinclude:: samples/security-groups-default-statefulness/security-groups-default-statefulness-update-response.json
   :language: javascript

Delete security groups default statefulness
===========================================

.. rest_method::  DELETE /v2.0/security-groups-default-statefulness/{security_groups_default_statefulness_id}

Deletes a security groups default statefulness configuration.

Normal response codes: 204

Error response codes: 401, 404, 412

Request
-------

.. rest_parameters:: parameters.yaml

   - security_groups_default_statefulness_id: sg_default_statefulness-id-path

Response
--------

There is no body content for the response of a successful DELETE request.
