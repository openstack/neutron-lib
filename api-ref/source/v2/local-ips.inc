.. -*- rst -*-

=====================
Local IPs (local_ips)
=====================

Extension that allows users to create a virtual IP that can later be assigned
to multiple ports/VMs (similar to anycast IP) and is guaranteed to only be
reachable within the same physical server/node boundaries.

Resource timestamps
===================

The ``standard-attr-timestamp`` extension adds the ``created_at`` and
``updated_at`` attributes to all resources that have standard attributes.

List Local IPs
==============

.. rest_method::  GET /v2.0/local_ips

Lists Local IPs visible to the user.

Default policy settings return only the Local IPs owned by the user's
project, unless the user has admin role.

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: 401

Request
-------

.. rest_parameters:: parameters.yaml

   - id: local_ip-id-query
   - name: name-query
   - description: description-query
   - project_id: project_id-query
   - local_port_id: local_ip-local_port_id-query
   - network_id: network_id-query
   - local_ip_address: local_ip_address-query
   - ip_mode: local_ip-ip_mode-query
   - revision_number: revision_number-query
   - sort_dir: sort_dir
   - sort_key: local_ip-sort_key
   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - local_ips: local_ips
   - id: local_ip-id
   - name: name
   - description: description
   - project_id: project_id
   - local_port_id: local_ip-local_port_id
   - network_id: network_id
   - local_ip_address: local_ip_address
   - ip_mode: local_ip-ip_mode
   - created_at: created_at_resource
   - updated_at: updated_at_resource
   - revision_number: revision_number

Response Example
----------------

.. literalinclude:: samples/local_ips/local-ips-list-response.json
   :language: javascript

Create Local IP
===============

.. rest_method::  POST /v2.0/local_ips

Creates a Local IP, and, if you don't specify existing port ID,
allocates an internal port with IP address from specified network.

The operation returns the ``Bad Request (400)`` response code for one of
reasons:

  - The requested local IP address does not fall in the subnet
    range for the specified network.

  - The local IP address is not valid.

  - Specified local_port_id has no fixed IP address

  - Specified local_port_id has multiple fixed IP address and local_ip
    was not specified

  - Specified ip_mode is not supported

If the local_port_id or network_id is not valid, this operation returns
``404`` response code.

The operation returns the ``Conflict (409)`` response code for one of
reasons:

  - Both local_port_id and network_id are specified in the request

  - Both local_port_id and local_ip are specified, but port has no such
    local IP

  - Both network_id and local_ip_address are specified, but network has
    no subnets to satisfy the IP requested

Normal response codes: 201

Error response codes: 400, 401, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - local_ip: local_ip
   - name: name-request
   - description: description-request
   - project_id: project_id-request
   - local_port_ip: local_ip-local_port_id-request
   - network_id: local_ip-network_id-request
   - local_ip_address: local_ip_address-request
   - ip_mode: local_ip-ip_mode-request

Request Example
---------------

.. literalinclude:: samples/local_ips/local_ip-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - local_ip: local_ip
   - id: local_ip-id
   - name: name
   - description: description
   - project_id: project_id
   - local_port_id: local_ip-local_port_id
   - network_id: local_ip-network_id
   - local_ip_address: local_ip_address
   - ip_mode: local_ip-ip_mode
   - created_at: created_at_resource
   - updated_at: updated_at_resource
   - revision_number: revision_number

Response Example
----------------

.. literalinclude:: samples/local_ips/local_ip-create-response.json
   :language: javascript

Show Local IP details
=====================

.. rest_method::  GET /v2.0/local_ips/{local_ip_id}

Shows details for a Local IP.

.. include:: filtering-show.inc

Normal response codes: 200

Error response codes: 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - local_ip_id: local_ip-id-path
   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - local_ip: local_ip
   - id: local_ip-id
   - name: name
   - description: description
   - project_id: project_id
   - local_port_id: local_ip-local_port_id
   - network_id: local_ip-network_id
   - local_ip_address: local_ip_address
   - ip_mode: local_ip-ip_mode
   - created_at: created_at_resource
   - updated_at: updated_at_resource
   - revision_number: revision_number

Response Example
----------------

.. literalinclude:: samples/local_ips/local_ip-show-response.json
   :language: javascript

Update Local IP
===============

.. rest_method::  PUT /v2.0/local_ips/{local_ip_id}

Updates a Local IP.

Normal response codes: 200

Error response codes: 400, 401, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - local_ip: local_ip
   - local_ip_id: local_ip-id-path
   - name: name-request
   - description: description-request

Request Example
---------------

.. literalinclude:: samples/local_ips/local_ip-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - local_ip: local_ip
   - id: local_ip-id
   - name: name
   - description: description
   - project_id: project_id
   - local_port_id: local_ip-local_port_id
   - network_id: local_ip-network_id
   - local_ip_address: local_ip_address
   - ip_mode: local_ip-ip_mode
   - created_at: created_at_resource
   - updated_at: updated_at_resource
   - revision_number: revision_number

Response Example
----------------

.. literalinclude:: samples/local_ips/local_ip-update-response.json
   :language: javascript

Delete Local IP
===============

.. rest_method::  DELETE /v2.0/local_ips/{local_ip_id}

Deletes a Local IP and, if applicable, its underlying port.
Underlying port is deleted in case it was created specifically for this
Local IP, and has corresponding device_owner and device_id.

The operation returns the ``Precondition Failed  (412)`` response code for
the following reason:

  - The requested Local IP is still associated with some ports.

Normal response codes: 204

Error response codes: 401, 404, 412

Request
-------

.. rest_parameters:: parameters.yaml

   - local_ip_id: local_ip-id-path

Response
--------

There is no body content for the response of a successful DELETE request.

=========================================
Local IP Associations (port_associations)
=========================================

The resource lets users assign Local IPs to user Ports.
This is a sub-resource of the Local IP resource.

List Local IP Associations
==========================

.. rest_method::  GET /v2.0/local_ips/{local_ip_id}/port_associations

Lists Associations for the given Local IP.

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: 401

Request
-------

.. rest_parameters:: parameters.yaml

   - local_ip_id: local_ip-id-path
   - fixed_port_id: local_ip_association-fixed_port_id-query
   - fixed_ip: local_ip_association-fixed_ip-query
   - host: local_ip_association-host-query
   - sort_dir: sort_dir
   - sort_key: local_ip_association-sort_key
   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - local_ip_associations: local_ip_associations
   - local_ip_id: local_ip-id
   - local_ip_address: local_ip_address
   - fixed_port_id: local_ip_association-fixed_port_id
   - fixed_ip: local_ip_association-fixed_ip
   - host: local_ip_association-host

Response Example
----------------

.. literalinclude:: samples/local_ips/local-ip-list-associations-response.json
   :language: javascript

Create Local IP Association
===========================

.. rest_method::  POST /v2.0/local_ips/{local_ip_id}/port_associations

Creates a Local IP association with a given Port.
If a Port has multiple fixed IPs user must specify which IP to use
for association.

The operation returns the ``Conflict (409)`` response code for one of
reasons:

  - Specified fixed_port_id has multiple fixed IP addresses and fixed_ip
    was not specified

  - Both fixed_port_id and fixed_ip are specified in the request, but port
    has no such fixed IP

Normal response codes: 201

Error response codes: 400, 401, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - local_ip_id: local_ip-id-path
   - fixed_port_id: local_ip_association-fixed_port_id-request
   - fixed_ip: local_ip_association-fixed_ip-request

Request Example
---------------

.. literalinclude:: samples/local_ips/local_ip_association-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - local_ip_association: local_ip_association
   - local_ip_id: local_ip_id
   - fixed_port_id: local_ip_association-fixed_port_id
   - fixed_ip: local_ip_association-fixed_ip
   - host: local_ip_association-host

Response Example
----------------

.. literalinclude:: samples/local_ips/local_ip_association-create-response.json
   :language: javascript

Delete Local IP Association
===========================

.. rest_method::  DELETE /v2.0/local_ips/{local_ip_id}/port_associations/{fixed_port_id}

Deletes a Local IP association.

Normal response codes: 204

Error response codes: 400, 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - local_ip_id: local_ip-id-path
   - fixed_port_id: local_ip_association-fixed_port_id-path

Response
--------

There is no body content for the response of a successful DELETE request.
