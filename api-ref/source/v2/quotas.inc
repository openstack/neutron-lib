.. -*- rst -*-
.. needs:method_verification
.. needs:parameter_verification
.. needs:example_verification
.. needs:body_verification

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

Normal response codes: 200

Error response codes: 401, 403

Request
-------

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - subnet: quota-subnet
   - network: quota-network
   - floatingip: quota-floatingip
   - subnetpool: quota-subnetpool
   - quotas: quotas
   - security_group_rule: quota-security_group_rule
   - security_group: quota-security_group
   - router: quota-router
   - rbac_policy: quota-rbac_policy
   - port: quota-port

Response Example
----------------

.. literalinclude:: samples/quotas/quotas-list-response.json
   :language: javascript

List quotas for a project
=========================

.. rest_method::  GET /v2.0/quotas/{project_id}

Lists quotas for a project.

Normal response codes: 200

Error response codes: 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - project_id: project_id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - subnet: quota-subnet
   - network: quota-network
   - floatingip: quota-floatingip
   - subnetpool: quota-subnetpool
   - quotas: quotas
   - security_group_rule: quota-security_group_rule
   - security_group: quota-security_group
   - router: quota-router
   - rbac_policy: quota-rbac_policy
   - port: quota-port

Response Example
----------------

.. literalinclude:: samples/quotas/quotas-list-for-project-response.json
   :language: javascript

Update quota for a project
==========================

.. rest_method::  PUT /v2.0/quotas/{project_id}

Updates quotas for a project. Use when non-default quotas are desired.

Normal response codes: 200

Error response codes: 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - project_id: project_id-path
   - subnet: quota-subnet
   - network: quota-network
   - floatingip: quota-floatingip
   - subnetpool: quota-subnetpool
   - quotas: quotas
   - security_group_rule: quota-security_group_rule
   - security_group: quota-security_group
   - router: quota-router
   - rbac_policy: quota-rbac_policy
   - port: quota-port

Request Example
---------------

.. literalinclude:: samples/quotas/quotas-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - subnet: quota-subnet
   - network: quota-network
   - floatingip: quota-floatingip
   - subnetpool: quota-subnetpool
   - quotas: quotas
   - security_group_rule: quota-security_group_rule
   - security_group: quota-security_group
   - router: quota-router
   - rbac_policy: quota-rbac_policy
   - port: quota-port

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

List default quotas for a project
=================================

.. rest_method::  GET /v2.0/quotas/{project_id}/default

Lists default quotas for a project.

Normal response codes: 200

Error response codes: 401, 403, 404

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
