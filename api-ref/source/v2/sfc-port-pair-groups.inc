.. -*- rst -*-
.. needs:method_verification
.. needs:parameter_verification
.. needs:example_verification
.. needs:body_verification

===================================
Port Pair Groups (port-pair-groups)
===================================

Lists, shows information for, creates, updates and deletes port pair groups.

List Port Pair Groups
=====================

.. rest_method:: GET /v1.0/sfc/port_pair_groups

Lists port pair groups.

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: unauthorized(401), forbidden(403)

Response
--------

.. rest_parameters:: parameters.yaml

  - id: port_pair_group_id
  - name: port_pair_group_name
  - description: description
  - port_pairs: port_pairs
  - port_pair_group_parameters: port_pair_group_parameters
  - tap_enabled: sfc_tap_enabled

Response Example
----------------

**Example List port pair groups: JSON response**

.. literalinclude:: samples/sfc-port-pair-groups/port-pair-group-list-resp.json
   :language: javascript

Create Port Pair Group
======================

.. rest_method:: POST /v1.0/sfc/port_pair_groups

Creates a port pair group.

Normal response codes: 200

Error response codes: badRequest(400), unauthorized(401), forbidden(403)

Request
-------

.. rest_parameters:: parameters.yaml

  - name: port_pair_group_name
  - description: description
  - port_pairs: port_pairs
  - port_pair_group_parameters: port_pair_group_parameters
  - tap_enabled: sfc_tap_enabled

**Example Create port pair group: JSON request**

.. literalinclude:: samples/sfc-port-pair-groups/port-pair-group-create-req.json
   :language: javascript

Response
--------

.. rest_parameters:: parameters.yaml

  - id: port_pair_group_id
  - name: port_pair_group_name
  - description: description
  - port_pairs: port_pairs
  - port_pair_group_parameters: port_pair_group_parameters
  - tap_enabled: sfc_tap_enabled

Response Example
----------------

**Example Create port pair group: JSON response**

.. literalinclude:: samples/sfc-port-pair-groups/port-pair-group-create-resp.json
   :language: javascript

Show Port Pair Group Details
============================

.. rest_method:: GET /v1.0/sfc/port_pair_groups/{port_pair_group_id}

Shows details for a port pair group.

.. include:: filtering-show.inc

Normal response codes: 200

Error response codes: badRequest(400), unauthorized(401), forbidden(403), itemNotFound(404)

Request
-------

.. rest_parameters:: parameters.yaml

  - port_pair_group_id: port_pair_group_id-path

Response
--------

.. rest_parameters:: parameters.yaml

  - id: port_pair_group_id
  - name: port_pair_group_name
  - description: description
  - port_pairs: port_pairs
  - port_pair_group_parameters: port_pair_group_parameters
  - tap_enabled: sfc_tap_enabled

Response Example
----------------

**Example Show port pair group: JSON response**

.. literalinclude:: samples/sfc-port-pair-groups/port-pair-group-get-resp.json
   :language: javascript

Update Port Pair Group
======================

.. rest_method:: PUT /v1.0/sfc/port_pair_groups/{port_pair_group_id}

Updates a port pair group. The current list of port pairs is replaced
by the port pair list in the Update request.

Normal response codes: 200

Error response codes: badRequest(400), unauthorized(401), forbidden(403), itemNotFound(404)

Request
-------

.. rest_parameters:: parameters.yaml

  - port_pair_group_id: port_pair_group_id-path
  - name: port_pair_group_name
  - description: description
  - port_pairs: port_pairs
  - port_pair_group_parameters: port_pair_group_parameters
  - tap_enabled: sfc_tap_enabled

Request Example
---------------

**Example Update port pair group: JSON request**

.. literalinclude:: samples/sfc-port-pair-groups/port-pair-group-update-req.json
   :language: javascript

Response
--------

.. rest_parameters:: parameters.yaml

  - id: port_pair_group_id
  - name: port_pair_group_name
  - description: description
  - port_pairs: port_pairs
  - port_pair_group_parameters: port_pair_group_parameters
  - tap_enabled: sfc_tap_enabled

Response Example
----------------

**Example Update port pair group: JSON response**

.. literalinclude:: samples/sfc-port-pair-groups/port-pair-group-update-resp.json
   :language: javascript

Delete Port Pair Group
======================

.. rest_method:: DELETE /v1.0/sfc/port-pair-groups/{port_pair_group_id}

Deletes a port pair group.

Normal response codes: 202

Error response codes: badRequest(400), unauthorized(401), forbidden(403), itemNotFound(404)

Request
-------

.. rest_parameters:: parameters.yaml

  - port_pair_group_id: port_pair_group_id-path

Response
--------

There is no body content for the response of a successful Delete request.
