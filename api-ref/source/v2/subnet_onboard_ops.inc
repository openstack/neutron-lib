.. -*- rst -*-

==============================================
Subnet onboard operations (subnet-onboard-ops)
==============================================

Onboard network subnets into a subnet pool

Onboard subnets
===============

.. rest_method::  PUT /v2.0/subnetpools/{subnetpool_id}/onboard_network_subnets

Onboard network subnets to a subnet pool.

Normal response codes: 200

Error response codes: 400

Request
-------

.. rest_parameters:: parameters.yaml

   - network_id: network_id
   - subnetpool_id: subnetpool_id

Request Example
---------------

.. literalinclude:: samples/subnets/subnets-onboard-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - subnetpool_id: subnetpool_id
   - cidr: cidr

Response Example
----------------

.. literalinclude:: samples/subnets/subnets-onboard-response.json
   :language: javascript
