.. -*- rst -*-

================================================================================
FWaaS v2.0 (CURRENT) (fwaas, firewall_groups, firewall_policies, firewall_rules)
================================================================================

.. warning::

    Due to lack of maintenance of the ``neutron-fwaas`` project, the reference
    implementation of the FWaaS API, is now deprecated and unmaintained
    anymore.
    This document describes the FWaaS API definitions without any official
    implementation.
    This API can be implemented by some third party solutions.

Use the Firewall-as-a-Service (FWaaS) v2.0 extension to deploy
firewall groups to protect your networks.

The FWaaS extension enables you to:

- Apply firewall rules on traffic entering and leaving project
  networks.

- Apply TCP, UDP, ICMP, or protocol-agnostic rules.

- Create and share firewall policies that hold an ordered collection
  of firewall rules.

- Audit firewall rules and policies.

This extension introduces the following resources:

- ``firewall_group``. A logical firewall resource that a project can
  create and manage. A firewall group can have a firewall policy for
  ingress traffic and/or a firewall policy for egress traffic.

- ``firewall_policy``. An ordered collection of firewall rules. You
  can share a firewall policy across projects. You can include a
  firewall policy as part of an audit workflow so that an
  authorized relevant entity can audit the firewall policy. This
  entity can differ from the user who created, or the projects
  that use, the firewall policy.

- ``firewall_rule``. A collection of attributes, such as source and
  destination ports, source and destination IP addresses, protocol,
  and IP version. These attributes define match criteria and an
  action to take, such as allow, reject, or deny, on matched data
  traffic.

List firewall groups
====================

.. rest_method::  GET /v2.0/fwaas/firewall_groups

Lists all firewall groups.

The list might be empty.

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

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - firewall_groups: firewall_groups_object
   - admin_state_up: firewall_group_admin_state_up-body-required
   - description: firewall_group_description-body-required
   - egress_firewall_policy_id: egress_firewall_policy_id-body-required
   - id: firewall_group_id-body-required
   - ingress_firewall_policy_id: ingress_firewall_policy_id-body-required
   - name: firewall_group_name-body-required
   - ports: firewall_group_ports-body-required
   - project_id: project_id-body-required
   - shared: firewall_group_shared-body-required
   - status: firewall_group_status-body-required
   - tenant_id: project_id-body-required

Response Example
----------------

.. literalinclude:: samples/firewall-v2/firewall-groups-list-response.json
   :language: javascript

Show firewall group details
===========================

.. rest_method::  GET /v2.0/fwaas/firewall_groups/{firewall_group_id}

Shows details for a firewall group.

If the user is not an administrative user and the firewall group
object does not belong to the project, this call returns the
``FirewallGroupNotFound (404)`` response code.

Normal response codes: 200

Error response codes: 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - firewall_group_id: firewall_group_id-path-required

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - firewall_group: firewall_group_object
   - admin_state_up: firewall_group_admin_state_up-body-required
   - description: firewall_group_description-body-required
   - egress_firewall_policy_id: egress_firewall_policy_id-body-required
   - id: firewall_group_id-body-required
   - ingress_firewall_policy_id: ingress_firewall_policy_id-body-required
   - name: firewall_group_name-body-required
   - ports: firewall_group_ports-body-required
   - project_id: project_id-body-required
   - shared: firewall_group_shared-body-required
   - status: firewall_group_status-body-required
   - tenant_id: project_id-body-required

Response Example
----------------

.. literalinclude:: samples/firewall-v2/firewall-group-show-response.json
   :language: javascript

Create firewall group
=====================

.. rest_method::  POST /v2.0/fwaas/firewall_groups

Creates a firewall group.

The firewall group may be associated with an ingress firewall policy
and/or an egress firewall policy.

If ``admin_state_up`` is ``false``, the firewall group will block all
traffic.

Normal response codes: 201

Error response codes: 400, 401

Request
-------

.. rest_parameters:: parameters.yaml

   - firewall_group: firewall_group_object
   - admin_state_up: firewall_group_admin_state_up-body-optional
   - description: firewall_group_description-body-optional
   - egress_firewall_policy_id: egress_firewall_policy_id-body-optional
   - ingress_firewall_policy_id: ingress_firewall_policy_id-body-optional
   - name: firewall_group_name-body-optional
   - ports: firewall_group_ports-body-optional
   - project_id: project_id-body-optional
   - shared: firewall_group_shared-body-optional
   - tenant_id: project_id-body-optional

Request Example
---------------

.. literalinclude:: samples/firewall-v2/firewall-group-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - firewall_group: firewall_group_object
   - admin_state_up: firewall_group_admin_state_up-body-required
   - description: firewall_group_description-body-required
   - egress_firewall_policy_id: egress_firewall_policy_id-body-required
   - id: firewall_group_id-body-required
   - ingress_firewall_policy_id: ingress_firewall_policy_id-body-required
   - name: firewall_group_name-body-required
   - ports: firewall_group_ports-body-required
   - project_id: project_id-body-required
   - shared: firewall_group_shared-body-required
   - status: firewall_group_status-body-required
   - tenant_id: project_id-body-required

Response Example
----------------

.. literalinclude:: samples/firewall-v2/firewall-group-create-response.json
   :language: javascript

Update firewall group
=====================

.. rest_method::  PUT /v2.0/fwaas/firewall_groups/{firewall_group_id}

Updates a firewall group.

The firewall group cannot be updated if its status is a PENDING_* status.

Normal response codes: 200

Error response codes: 400, 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - firewall_group_id: firewall_group_id-path-required
   - firewall_group: firewall_group_object
   - admin_state_up: firewall_group_admin_state_up-body-optional
   - description: firewall_group_description-body-optional
   - egress_firewall_policy_id: egress_firewall_policy_id-body-optional
   - ingress_firewall_policy_id: ingress_firewall_policy_id-body-optional
   - name: firewall_group_name-body-optional
   - ports: firewall_group_ports-body-optional
   - shared: firewall_group_shared-body-optional

Request Example
---------------

.. literalinclude:: samples/firewall-v2/firewall-group-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - firewall_group: firewall_group_object
   - admin_state_up: firewall_group_admin_state_up-body-required
   - description: firewall_group_description-body-required
   - egress_firewall_policy_id: egress_firewall_policy_id-body-required
   - id: firewall_group_id-body-required
   - ingress_firewall_policy_id: ingress_firewall_policy_id-body-required
   - name: firewall_group_name-body-required
   - ports: firewall_group_ports-body-required
   - project_id: project_id-body-required
   - shared: firewall_group_shared-body-required
   - status: firewall_group_status-body-required
   - tenant_id: project_id-body-required

Response Example
----------------

.. literalinclude:: samples/firewall-v2/firewall-group-update-response.json
   :language: javascript

Delete firewall group
=====================

.. rest_method::  DELETE /v2.0/fwaas/firewall_groups/{firewall_group_id}

Deletes a firewall group.

Normal response codes: 204

Error response codes: 401, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - firewall_group_id: firewall_group_id-path-required

Response
--------

There is no body content for the response of a successful DELETE request.

List firewall policies
======================

.. rest_method::  GET /v2.0/fwaas/firewall_policies

Lists all firewall policies.

The list might be empty.

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

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - firewall_policies: firewall_policies_object
   - audited: firewall_policy_audited-body-required
   - description: firewall_policy_description-body-required
   - id: firewall_policy_id-body-required
   - firewall_rules: firewall_rules-body-required
   - name: firewall_policy_name-body-required
   - project_id: project_id-body-required
   - shared: firewall_policy_shared-body-required
   - tenant_id: project_id-body-required

Response Example
----------------

.. literalinclude:: samples/firewall-v2/firewall-policies-list-response.json
   :language: javascript

Show firewall policy details
============================

.. rest_method::  GET /v2.0/fwaas/firewall_policies/{firewall_policy_id}

Shows details of a firewall policy.

Normal response codes: 200

Error response codes: 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - firewall_policy_id: firewall_policy_id-path-required

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - audited: firewall_policy_audited-body-required
   - description: firewall_policy_description-body-required
   - firewall_rules: firewall_rules-body-required
   - id: firewall_policy_id-body-required
   - name: firewall_policy_name-body-required
   - project_id: project_id-body-required
   - shared: firewall_policy_shared-body-required
   - tenant_id: project_id-body-required

Response Example
----------------

.. literalinclude:: samples/firewall-v2/firewall-policy-show-response.json
   :language: javascript

Create firewall policy
======================

.. rest_method::  POST /v2.0/fwaas/firewall_policies

Creates a firewall policy.

Normal response codes: 201

Error response codes: 400, 401

Request
-------

.. rest_parameters:: parameters.yaml

   - firewall_policy: firewall_policy_object
   - audited: firewall_policy_audited-body-optional
   - description: firewall_policy_description-body-optional
   - firewall_rules: firewall_rules-body-optional
   - name: firewall_policy_name-body-optional
   - project_id: project_id-body-optional
   - shared: firewall_policy_shared-body-optional
   - tenant_id: project_id-body-optional

Request Example
---------------

.. literalinclude:: samples/firewall-v2/firewall-policy-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - firewall_policy: firewall_policy_object
   - audited: firewall_policy_audited-body-required
   - description: firewall_policy_description-body-required
   - firewall_rules: firewall_rules-body-required
   - id: firewall_policy_id-body-required
   - name: firewall_policy_name-body-required
   - project_id: project_id-body-required
   - shared: firewall_policy_shared-body-required
   - tenant_id: project_id-body-required

Response Example
----------------

.. literalinclude:: samples/firewall-v2/firewall-policy-create-response.json
   :language: javascript

Update firewall policy
======================

.. rest_method::  PUT /v2.0/fwaas/firewall_policies/{firewall_policy_id}

Updates a firewall policy.

Normal response codes: 200

Error response codes: 400, 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - firewall_policy_id: firewall_policy_id-path-required
   - firewall_policy: firewall_policy_object
   - audited: firewall_policy_audited-body-optional
   - description: firewall_policy_description-body-optional
   - firewall_rules: firewall_rules-body-optional
   - name: firewall_policy_name-body-optional
   - project_id: project_id-body-optional
   - shared: firewall_policy_shared-body-optional
   - tenant_id: project_id-body-optional

Request Example
---------------

.. literalinclude:: samples/firewall-v2/firewall-policy-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - firewall_policy: firewall_policy_object
   - audited: firewall_policy_audited-body-required
   - description: firewall_policy_description-body-required
   - firewall_rules: firewall_rules-body-required
   - id: firewall_policy_id-body-required
   - name: firewall_policy_name-body-required
   - shared: firewall_policy_shared-body-required
   - project_id: project_id-body-required
   - tenant_id: project_id-body-required

Response Example
----------------

.. literalinclude:: samples/firewall-v2/firewall-policy-update-response.json
   :language: javascript

Delete firewall policy
======================

.. rest_method::  DELETE /v2.0/fwaas/firewall_policies/{firewall_policy_id}

Deletes a firewall policy.

Normal response codes: 204

Error response codes: 401, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - firewall_policy_id: firewall_policy_id-path-required

Response
--------

There is no body content for the response of a successful DELETE request.

List firewall rules
===================

.. rest_method::  GET /v2.0/fwaas/firewall_rules

Lists all firewall rules.

The list might be empty.

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

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - firewall_rules: firewall_rules_object
   - action: firewall_rule_action-body-required
   - description: firewall_rule_description-body-required
   - destination_firewall_group_id: destination_firewall_group_id-body-required
   - destination_ip_address: firewall_rule_destination_ip_address-body-required
   - destination_port: firewall_rule_destination_port-body-required
   - enabled: firewall_rule_enabled-body-required
   - firewall_policy_id: firewall_policy_id-body-required
   - id: firewall_rule_id-body-required
   - ip_version: firewall_rule_ip_version-body-required
   - name: firewall_rule_name-body-required
   - project_id: project_id-body-required
   - protocol: firewall_rule_protocol-body-required
   - shared: firewall_rule_shared-body-required
   - source_firewall_group_id: source_firewall_group_id-body-required
   - source_ip_address: firewall_rule_source_ip_address-body-required
   - source_port: firewall_rule_source_port-body-required
   - tenant_id: project_id-body-required

Response Example
----------------

.. literalinclude:: samples/firewall-v2/firewall-rules-list-response.json
   :language: javascript

Show firewall rule details
==========================

.. rest_method::  GET /v2.0/fwaas/firewall_rules/{firewall_rule_id}

Shows details for a firewall rule.

If the user is not an administrative user and the firewall rule
object does not belong to the project, this call returns the
``Forbidden (403)`` response code.

Normal response codes: 200

Error response codes: 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - firewall_rule_id: firewall_rule_id-path-required

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - firewall_rule: firewall_rule_object
   - action: firewall_rule_action-body-required
   - description: firewall_rule_description-body-required
   - destination_firewall_group_id: destination_firewall_group_id-body-required
   - destination_ip_address: firewall_rule_destination_ip_address-body-required
   - destination_port: firewall_rule_destination_port-body-required
   - enabled: firewall_rule_enabled-body-required
   - firewall_policy_id: firewall_policy_id-body-required
   - id: firewall_rule_id-body-required
   - ip_version: firewall_rule_ip_version-body-required
   - name: firewall_rule_name-body-required
   - project_id: project_id-body-required
   - protocol: firewall_rule_protocol-body-required
   - shared: firewall_rule_shared-body-required
   - source_firewall_group_id: source_firewall_group_id-body-required
   - source_ip_address: firewall_rule_source_ip_address-body-required
   - source_port: firewall_rule_source_port-body-required
   - tenant_id: project_id-body-required

Response Example
----------------

.. literalinclude:: samples/firewall-v2/firewall-rule-show-response.json
   :language: javascript

Create firewall rule
====================

.. rest_method::  POST /v2.0/fwaas/firewall_rules

Creates a firewall rule.

Normal response codes: 201

Error response codes: 400, 401

Request
-------

.. rest_parameters:: parameters.yaml

   - firewall_rule: firewall_rule_object
   - action: firewall_rule_action-body-optional
   - description: firewall_rule_description-body-optional
   - destination_firewall_group_id: destination_firewall_group_id-body-optional
   - destination_ip_address: firewall_rule_destination_ip_address-body-optional
   - destination_port: firewall_rule_destination_port-body-optional
   - enabled: firewall_rule_enabled-body-optional
   - ip_version: firewall_rule_ip_version-body-optional
   - name: firewall_rule_name-body-optional
   - project_id: project_id-body-optional
   - protocol: firewall_rule_protocol-body-optional
   - shared: firewall_rule_shared-body-optional
   - source_firewall_group_id: source_firewall_group_id-body-optional
   - source_ip_address: firewall_rule_source_ip_address-body-optional
   - source_port: firewall_rule_source_port-body-optional
   - tenant_id: project_id-body-optional

Request Example
---------------

.. literalinclude:: samples/firewall-v2/firewall-rule-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - firewall_rule: firewall_rule_object
   - action: firewall_rule_action-body-required
   - description: firewall_rule_description-body-required
   - destination_firewall_group_id: destination_firewall_group_id-body-required
   - destination_ip_address: firewall_rule_destination_ip_address-body-required
   - destination_port: firewall_rule_destination_port-body-required
   - enabled: firewall_rule_enabled-body-required
   - firewall_policy_id: firewall_policy_id-body-required
   - id: firewall_rule_id-body-required
   - ip_version: firewall_rule_ip_version-body-required
   - name: firewall_rule_name-body-required
   - project_id: project_id-body-required
   - protocol: firewall_rule_protocol-body-required
   - shared: firewall_rule_shared-body-required
   - source_firewall_group_id: source_firewall_group_id-body-required
   - source_ip_address: firewall_rule_source_ip_address-body-required
   - source_port: firewall_rule_source_port-body-required
   - tenant_id: project_id-body-required

Response Example
----------------

.. literalinclude:: samples/firewall-v2/firewall-rule-create-response.json
   :language: javascript

Update firewall rule
====================

.. rest_method::  PUT /v2.0/fwaas/firewall_rules/{firewall_rule_id}

Updates a firewall rule.

Normal response codes: 200

Error response codes: 400, 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - firewall_rule_id: firewall_rule_id-path-required
   - firewall_rule: firewall_rule_object
   - action: firewall_rule_action-body-optional
   - description: firewall_rule_description-body-optional
   - destination_firewall_group_id: destination_firewall_group_id-body-optional
   - destination_ip_address: firewall_rule_destination_ip_address-body-optional
   - destination_port: firewall_rule_destination_port-body-optional
   - enabled: firewall_rule_enabled-body-optional
   - firewall_policy_id: firewall_policy_id-body-required
   - ip_version: firewall_rule_ip_version-body-optional
   - name: firewall_rule_name-body-optional
   - project_id: project_id-body-optional
   - protocol: firewall_rule_protocol-body-optional
   - shared: firewall_rule_shared-body-optional
   - source_firewall_group_id: source_firewall_group_id-body-optional
   - source_ip_address: firewall_rule_source_ip_address-body-optional
   - source_port: firewall_rule_source_port-body-optional
   - tenant_id: project_id-body-optional

Request Example
---------------

.. literalinclude:: samples/firewall-v2/firewall-rule-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - firewall_rule: firewall_rule_object
   - action: firewall_rule_action-body-required
   - description: firewall_rule_description-body-required
   - destination_firewall_group_id: destination_firewall_group_id-body-required
   - destination_ip_address: firewall_rule_destination_ip_address-body-required
   - destination_port: firewall_rule_destination_port-body-required
   - enabled: firewall_rule_enabled-body-required
   - firewall_policy_id: firewall_policy_id-body-required
   - id: firewall_rule_id-body-required
   - ip_version: firewall_rule_ip_version-body-required
   - name: firewall_rule_name-body-required
   - project_id: project_id-body-required
   - protocol: firewall_rule_protocol-body-required
   - shared: firewall_rule_shared-body-required
   - source_firewall_group_id: source_firewall_group_id-body-required
   - source_ip_address: firewall_rule_source_ip_address-body-required
   - source_port: firewall_rule_source_port-body-required
   - tenant_id: project_id-body-required

Response Example
----------------

.. literalinclude:: samples/firewall-v2/firewall-rule-update-response.json
   :language: javascript

Delete firewall rule
====================

.. rest_method::  DELETE /v2.0/fwaas/firewall_rules/{firewall_rule_id}

Deletes a firewall rule.
samples/firewall-v2/firewall-policy-create-response.json

Normal response codes: 204

Error response codes: 401, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - firewall_rule_id: firewall_rule_id-path-required

Insert rule into a firewall policy
==================================

.. rest_method::  PUT /v2.0/fwaas/firewall_policies/{firewall_policy_id}/insert_rule

Insert firewall rule into a policy.

A firewall_rule_id is inserted relative to the position of the
firewall_rule_id set in ``insert_before`` or ``insert_after``. If
``insert_before`` is set, ``insert_after`` is ignored. If both
``insert_before`` and ``insert_after`` are not set, the new
firewall_rule_id is inserted as the first rule of the policy.

Normal response codes: 200

Error response codes: 400, 401, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - firewall_policy_id: firewall_policy_id-path-required
   - firewall_rule_id: firewall_rule_id-body-required
   - insert_after: firewall_rule_insert_after-body-required
   - insert_before: firewall_rule_insert_before-body-required

Request Example
---------------

.. literalinclude:: samples/firewall-v2/firewall-policy-insert-rule-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - audited: firewall_policy_audited-body-required
   - description: firewall_policy_description-body-required
   - firewall_rules: firewall_rules-body-required
   - id: firewall_policy_id-body-required
   - name: firewall_policy_name-body-required
   - project_id: project_id-body-required
   - shared: firewall_policy_shared-body-required
   - tenant_id: project_id-body-required

Response Example
----------------

.. literalinclude:: samples/firewall-v2/firewall-policy-insert-rule-response.json
   :language: javascript

Remove rule from firewall policy
================================

.. rest_method::  PUT /v2.0/fwaas/firewall_policies/{firewall_policy_id}/remove_rule

Remove firewall rule from a policy.

Normal response codes: 200

Error response codes: 400, 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - firewall_policy_id: firewall_policy_id-path-required
   - firewall_rule_id: firewall_rule_id-body-required

Request Example
---------------

.. literalinclude:: samples/firewall-v2/firewall-policy-remove-rule-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - audited: firewall_policy_audited-body-required
   - description: firewall_policy_description-body-required
   - firewall_rules: firewall_rules-body-required
   - id: firewall_policy_id-body-required
   - name: firewall_policy_name-body-required
   - project_id: project_id-body-required
   - shared: firewall_policy_shared-body-required
   - tenant_id: project_id-body-required

Response Example
----------------

.. literalinclude:: samples/firewall-v2/firewall-policy-remove-rule-response.json
   :language: javascript

