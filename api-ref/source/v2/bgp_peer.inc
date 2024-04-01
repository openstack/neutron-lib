.. -*- rst -*-

========
BGP Peer
========

BGP peer defined in Neutron represents real BGP infrastructure such as
routers, route reflectors and route servers.

When a BGP peer is defined and associated with a BGP Speaker, Neutron will
attempt to open a BGP peering session with the mentioned remote peer. It is
this session, using which Neutron announces it's routes.

List BGP Peers
=================

.. rest_method:: GET /v2.0/bgp-peers

Issue a ``GET`` request to ``/v2.0/bgp-peers`` to retrieve the list of available
BGP peers.

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: 400, 401, 403

Request
-------

.. rest_parameters:: parameters.yaml

   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - bgp_peers: bgp_peers
   - remote_as: bgp_peer_remote_as_body
   - name: bgp_peer_name_body
   - peer_ip: bgp_peer_ip_body
   - id: bgp_peer_id_body
   - tenant_id: project_id
   - project_id: project_id

Response Example
----------------

.. literalinclude:: samples/bgp/bgp_peer-list-response.json
   :language: javascript

Show BGP Peer details
=====================

.. rest_method:: GET /v2.0/bgp-peers/{bgp-peer-id}

.. include:: filtering-show.inc

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - bgp-speaker-id: bgp_speaker_id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - bgp_peers: bgp_peers
   - remote_as: bgp_peer_remote_as_body
   - name: bgp_peer_name_body
   - peer_ip: bgp_peer_ip_body
   - id: bgp_peer_id_body
   - tenant_id: project_id
   - project_id: project_id

Response Example
----------------

.. literalinclude:: samples/bgp/bgp_peer-show-response.json
   :language: javascript

Create a BGP Peer
=================

.. rest_method:: POST /v2.0/bgp-peers

Create a BGP Peer.

Normal response codes: 201

Error response codes: 401, 403, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - auth_type: bgp_peer_auth_type_body
   - remote_as: bgp_peer_remote_as_body
   - name: bgp_peer_name_body
   - peer_ip: bgp_peer_ip_body

Request Example
---------------

.. literalinclude:: samples/bgp/bgp_peer-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - bgp_peer: bgp_peer_body
   - auth_type: bgp_peer_auth_type_body
   - password: bgp_peer_password_body
   - remote_as: bgp_peer_remote_as_body
   - name: bgp_peer_name_body
   - peer_ip: bgp_peer_ip_body
   - id: bgp_peer_id_body
   - tenant_id: project_id
   - project_id: project_id

Response Example
----------------

.. literalinclude:: samples/bgp/bgp_peer-create-response.json
   :language: javascript

Update a BGP Peer
=================

.. rest_method:: PUT /v2.0/bgp-peers/{bgp-peer-id}

Update a specific BGP Peer.

Normal response codes: 200

Error response codes: 400, 401, 404, 41

Request
-------

.. rest_parameters:: parameters.yaml

   - name: bgp_peer_name_body
   - password: bgp_peer_password_body

Delete a BGP Peer
=================

.. rest_method:: DELETE /v2.0/bgp-peers/{bgp-peer-id}

Delete a specific BGP Peer.

Normal response codes: 204

Error response codes: 400, 401, 404, 412
