.. -*- rst -*-

===============
 Firewall Logs
===============

.. note:: Currently this extension ``logging-resource`` is only available for networking-midonet.

Lists, shows information for, creates, updates and deletes firewall logs.

List Firewall Logs
==================

.. rest_method:: GET /v2.0/logging/logging_resources/{logging_resource_id}/firewall_logs

Lists firewall logs.

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

  - logging_resource_id: logging_resource_id
  - fields: fields

Response
--------

.. rest_parameters:: parameters.yaml

  - firewall_logs: firewall_logs
  - logging_resource_id: logging_resource_id-body
  - id: firewall_log_id-body
  - tenant_id: project_id
  - project_id: project_id
  - description: description
  - fw_event: fw_event
  - firewall_id: firewall_id-body

Response Example
----------------

.. literalinclude:: samples/firewall_log/firewall_logs-list-response.json
   :language: javascript

Create Firewall Log
===================

.. rest_method:: POST /v2.0/logging/logging_resources/{logging_resource_id}/firewall_logs

Creates a firewall log.

Normal response codes: 200

Error response codes: 400, 401, 403

Request
-------

.. rest_parameters:: parameters.yaml

  - logging_resource_id: logging_resource_id
  - firewall_log: firewall_log
  - tenant_id: project_id-request
  - project_id: project_id-request
  - description: description-request
  - fw_event: fw_event-request
  - firewall_id: firewall_id-body

Request Example
---------------

.. literalinclude:: samples/firewall_log/firewall_log-create-request.json
   :language: javascript

Response
--------

.. rest_parameters:: parameters.yaml

  - firewall_log: firewall_log
  - logging_resource_id: logging_resource_id-body
  - id: firewall_log_id-body
  - tenant_id: project_id
  - project_id: project_id
  - description: description
  - fw_event: fw_event
  - firewall_id: firewall_id-body

Response Example
----------------

.. literalinclude:: samples/firewall_log/firewall_log-create-response.json
   :language: javascript

Show Firewall Log Details
=========================

.. rest_method:: GET /v2.0/logging/logging_resources/{logging_resource_id}/firewall_logs/{firewall_log_id}

Shows details for a firewall log.

Use the ``fields`` query parameter to control which fields are
returned in the response body. Additionally, you can filter results
by using query string parameters. For information, see `Filtering
and Column Selection <https://wiki.openstack.org/wiki/Neutron/APIv2
-specification#Filtering_and_Column_Selection>`__.

Normal response codes: 200

Error response codes: 400, 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

  - logging_resource_id: logging_resource_id
  - firewall_log_id: firewall_log_id
  - fields: fields

Response
--------

.. rest_parameters:: parameters.yaml

  - firewall_log: firewall_log
  - logging_resource_id: logging_resource_id-body
  - id: firewall_log_id-body
  - tenant_id: project_id
  - project_id: project_id
  - description: description
  - fw_event: fw_event
  - firewall_id: firewall_id-body

Response Example
----------------

.. literalinclude:: samples/firewall_log/firewall_log-show-response.json
   :language: javascript

Update Firewall Log
===================

.. rest_method:: PUT /v2.0/logging/logging_resources/{logging_resource_id}/firewall_logs/{firewall_log_id}

Updates a firewall log.

Normal response codes: 200

Error response codes: 400, 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

  - logging_resource_id: logging_resource_id
  - firewall_log_id: firewall_log_id
  - firewall_log: firewall_log
  - description: description-request-put
  - fw_event: fw_event-request-put

Request Example
----------------

.. literalinclude:: samples/firewall_log/firewall_log-update-request.json
   :language: javascript

Response
--------

.. rest_parameters:: parameters.yaml

  - firewall_log: firewall_log
  - logging_resource_id: logging_resource_id-body
  - id: firewall_log_id-body
  - tenant_id: project_id
  - project_id: project_id
  - description: description
  - fw_event: fw_event
  - firewall_id: firewall_id-body

Response Example
----------------

.. literalinclude:: samples/firewall_log/firewall_log-update-response.json
   :language: javascript

Delete Firewall Log
===================

.. rest_method:: DELETE /v2.0/logging/logging_resources/{logging_resource_id}/firewall_logs/{firewall_log_id}

Deletes a firewall log.

Normal response codes: 202

Error response codes: 400, 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

  - logging_resource_id: logging_resource_id
  - firewall_log_id: firewall_log_id

Response
--------

There is no body content for the response of a successful DELETE request.
