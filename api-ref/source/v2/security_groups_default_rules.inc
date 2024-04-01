.. -*- rst -*-

.. _security_group_default_rules:

===========================================================
Security group default rules (security-group-default-rules)
===========================================================

Lists, creates, shows information for, and deletes security group
default rules.

List security group default rules
=================================

.. rest_method::  GET /v2.0/default-security-group-rules

Lists a summary of all OpenStack Networking security group rules that are used
for every newly created Security Group.

The list provides the ID for each security group default rule.

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: 401

Request
-------

.. rest_parameters:: parameters.yaml

   - remote_group_id: remote_group_id_template-query
   - direction: direction-query
   - protocol: protocol-query
   - ethertype: ethertype-query
   - port_range_max: port_range_max-query
   - port_range_min: port_range_min-query
   - remote_ip_prefix: remote_ip_prefix-query
   - remote_address_group_id: remote_address_group_id-query
   - used_in_default_sg: used_in_default_sg-query
   - used_in_non_default_sg: used_in_non_default_sg-query
   - id: id-query
   - description: description-query
   - sort_dir: sort_dir
   - sort_key: security_group_rule-sort_key
   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - security_group_rules: security_group_rules
   - remote_group_id: remote_group_id_template-query
   - direction: direction
   - protocol: protocol
   - ethertype: ethertype
   - port_range_max: port_range_max
   - port_range_min: port_range_min
   - remote_ip_prefix: remote_ip_prefix
   - remote_address_group_id: remote_address_group_id
   - used_in_default_sg: used_in_default_sg
   - used_in_non_default_sg: used_in_non_default_sg
   - id: default_security_group_rule-id
   - description: description

Response Example
----------------

.. literalinclude:: samples/security-group-default-rules/security-group-default-rules-list-response.json
   :language: javascript

Create security group default rule
==================================

.. rest_method::  POST /v2.0/default-security-group-rules

Creates an Openstack Networking security group rule template.

Normal response codes: 201

Error response codes: 400, 401, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - default_security_group_rule: security_group_default_rule
   - remote_group_id: remote_group_id-request
   - direction: direction
   - protocol: protocol-request
   - ethertype: ethertype-request
   - port_range_max: port_range_max-request
   - port_range_min: port_range_min-request
   - remote_ip_prefix: remote_ip_prefix-request
   - remote_address_group_id: remote_address_group_id-request
   - used_in_default_sg: used_in_default_sg
   - used_in_non_default_sg: used_in_non_default_sg
   - description: description-request

Request Example
---------------

.. literalinclude:: samples/security-group-default-rules/security-group-default-rule-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - remote_group_id: remote_group_id
   - direction: direction
   - protocol: protocol
   - ethertype: ethertype
   - port_range_max: port_range_max
   - port_range_min: port_range_min
   - remote_ip_prefix: remote_ip_prefix
   - remote_address_group_id: remote_address_group_id
   - used_in_default_sg: used_in_default_sg
   - used_in_non_default_sg: used_in_non_default_sg
   - id: default_security_group_rule-id
   - description: description

Response Example
----------------

.. literalinclude:: samples/security-group-default-rules/security-group-default-rule-create-response.json
   :language: javascript

.. warning::

    The security group rule template APIs do not validate the UUID of the resources
    like ``remote address group id`` or ``remote group ID``.  Any string can be
    provided here, but please note that it will be used to create real security
    group rules for projects, and if the UUID of a non-existing ``security
    group`` or ``remote address group`` is used, it will cause errors during
    creation of the security groups.

Show security group default rule
================================

.. rest_method::  GET /v2.0/default-security-group-rules/{default_security_group_rule_id}

Shows detailed information for a security group default rule.

The response body contains the following information about the
security group rule:

.. include:: filtering-show.inc

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - default_security_group_rule_id: default_security_group_rule-id-path
   - verbose: verbose
   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - default_security_group_rule: security_group_default_rule
   - remote_group_id: remote_group_id
   - direction: direction
   - protocol: protocol
   - ethertype: ethertype
   - port_range_max: port_range_max
   - port_range_min: port_range_min
   - remote_ip_prefix: remote_ip_prefix
   - remote_address_group_id: remote_address_group_id
   - used_in_default_sg: used_in_default_sg
   - used_in_non_default_sg: used_in_non_default_sg
   - id: default_security_group_rule-id
   - description: description

Response Example
----------------

.. literalinclude:: samples/security-group-default-rules/security-group-default-rule-show-response.json
   :language: javascript

Delete security group default rule
==================================

.. rest_method::  DELETE /v2.0/default-security-group-rules/{default_security_group_rule_id}

Deletes an OpenStack Networking security group rule template.

Normal response codes: 204

Error response codes: 401, 404, 412

Request
-------

.. rest_parameters:: parameters.yaml

   - default_security_group_rule_id: default_security_group_rule-id-path

Response
--------

There is no body content is returned on a successful DELETE request.
