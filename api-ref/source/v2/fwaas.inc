==========================================================================
FWaaS v1.0 (DEPRECATED) (fw, firewalls, firewall_policies, firewall_rules)
==========================================================================

.. note::

    While FWaaS v1.0 is still maintained, new features will be
    implemented in FWaaS v2.0 API.

Use the Firewall-as-a-Service (FWaaS) v1.0 extension to deploy
firewalls to protect your networks.

The FWaaS extension enables you to:

- Apply firewall rules on traffic entering and leaving project
  networks.

- Apply TCP, UDP, ICMP, or protocol-agnostic rules.

- Create and share firewall policies that hold an ordered collection
  of the firewall rules.

- Audit firewall rules and policies.

This extension introduces these resources:

- ``firewall``. A logical firewall resource that a project can
  instantiate and manage. A firewall can have one firewall policy.

- ``firewall_policy``. An ordered collection of firewall rules. You
  can share a firewall policy across projects. You can include a
  firewall policy as part of an audit workflow so that an
  authorized relevant entity can audit the firewall policy. This
  entity can differ from the user who created, or the projects
  that use, the firewall policy.

- ``firewall_rule``. A collection of attributes, such as ports and
  IP addresses. These attributes define match criteria and an
  action to take, such as allow or deny, on matched data traffic.

List firewall policies
======================

.. rest_method::  GET /v2.0/fw/firewall_policies

Lists all firewall policies.

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

   - tenant_id: project_id
   - firewall_policies: firewall_policies
   - audited: audited
   - description: description
   - firewall_rules: firewall_rules
   - id: firewall_policy_id-body
   - name: name
   - shared: shared-response
   - project_id: project_id

Response Example
----------------

.. literalinclude:: samples/firewalls/firewall-policies-list-response.json
   :language: javascript

Create firewall policy
======================

.. rest_method::  POST /v2.0/fw/firewall_policies

Creates a firewall policy.

Normal response codes: 201

Error response codes: 400, 401

Request
-------

.. rest_parameters:: parameters.yaml

   - firewall_policy: firewall_policy
   - firewall_rules_id: firewall_rules_id
   - name: name
   - tenant_id: project_id-request
   - project_id: project_id-request
   - shared: shared
   - audited: audited
   - description: description-request

Request Example
---------------

.. literalinclude:: samples/firewalls/firewall-policy-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - firewall_policy: firewall_policy
   - name: name
   - firewall_rules: firewall_rules
   - tenant_id: project_id
   - project_id: project_id
   - audited: audited
   - shared: shared-response
   - id: firewall_policy_id-body
   - description: description

Show firewall policy details
============================

.. rest_method::  GET /v2.0/fw/firewall_policies/{firewall_policy_id}

Shows details for a firewall policy.

If the user is not an administrative user and the firewall policy
object does not belong to the project, this call returns the
``Forbidden (403)`` response code.

Normal response codes: 200

Error response codes: 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - firewall_policy_id: firewall_policy_id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - firewall_policy: firewall_policy
   - tenant_id: project_id
   - project_id: project_id
   - audited: audited
   - description: description
   - firewall_rules: firewall_rules
   - id: firewall_policy_id-body
   - name: name
   - shared: shared-response

Response Example
----------------

.. literalinclude:: samples/firewalls/firewall-policy-show-response.json
   :language: javascript

Update firewall policy
======================

.. rest_method::  PUT /v2.0/fw/firewall_policies/{firewall_policy_id}

Updates a firewall policy.

Normal response codes: 200

Error response codes: 400, 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - firewall_policy_id: firewall_policy_id-path
   - firewall_rule: firewall_rule
   - shared: shared
   - audited: audited
   - description: description-request
   - name: name

Request Example
---------------

.. literalinclude:: samples/firewalls/firewall-policy-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - firewall_policy: firewall_policy
   - project_id: project_id
   - audited: audited
   - description: description
   - firewall_rules: firewall_rules
   - id: firewall_policy_id-body
   - name: name
   - shared: shared-response
   - tenant_id: project_id

Response Example
----------------

.. literalinclude:: samples/firewalls/firewall-policy-update-response.json
   :language: javascript

Delete firewall policy
======================

.. rest_method::  DELETE /v2.0/fw/firewall_policies/{firewall_policy_id}

Deletes a firewall policy.

Normal response codes: 204

Error response codes: 401, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - firewall_policy_id: firewall_policy_id-path

Response
--------

There is no body content for the response of a successful DELETE request.

Insert rule into a firewall policy
==================================

.. rest_method::  PUT /v2.0/fw/firewall_policies/{firewall_policy_id}/insert_rule

Insert firewall rule into a policy.

A firewall_rule_id is inserted relative to the position of the
firewall_rule_id set in ``insert_before`` or ``insert_after``. If
``insert_before`` is set, ``insert_after`` is ignored. If both
``insert_before`` and ``insert_after`` are not set, the new
firewall_rule_id is inserted at the top of the policy.

Normal response codes: 200

Error response codes: 400, 401, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - firewall_policy_id: firewall_policy_id-path
   - firewall_rule_id: firewall_rule_id-body
   - insert_after: insert_after
   - insert_before: insert_before

Request Example
---------------

.. literalinclude:: samples/firewalls/firewall-policy-insert-rule-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - audited: audited
   - description: description
   - firewall_list: firewall_list
   - firewall_rules: firewall_rules
   - tenant_id: project_id
   - project_id: project_id
   - id: firewall_policy_id-body
   - name: name
   - shared: shared-response

Response Example
----------------

.. literalinclude:: samples/firewalls/firewall-policy-insert-rule-response.json
   :language: javascript

Remove rule from firewall policy
================================

.. rest_method::  PUT /v2.0/fw/firewall_policies/{firewall_policy_id}/remove_rule

Remove firewall rule from a policy.

Normal response codes: 200

Error response codes: 400, 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - firewall_policy_id: firewall_policy_id-path
   - firewall_rule_id: firewall_rule_id-body

Request Example
---------------

.. literalinclude:: samples/firewalls/firewall-policy-remove-rule-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - tenant_id: project_id
   - project_id: project_id
   - audited: audited
   - description: description
   - firewall_list: firewall_list
   - firewall_rules: firewall_rules
   - id: firewall_id-body
   - name: name
   - shared: shared-response

Response Example
----------------

.. literalinclude:: samples/firewalls/firewall-policy-remove-rule-response.json
   :language: javascript

List firewall rules
===================

.. rest_method::  GET /v2.0/fw/firewall_rules

Lists all firewall rules.

The list might be empty.

Normal response codes: 200

Error response codes: 401, 403

Request
-------

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - firewall_rule: firewall_rule
   - action: action-response
   - description: description
   - tenant_id: project_id
   - project_id: project_id
   - destination_ip_address: destination_ip_address-response
   - destination_port: destination_port-response
   - enabled: enabled-response
   - firewall_policy_id: firewall_policy_id-body
   - id: firewall_id-body
   - ip_version: ip_version-response
   - name: name
   - position: position
   - protocol: protocol-response
   - shared: shared-response
   - source_ip_address: source_ip_address
   - source_port: source_port-response

Response Example
----------------

.. literalinclude:: samples/firewalls/firewall-rules-list-response.json
   :language: javascript

Create firewall rule
====================

.. rest_method::  POST /v2.0/fw/firewall_rules

Creates a firewall rule.

Normal response codes: 201

Error response codes: 400, 401

Request
-------

.. rest_parameters:: parameters.yaml

   - firewall_rule: firewall_rule
   - action: action
   - destination_port: destination_port
   - enabled: enabled
   - description: description-request
   - tenant_id: project_id-request
   - project_id: project_id-request
   - enabled: enabled
   - name: name
   - protocol: protocol
   - ip_version: ip_version
   - destination_ip_address: destination_ip_address
   - source_port: source_port
   - shared: shared

Request Example
---------------

.. literalinclude:: samples/firewalls/firewall-rule-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - firewall_rule: firewall_rule
   - action: action-response
   - description: description
   - tenant_id: project_id
   - project_id: project_id
   - destination_ip_address: destination_ip_address-response
   - destination_port: destination_port-response
   - enabled: enabled-response
   - firewall_policy_id: firewall_policy_id-body
   - id: firewall_id-body
   - ip_version: ip_version-response
   - name: name
   - position: position
   - protocol: protocol-response
   - shared: shared-response
   - source_ip_address: source_ip_address
   - source_port: source_port-response

Response Example
----------------

.. literalinclude:: samples/firewalls/firewall-rule-create-response.json
   :language: javascript

Show firewall rule details
==========================

.. rest_method::  GET /v2.0/fw/firewall_rules/{firewall_rule_id}

Shows details for a firewall rule.

If the user is not an administrative user and the firewall rule
object does not belong to the project, this call returns the
``Forbidden (403)`` response code.

Normal response codes: 200

Error response codes: 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - firewall_rule_id: firewall_rule_id

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - firewall_rule: firewall_rule
   - action: action-response
   - description: description
   - tenant_id: project_id
   - project_id: project_id
   - destination_ip_address: destination_ip_address-response
   - destination_port: destination_port-response
   - enabled: enabled-response
   - firewall_policy_id: firewall_policy_id
   - id: firewall_rule_id-body
   - ip_version: ip_version-response
   - name: name
   - position: position
   - protocol: protocol-response
   - shared: shared-response
   - source_ip_address: source_ip_address
   - source_port: source_port-response

Response Example
----------------

.. literalinclude:: samples/firewalls/firewall-rule-show-response.json
   :language: javascript

Update firewall rule
====================

.. rest_method::  PUT /v2.0/fw/firewall_rules/{firewall_rule_id}

Updates a firewall rule.

Normal response codes: 200

Error response codes: 400, 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - firewall_rule_id: firewall_rule_id
   - firewall_rule: firewall_rule
   - shared: shared
   - description: description-request
   - tenant_id: project_id-request
   - project_id: project_id-request
   - enabled: enabled
   - ip_version: ip_version
   - destination_ip_address: destination_ip_address
   - source_port: source_port
   - action: action
   - protocol: protocol
   - destination_port: destination_port
   - name: name

Request Example
---------------

.. literalinclude:: samples/firewalls/firewall-rule-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - firewall_rule: firewall_rule
   - action: action-response
   - description: description
   - source_ip_address: source_ip_address
   - tenant_id: project_id
   - project_id: project_id
   - enabled: enabled
   - protocol: protocol
   - source_port: source_port
   - ip_version: ip_version
   - destination_ip_address: destination_ip_address-response
   - destination_port: destination_port-response
   - enabled: enabled-response
   - firewall_policy_id: firewall_policy_id
   - id: firewall_rule_id-body
   - ip_version: ip_version-response
   - name: name
   - position: position
   - protocol: protocol-response
   - shared: shared-response
   - source_ip_address: source_ip_address
   - source_port: source_port-response

Response Example
----------------

.. literalinclude:: samples/firewalls/firewall-rule-update-response.json
   :language: javascript

Delete firewall rule
====================

.. rest_method::  DELETE /v2.0/fw/firewall_rules/{firewall_rule_id}

Deletes a firewall rule.

Normal response codes: 204

Error response codes: 401, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - firewall_rule_id: firewall_rule_id

Response
--------

There is no body content for the response of a successful DELETE request.

List firewalls
==============

.. rest_method::  GET /v2.0/fw/firewalls

Lists all firewalls.

The list might be empty.

Normal response codes: 200

Error response codes: 401, 403

Request
-------

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - firewalls: firewalls
   - admin_state_up: admin_state_up
   - tenant_id: project_id
   - project_id: project_id
   - description: description
   - firewall_policy_id: firewall_policy_id-body
   - id: firewall_id-body
   - name: name
   - status: firewall-status

Response Example
----------------

.. literalinclude:: samples/firewalls/firewalls-list-response.json
   :language: javascript

Create firewall
===============

.. rest_method::  POST /v2.0/fw/firewalls

Creates a firewall.

The firewall must be associated with a firewall policy.

If ``admin_state_up`` is ``false``, the firewall would block all
traffic.

Normal response codes: 201

Error response codes: 400, 401

Request
-------

.. rest_parameters:: parameters.yaml

   - firewall: firewall
   - admin_state_up: admin_state_up
   - firewall_policy_id: firewall_policy_id-body
   - description: description-request
   - name: name
   - router_ids: router_ids

Request Example
---------------

.. literalinclude:: samples/firewalls/firewall-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - firewall: firewall
   - tenant_id: project_id
   - project_id: project_id
   - admin_state_up: admin_state_up
   - description: description
   - firewall_policy_id: firewall_policy_id-body
   - id: firewall_id-body
   - name: name
   - status: firewall-status
   - router_ids: router_ids-response

Response Example
----------------

.. literalinclude:: samples/firewalls/firewall-create-response.json
   :language: javascript

Show firewall details
=====================

.. rest_method::  GET /v2.0/fw/firewalls/{firewall_id}

Shows details for a firewall.

If the user is not an administrative user and the firewall object
does not belong to the project, this call returns the
``Forbidden (403)`` response code.

Normal response codes: 200

Error response codes: 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - firewall_id: firewall_id

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - firewall: firewall
   - tenant_id: project_id
   - project_id: project_id
   - admin_state_up: admin_state_up
   - description: description
   - status: firewall-status
   - firewall_policy_id: firewall_policy_id
   - id: firewall_rule_id-body
   - name: name
   - router_ids: router_ids-response

Response Example
----------------

.. literalinclude:: samples/firewalls/firewall-show-response.json
   :language: javascript

Update firewall
===============

.. rest_method::  PUT /v2.0/fw/firewalls/{firewall_id}

Updates a firewall.

To update a service, the service status cannot be a ``PENDING_*``
status.

Normal response codes: 200

Error response codes: 400, 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - firewall_id: firewall_id
   - firewall: firewall
   - admin_state_up: admin_state_up
   - description: description-request
   - firewall_policy_id: firewall_policy_id-body
   - name: name
   - router_ids: router_ids

Request Example
---------------

.. literalinclude:: samples/firewalls/firewall-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - firewall: firewall
   - tenant_id: project_id
   - project_id: project_id
   - admin_state_up: admin_state_up
   - description: description
   - status: firewall-status
   - firewall_policy_id: firewall_policy_id-body
   - id: firewall_id-body
   - name: name
   - router_ids: router_ids-response

Response Example
----------------

.. literalinclude:: samples/firewalls/firewall-update-response.json
   :language: javascript

Delete firewall
===============

.. rest_method::  DELETE /v2.0/fw/firewalls/{firewall_id}

Deletes a firewall.

Normal response codes: 204

Error response codes: 401, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - firewall_id: firewall_id

Response
--------

There is no body content for the response of a successful DELETE request.
