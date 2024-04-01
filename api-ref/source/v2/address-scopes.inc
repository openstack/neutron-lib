.. -*- rst -*-

==============
Address scopes
==============

Lists, creates, shows details for, updates, and deletes address scopes.

Show address scope
==================

.. rest_method::  GET /v2.0/address-scopes/{address_scope_id}

Shows information for an address scope.

.. include:: filtering-show.inc

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - address_scope_id: address_scope_id-path
   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - address_scope: address_scope
   - id: address_scope_id_body
   - name: name
   - tenant_id: project_id
   - project_id: project_id
   - ip_version: ip_version-response
   - shared: shared-response

Response Example
----------------

.. literalinclude:: samples/address-scopes/address-scope-show-response.json
   :language: javascript

Update an address scope
=======================

.. rest_method::  PUT /v2.0/address-scopes/{address_scope_id}

Updates an address scope.

Normal response codes: 200

Error response codes: 400, 401, 403, 404, 412

Request
-------

.. rest_parameters:: parameters.yaml

   - address_scope_id: address_scope_id-path
   - address_scope: address_scope
   - name: name-request
   - shared: shared

Request Example
---------------

.. literalinclude:: samples/address-scopes/address-scope-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - address_scope: address_scope
   - id: address_scope_id_body
   - name: name
   - tenant_id: project_id
   - project_id: project_id
   - ip_version: ip_version-response
   - shared: shared-response

Response Example
----------------

.. literalinclude:: samples/address-scopes/address-scope-update-response.json
   :language: javascript

Delete an address scope
=======================

.. rest_method::  DELETE /v2.0/address-scopes/{address_scope_id}

Deletes an address scope.

Normal response codes: 204

Error response codes: 401, 404, 412

Request
-------

.. rest_parameters:: parameters.yaml

   - address_scope_id: address_scope_id-path

Response
--------

There is no body content for the response of a successful DELETE request.

List address scopes
===================

.. rest_method::  GET /v2.0/address-scopes

Lists address scopes that the project has access to.

Default policy settings return only the address scopes owned by
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
   - ip_version: ip_version-query
   - shared: shared-query
   - sort_key: address_scope-sort_key
   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - address_scopes: address_scopes
   - id: address_scope_id_body
   - name: name
   - tenant_id: project_id
   - project_id: project_id
   - ip_version: ip_version-response
   - shared: shared-response

Response Example
----------------

.. literalinclude:: samples/address-scopes/address-scopes-list-response.json
   :language: javascript

Create address scope
====================

.. rest_method::  POST /v2.0/address-scopes

Creates an address scope.

Normal response codes: 201

Error response codes: 400, 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - address_scope: address_scope
   - name: name-request
   - tenant_id: project_id-request
   - project_id: project_id-request
   - ip_version: ip_version-required
   - shared: shared

Request Example
---------------

.. literalinclude:: samples/address-scopes/address-scope-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - address_scope: address_scope
   - id: address_scope_id_body
   - name: name
   - tenant_id: project_id
   - project_id: project_id
   - ip_version: ip_version-response
   - shared: shared-response

Response Example
----------------

.. literalinclude:: samples/address-scopes/address-scope-create-response.json
   :language: javascript
