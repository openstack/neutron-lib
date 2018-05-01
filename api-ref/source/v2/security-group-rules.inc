.. -*- rst -*-

.. _security_group_rules:

===========================================
Security group rules (security-group-rules)
===========================================

Lists, creates, shows information for, and deletes security group
rules.

Resource timestamps
===================

The ``standard-attr-timestamp`` extension adds the ``created_at`` and
``updated_at`` attributes to all resources that have standard attributes.

List security group rules
=========================

.. rest_method::  GET /v2.0/security-group-rules

Lists a summary of all OpenStack Networking security group rules that the project can access.

The list provides the ID for each security group rule.

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

   - remote_group_id: remote_group_id-query
   - direction: direction-query
   - protocol: protocol-query
   - ethertype: ethertype-query
   - port_range_max: port_range_max-query
   - security_group_id: security_group_rule-security_group_id-query
   - tenant_id: project_id-query
   - project_id: project_id-query
   - port_range_min: port_range_min-query
   - remote_ip_prefix: remote_ip_prefix-query
   - revision_number: revision_number-query
   - id: id-query
   - description: description-query
   - sort_dir: sort_dir
   - sort_key: security_group_rule-sort_key
   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - security_group_rules: security_group_rules
   - remote_group_id: remote_group_id
   - direction: direction
   - protocol: protocol
   - ethertype: ethertype
   - port_range_max: port_range_max
   - security_group_id: security_group_rule-security_group_id
   - tenant_id: project_id
   - project_id: project_id
   - port_range_min: port_range_min
   - remote_ip_prefix: remote_ip_prefix
   - created_at: created_at_resource
   - updated_at: updated_at_resource
   - revision_number: revision_number
   - id: security_group_rule-id
   - description: description

Response Example
----------------

.. literalinclude:: samples/security-groups/security-group-rules-list-response.json
   :language: javascript

Create security group rule
==========================

.. rest_method::  POST /v2.0/security-group-rules

Creates an OpenStack Networking security group rule.

Normal response codes: 201

Error response codes: 400, 401, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - security_group_rule: security_group_rule
   - remote_group_id: remote_group_id-request
   - direction: direction
   - protocol: protocol-request
   - ethertype: ethertype-request
   - port_range_max: port_range_max-request
   - security_group_id: security_group_rule-security_group_id
   - port_range_min: port_range_min-request
   - remote_ip_prefix: remote_ip_prefix-request
   - description: description-request

Request Example
---------------

.. literalinclude:: samples/security-groups/security-group-rule-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - security_group_rule: security_group_rule
   - remote_group_id: remote_group_id
   - direction: direction
   - protocol: protocol
   - ethertype: ethertype
   - port_range_max: port_range_max
   - security_group_id: security_group_rule-security_group_id
   - tenant_id: project_id
   - project_id: project_id
   - port_range_min: port_range_min
   - remote_ip_prefix: remote_ip_prefix
   - created_at: created_at_resource
   - updated_at: updated_at_resource
   - revision_number: revision_number
   - id: security_group_rule-id
   - description: description

Response Example
----------------

.. literalinclude:: samples/security-groups/security-group-rule-create-response.json
   :language: javascript

Show security group rule
========================

.. rest_method::  GET /v2.0/security-group-rules/{security_group_rule_id}

Shows detailed information for a security group rule.

The response body contains the following information about the
security group rule:

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - security_group_rule_id: security_group_rule-id-path
   - verbose: verbose
   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - security_group_rule: security_group_rule
   - remote_group_id: remote_group_id
   - direction: direction
   - protocol: protocol
   - ethertype: ethertype
   - port_range_max: port_range_max
   - security_group_id: security_group_rule-security_group_id
   - tenant_id: project_id
   - project_id: project_id
   - port_range_min: port_range_min
   - remote_ip_prefix: remote_ip_prefix
   - created_at: created_at_resource
   - updated_at: updated_at_resource
   - revision_number: revision_number
   - id: security_group_rule-id
   - description: description

Response Example
----------------

.. literalinclude:: samples/security-groups/security-group-rule-show-response.json
   :language: javascript

Delete security group rule
==========================

.. rest_method::  DELETE /v2.0/security-group-rules/{security_group_rule_id}

Deletes a rule from an OpenStack Networking security group.

Normal response codes: 204

Error response codes: 401, 404, 412

Request
-------

.. rest_parameters:: parameters.yaml

   - security_group_rule_id: security_group_rule-id-path

Response
--------

There is no body content is returned on a successful DELETE request.
