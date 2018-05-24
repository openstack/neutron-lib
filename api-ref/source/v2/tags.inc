
====================
Tag extension (tags)
====================

Shows details for, updates, and deletes tags.

The maximum number of characters allowed in a tag is 60. If the length
is longer than 60, the API returns the HTTP ``Bad Request (400)`` response
code with 'invalid input for operation' error message.

Tag Extension
=============

.. note::

    NOTE: This extension is deprecated in favor of ``standard-attr-tag``.

The ``tag`` extension allows users to set tags on their networks.
This extension supports networks only.

Enhanced Tag Extension
======================

.. note::

    NOTE: This extension is deprecated in favor of ``standard-attr-tag``.

The ``tag-ext`` extension allows users to set tags on their resources.
This extension supports subnets, ports, routers, and subnet pools.

Standard Attributes Tag Extension
=================================

The ``standard-attr-tag`` extends tagging support to some resources that support
standard attributes. This includes networks, ports, subnets, subnet pools,
floating IPs, routers, security groups, security group rules, QoS policies and
trunks.

Replace all tags
================

.. rest_method::  PUT /v2.0/{resource_type}/{resource_id}/tags

Replaces all tags on the resource.

Normal response codes: 200

Error response codes: 400, 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - resource_type: resource_type
   - resource_id: resource_id
   - tags: tags

Request Example
---------------

.. literalinclude:: samples/tag/tag-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - tags: tags

Response Example
----------------

.. literalinclude:: samples/tag/tag-update-response.json
   :language: javascript

Remove all tags
===============

.. rest_method::  DELETE /v2.0/{resource_type}/{resource_id}/tags

Removes all tags on the resource.

Normal response codes: 204

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - resource_type: resource_type
   - resource_id: resource_id

Response
--------

There is no body content for the response of a successful DELETE request.

Confirm a tag
=============

.. rest_method::  GET /v2.0/{resource_type}/{resource_id}/tags/{tag}

Confirms a given tag is set on the resource.

Normal response codes: 204

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - resource_type: resource_type
   - resource_id: resource_id
   - tag: tag

Response
--------

There is no body content for the response of a successful GET request.

Add a tag
=========

.. rest_method::  PUT /v2.0/{resource_type}/{resource_id}/tags/{tag}

Adds a tag on the resource.

Normal response codes: 201

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - resource_type: resource_type
   - resource_id: resource_id
   - tag: tag

Response
--------

There is no body content for the response of a successful PUT request.

Obtain Tag List
===============

.. rest_method::  GET /v2.0/{resource_type}/{resource_id}/tags

Obtains the tags for a resource.

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - resource_type: resource_type
   - resource_id: resource_id

Response
--------

.. rest_parameters:: parameters.yaml

   - tags: tags

Response Example
----------------

.. literalinclude:: samples/tag/tag-obtain-response.json
   :language: javascript

Remove a tag
============

.. rest_method::  DELETE /v2.0/{resource_type}/{resource_id}/tags/{tag}

Removes a tag on the resource.

Normal response codes: 204

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - resource_type: resource_type
   - resource_id: resource_id
   - tag: tag

Response
--------

There is no body content for the response of a successful DELETE request.

