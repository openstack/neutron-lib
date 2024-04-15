.. -*- rst -*-

=================================
Security groups (security-groups)
=================================

Lists, creates, shows information for, updates, and deletes
security groups.

Resource timestamps
===================

The ``standard-attr-timestamp`` extension adds the ``created_at`` and
``updated_at`` attributes to all resources that have standard attributes.

Tag extension
=============

The ``standard-attr-tag`` adds Tag support for resources with
standard attributes by adding the ``tags`` attribute
allowing consumers to associate tags with resources.

Stateful security groups extension (``stateful-security-group``)
================================================================

The stateful security group extension (``stateful-security-group``) adds the
``stateful`` field to security groups, allowing users to configure stateful
or stateless security groups for ``ports``.

A stateless security group bypasses connection tracking in the underlying
firewall, potentially providing performance and simplicity benefits. On the
other hand, using stateless security groups adds more complexity to rule
definitions: the user now has to explicitly define rules for both directions of
a duplex connection, so e.g. two rules have to be defined to allow a TCP flow:
one for packets sent from a port and another one for packets received by the
port.

The existing security groups will all be considered as stateful. Update of the
``stateful`` attribute is allowed when there is no port associated with the
security group.

Regardless of rules defined for a stateless security group, the following
protocols are expected to work: ARP, DHCP, IPv6 SLAAC / DHCPv6 stateless
address configuration, IPv6 Router and Neighbour Discovery.

Note: metadata service is not enabled by default. If your workload requires
metadata for configuration, make sure to create a security group rule that
would allow HTTP replies from the metadata service IP address / port pair.

Shared filtering extension
==========================

The ``security-groups-shared-filtering`` extension adds the ``shared`` field
to security groups and allows users to filter security groups based on the
``shared`` field.

List security groups
====================

.. rest_method::  GET /v2.0/security-groups

Lists OpenStack Networking security groups to which the project has access.

The response is an array of ``security_group`` objects which contains a list of
``security_group_rules`` objects.

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: 401

Request
-------

.. rest_parameters:: parameters.yaml

   - id: id-query
   - tenant_id: project_id-query
   - project_id: project_id-query
   - revision_number: revision_number-query
   - name: name-query
   - description: description-query
   - sort_dir: sort_dir
   - sort_key: security_group-sort_key
   - shared: security_group-shared-query
   - tags: tags-query
   - tags-any: tags-any-query
   - not-tags: not-tags-query
   - not-tags-any: not-tags-any-query
   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - security_groups: security_groups-obj
   - id: security_group-id
   - tenant_id: project_id
   - project_id: project_id
   - created_at: created_at_resource
   - updated_at: updated_at_resource
   - revision_number: revision_number
   - name: name
   - description: description
   - security_group_rules: security_group_rules
   - tags: tags
   - stateful: stateful_enabled
   - shared: security_group-shared-response

Response Example
----------------

.. literalinclude:: samples/security-groups/security-groups-list-response.json
   :language: javascript

Create security group
=====================

.. rest_method::  POST /v2.0/security-groups

Creates an OpenStack Networking security group.

This operation creates a security group with default security group
rules for the IPv4 and IPv6 ether types.

Normal response codes: 201

Error response codes: 400, 401, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - security_group: security_group
   - tenant_id: project_id
   - project_id: project_id
   - description: description-request
   - name: name
   - stateful: stateful_enabled

Request Example
---------------

.. literalinclude:: samples/security-groups/security-group-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - security_group: security_group
   - id: security_group-id
   - tenant_id: project_id
   - project_id: project_id
   - created_at: created_at_resource
   - updated_at: updated_at_resource
   - revision_number: revision_number
   - name: name
   - description: description
   - security_group_rules: security_group_rules
   - tags: tags
   - stateful: stateful_enabled
   - shared: security_group-shared-response

Response Example
----------------

.. literalinclude:: samples/security-groups/security-group-create-response.json
   :language: javascript

Show security group
===================

.. rest_method::  GET /v2.0/security-groups/{security_group_id}

Shows details for a security group.

The associated security group rules are contained in the response.

.. include:: filtering-show.inc

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - security_group_id: security_group-id-path
   - verbose: verbose
   - fields: fields

Request Example
---------------

.. literalinclude:: samples/security-groups/security-group-show-request-json-http.txt
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - security_group: security_group
   - id: security_group-id
   - tenant_id: project_id
   - project_id: project_id
   - created_at: created_at_resource
   - updated_at: updated_at_resource
   - revision_number: revision_number
   - name: name
   - description: description
   - security_group_rules: security_group_rules
   - tags: tags
   - stateful: stateful_enabled
   - shared: security_group-shared-response

Response Example
----------------

.. literalinclude:: samples/security-groups/security-group-show-response.json
   :language: javascript

Update security group
=====================

.. rest_method::  PUT /v2.0/security-groups/{security_group_id}

Updates a security group.

Normal response codes: 200

Error response codes: 400, 401, 403, 404, 412

Request
-------

.. rest_parameters:: parameters.yaml

   - security_group_id: security_group-id-path
   - security_group: security_group
   - description: description-request
   - name: name

Request Example
---------------

.. literalinclude:: samples/security-groups/security-group-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - security_group: security_group
   - id: security_group-id
   - tenant_id: project_id
   - project_id: project_id
   - created_at: created_at_resource
   - updated_at: updated_at_resource
   - revision_number: revision_number
   - name: name
   - description: description
   - security_group_rules: security_group_rules
   - tags: tags
   - stateful: stateful_enabled
   - shared: security_group-shared-response

Response Example
----------------

.. literalinclude:: samples/security-groups/security-group-update-response.json
   :language: javascript

Delete security group
=====================

.. rest_method::  DELETE /v2.0/security-groups/{security_group_id}

Deletes an OpenStack Networking security group.

This operation deletes an OpenStack Networking security group and
its associated security group rules, provided that a port is not
associated with the security group. If a port is associated with the security
group 409 (Conflict) is returned.

This operation does not require a request body. This operation does
not return a response body.

Normal response codes: 204

Error response codes: 401, 404, 409, 412

Request
-------

.. rest_parameters:: parameters.yaml

   - security_group_id: security_group-id-path

Request Example
---------------

.. literalinclude:: samples/security-groups/security-group-delete-request-json-http.txt
   :language: javascript

Response
--------

There is no body content for the response of a successful DELETE request.
