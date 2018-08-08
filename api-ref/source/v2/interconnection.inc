.. -*- rst -*-

===============================
Neutron-Neutron Interconnection
===============================

Introduces a new ``interconnection`` resource.

When an interconnection is created by a tenant, parameters specific to the
interconnection mechanism (``local_parameters`` and ``remote_parameters``) are
only visible by the admin or users with specific role (default role:
``neutron_interconnection_peer``).

Creates, modifies, and deletes Neutron-Neutron interconnections.

List interconnections
=====================

.. rest_method::  GET /v2.0/interconnection/interconnections

Lists all interconnections belonging to the project.

Use the ``fields`` query parameter to control which fields are
returned in the response body. Additionally, you can filter results
by using query string parameters. For information, see `Filtering
and Column Selection <https://wiki.openstack.org/wiki/Neutron/APIv2
-specification#Filtering_and_Column_Selection>`__.

Normal response codes: 200

Error response codes: 400, 401, 403

Request
-------

.. rest_parameters:: parameters.yaml

   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - interconnections: interconnections
   - project_id: project_id
   - id: interconnection-id-body
   - name: interconnection-name-required
   - type: interconnection-type-required
   - state: interconnection-state
   - local_resource_id: interconnection-local_resource_id
   - remote_resource_id: interconnection-remote_resource_id
   - remote_keystone: interconnection-remote_keystone
   - remote_region: interconnection-remote_region
   - remote_interconnection_id: interconnection-remote_interconnection_id
   - local_parameters: interconnection-local_parameters
   - remote_parameters: interconnection-remote_parameters

Response Example
----------------

.. literalinclude:: samples/interconnection/interconnections-list-response.json
   :language: javascript

Create interconnection
======================

.. rest_method::  POST /v2.0/interconnection/interconnections

Creates an interconnection.

Normal response codes: 201

Error response codes: 400, 401, 403

Request
-------

.. rest_parameters:: parameters.yaml

   - interconnection: interconnection
   - project_id: project_id-request
   - name: interconnection-name
   - type: interconnection-type
   - local_resource_id: interconnection-local_resource_id
   - remote_resource_id: interconnection-remote_resource_id
   - remote_keystone: interconnection-remote_keystone
   - remote_region: interconnection-remote_region

Request Example
---------------

.. literalinclude:: samples/interconnection/interconnection-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - interconnection: interconnection
   - project_id: project_id
   - id: interconnection-id-body
   - name: interconnection-name-required
   - type: interconnection-type-required
   - state: interconnection-state
   - local_resource_id: interconnection-local_resource_id
   - remote_resource_id: interconnection-remote_resource_id
   - remote_keystone: interconnection-remote_keystone
   - remote_region: interconnection-remote_region
   - remote_interconnection_id: interconnection-remote_interconnection_id
   - local_parameters: interconnection-local_parameters
   - remote_parameters: interconnection-remote_parameters

Response Example
----------------

.. literalinclude:: samples/interconnection/interconnection-create-response.json
   :language: javascript

Show interconnection details
============================

.. rest_method::  GET /v2.0/interconnection/interconnections/{interconnection_id}

Shows an interconnection details.

Normal response codes: 200

Error response codes: 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - interconnection_id: interconnection-id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - interconnection: interconnection
   - project_id: project_id
   - id: interconnection-id-body
   - name: interconnection-name-required
   - type: interconnection-type-required
   - state: interconnection-state
   - local_resource_id: interconnection-local_resource_id
   - remote_resource_id: interconnection-remote_resource_id
   - remote_keystone: interconnection-remote_keystone
   - remote_region: interconnection-remote_region
   - remote_interconnection_id: interconnection-remote_interconnection_id
   - local_parameters: interconnection-local_parameters
   - remote_parameters: interconnection-remote_parameters

Response Example
----------------

.. literalinclude:: samples/interconnection/interconnection-show-response.json
   :language: javascript

Update an interconnection
=========================

.. rest_method::  PUT /v2.0/interconnection/interconnections/{interconnection_id}

Updates an interconnection.

Normal response codes: 201

Error response codes: 400, 401, 403, 404

Request
-------
A user can only update the name parameter.

.. rest_parameters:: parameters.yaml

   - interconnection_id: interconnection-id-path
   - interconnection: interconnection
   - name: interconnection-name

Request Example
---------------

.. literalinclude:: samples/interconnection/interconnection-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - interconnection: interconnection
   - project_id: project_id
   - id: interconnection-id-body
   - name: interconnection-name-required
   - type: interconnection-type-required
   - state: interconnection-state
   - local_resource_id: interconnection-local_resource_id
   - remote_resource_id: interconnection-remote_resource_id
   - remote_keystone: interconnection-remote_keystone
   - remote_region: interconnection-remote_region
   - remote_interconnection_id: interconnection-remote_interconnection_id
   - local_parameters: interconnection-local_parameters
   - remote_parameters: interconnection-remote_parameters

Response Example
----------------

.. literalinclude:: samples/interconnection/interconnection-update-response.json
   :language: javascript

Delete interconnection
======================

.. rest_method::  DELETE /v2.0/interconnection/interconnections/{interconnection_id}

Deletes an interconnection.

Normal response codes: 204

Error response codes: 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - interconnection_id: interconnection-id-path

Response
--------

There is no body content for the response of a successful DELETE request.
