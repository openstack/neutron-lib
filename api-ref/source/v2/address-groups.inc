.. -*- rst -*-

==============
Address groups
==============

Lists, creates, shows details for, updates, and deletes address groups.

Show address group
==================

.. rest_method::  GET /v2.0/address-groups/{address_group_id}

Shows information for an address group.

.. include:: filtering-show.inc

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - address_group_id: address_group_id-path
   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - address_group: address_group
   - id: address_group_id_body
   - name: name
   - description: description
   - tenant_id: project_id
   - project_id: project_id
   - addresses: addresses

Response Example
----------------

.. literalinclude:: samples/address-groups/address-group-show-response.json
   :language: javascript

Update an address group
=======================

.. rest_method::  PUT /v2.0/address-groups/{address_group_id}

Updates an address group.

Normal response codes: 200

Error response codes: 400, 401, 403, 404, 412

Request
-------

.. rest_parameters:: parameters.yaml

   - address_group_id: address_group_id-path
   - address_group: address_group
   - name: name-request
   - description: description

Request Example
---------------

.. literalinclude:: samples/address-groups/address-group-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - address_group: address_group
   - id: address_group_id_body
   - name: name
   - description: description
   - tenant_id: project_id
   - project_id: project_id
   - addresses: addresses

Response Example
----------------

.. literalinclude:: samples/address-groups/address-group-update-response.json
   :language: javascript

Delete an address group
=======================

.. rest_method::  DELETE /v2.0/address-groups/{address_group_id}

Deletes an address group.

Normal response codes: 204

Error response codes: 401, 404, 412

Request
-------

.. rest_parameters:: parameters.yaml

   - address_group_id: address_group_id-path

Response
--------

There is no body content for the response of a successful DELETE request.

List address groups
===================

.. rest_method::  GET /v2.0/address-groups

Lists address groups that the project has access to.

Default policy settings return only the address groups owned by
the project of the user submitting the request, unless the
user has administrative role.

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: 401

Request
-------

.. rest_parameters:: parameters.yaml

   - id: id-query
   - name: name-query
   - tenant_id: project_id-query
   - project_id: project_id-query
   - sort_key: address_group-sort_key
   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - address_groups: address_groups
   - id: address_group_id_body
   - name: name
   - tenant_id: project_id
   - project_id: project_id
   - addresses: addresses

Response Example
----------------

.. literalinclude:: samples/address-groups/address-groups-list-response.json
   :language: javascript

Create address group
====================

.. rest_method::  POST /v2.0/address-groups

Creates an address group.

Normal response codes: 201

Error response codes: 400, 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - address_group_id: address_group_id-path
   - address_group: address_group
   - name: name-request
   - description: description
   - addresses: addresses

Request Example
---------------

.. literalinclude:: samples/address-groups/address-group-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - address_group: address_group
   - id: address_group_id_body
   - name: name
   - description: description
   - tenant_id: project_id
   - project_id: project_id
   - addresses: addresses

Response Example
----------------

.. literalinclude:: samples/address-groups/address-group-create-response.json
   :language: javascript

Add IP addresses to address group
=================================

.. rest_method::  PUT /v2.0/address-group/{address_group_id}/add_addresses

Atomically adds a set of IP addresses to the address group's already existing
addresses.

Normal response codes: 200

Error response codes: 400, 401, 404, 412

Request
-------

.. rest_parameters:: parameters.yaml

   - address_group_id: address_group_id-path
   - addresses: addresses

Request Example
---------------

.. literalinclude:: samples/address-groups/address-group-add-addresses-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - address_group: address_group
   - id: address_group_id_body
   - name: name
   - description: description
   - tenant_id: project_id
   - project_id: project_id
   - addresses: addresses

Response Example
----------------

.. literalinclude:: samples/address-groups/address-group-add-addresses-response.json
   :language: javascript

Remove IP addresses to address group
====================================

.. rest_method::  PUT /v2.0/address-group/{address_group_id}/remove_addresses

Atomically removes a set of IP addresses from the address group's already
existing addresses.

Normal response codes: 200

Error response codes: 400, 401, 404, 412

Request
-------

.. rest_parameters:: parameters.yaml

   - address_group_id: address_group_id-path
   - addresses: addresses

Request Example
---------------

.. literalinclude:: samples/address-groups/address-group-remove-addresses-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - address_group: address_group
   - id: address_group_id_body
   - name: name
   - description: description
   - tenant_id: project_id
   - project_id: project_id
   - addresses: addresses

Response Example
----------------

.. literalinclude:: samples/address-groups/address-group-remove-addresses-response.json
   :language: javascript
