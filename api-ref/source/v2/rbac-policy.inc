.. -*- rst -*-

=============
RBAC Policies
=============

Lists, shows details for, creates, updates, and deletes RBAC policies.

The presence of the ``rbac-security-groups`` extension extends this
API to support object types of ``security_group``.

The presence of the ``rbac-address-scope`` extension extends this
API to support object types of ``address-scope``.

The presence of the ``rbac-subnetpool`` extension extends this
API to support object types of ``subnetpool``.

The presence of the ``rbac-address-group`` extension extends this
API to support object types of ``address-group``.

The presence of the ``rbac-bgpvpn`` extension extends this
API to support object types of ``bgpvpn``.

Show RBAC policy details
========================

.. rest_method::  GET /v2.0/rbac-policies/{rbac_policy_id}

Show details for a given RBAC policy.

.. include:: filtering-show.inc

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - rbac_policy_id: rbac_policy_id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - target_tenant: target_tenant
   - tenant_id: project_id-body-required
   - object_type: object_type
   - object_id: object_id
   - action: rbac_action
   - project_id: project_id
   - id: rbac_policy_id

Response Example
----------------

.. literalinclude:: samples/rbac_policy/rbac-policy-show-response.json
   :language: javascript

Update RBAC policy
==================

.. rest_method::  PUT /v2.0/rbac-policies/{rbac_policy_id}

Update RBAC policy for given tenant.

Normal response codes: 200

Error response codes: 400, 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - rbac_policy_id: rbac_policy_id-path
   - target_tenant: target_tenant-rbac-create-update

Request Example
---------------

.. literalinclude:: samples/rbac_policy/rbac-policy-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - target_tenant: target_tenant
   - tenant_id: project_id-body-required
   - object_type: object_type
   - object_id: object_id
   - action: rbac_action
   - project_id: project_id
   - id: rbac_policy_id

Response Example
----------------

.. literalinclude:: samples/rbac_policy/rbac-policy-update-response.json
   :language: javascript

Delete RBAC policy
==================

.. rest_method::  DELETE /v2.0/rbac-policies/{rbac_policy_id}

Delete an RBAC policy.

Normal response codes: 204

Error response codes: 401, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - rbac_policy_id: rbac_policy_id-path

Response
--------

There is no body content for the response of a successful DELETE request.

List RBAC policies
==================

.. rest_method::  GET /v2.0/rbac-policies

List RBAC policies that belong to a given tenant.

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: 401

Request
-------

.. rest_parameters:: parameters.yaml

   - target_tenant: target_tenant-query
   - tenant_id: project_id-query
   - object_type: object_type-query
   - object_id: object_id-query
   - action: rbac_action-query
   - project_id: project_id-query
   - id: id-query
   - sort_dir: sort_dir
   - sort_key: rbac-sort_key
   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - target_tenant: target_tenant
   - tenant_id: project_id-body-required
   - object_type: object_type
   - object_id: object_id
   - action: rbac_action
   - project_id: project_id
   - id: rbac_policy_id

Response Example
----------------

.. literalinclude:: samples/rbac_policy/rbac-policies-list-response.json
   :language: javascript

Create RBAC policy
==================

.. rest_method::  POST /v2.0/rbac-policies

Create RBAC policy for given tenant.

Normal response codes: 201

Error response codes: 400, 401

Request
-------

.. rest_parameters:: parameters.yaml

   - target_tenant: target_tenant-rbac-create-update
   - object_type: object_type
   - object_id: object_id
   - action: rbac_action

Request Example
---------------

.. literalinclude:: samples/rbac_policy/rbac-policy-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - target_tenant: target_tenant
   - tenant_id: project_id-body-required
   - object_type: object_type
   - object_id: object_id
   - action: rbac_action
   - project_id: project_id
   - id: rbac_policy_id

Response Example
----------------

.. literalinclude:: samples/rbac_policy/rbac-policy-create-response.json
   :language: javascript
