====================================
Floating IP pools (floatingip_pools)
====================================

Lists floating IP pools.

List floating IP Pools
======================

.. rest_method::  GET /v2.0/floatingip_pools

Lists floating IP pools visible to the user.

Normal response codes: 200

Error response codes: 401

Request
-------

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - floatingip_pools: floatingip_pools
   - subnet_id: subnet-id-body
   - network_id: subnet-network_id
   - subnet_name: subnet-name
   - tenant_id: project_id
   - project_id: project_id
   - cidr: cidr

Response Example
----------------

.. literalinclude:: samples/floatingips/floating-ip-pools-list-response.json
   :language: javascript
