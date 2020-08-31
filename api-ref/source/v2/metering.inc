.. -*- rst -*-

=================================================================
Metering labels and rules (metering-labels, metering-label-rules)
=================================================================

Creates, modifies, and deletes OpenStack Layer3 metering labels and
rules.

List metering labels
====================

.. rest_method::  GET /v2.0/metering/metering-labels

Lists all L3 metering labels that belong to the project.

The list shows the ID for each metering label.

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

   - description: description-query
   - tenant_id: project_id-query
   - project_id: project_id-query
   - shared: shared-query
   - id: id-query
   - name: name-query
   - sort_dir: sort_dir
   - sort_key: metering_label-sort_key
   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - metering_labels: metering_labels
   - description: description
   - tenant_id: project_id
   - project_id: project_id
   - shared: metering_label-shared
   - id: metering_label-id
   - name: name

Response Example
----------------

.. literalinclude:: samples/metering/metering-labels-list-response.json
   :language: javascript

Create metering label
=====================

.. rest_method::  POST /v2.0/metering/metering-labels

Creates an L3 metering label.

Normal response codes: 201

Error response codes: 400, 401, 403

Request
-------

.. rest_parameters:: parameters.yaml

   - metering_label: metering_label
   - shared: metering_label-shared-request
   - description: description-request
   - name: name-request
   - tenant_id: project_id-request
   - project_id: project_id-request

Request Example
---------------

.. literalinclude:: samples/metering/metering-label-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - metering_label: metering_label
   - description: description
   - tenant_id: project_id
   - project_id: project_id
   - shared: metering_label-shared
   - id: metering_label-id
   - name: name

Response Example
----------------

.. literalinclude:: samples/metering/metering-label-create-response.json
   :language: javascript

Show metering label details
===========================

.. rest_method::  GET /v2.0/metering/metering-labels/{metering_label_id}

Shows details for a metering label.

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - metering_label_id: metering_label-id-path

Request Example
---------------

.. literalinclude:: samples/metering/metering-label-show-request-json-http.txt
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - metering_label: metering_label
   - description: description
   - tenant_id: project_id
   - project_id: project_id
   - shared: metering_label-shared
   - id: metering_label-id
   - name: name

Response Example
----------------

.. literalinclude:: samples/metering/metering-label-show-response.json
   :language: javascript

Delete metering label
=====================

.. rest_method::  DELETE /v2.0/metering/metering-labels/{metering_label_id}

Deletes an L3 metering label.

Normal response codes: 204

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - metering_label_id: metering_label-id-path

Request Example
---------------

.. literalinclude:: samples/metering/metering-label-delete-request-json-http.txt
   :language: javascript

Response
--------

There is no body content for the response of a successful DELETE request.

List metering label rules
=========================

.. rest_method::  GET /v2.0/metering/metering-label-rules

Lists a summary of all L3 metering label rules that belong to the project.

The list shows the ID for each metering label rule.

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

   - direction: metering_label_rule-direction-query
   - remote_ip_prefix: metering_label_rule-remote_ip_prefix-query
   - source_ip_prefix: metering_label_rule-source_ip_prefix-query
   - destination_ip_prefix: metering_label_rule-destination_ip_prefix-query
   - excluded : excluded-query
   - metering_label_id: metering_label-id-query
   - id: id-query
   - sort_dir: sort_dir
   - sort_key: metering_label_rule-sort_key
   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - metering_label_rules: metering_label_rules
   - direction: metering_label_rule-direction
   - remote_ip_prefix: metering_label_rule-remote_ip_prefix
   - source_ip_prefix: metering_label_rule-source_ip_prefix-query
   - destination_ip_prefix: metering_label_rule-destination_ip_prefix-query
   - excluded : excluded
   - metering_label_id: metering_label-id-body
   - id: metering_label_rule-id

Response Example
----------------

.. literalinclude:: samples/metering/metering-label-rules-list-response.json
   :language: javascript

Create metering label rule
==========================

.. rest_method::  POST /v2.0/metering/metering-label-rules

Creates an L3 metering label rule.

Normal response codes: 201

Error response codes: 400, 401, 403, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - metering_label_rule: metering_label_rule
   - remote_ip_prefix: metering_label_rule-remote_ip_prefix
   - source_ip_prefix: metering_label_rule-source_ip_prefix-query
   - destination_ip_prefix: metering_label_rule-destination_ip_prefix-query
   - direction: metering_label_rule-direction
   - metering_label_id: metering_label-id-body
   - excluded: excluded-request

Request Example
---------------

.. literalinclude:: samples/metering/metering-label-rule-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - metering_label_rule: metering_label_rule
   - direction: metering_label_rule-direction
   - remote_ip_prefix: metering_label_rule-remote_ip_prefix
   - source_ip_prefix: metering_label_rule-source_ip_prefix-query
   - destination_ip_prefix: metering_label_rule-destination_ip_prefix-query
   - excluded : excluded
   - metering_label_id: metering_label-id-body
   - id: metering_label_rule-id

Response Example
----------------

.. literalinclude:: samples/metering/metering-label-rule-create-response.json
   :language: javascript

Show metering label rule details
================================

.. rest_method::  GET /v2.0/metering/metering-label-rules/{metering_label_rule_id}

Shows details for a metering label rule.

The response body shows this information for each metering label rule:

- ``direction``. Either ingress or egress.

- ``excluded``. Either ``true`` or ``false``.

- The ID for the metering label rule.

- The remote IP prefix (deprecated).

- The source IP prefix

- The destination IP prefix

- The metering label ID for the metering label with which the rule
  is associated.

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - metering_label_rule_id: metering_label_rule-id-path

Request Example
---------------

.. literalinclude:: samples/metering/metering-label-rule-show-request-json-http.txt
   :language: javascript

Response Paramters
------------------

.. rest_parameters:: parameters.yaml

   - metering_label_rule: metering_label_rule
   - direction: metering_label_rule-direction
   - remote_ip_prefix: metering_label_rule-remote_ip_prefix
   - source_ip_prefix: metering_label_rule-source_ip_prefix-query
   - destination_ip_prefix: metering_label_rule-destination_ip_prefix-query
   - excluded : excluded
   - metering_label_id: metering_label-id-body
   - id: metering_label_rule-id

Response Example
----------------

.. literalinclude:: samples/metering/metering-label-rule-show-response.json
   :language: javascript

Delete metering label rule
==========================

.. rest_method::  DELETE /v2.0/metering/metering-label-rules/{metering_label_rule_id}

Deletes an L3 metering label rule.

Normal response codes: 204

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - metering_label_rule_id: metering_label_rule-id-path

Request Example
---------------

.. literalinclude:: samples/metering/metering-label-rule-delete-request-json-http.txt
   :language: javascript

Response
--------

There is no body content for the response of a successful DELETE request.
