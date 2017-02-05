.. -*- rst -*-
.. needs:method_verification
.. needs:parameter_verification
.. needs:example_verification
.. needs:body_verification

==================
QoS policies (qos)
==================

Lists, creates, shows information for, and updates QoS policies.

Show bandwidth limit rule details
=================================

.. rest_method::  GET /v2.0/qos/policies/{policy_id}/bandwidth_limit_rules/{rule_id}

Shows details for a bandwidth limit rule for a QoS policy.

Normal response codes: 200

Error response codes: 401

Request
-------

.. rest_parameters:: parameters.yaml

   - rule_id: rule_id
   - policy_id: policy_id

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - bandwidth_limit_rule: bandwidth_limit_rule
   - max_kbps: max_kbps
   - id: id
   - max_burst_kbps: max_burst_kbps
   - policy_id: policy_id

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

Normal response codes: 200

Error response codes: 400, 401, 413

Request
-------

.. rest_parameters:: parameters.yaml

   - bandwidth_limit_rule: bandwidth_limit_rule
   - max_kbps: max_kbps
   - max_burst_kbps: max_burst_kbps
   - policy_id: policy_id
   - rule_id: rule_id
   - policy_id: policy_id

Request Example
---------------

.. literalinclude:: samples/qos/bandwidth_limit_rule-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - bandwidth_limit_rule: bandwidth_limit_rule
   - max_kbps: max_kbps
   - id: id
   - max_burst_kbps: max_burst_kbps
   - policy_id: policy_id

Response Example
----------------

.. literalinclude:: samples/qos/bandwidth_limit_rule-update-response.json
   :language: javascript

Delete bandwidth limit rule
===========================

.. rest_method::  DELETE /v2.0/qos/policies/{policy_id}/bandwidth_limit_rules/{rule_id}

Deletes a bandwidth limit rule for a QoS policy.

Normal response codes: 204

Error response codes: 400, 401, 413

Request
-------

.. rest_parameters:: parameters.yaml

   - rule_id: rule_id
   - policy_id: policy_id

List QoS policies
=================

.. rest_method::  GET /v2.0/qos/policies

Lists all QoS policies associated with your project.

The list might be empty.

Normal response codes: 200

Error response codes: 401

Request
-------

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - description: description
   - policy_id: policy_id
   - tenant_id: project_id
   - project_id: project_id
   - policies: policies
   - shared: shared
   - id: id
   - rules: rules
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

If the caller is not an administrative user, this call returns the
HTTP ``Forbidden (403)`` response code.

Users with an administrative role can create policies on behalf of
other projects by specifying a project ID that is different than
their own.

Normal response codes: 201

Error response codes: 401, 404, 409, 413

Request
-------

.. rest_parameters:: parameters.yaml

   - description: description
   - tenant_id: project_id
   - project_id: project_id
   - policy: policy
   - shared: shared
   - type: type
   - name: name

Request Example
---------------

.. literalinclude:: samples/qos/policy-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - description: description
   - tenant_id: project_id
   - project_id: project_id
   - policy: policy
   - shared: shared
   - id: id
   - name: name

Show DSCP marking rule details
==============================

.. rest_method::  GET /v2.0/qos/policies/{policy_id}/dscp_marking_rules/{dscp_rule_id}

Shows details for a DSCP marking rule for a QoS policy.

Normal response codes: 200

Error response codes: 401

Request
-------

.. rest_parameters:: parameters.yaml

   - dscp_rule_id: dscp_rule_id
   - policy_id: policy_id

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - dscp_marking_rule: dscp_marking_rule
   - dscp_mark: dscp_mark
   - id: id
   - policy_id: policy_id

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

Normal response codes: 200

Error response codes: 400, 401, 413

Request
-------

.. rest_parameters:: parameters.yaml

   - dscp_marking_rule: dscp_marking_rule
   - dscp_mark: dscp_mark
   - policy_id: policy_id
   - dscp_rule_id: dscp_rule_id

Request Example
---------------

.. literalinclude:: samples/qos/dscp_marking_rule-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - dscp_marking_rule: dscp_marking_rule
   - dscp_mark: dscp_mark
   - id: id
   - policy_id: policy_id

Response Example
----------------

.. literalinclude:: samples/qos/dscp_marking_rule-update-response.json
   :language: javascript

Delete DSCP marking rule
========================

.. rest_method::  DELETE /v2.0/qos/policies/{policy_id}/dscp_marking_rules/{dscp_rule_id}

Deletes a DSCP marking rule for a QoS policy.

Normal response codes: 204

Error response codes: 400, 401, 413

Request
-------

.. rest_parameters:: parameters.yaml

   - policy_id: policy_id
   - dscp_rule_id: dscp_rule_id

List DSCP marking rules for QoS policy
======================================

.. rest_method::  GET /v2.0/qos/policies/{policy_id}/dscp_marking_rules

Lists all DSCP marking rules for a QoS policy.

The list may be empty.

Normal response codes: 200

Error response codes: 401

Request
-------

.. rest_parameters:: parameters.yaml

   - policy_id: policy_id

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - dscp_marking_rules: dscp_marking_rules
   - dscp_mark: dscp_mark
   - id: id
   - policy_id: policy_id

Response Example
----------------

.. literalinclude:: samples/qos/dscp_marking_rules-list-response.json
   :language: javascript

Create DSCP marking rule
========================

.. rest_method::  POST /v2.0/qos/policies/{policy_id}/dscp_marking_rules

Creates a DSCP marking rule for a QoS policy.

Normal response codes: 201

Error response codes: 401, 404, 409, 413

Request
-------

.. rest_parameters:: parameters.yaml

   - dscp_marking_rule: dscp_marking_rule
   - dscp_mark: dscp_mark
   - policy_id: policy_id

Request Example
---------------

.. literalinclude:: samples/qos/dscp_marking_rule-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - dscp_marking_rule: dscp_marking_rule
   - dscp_mark: dscp_mark
   - id: id
   - policy_id: policy_id

Show QoS policy details
=======================

.. rest_method::  GET /v2.0/qos/policies/{policy_id}

Shows details for a QoS policy.

Normal response codes: 200

Error response codes: 401

Request
-------

.. rest_parameters:: parameters.yaml

   - policy_id: policy_id

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - description: description
   - policy_id: policy_id
   - tenant_id: project_id
   - project_id: project_id
   - policy: policy
   - shared: shared
   - rules: rules
   - id: id
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

Normal response codes: 200

Error response codes: 400, 401, 413

Request
-------

.. rest_parameters:: parameters.yaml

   - description: description
   - tenant_id: project_id
   - project_id: project_id
   - policy: policy
   - shared: shared
   - type: type
   - name: name
   - policy_id: policy_id

Request Example
---------------

.. literalinclude:: samples/qos/policy-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - description: description
   - tenant_id: project_id
   - project_id: project_id
   - policy: policy
   - shared: shared
   - id: id
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

Error response codes: 400, 401, 413

Request
-------

.. rest_parameters:: parameters.yaml

   - policy_id: policy_id

List bandwidth limit rules for QoS policy
=========================================

.. rest_method::  GET /v2.0/qos/policies/{policy_id}/bandwidth_limit_rules

Lists all bandwidth limit rules for a QoS policy.

The list might be empty.

Normal response codes: 200

Error response codes: 401

Request
-------

.. rest_parameters:: parameters.yaml

   - policy_id: policy_id

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - max_kbps: max_kbps
   - bandwidth_limit_rules: bandwidth_limit_rules
   - id: id
   - max_burst_kbps: max_burst_kbps
   - policy_id: policy_id

Response Example
----------------

.. literalinclude:: samples/qos/bandwidth_limit_rules-list-response.json
   :language: javascript

Create bandwidth limit rule
===========================

.. rest_method::  POST /v2.0/qos/policies/{policy_id}/bandwidth_limit_rules

Creates a bandwidth limit rule for a QoS policy.

Normal response codes: 201

Error response codes: 401, 404, 409, 413

Request
-------

.. rest_parameters:: parameters.yaml

   - bandwidth_limit_rule: bandwidth_limit_rule
   - max_kbps: max_kbps
   - max_burst_kbps: max_burst_kbps
   - policy_id: policy_id

Request Example
---------------

.. literalinclude:: samples/qos/bandwidth_limit_rule-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - bandwidth_limit_rule: bandwidth_limit_rule
   - max_kbps: max_kbps
   - id: id
   - max_burst_kbps: max_burst_kbps
   - policy_id: policy_id

