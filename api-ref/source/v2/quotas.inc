.. -*- rst -*-

=========================
Quotas extension (quotas)
=========================

Lists default quotas, current quotas for projects with non-default quota
values, and shows, updates, and resets quotas for a project.

A quota value of ``-1`` means that quota has no limit.

List quotas for projects with non-default quota values
======================================================

.. rest_method::  GET /v2.0/quotas

Lists quotas for projects with non-default quota values.

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: 401, 403

Request
-------

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - quotas: quotas
   - floatingip: quota-floatingip
   - network: quota-network
   - port: quota-port
   - project_id: project_id
   - rbac_policy: quota-rbac_policy
   - router: quota-router
   - security_group: quota-security_group
   - security_group_rule: quota-security_group_rule
   - subnet: quota-subnet
   - subnetpool: quota-subnetpool
   - tenant_id: project_id

Response Example
----------------

.. literalinclude:: samples/quotas/quotas-list-response.json
   :language: javascript

List quotas for a project
=========================

.. rest_method::  GET /v2.0/quotas/{project_id}

Lists quotas for a project.

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: 401, 403

Request
-------

.. rest_parameters:: parameters.yaml

   - project_id: project_id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - quota: quota
   - floatingip: quota-floatingip
   - network: quota-network
   - port: quota-port
   - rbac_policy: quota-rbac_policy
   - router: quota-router
   - security_group: quota-security_group
   - security_group_rule: quota-security_group_rule
   - subnet: quota-subnet
   - subnetpool: quota-subnetpool

Response Example
----------------

.. literalinclude:: samples/quotas/quotas-list-for-project-response.json
   :language: javascript

Update quota for a project
==========================

.. rest_method::  PUT /v2.0/quotas/{project_id}

Updates quotas for a project. Use when non-default quotas are desired.

Normal response codes: 200

Error response codes: 401, 403

Request
-------

.. rest_parameters:: parameters.yaml

   - project_id: project_id-path
   - quota: quota
   - floatingip: quota-floatingip-request
   - network: quota-network-request
   - port: quota-port-request
   - rbac_policy: quota-rbac_policy-request
   - router: quota-router-request
   - security_group: quota-security_group-request
   - security_group_rule: quota-security_group_rule-request
   - subnet: quota-subnet-request
   - subnetpool: quota-subnetpool-request
   - check_limit: quota-check-limit
   - force: quota-force

Request Example
---------------

.. literalinclude:: samples/quotas/quotas-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - quota: quota
   - floatingip: quota-floatingip
   - network: quota-network
   - port: quota-port
   - rbac_policy: quota-rbac_policy
   - router: quota-router
   - security_group: quota-security_group
   - security_group_rule: quota-security_group_rule
   - subnet: quota-subnet
   - subnetpool: quota-subnetpool

Response Example
----------------

.. literalinclude:: samples/quotas/quotas-update-response.json
   :language: javascript

Reset quota for a project
=========================

.. rest_method::  DELETE /v2.0/quotas/{project_id}

Resets quotas to default values for a project.

Normal response codes: 204

Error response codes: 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - project_id: project_id-path

Response
--------

There is no body content for the response of a successful DELETE request.

List default quotas for a project
=================================

.. rest_method::  GET /v2.0/quotas/{project_id}/default

Lists default quotas for a project.

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: 401, 403

Request
-------

.. rest_parameters:: parameters.yaml

   - project_id: project_id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - quota: quota
   - floatingip: quota-floatingip
   - network: quota-network
   - port: quota-port
   - rbac_policy: quota-rbac_policy
   - router: quota-router
   - security_group: quota-security_group
   - security_group_rule: quota-security_group_rule
   - subnet: quota-subnet
   - subnetpool: quota-subnetpool

Response Example
----------------

.. literalinclude:: samples/quotas/quotas-list-for-project-response.json
   :language: javascript
