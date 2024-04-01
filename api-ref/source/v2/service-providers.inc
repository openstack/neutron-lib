.. -*- rst -*-

=================
Service providers
=================

Lists service providers.

List service providers
======================

.. rest_method::  GET /v2.0/service-providers

Lists service providers and their associated service types.

.. include:: filtering-list.inc

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
