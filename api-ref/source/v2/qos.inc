.. -*- rst -*-

.. _quality-of-service:

==============
QoS rule types
==============

Lists and shows information for QoS rule types available in current deployment.

Rule type details
=================

The ``qos-rule-type-details`` extension adds the ``drivers`` attribute to
QoS rule types. The ``drivers`` attribute's value is a list of driver objects.
Each driver object represents a loaded backend QoS driver and includes the
driver's ``name`` as well as a list of its ``supported_parameters`` and
acceptable values.

List QoS rule types
===================

.. rest_method::  GET /v2.0/qos/rule-types

Lists available qos rule types.

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: 401

Request
-------

.. rest_parameters:: parameters.yaml

   - all_supported: qos-rule-type-all-supported
   - all_rules: qos-rule-type-all-rules

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

.. include:: filtering-show.inc

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

Response Example (type "bandwidth_limit")
-----------------------------------------

.. literalinclude:: samples/qos/rule_type-details-bandwidth_limit-response.json
   :language: javascript

Response Example (type "dscp_marking")
--------------------------------------

.. literalinclude:: samples/qos/rule_type-details-dscp_marking-response.json
   :language: javascript

==================
QoS policies (qos)
==================

Lists, creates, deletes, shows information for, and updates QoS policies.

Resource timestamps extension
=============================

The ``standard-attr-timestamp`` extension adds the ``created_at`` and
``updated_at`` attributes to all resources that have standard attributes.

QoS default extension
=====================
The QoS default extension (``qos-default``) allows a per project
default QoS policy by adding the ``is_default`` attribute
to ``policy`` resources.

Tag extension
=============

The ``standard-attr-tag`` adds Tag support for resources with
standard attributes by adding the ``tags`` attribute
allowing consumers to associate tags with resources.


List QoS policies
=================

.. rest_method::  GET /v2.0/qos/policies

Lists all QoS policies associated with your project. One policy can contain
more than one rule type.

The list might be empty.

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: 401

Request
-------

.. rest_parameters:: parameters.yaml

   - description: description-query
   - tenant_id: project_id-query
   - project_id: project_id-query
   - revision_number: revision_number-query
   - shared: qos-shared-query
   - id: id-query
   - is_default: qos_is_default-query
   - name: name-query
   - tags: tags-query
   - tags-any: tags-any-query
   - not-tags: not-tags-query
   - not-tags-any: not-tags-any-query
   - sort_dir: sort_dir
   - sort_key: qos-sort_key
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
   - is_default: qos_is_default
   - rules: qos-rules
   - name: name
   - created_at: created_at_resource
   - updated_at: updated_at_resource
   - tags: tags

Response Example
----------------

.. literalinclude:: samples/qos/policies-list-response.json
   :language: javascript

Create QoS policy
=================

.. rest_method::  POST /v2.0/qos/policies

Creates a QoS policy.

Creates a QoS policy by using the configuration that you define in
the request object.
A response object is returned. The object contains a unique ID.

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
   - is_default: qos_is_default-request
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
   - is_default: qos_is_default
   - name: name
   - created_at: created_at_resource
   - updated_at: updated_at_resource

Response Example
----------------

.. literalinclude:: samples/qos/policy-create-response.json
   :language: javascript

Show QoS policy details
=======================

.. rest_method::  GET /v2.0/qos/policies/{policy_id}

Shows details for a QoS policy. One policy can contain more than one rule type.

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
   - is_default: qos_is_default
   - name: name
   - created_at: created_at_resource
   - updated_at: updated_at_resource

Response Example
----------------

.. literalinclude:: samples/qos/policy-show-response.json
   :language: javascript

Update QoS policy
=================

.. rest_method::  PUT /v2.0/qos/policies/{policy_id}

Updates a QoS policy.

Normal response codes: 200

Error response codes: 400, 401, 404, 412

Request
-------

.. rest_parameters:: parameters.yaml

   - policy_id: qos-policy-id-path
   - policy: policy
   - description: description-request
   - is_default: qos_is_default-request
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
   - is_default: qos_is_default
   - rules: qos-rules
   - name: name
   - created_at: created_at_resource
   - updated_at: updated_at_resource

Response Example
----------------

.. literalinclude:: samples/qos/policy-update-response.json
   :language: javascript

Delete QoS policy
=================

.. rest_method::  DELETE /v2.0/qos/policies/{policy_id}

Deletes a QoS policy.

Normal response codes: 204

Error response codes: 400, 401, 404, 412

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

Bandwidth limit direction
=========================

The ``qos-bw-limit-direction`` extension adds the ``direction`` attribute to
QoS rule types. The ``direction`` attribute allows to configure QoS bandwidth
limit rule with specific direction: ``ingress`` or ``egress``.
Default is ``egress``.

List bandwidth limit rules for QoS policy
=========================================

.. rest_method::  GET /v2.0/qos/policies/{policy_id}/bandwidth_limit_rules

Lists all bandwidth limit rules for a QoS policy.

The list might be empty.

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - policy_id: qos-policy-id-path
   - max_kbps: max_kbps-response-query
   - id: id-query
   - max_burst_kbps: max_burst_kbps-query
   - direction: qos-rule-direction-query
   - sort_dir: sort_dir
   - sort_key: qos_bandwidth_limit_rule-sort_key

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - bandwidth_limit_rules: bandwidth_limit_rules
   - max_kbps: max_kbps-response
   - id: qos_bandwidth_limit_rule-id
   - max_burst_kbps: max_burst_kbps-response
   - direction: qos-rule-direction-response
   - tags: tags

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
   - tags: tags

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
   - tags: tags

Response Example
----------------

.. literalinclude:: samples/qos/bandwidth_limit_rule-show-response.json
   :language: javascript

Update bandwidth limit rule
===========================

.. rest_method::  PUT /v2.0/qos/policies/{policy_id}/bandwidth_limit_rules/{rule_id}

Updates a bandwidth limit rule for a QoS policy.

Normal response codes: 200

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
   - tags: tags

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

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - policy_id: qos-policy-id-path
   - dscp_mark: dscp_mark-query
   - id: id-query
   - sort_dir: sort_dir
   - sort_key: qos_dscp_marking_rule-sort_key

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - dscp_marking_rules: dscp_marking_rules
   - dscp_mark: dscp_mark-response
   - id: qos_dscp_marking_rule-id
   - tags: tags

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
   - tags: tags

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
   - tags: tags

Response Example
----------------

.. literalinclude:: samples/qos/dscp_marking_rule-show-response.json
   :language: javascript

Update DSCP marking rule
========================

.. rest_method::  PUT /v2.0/qos/policies/{policy_id}/dscp_marking_rules/{dscp_rule_id}

Updates a DSCP marking rule for a QoS policy.

Normal response codes: 200

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
   - tags: tags

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

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - policy_id: qos-policy-id-path
   - min_kbps: min_kbps-query
   - id: id-query
   - direction: qos-rule-direction-query
   - sort_dir: sort_dir
   - sort_key: qos_minimum_bandwidth_rule-sort_key

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - minimum_bandwidth_rules: minimum_bandwidth_rules
   - min_kbps: min_kbps-response
   - id: qos_minimum_bandwidth_rule-id
   - direction: qos-rule-direction-response
   - tags: tags

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
   - tags: tags

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
   - tags: tags

Response Example
----------------

.. literalinclude:: samples/qos/minimum_bandwidth_rule-show-response.json
   :language: javascript

Update minimum bandwidth rule
=============================

.. rest_method::  PUT /v2.0/qos/policies/{policy_id}/minimum_bandwidth_rules/{rule_id}

Updates a minimum bandwidth rule for a QoS policy.

Note that the rule cannot be updated, and the update is rejected with error
code 501, if there is any bound port referring to the rule via the qos policy.

Normal response codes: 200

Error response codes: 400, 401, 404, 501

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
   - tags: tags

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

=============================
QoS minimum packet rate rules
=============================

Lists, creates, deletes, shows information for, and updates QoS minimum packet
rate rules.

List minimum packet rate rules for QoS policy
=============================================

.. rest_method::  GET /v2.0/qos/policies/{policy_id}/minimum_packet_rate_rules

Lists all minimum packet rate rules for a QoS policy.

The list might be empty.

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - policy_id: qos-policy-id-path
   - min_kpps: min_kpps-query
   - id: id-query
   - direction: qos-rule-minimum-packet-rate-direction-query
   - sort_dir: sort_dir
   - sort_key: qos_minimum_packet_rate_rule-sort_key

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - minimum_packet_rate_rules: minimum_packet_rate_rules
   - min_kpps: min_kpps-response
   - id: qos_minimum_packet_rate_rule-id
   - direction: qos-rule-minimum-packet-rate-direction
   - tags: tags

Response Example
----------------

.. literalinclude:: samples/qos/minimum_packet_rate_rules-list-response.json
   :language: javascript

Create minimum packet rate rule
===============================

.. rest_method::  POST /v2.0/qos/policies/{policy_id}/minimum_packet_rate_rules

Creates a minimum packet rate rule for a QoS policy.

Normal response codes: 201

Error response codes: 400, 401, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - policy_id: qos-policy-id-path
   - minimum_packet_rate_rule: minimum_packet_rate_rule
   - min_kpps: min_kpps
   - direction: qos-rule-minimum-packet-rate-direction

Request Example
---------------

.. literalinclude:: samples/qos/minimum_packet_rate_rule-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - minimum_packet_rate_rule: minimum_packet_rate_rule
   - min_kpps: min_kpps-response
   - id: qos_minimum_packet_rate_rule-id
   - direction: qos-rule-minimum-packet-rate-direction
   - tags: tags

Response Example
----------------

.. literalinclude:: samples/qos/minimum_packet_rate_rule-create-response.json
   :language: javascript

Show minimum packet rate rule details
=====================================

.. rest_method::  GET /v2.0/qos/policies/{policy_id}/minimum_packet_rate_rules/{rule_id}

Shows details for a minimum packet rate rule for a QoS policy.

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

   - minimum_packet_rate_rule: minimum_packet_rate_rule
   - min_kpps: min_kpps-response
   - id: qos_minimum_packet_rate_rule-id
   - direction: qos-rule-minimum-packet-rate-direction
   - tags: tags

Response Example
----------------

.. literalinclude:: samples/qos/minimum_packet_rate_rule-show-response.json
   :language: javascript

Update minimum packet rate rule
===============================

.. rest_method::  PUT /v2.0/qos/policies/{policy_id}/minimum_packet_rate_rules/{rule_id}

Updates a minimum packet rate rule for a QoS policy.

Note that the rule cannot be updated, and the update is rejected with error
code 501, if there is any bound port referring to the rule via the qos policy.

Normal response codes: 200

Error response codes: 400, 401, 404, 409, 501

Request
-------

.. rest_parameters:: parameters.yaml

   - policy_id: qos-policy-id-path
   - rule_id: qos-rule_id
   - minimum_packet_rate_rule: minimum_packet_rate_rule
   - min_kpps: min_kpps-update
   - direction: qos-rule-minimum-packet-rate-direction-update

Request Example
---------------

.. literalinclude:: samples/qos/minimum_packet_rate_rule-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - minimum_packet_rate_rule: minimum_packet_rate_rule
   - min_kpps: min_kpps-response
   - id: qos_minimum_packet_rate_rule-id
   - direction: qos-rule-minimum-packet-rate-direction
   - tags: tags

Response Example
----------------

.. literalinclude:: samples/qos/minimum_packet_rate_rule-update-response.json
   :language: javascript

Delete minimum packet rate rule
===============================

.. rest_method::  DELETE /v2.0/qos/policies/{policy_id}/minimum_packet_rate_rules/{rule_id}

Deletes a minimum packet rate rule for a QoS policy.

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

===========================
QoS packet rate limit rules
===========================

Lists, creates, deletes, shows information for, and updates QoS packet rate limit rules.

List packet rate limit rules for QoS policy
===========================================

.. rest_method::  GET /v2.0/qos/policies/{policy_id}/packet_rate_limit_rules

Lists all packet rate limit rules for a QoS policy.

The list might be empty.

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - policy_id: qos-policy-id-path
   - max_kpps: max_kpps-query
   - max_burst_kpps: max_burst_kpps-query
   - id: id-query
   - direction: qos-rule-direction-query
   - sort_dir: sort_dir
   - sort_key: qos_packet_rate_limit_rule-sort_key

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - packet_rate_limit_rules: packet_rate_limit_rules
   - max_kpps: max_kpps-response
   - max_burst_kpps: max_burst_kpps-response
   - id: qos_packet_rate_limit_rule-id
   - direction: qos-rule-direction-response
   - tags: tags

Response Example
----------------

.. literalinclude:: samples/qos/packet_rate_limit_rules-list-response.json
   :language: javascript

Create packet rate limit rule
=============================

.. rest_method::  POST /v2.0/qos/policies/{policy_id}/packet_rate_limit_rules

Creates a packet rate limit rule for a QoS policy.

Normal response codes: 201

Error response codes: 400, 401, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - policy_id: qos-policy-id-path
   - packet_rate_limit_rule: packet_rate_limit_rule
   - max_kpps: max_kpps
   - max_burst_kpps: max_burst_kpps
   - direction: qos-rule-direction

Request Example
---------------

.. literalinclude:: samples/qos/packet_rate_limit_rule-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - packet_rate_limit_rule: packet_rate_limit_rule
   - max_kpps: max_kpps-response
   - max_burst_kpps: max_burst_kpps-response
   - id: qos_packet_rate_limit_rule-id
   - direction: qos-rule-direction-response
   - tags: tags

Response Example
----------------

.. literalinclude:: samples/qos/packet_rate_limit_rule-create-response.json
   :language: javascript

Show packet rate limit rule details
===================================

.. rest_method::  GET /v2.0/qos/policies/{policy_id}/packet_rate_limit_rules/{rule_id}

Shows details for a packet rate limit rule for a QoS policy.

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

   - packet_rate_limit_rule: packet_rate_limit_rule
   - max_kpps: max_kpps-response
   - max_burst_kpps: max_burst_kpps-response
   - id: qos_packet_rate_limit_rule-id
   - direction: qos-rule-direction-response
   - tags: tags

Response Example
----------------

.. literalinclude:: samples/qos/packet_rate_limit_rule-show-response.json
   :language: javascript

Update packet rate limit rule
=============================

.. rest_method::  PUT /v2.0/qos/policies/{policy_id}/packet_rate_limit_rules/{rule_id}

Updates a packet rate limit rule for a QoS policy.

Normal response codes: 200

Error response codes: 400, 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - policy_id: qos-policy-id-path
   - rule_id: qos-rule_id
   - packet_rate_limit_rule: packet_rate_limit_rule
   - max_kpps: max_kpps
   - max_burst_kpps: max_burst_kpps
   - direction: qos-rule-direction-update

Request Example
---------------

.. literalinclude:: samples/qos/packet_rate_limit_rule-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - packet_rate_limit_rule: packet_rate_limit_rule
   - max_kpps: max_kpps-response
   - max_burst_kpps: max_burst_kpps-response
   - id: qos_packet_rate_limit_rule-id
   - direction: qos-rule-direction-update-response
   - tags: tags

Response Example
----------------

.. literalinclude:: samples/qos/packet_rate_limit_rule-update-response.json
   :language: javascript

Delete packet rate limit rule
=============================

.. rest_method::  DELETE /v2.0/qos/policies/{policy_id}/packet_rate_limit_rules/{rule_id}

Deletes a packet rate limit rule for a QoS policy.

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

==================================
Quality of Service rules alias API
==================================

The purpose of this API extension is to enable callers to execute the requests
to delete, show and update QoS rules without specifying the corresponding
policy ID. Otherwise, these requests have the exact same behavior as their
counterparts described in other parts of this documentation. The requests
available in this API extension are:

Show bandwidth limit rule details alias
=======================================

.. rest_method::  GET /v2.0/qos/alias_bandwidth_limit_rules/{rule_id}

Please refer to
`Show bandwidth limit rule details <#show-bandwidth-limit-rule-details>`__
for more information on the request, response and return codes.

Update bandwidth limit rule alias
=================================

.. rest_method::  PUT /v2.0/qos/alias_bandwidth_limit_rules/{rule_id}

Please refer to
`Update bandwidth limit rule <#update-bandwidth-limit-rule>`__
for more information on the request, response and return codes.

Delete bandwidth limit rule alias
=================================

.. rest_method::  DELETE /v2.0/qos/alias_bandwidth_limit_rules/{rule_id}

Please refer to
`Delete bandwidth limit rule <#delete-bandwidth-limit-rule>`__
for more information on the request, response and return codes.

Show DSCP marking rule details alias
====================================

.. rest_method::  GET /v2.0/qos/alias_dscp_marking_rules/{dscp_rule_id}

Please refer to
`Show DSCP marking rule details <#show-dscp-marking-rule-details>`__
for more information on the request, response and return codes.

Update DSCP marking rule alias
==============================

.. rest_method::  PUT /v2.0/qos/alias_dscp_marking_rules/{dscp_rule_id}

Please refer to
`Update DSCP marking rule <#update-dscp-marking-rule>`__
for more information on the request, response and return codes.

Delete DSCP marking rule alias
==============================

.. rest_method::  DELETE /v2.0/qos/alias_dscp_marking_rules/{dscp_rule_id}

Please refer to
`Delete DSCP marking rule <#delete-dscp-marking-rule>`__
for more information on the request, response and return codes.

Show minimum bandwidth rule details alias
=========================================

.. rest_method::  GET /v2.0/qos/alias_minimum_bandwidth_rules/{rule_id}

Please refer to
`Show minimum bandwidth rule details <#show-minimum-bandwidth-rule-details>`__
for more information on the request, response and return codes.

Update minimum bandwidth rule alias
===================================

.. rest_method::  PUT /v2.0/qos/alias_minimum_bandwidth_rules/{rule_id}

Please refer to
`Update minimum bandwidth rule <#update-minimum-bandwidth-rule>`__
for more information on the request, response and return codes.

Delete minimum bandwidth rule alias
===================================

.. rest_method::  DELETE /v2.0/qos/alias_minimum_bandwidth_rules/{rule_id}

Please refer to
`Delete minimum bandwidth rule <#delete-minimum-bandwidth-rule>`__
for more information on the request, response and return codes.

======================================================
Quality of Service minimum packet rate rule alias API
======================================================

This API extension enables callers to execute the requests to delete, show and
update QoS minimum packet rate rule without specifying the corresponding
policy ID.

Show minimum packet rate rule details alias
===========================================

.. rest_method::  GET /v2.0/qos/alias_minimum_packet_rate_rules/{rule_id}

Please refer to
`Show minimum packet rate rule details <#show-minimum-packet-rate-rule-details>`__
for more information on the request, response and return codes.

Update minimum packet rate rule alias
=====================================

.. rest_method::  PUT /v2.0/qos/alias_minimum_packet_rate_rules/{rule_id}

Please refer to
`Update minimum packet rate rule <#update-minimum-packet-rate-rule>`__
for more information on the request, response and return codes.

Delete minimum packet rate rule alias
=====================================

.. rest_method::  DELETE /v2.0/qos/alias_minimum_packet_rate_rules/{rule_id}

Please refer to
`Delete minimum packet rate rule <#delete-minimum-packet-rate-rule>`__
for more information on the request, response and return codes.
