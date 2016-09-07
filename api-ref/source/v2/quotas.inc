.. -*- rst -*-
.. needs:method_verification
.. needs:parameter_verification
.. needs:example_verification
.. needs:body_verification

=========================
Quotas extension (quotas)
=========================

Lists default quotas, current quotas for tenants who have non-default quota
values, and shows, updates, and resets quotas for a tenant.

A quota value of ``-1`` means that quota has no limit.

List quotas for tenants with non-default quota values
=====================================================

.. rest_method::  GET /v2.0/quotas

Lists quotas for tenants who have non-default quota values.

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

List quotas for a tenant
========================

.. rest_method::  GET /v2.0/quotas/{tenant_id}

Lists quotas for a tenant.

Normal response codes: 200

Error response codes: 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - tenant_id: tenant_id-path

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

.. literalinclude:: samples/quotas/quotas-list-for-tenant-response.json
   :language: javascript

Update quota for a tenant
=========================

.. rest_method::  PUT /v2.0/quotas/{tenant_id}

Updates quotas for a tenant. Use when non-default quotas are desired.

Normal response codes: 200

Error response codes: 401, 403, 404

Request
-------

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
   - tenant_id: tenant_id

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
   - tenant_id: tenant_id

Response Example
----------------

.. literalinclude:: samples/quotas/quotas-update-response.json
   :language: javascript

Reset quota for a tenant
========================

.. rest_method::  DELETE /v2.0/quotas/{tenant_id}

Resets quotas to default values for a tenant.

Error response codes: 204, 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - tenant_id: tenant_id-path

List default quotas for a tenant
================================

.. rest_method::  GET /v2.0/quotas/{tenant_id}/default

Lists default quotas for a tenant.

Normal response codes: 200

Error response codes: 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - tenant_id: tenant_id-path

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

.. literalinclude:: samples/quotas/quotas-list-for-tenant-response.json
   :language: javascript
