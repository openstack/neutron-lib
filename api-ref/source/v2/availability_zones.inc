.. -*- rst -*-

==================
Availability Zones
==================

Lists availability zones.

List all availability zones
===========================

.. rest_method::  GET /v2.0/availability_zones

Lists all availability zones.

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: 401

Request
-------

.. rest_parameters:: parameters.yaml

   - state: state-query
   - resource: resource-query
   - name: name-query

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - availability_zones: availability_zones-list
   - state: state
   - resource: resource
   - name: name

Response Example
----------------

.. literalinclude:: samples/availability-zones/azs-list-response.json
   :language: javascript
