.. -*- rst -*-

===================
 Logging Resources
===================

.. note:: Currently this extension ``logging-resource`` is only available for networking-midonet.

Lists, shows information for, creates, updates and deletes logging resources.

List Logging Resources
======================

.. rest_method:: GET /v2.0/logging/logging_resources

Lists logging resources.

Use the ``fields`` query parameter to control which fields are
returned in the response body. Additionally, you can filter results
by using query string parameters. For information, see `Filtering
and Column Selection <https://wiki.openstack.org/wiki/Neutron/APIv2
-specification#Filtering_and_Column_Selection>`__.

Normal response codes: 200

Error response codes: 401, 403

Request
-------

.. rest_parameters:: parameters.yaml

   - fields: fields

Response
--------

.. rest_parameters:: parameters.yaml

  - logging_resources: logging_resources
  - id: logging_resource_id-body
  - tenant_id: project_id
  - project_id: project_id
  - firewall_logs: firewall_logs
  - name: name
  - description: description
  - enabled: logging_resource_enabled

Response Example
----------------

.. literalinclude:: samples/logging_resource/logging_resources-list-response.json
   :language: javascript

Create Logging Resource
=======================

.. rest_method:: POST /v2.0/logging/logging_resources

Creates a logging resource.

Normal response codes: 200

Error response codes: 400, 401, 403

Request
-------

.. rest_parameters:: parameters.yaml

  - logging_resource: logging_resource
  - tenant_id: project_id-request
  - project_id: project_id-request
  - name: name-request
  - description: description-request
  - enabled: logging_resource_enabled-request

Request Example
---------------

.. literalinclude:: samples/logging_resource/logging_resource-create-request.json
   :language: javascript

Response
--------

.. rest_parameters:: parameters.yaml

  - logging_resource: logging_resource
  - id: logging_resource_id-body
  - tenant_id: project_id
  - project_id: project_id
  - firewall_logs: firewall_logs
  - name: name
  - description: description
  - enabled: logging_resource_enabled

Response Example
----------------

.. literalinclude:: samples/logging_resource/logging_resource-create-response.json
   :language: javascript

Show Logging Resource Details
=============================

.. rest_method:: GET /v2.0/logging/logging_resources/{logging_resource_id}

Shows details for a logging resource.

Use the ``fields`` query parameter to control which fields are
returned in the response body. For information, see `Filtering and
Column Selection <http://specs.openstack.org/openstack/neutron-
specs/specs/api/networking_general_api_information.html#filtering-
and-column-selection>`__.

Normal response codes: 200

Error response codes: 400, 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

  - logging_resource_id: logging_resource_id
  - fields: fields

Response
--------

.. rest_parameters:: parameters.yaml

  - logging_resource: logging_resource
  - id: logging_resource_id-body
  - tenant_id: project_id
  - project_id: project_id
  - firewall_logs: firewall_logs
  - name: name
  - description: description
  - enabled: logging_resource_enabled

Response Example
----------------

.. literalinclude:: samples/logging_resource/logging_resource-show-response.json
   :language: javascript

Update Logging Resource
=======================

.. rest_method:: PUT /v2.0/logging/logging_resources/{logging_resource_id}

Updates a logging resource.

Normal response codes: 200

Error response codes: 400, 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

  - logging_resource_id: logging_resource_id
  - logging_resource: logging_resource
  - name: name-request-put
  - description: description-request-put
  - enabled: logging_resource_enabled-request-put

Request Example
----------------

.. literalinclude:: samples/logging_resource/logging_resource-update-request.json
   :language: javascript

Response
--------

.. rest_parameters:: parameters.yaml

  - logging_resource: logging_resource
  - id: logging_resource_id-body
  - tenant_id: project_id
  - project_id: project_id
  - firewall_logs: firewall_logs
  - name: name
  - description: description
  - enabled: logging_resource_enabled

Response Example
----------------

.. literalinclude:: samples/logging_resource/logging_resource-update-response.json
   :language: javascript

Delete Logging Resource
=======================

.. rest_method:: DELETE /v2.0/logging/logging_resources/{logging_resource_id}

Deletes a logging resource.

Normal response codes: 202

Error response codes: 400, 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

  - logging_resource_id: logging_resource_id

Response
--------

There is no body content for the response of a successful DELETE request.
