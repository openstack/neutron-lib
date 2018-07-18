.. -*- rst -*-

====================================
Subnet pools extension (subnetpools)
====================================

Lists, creates, shows details for, updates, and deletes subnet
pools.

Address Scopes Extension
========================

The ``address-scope`` extension adds the ``address_scope_id`` attribute to
subnet pools. ``address_scope_id`` is the ID of the address scope that the
subnet pool belongs to.

Resource timestamps
===================

The ``standard-attr-timestamp`` extension adds the ``created_at`` and
``updated_at`` attributes to all resources that have standard attributes.

Tag extension
=============

The ``standard-attr-tag`` adds Tag support for resources with
standard attributes by adding the ``tags`` attribute
allowing consumers to associate tags with resources.

Show subnet pool
================

.. rest_method::  GET /v2.0/subnetpools/{subnetpool_id}

Shows information for a subnet pool.

Use the ``fields`` query parameter to control which fields are returned in the response body.
Additionally, you can filter results by using query string parameters.
For information, see `Filtering and Column Selection <https://wiki.openstack.org/wiki/Neutron/APIv2
-specification#Filtering_and_Column_Selection>`__.

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - subnetpool_id: subnetpool_id
   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - subnetpool: subnetpool
   - id: subnetpool_id_body
   - name: name
   - default_quota: default_quota
   - tenant_id: project_id
   - project_id: project_id
   - created_at: created_at_resource
   - updated_at: updated_at_resource
   - prefixes: prefixes
   - min_prefixlen: min_prefixlen
   - address_scope_id: address_scope_id
   - ip_version: ip_version
   - shared: shared
   - default_prefixlen: default_prefixlen
   - max_prefixlen: max_prefixlen
   - description: description
   - is_default: subnetpool_is_default
   - revision_number: revision_number
   - tags: tags

Response Example
----------------

.. literalinclude:: samples/subnets/subnetpool-show-response.json
   :language: javascript

Update subnet pool
==================

.. rest_method::  PUT /v2.0/subnetpools/{subnetpool_id}

Updates a subnet pool.

Normal response codes: 200

Error response codes: 400, 401, 403, 404, 412

Request
-------

.. rest_parameters:: parameters.yaml

   - subnetpool_id: subnetpool_id
   - subnetpool: subnetpool
   - name: name
   - default_quota: default_quota
   - tenant_id: project_id
   - project_id: project_id
   - prefixes: prefixes
   - min_prefixlen: min_prefixlen
   - address_scope_id: address_scope_id
   - default_prefixlen: default_prefixlen
   - max_prefixlen: max_prefixlen
   - description: description-request
   - is_default: subnetpool_is_default-request

Request Example
---------------

.. literalinclude:: samples/subnets/subnetpool-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - subnetpool: subnetpool
   - id: subnetpool_id_body
   - name: name
   - default_quota: default_quota
   - tenant_id: project_id
   - project_id: project_id
   - created_at: created_at_resource
   - updated_at: updated_at_resource
   - prefixes: prefixes
   - min_prefixlen: min_prefixlen
   - address_scope_id: address_scope_id
   - ip_version: ip_version
   - shared: shared
   - default_prefixlen: default_prefixlen
   - max_prefixlen: max_prefixlen
   - description: description
   - is_default: subnetpool_is_default
   - revision_number: revision_number
   - tags: tags

Response Example
----------------

.. literalinclude:: samples/subnets/subnetpool-update-response.json
   :language: javascript

Delete subnet pool
==================

.. rest_method::  DELETE /v2.0/subnetpools/{subnetpool_id}

Deletes a subnet pool.

The operation fails if any subnets allocated from the subnet pool
are still in use.

Normal response codes: 204

Error response codes: 401, 404, 412

Request
-------

.. rest_parameters:: parameters.yaml

   - subnetpool_id: subnetpool_id

Response
--------

There is no body content for the response of a successful DELETE request.

List subnet pools
=================

.. rest_method::  GET /v2.0/subnetpools

Lists subnet pools that the project has access to.

Default policy settings return only the subnet pools owned by
the project of the user submitting the request, unless the
user has administrative role.

Use the ``fields`` query parameter to control which fields are returned in the response body.
Additionally, you can filter results by using query string parameters.
For information, see `Filtering and Column Selection <https://wiki.openstack.org/wiki/Neutron/APIv2
-specification#Filtering_and_Column_Selection>`__.

Normal response codes: 200

Error response codes: 401

Request
-------

.. rest_parameters:: parameters.yaml

   - id: id-query
   - name: name-query
   - default_quota: default_quota-query
   - tenant_id: project_id-query
   - project_id: project_id-query
   - min_prefixlen: min_prefixlen-query
   - address_scope_id: address_scope_id-query
   - ip_version: ip_version-query
   - shared: shared-query
   - default_prefixlen: default_prefixlen-query
   - max_prefixlen: max_prefixlen-query
   - description: description-query
   - is_default: subnetpool_is_default-query
   - revision_number: revision_number-query
   - sort_dir: sort_dir
   - sort_key: subnetpool-sort_key
   - tags: tags-query
   - tags-any: tags-any-query
   - not-tags: not-tags-query
   - not-tags-any: not-tags-any-query
   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - subnetpools: subnetpools
   - id: subnetpool_id_body
   - name: name
   - default_quota: default_quota
   - tenant_id: project_id
   - project_id: project_id
   - created_at: created_at_resource
   - updated_at: updated_at_resource
   - prefixes: prefixes
   - min_prefixlen: min_prefixlen
   - address_scope_id: address_scope_id
   - ip_version: ip_version
   - shared: shared
   - default_prefixlen: default_prefixlen
   - max_prefixlen: max_prefixlen
   - description: description
   - is_default: subnetpool_is_default
   - revision_number: revision_number
   - tags: tags

Response Example
----------------

.. literalinclude:: samples/subnets/subnetpools-list-response.json
   :language: javascript

Create subnet pool
==================

.. rest_method::  POST /v2.0/subnetpools

Creates a subnet pool.

Normal response codes: 201

Error response codes: 400, 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - subnetpool: subnetpool
   - name: name
   - default_quota: default_quota
   - tenant_id: project_id
   - project_id: project_id
   - prefixes: prefixes
   - min_prefixlen: min_prefixlen
   - address_scope_id: address_scope_id
   - shared: shared
   - default_prefixlen: default_prefixlen
   - max_prefixlen: max_prefixlen
   - description: description-request
   - is_default: subnetpool_is_default

Request Example
---------------

.. literalinclude:: samples/subnets/subnetpool-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - subnetpool: subnetpool
   - id: subnetpool_id_body
   - name: name
   - default_quota: default_quota
   - tenant_id: project_id
   - project_id: project_id
   - created_at: created_at_resource
   - updated_at: updated_at_resource
   - prefixes: prefixes
   - min_prefixlen: min_prefixlen
   - address_scope_id: address_scope_id
   - ip_version: ip_version
   - shared: shared
   - default_prefixlen: default_prefixlen
   - max_prefixlen: max_prefixlen
   - description: description
   - is_default: subnetpool_is_default
   - revision_number: revision_number
   - tags: tags

Response Example
----------------

.. literalinclude:: samples/subnets/subnetpool-create-response.json
   :language: javascript
