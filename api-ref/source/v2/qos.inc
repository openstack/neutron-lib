.. -*- rst -*-

==============
QoS rule types
==============

Lists and shows information for QoS rule types available in current deployment.

List QoS rule types
===================

.. rest_method::  GET /v2.0/qos/rule-types

Lists available qos rule types.

Normal response codes: 200

Error response codes: 401

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - rule_types: qos-rule-types
   - type: qos-rule-type

Response Example
----------------

.. literalinclude:: samples/qos/rule_types-list-response.json
   :language: javascript

Show QoS rule type details
==========================

.. rest_method:: GET /v2.0/qos/rule-types/{rule_type}

Shows details for an available QoS rule type.

To determine if this API call is available, a user can check whether
the ``qos-rule-type-details`` extension API is available.

You can control which response parameters are returned by using the
fields query parameter. For information, see `Filtering and column
selection <http://specs.openstack.org/openstack/neutron-
specs/specs/api/networking_general_api_information.html#filtering-
and-column-selection>`__.

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - rule_type: qos-rule_type

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - type: qos-rule-type
   - drivers: qos-backend-drivers

Response Example
----------------

.. literalinclude:: samples/qos/rule_type-details-response.json
   :language: javascript

==================
QoS policies (qos)
==================

Lists, creates, deletes, shows information for, and updates QoS policies.

List QoS policies
=================

.. rest_method::  GET /v2.0/qos/policies

Lists all QoS policies associated with your project.

The list might be empty.

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

   - policies: policies
   - description: description
   - tenant_id: project_id
   - project_id: project_id
   - revision_number: revision_number
   - shared: qos-shared
   - id: qos_policy_id
   - rules: qos-rules
   - name: name

Response Example
----------------

.. literalinclude:: samples/qos/policies-list-response.json
   :language: javascript

Create QoS policy
=================

.. rest_method::  POST /v2.0/qos/policies

Creates a QoS policy.

Creates a QoS policy by using the configuration that you define in
the request object. A response object is returned. The object
contains a unique ID.

By the default policy configuration, if the caller is not an administrative
user, this call returns the HTTP ``Forbidden (403)`` response code.

Users with an administrative role can create policies on behalf of
other projects by specifying a project ID that is different than
their own.

Normal response codes: 201

Error response codes: 401, 403, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - policy: policy
   - description: description-request
   - tenant_id: project_id-request
   - project_id: project_id-request
   - shared: qos-shared-request
   - name: qos_policy-name

Request Example
---------------

.. literalinclude:: samples/qos/policy-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - policy: policy
   - description: description
   - tenant_id: project_id
   - project_id: project_id
   - revision_number: revision_number
   - shared: qos-shared
   - rules: qos-rules
   - id: qos_policy_id
   - name: name

Response Example
----------------

.. literalinclude:: samples/qos/policy-create-response.json
   :language: javascript

Show QoS policy details
=======================

.. rest_method::  GET /v2.0/qos/policies/{policy_id}

Shows details for a QoS policy.

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - policy_id: qos-policy-id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - policy: policy
   - description: description
   - tenant_id: project_id
   - project_id: project_id
   - revision_number: revision_number
   - shared: qos-shared
   - rules: qos-rules
   - id: qos_policy_id
   - name: name

Response Example
----------------

.. literalinclude:: samples/qos/policy-show-response.json
   :language: javascript

Update QoS policy
=================

.. rest_method::  PUT /v2.0/qos/policies/{policy_id}

Updates a QoS policy.

If the request is valid, the service returns the ``Accepted (202)``
response code.

Normal response codes: 202

Error response codes: 400, 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - policy_id: qos-policy-id-path
   - policy: policy
   - description: description-request
   - shared: qos-shared-request
   - name: qos_policy-name

Request Example
---------------

.. literalinclude:: samples/qos/policy-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - policy: policy
   - description: description
   - tenant_id: project_id
   - project_id: project_id
   - revision_number: revision_number
   - shared: qos-shared
   - id: qos_policy_id
   - rules: qos-rules
   - name: name

Response Example
----------------

.. literalinclude:: samples/qos/policy-update-response.json
   :language: javascript

Delete QoS policy
=================

.. rest_method::  DELETE /v2.0/qos/policies/{policy_id}

Deletes a QoS policy.

Normal response codes: 204

Error response codes: 400, 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - policy_id: qos-policy-id-path

Response
--------

There is no body content for the response of a successful DELETE request.

=========================
QoS bandwidth limit rules
=========================

Lists, creates, deletes, shows information for, and updates QoS bandwidth limit rules.

List bandwidth limit rules for QoS policy
=========================================

.. rest_method::  GET /v2.0/qos/policies/{policy_id}/bandwidth_limit_rules

Lists all bandwidth limit rules for a QoS policy.

The list might be empty.

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - policy_id: qos-policy-id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - bandwidth_limit_rules: bandwidth_limit_rules
   - max_kbps: max_kbps-response
   - id: qos_bandwidth_limit_rule-id
   - max_burst_kbps: max_burst_kbps-response
   - direction: qos-rule-direction-response

Response Example
----------------

.. literalinclude:: samples/qos/bandwidth_limit_rules-list-response.json
   :language: javascript

Create bandwidth limit rule
===========================

.. rest_method::  POST /v2.0/qos/policies/{policy_id}/bandwidth_limit_rules

Creates a bandwidth limit rule for a QoS policy.

Normal response codes: 201

Error response codes: 400, 401, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - policy_id: qos-policy-id-path
   - bandwidth_limit_rule: bandwidth_limit_rule
   - max_kbps: max_kbps
   - max_burst_kbps: max_burst_kbps
   - direction: qos-rule-direction

Request Example
---------------

.. literalinclude:: samples/qos/bandwidth_limit_rule-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - bandwidth_limit_rule: bandwidth_limit_rule
   - max_kbps: max_kbps-response
   - id: qos_bandwidth_limit_rule-id
   - max_burst_kbps: max_burst_kbps-response
   - direction: qos-rule-direction-response

Response Example
----------------

.. literalinclude:: samples/qos/bandwidth_limit_rule-create-response.json
   :language: javascript

Show bandwidth limit rule details
=================================

.. rest_method::  GET /v2.0/qos/policies/{policy_id}/bandwidth_limit_rules/{rule_id}

Shows details for a bandwidth limit rule for a QoS policy.

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - policy_id: qos-policy-id-path
   - rule_id: qos-rule_id

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - bandwidth_limit_rule: bandwidth_limit_rule
   - max_kbps: max_kbps-response
   - id: qos_bandwidth_limit_rule-id
   - max_burst_kbps: max_burst_kbps-response
   - direction: qos-rule-direction-response

Response Example
----------------

.. literalinclude:: samples/qos/bandwidth_limit_rule-show-response.json
   :language: javascript

Update bandwidth limit rule
===========================

.. rest_method::  PUT /v2.0/qos/policies/{policy_id}/bandwidth_limit_rules/{rule_id}

Updates a bandwidth limit rule for a QoS policy.

If the request is valid, the service returns the ``Accepted (202)``
response code.

Normal response codes: 202

Error response codes: 400, 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - policy_id: qos-policy-id-path
   - rule_id: qos-rule_id
   - bandwidth_limit_rule: bandwidth_limit_rule
   - max_kbps: max_kbps
   - max_burst_kbps: max_burst_kbps
   - direction: qos-rule-direction-update

Request Example
---------------

.. literalinclude:: samples/qos/bandwidth_limit_rule-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - bandwidth_limit_rule: bandwidth_limit_rule
   - max_kbps: max_kbps-response
   - id: qos_bandwidth_limit_rule-id
   - max_burst_kbps: max_burst_kbps-response
   - direction: qos-rule-direction-update-response

Response Example
----------------

.. literalinclude:: samples/qos/bandwidth_limit_rule-update-response.json
   :language: javascript

Delete bandwidth limit rule
===========================

.. rest_method::  DELETE /v2.0/qos/policies/{policy_id}/bandwidth_limit_rules/{rule_id}

Deletes a bandwidth limit rule for a QoS policy.

Normal response codes: 204

Error response codes: 400, 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - policy_id: qos-policy-id-path
   - rule_id: qos-rule_id

Response
--------

There is no body content for the response of a successful DELETE request.

======================
QoS DSCP marking rules
======================

Lists, creates, deletes, shows information for, and updates QoS DSCP marking rules.

List DSCP marking rules for QoS policy
======================================

.. rest_method::  GET /v2.0/qos/policies/{policy_id}/dscp_marking_rules

Lists all DSCP marking rules for a QoS policy.

The list may be empty.

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - policy_id: qos-policy-id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - dscp_marking_rules: dscp_marking_rules
   - dscp_mark: dscp_mark-response
   - id: qos_dscp_marking_rule-id

Response Example
----------------

.. literalinclude:: samples/qos/dscp_marking_rules-list-response.json
   :language: javascript

Create DSCP marking rule
========================

.. rest_method::  POST /v2.0/qos/policies/{policy_id}/dscp_marking_rules

Creates a DSCP marking rule for a QoS policy.

Normal response codes: 201

Error response codes: 400, 401, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - policy_id: qos-policy-id-path
   - dscp_marking_rule: dscp_marking_rule
   - dscp_mark: dscp_mark

Request Example
---------------

.. literalinclude:: samples/qos/dscp_marking_rule-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - dscp_marking_rule: dscp_marking_rule
   - dscp_mark: dscp_mark-response
   - id: qos_dscp_marking_rule-id

Response Example
----------------

.. literalinclude:: samples/qos/dscp_marking_rule-create-response.json
   :language: javascript

Show DSCP marking rule details
==============================

.. rest_method::  GET /v2.0/qos/policies/{policy_id}/dscp_marking_rules/{dscp_rule_id}

Shows details for a DSCP marking rule for a QoS policy.

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - policy_id: qos-policy-id-path
   - dscp_rule_id: dscp_rule_id

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - dscp_marking_rule: dscp_marking_rule
   - dscp_mark: dscp_mark
   - id: qos_dscp_marking_rule-id

Response Example
----------------

.. literalinclude:: samples/qos/dscp_marking_rule-show-response.json
   :language: javascript

Update DSCP marking rule
========================

.. rest_method::  PUT /v2.0/qos/policies/{policy_id}/dscp_marking_rules/{dscp_rule_id}

Updates a DSCP marking rule for a QoS policy.

If the request is valid, the service returns the ``Accepted (202)``
response code.

Normal response codes: 202

Error response codes: 400, 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - policy_id: qos-policy-id-path
   - dscp_rule_id: dscp_rule_id
   - dscp_marking_rule: dscp_marking_rule
   - dscp_mark: dscp_mark

Request Example
---------------

.. literalinclude:: samples/qos/dscp_marking_rule-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - dscp_marking_rule: dscp_marking_rule
   - dscp_mark: dscp_mark-response
   - id: qos_dscp_marking_rule-id

Response Example
----------------

.. literalinclude:: samples/qos/dscp_marking_rule-update-response.json
   :language: javascript

Delete DSCP marking rule
========================

.. rest_method::  DELETE /v2.0/qos/policies/{policy_id}/dscp_marking_rules/{dscp_rule_id}

Deletes a DSCP marking rule for a QoS policy.

Normal response codes: 204

Error response codes: 400, 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - policy_id: qos-policy-id-path
   - dscp_rule_id: dscp_rule_id

Response
--------

There is no body content for the response of a successful DELETE request.

===========================
QoS minimum bandwidth rules
===========================

Lists, creates, deletes, shows information for, and updates QoS minimum bandwidth rules.

List minimum bandwidth rules for QoS policy
===========================================

.. rest_method::  GET /v2.0/qos/policies/{policy_id}/minimum_bandwidth_rules

Lists all minimum bandwidth rules for a QoS policy.

The list might be empty.

You can control which response parameters are returned by using the
fields query parameter. For information, see `Filtering and column
selection <http://specs.openstack.org/openstack/neutron-
specs/specs/api/networking_general_api_information.html#filtering-
and-column-selection>`__.

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - policy_id: qos-policy-id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - minimum_bandwidth_rules: minimum_bandwidth_rules
   - min_kbps: min_kbps-response
   - id: qos_minimum_bandwidth_rule-id
   - direction: qos-rule-direction-response

Response Example
----------------

.. literalinclude:: samples/qos/minimum_bandwidth_rules-list-response.json
   :language: javascript

Create minimum bandwidth rule
=============================

.. rest_method::  POST /v2.0/qos/policies/{policy_id}/minimum_bandwidth_rules

Creates a minimum bandwidth rule for a QoS policy.

Normal response codes: 201

Error response codes: 400, 401, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - policy_id: qos-policy-id-path
   - minimum_bandwidth_rule: minimum_bandwidth_rule
   - min_kbps: min_kbps
   - direction: qos-rule-direction

Request Example
---------------

.. literalinclude:: samples/qos/minimum_bandwidth_rule-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - minimum_bandwidth_rule: minimum_bandwidth_rule
   - min_kbps: min_kbps-response
   - id: qos_minimum_bandwidth_rule-id
   - direction: qos-rule-direction-response

Response Example
----------------

.. literalinclude:: samples/qos/minimum_bandwidth_rule-create-response.json
   :language: javascript

Show minimum bandwidth rule details
===================================

.. rest_method::  GET /v2.0/qos/policies/{policy_id}/minimum_bandwidth_rules/{rule_id}

Shows details for a minimum bandwidth rule for a QoS policy.

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - policy_id: qos-policy-id-path
   - rule_id: qos-rule_id

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - minimum_bandwidth_rule: minimum_bandwidth_rule
   - min_kbps: min_kbps-response
   - id: qos_minimum_bandwidth_rule-id
   - direction: qos-rule-direction-response

Response Example
----------------

.. literalinclude:: samples/qos/minimum_bandwidth_rule-show-response.json
   :language: javascript

Update minimum bandwidth rule
=============================

.. rest_method::  PUT /v2.0/qos/policies/{policy_id}/minimum_bandwidth_rules/{rule_id}

Updates a minimum bandwidth rule for a QoS policy.

If the request is valid, the service returns the ``Accepted (202)``
response code.

Normal response codes: 202

Error response codes: 400, 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - policy_id: qos-policy-id-path
   - rule_id: qos-rule_id
   - minimum_bandwidth_rule: minimum_bandwidth_rule
   - min_kbps: min_kbps
   - direction: qos-rule-direction-update

Request Example
---------------

.. literalinclude:: samples/qos/minimum_bandwidth_rule-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - minimum_bandwidth_rule: minimum_bandwidth_rule
   - min_kbps: min_kbps-response
   - id: qos_minimum_bandwidth_rule-id
   - direction: qos-rule-direction-update-response

Response Example
----------------

.. literalinclude:: samples/qos/minimum_bandwidth_rule-update-response.json
   :language: javascript

Delete minimum bandwidth rule
=============================

.. rest_method::  DELETE /v2.0/qos/policies/{policy_id}/minimum_bandwidth_rules/{rule_id}

Deletes a minimum bandwidth rule for a QoS policy.

Normal response codes: 204

Error response codes: 400, 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - policy_id: qos-policy-id-path
   - rule_id: qos-rule_id

Response
--------

There is no body content for the response of a successful DELETE request.
