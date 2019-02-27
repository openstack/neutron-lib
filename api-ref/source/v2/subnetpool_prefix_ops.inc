.. -*- rst -*-

=====================================================
Subnet pool prefix operations (subnetpool-prefix-ops)
=====================================================

Add and remove prefixes from a subnet pool prefix list.

Add prefixes
============

.. rest_method::  PUT /v2.0/subnetpools/{subnetpool_id}/add_prefixes

Adds prefixes to a subnet pool.

Normal response codes: 200

Error response codes: 400, 401, 403, 404, 409, 412

Request
-------

.. rest_parameters:: parameters.yaml

   - subnetpool_id: subnetpool_id
   - prefixes: prefixes

Request Example
---------------

.. literalinclude:: samples/subnets/subnetpool-add-prefixes-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - prefixes: prefixes-response

Response Example
----------------

.. literalinclude:: samples/subnets/subnetpool-add-prefixes-response.json
   :language: javascript

Remove prefixes
===============

.. rest_method::  PUT /v2.0/subnetpools/{subnetpool_id}/remove_prefixes

Remove prefixes from a subnet pool.

Normal response codes: 200

Error response codes: 400, 401, 403, 404, 409, 412

Request
-------

.. rest_parameters:: parameters.yaml

   - subnetpool_id: subnetpool_id
   - prefixes: prefixes_remove

Request Example
---------------

.. literalinclude:: samples/subnets/subnetpool-remove-prefixes-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - prefixes: prefixes-response

Response Example
----------------

.. literalinclude:: samples/subnets/subnetpool-remove-prefixes-response.json
   :language: javascript
