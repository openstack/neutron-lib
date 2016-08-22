.. -*- rst -*-

=================
Service providers
=================

Lists service providers.

List service providers
======================

.. rest_method::  GET /v2.0/service-providers

Lists service providers and their associated service types.

Use the ``fields`` query parameter to control which fields are
returned in the response body. Additionally, you can filter results
by using query string parameters. For information, see `Filtering
and Column Selection <https://wiki.openstack.org/wiki/Neutron/APIv2
-specification#Filtering_and_Column_Selection>`__.

Normal response codes: 200

Error response codes: 401

Request
-------

.. rest_parameters:: parameters.yaml

   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - service_providers: service_providers
   - service_type: service_type
   - name: name
   - default: default

Response Example
----------------

.. literalinclude:: samples/service-type-response.json
   :language: javascript
