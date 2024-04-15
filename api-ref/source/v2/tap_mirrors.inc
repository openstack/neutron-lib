.. -*- rst -*-

===========
Tap Mirrors
===========

Tap Mirrors provide a way to mirror traffic from a Neutron port to an external
IP in a GRE or ERSPAN v1 tunnel.

List Tap Mirrors
=================

.. rest_method:: GET /v2.0/taas/tap_mirrors

List tap mirrors that belong to a given project.

The list might be empty.

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: 401

Request Parameters
------------------

.. rest_parameters:: parameters.yaml

   - project: project_id-query
   - project-domain: project-domain_taas

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - id: tap_mirror_id
   - name: tap_mirror_name
   - description: description
   - tenant_id: project_id
   - port_id: tap_mirror_port_id
   - mirror_type: mirror_type
   - remote_ip: remote_ip_tap_mirror
   - directions: directions_tap_mirror

Response Example
----------------

.. literalinclude:: samples/taas/tap_mirror-list-response.json
   :language: javascript

Create Tap Mirror
=================

.. rest_method:: POST /v2.0/taas/tap_mirrors

Creates a Tap Mirror.

Error response codes: 401, 403, 404, 409

Request Parameters
------------------

.. rest_parameters:: parameters.yaml

   - project: project_id-query
   - project-domain: project-domain_taas
   - tenant_id: project_id
   - name: tap_mirror_name
   - port_id: tap_mirror_port_id
   - mirror_type: mirror_type
   - remote_ip: remote_ip_tap_mirror
   - directions: directions_tap_mirror
   - description: description

Request Example
---------------

.. literalinclude:: samples/taas/tap_mirror-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - id: tap_mirror_id
   - name: tap_mirror_name
   - description: description
   - tenant_id: project_id
   - port_id: tap_mirror_port_id
   - mirror_type: mirror_type
   - remote_ip: remote_ip_tap_mirror
   - directions: directions_tap_mirror

Response Example
----------------

.. literalinclude:: samples/taas/tap_mirror-create-response.json
   :language: javascript

Update Tap Mirror
=================

.. rest_method:: PUT /v2.0/taas/tap_mirrors/{tap_mirror_id}

Updates Tap Mirror.

Normal response codes: 200

Error response codes: 400, 401, 404, 412

Request Parameters
------------------

.. rest_parameters:: parameters.yaml

   - tap_mirror_id: tap_mirror_id-query
   - description: description
   - name: tap_mirror_name

Request Example
---------------

.. literalinclude:: samples/taas/tap_mirror-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - id: tap_mirror_id
   - name: tap_mirror_name
   - description: description
   - tenant_id: project_id
   - port_id: tap_mirror_port_id
   - mirror_type: mirror_type
   - remote_ip: remote_ip_tap_mirror
   - directions: directions_tap_mirror

Response Example
----------------

.. literalinclude:: samples/taas/tap_mirror-update-response.json
   :language: javascript

Delete Tap Mirror
=================

.. rest_method:: DELETE /v2.0/taas/tap_mirrors/{tap_mirror_id}

Deleted a Tap Mirror.

Normal response codes: 204

Error response codes: 400, 401, 404, 412

Request Parameters
------------------

.. rest_parameters:: parameters.yaml

   - tap_mirror_id: tap_mirror_id-query

Response Parameters
-------------------

There is no body content for the response of a successful DELETE request.

Show Tap Mirror
===============

.. rest_method:: GET /v2.0/taas/tap_mirrors/{tap_mirror_id}

Shows details for a tap mirror.

.. include:: filtering-show.inc

Normal response codes: 200

Error response codes: 401, 404

Request Parameters
------------------

.. rest_parameters:: parameters.yaml

   - project: project_id-query
   - project-domain: project-domain_taas
   - tap_mirror_id: tap_mirror_id-query

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - id: tap_mirror_id
   - name: tap_mirror_name
   - description: description
   - tenant_id: project_id
   - port_id: tap_mirror_port_id
   - mirror_type: mirror_type
   - remote_ip: remote_ip_tap_mirror
   - directions: directions_tap_mirror

Response Example
----------------

.. literalinclude:: samples/taas/tap_mirror-show-response.json
   :language: javascript
