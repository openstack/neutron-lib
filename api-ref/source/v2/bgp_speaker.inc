.. -*- rst -*-

===========
BGP Speaker
===========

BGP Speaker acts as a route server using BGP routing protocol. It advertises
routes to the BGP peers which are added to the BGP Speaker.
Currently, BGP Speaker only advertises routes for a network to which it is associated.

A BGP Speaker requires association with a "gateway" network to determine eligible routes.
In Neutron, a "gateway" network connects Neutron routers to the upstream routers. An
external network is best for being used as a gateway network.

The association builds a list of all virtual routers with gateways on provider
and self-service networks within the same address scope.

List BGP Speakers
=================

.. rest_method:: GET /v2.0/bgp-speakers

Issue a ``GET`` request to ``/v2.0/bgp-speakers`` to retrieve this list of available
BGP Speakers.

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

   - bgp_speakers: bgp_speakers
   - id: bgp_speaker-id-body
   - name: bgp_speaker-name-body
   - ip_version: bgp_speaker_ip_version-body
   - advertise_floating_ip_host_routes: bgp_speaker_advertise_fip_host_routes-body
   - advertise_tenant_networks: bgp_speaker_advertise_tenant_net-body
   - local_as: bgp_speaker_local_as_body
   - networks: bgp_speaker-networks-body
   - tenant_id: project_id
   - project_id: project_id

Response Example
----------------

.. literalinclude:: samples/bgp/bgp_speaker-list-response.json
   :language: javascript

Show BGP Speaker details
========================

.. rest_method:: GET /v2.0/bgp-speakers/{bgp-speaker-id}

Issue a ``GET`` request to ``/v2.0/bgp-speakers/<bgp-speaker-id>`` to retrieve the
detail about a specific BGP Speaker.

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

   - id: bgp_speaker-id-body
   - name: bgp_speaker-name-body
   - ip_version: bgp_speaker_ip_version-body
   - advertise_floating_ip_host_routes: bgp_speaker_advertise_fip_host_routes-body
   - advertise_tenant_networks: bgp_speaker_advertise_tenant_net-body
   - local_as: bgp_speaker_local_as_body
   - networks: bgp_speaker-networks-body
   - tenant_id: project_id
   - project_id: project_id

Response Example
----------------

.. literalinclude:: samples/bgp/bgp_speaker-show-response.json
   :language: javascript

Create BGP Speaker
==================

.. rest_method:: POST /v2.0/bgp-speakers

Issue a ``POST`` request to ``/v2.0/bgp-speakers`` with following JSON-encoded
data to create a BGP Speaker.

Normal response codes: 201

Error response codes: 401, 403, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - name: bgp_speaker-name-body
   - ip_version: bgp_speaker_ip_version-body
   - advertise_floating_ip_host_routes: bgp_speaker_advertise_fip_host_routes-body
   - advertise_tenant_networks: bgp_speaker_advertise_tenant_net-body
   - local_as: bgp_speaker_local_as_body
   - networks: bgp_speaker-networks-body

Request Example
---------------

.. literalinclude:: samples/bgp/bgp_speaker-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - id: bgp_speaker-id-body
   - name: bgp_speaker-name-body
   - ip_version: bgp_speaker_ip_version-body
   - advertise_floating_ip_host_routes: bgp_speaker_advertise_fip_host_routes-body
   - advertise_tenant_networks: bgp_speaker_advertise_tenant_net-body
   - local_as: bgp_speaker_local_as_body
   - networks: bgp_speaker-networks-body
   - tenant_id: project_id
   - project_id: project_id

Response Example
----------------

.. literalinclude:: samples/bgp/bgp_speaker-create-response.json
   :language: javascript

Update a BGP Speaker
====================

.. rest_method:: PUT /v2.0/bgp-speakers/{bgp-speaker-id}

Issue ``PUT`` request to ``/v2.0/bgp-speakers/<bgp-speaker-id>`` to update a
specific BGP Speaker. Following attributes can be updated.

Normal response codes: 200

Error response codes: 400, 401, 404, 41

Request
-------

.. rest_parameters:: parameters.yaml

   - bgp-speakeriid: bgp_speaker_id-path
   - name: bgp_speaker-name-body
   - advertise_floating_ip_host_routes: bgp_speaker_advertise_fip_host_routes-body
   - advertise_tenant_networks: bgp_speaker_advertise_tenant_net-body

Request Example
---------------

.. literalinclude:: samples/bgp/bgp_speaker-update-request.json
   :language: javascript

Delete a BGP Speaker
====================

.. rest_method:: DELETE /v2.0/bgp-speakers/{bgp-speaker-id}

Delete a specific BGP Speaker.

Normal response codes: 204

Error response codes: 400, 401, 404, 412

Request
-------

.. rest_parameters:: parameters.yaml

   - bgp-speakeri-id: bgp_speaker_id-path

Response
--------

There is no body content for the response of a successful DELETE request.

Add BGP Peer to a BGP Speaker
=============================

.. rest_method:: PUT /v2.0/bgp-speakers/{bgp-speaker-id}/add_bgp_peer

Bind the BGP peer to the specified BGP Speaker.

Normal response codes: 200

Request
-------

.. rest_parameters:: parameters.yaml

   - bgp-speaker-id: bgp_speaker_id-path
   - bgp_peer_id: bgp_speaker_peer_id-body

Request Example
---------------

.. literalinclude:: samples/bgp/bgp_speaker_add_peer-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

    - bgp_peer_id: bgp_speaker_peer_id-body

Response Example
----------------

.. literalinclude:: samples/bgp/bgp_speaker_add_peer-response.json
   :language: javascript

Remove BGP Peer from a BGP Speaker
==================================

.. rest_method:: PUT /v2.0/bgp-speakers/{bgp-speaker-id}/remove_bgp_peer

Unbind the BGP peer from a BGP Speaker.

Normal response codes: 200

Request
-------

.. rest_parameters:: parameters.yaml

   - bgp-speaker-id: bgp_speaker_id-path
   - bgp_peer_id: bgp_speaker_peer_id-body

Request Example
---------------

.. literalinclude:: samples/bgp/bgp_speaker_remove_peer-request.json
   :language: javascript

Response
--------

There is no body content for the response of a successful DELETE request.

Add Network to a BGP Speaker
============================

.. rest_method:: PUT /v2.0/bgp-speakers/{bgp-speaker-id}/add_gateway_network

Add a network to the specified BGP speaker.

Normal response codes: 200

Request
-------

.. rest_parameters:: parameters.yaml

   - bgp-speaker-id: bgp_speaker_id-path
   - network_id: network_id

Request Example
---------------

.. literalinclude:: samples/bgp/bgp_speaker_add_network-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

    - bgp_peer_id: bgp_speaker_peer_id-body
    - network_id: network_id

Response Example
----------------

.. literalinclude:: samples/bgp/bgp_speaker_add_network-response.json
   :language: javascript

Delete Network from a BGP Speaker
=================================

.. rest_method:: PUT /v2.0/bgp-speakers/{bgp-speaker-id}/remove_gateway_network

Remove a network from the specified BGP speaker.

Normal response codes: 200

Request
-------

.. rest_parameters:: parameters.yaml

   - bgp-speaker-id: bgp_speaker_id-path
   - network_id: network_id

Request Example
---------------

.. literalinclude:: samples/bgp/bgp_speaker_remove_network-request.json
   :language: javascript

Response
--------

There is no body content for the response of a successful DELETE request.

List routes advertised by a BGP Speaker
=======================================

.. rest_method:: GET /v2.0/bgp-speakers/{bgp-speaker-id}/get_advertised_routes

List all routes advertised by the specified BGP Speaker.

.. include:: filtering-list.inc

Normal response codes: 200

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

    - advertised_routes: bgp_speaker_advertised_routes-body
    - cidr: bgp_speaker_cidr-body
    - nexthop: bgp_speaker_nexthop-body

Response Example
----------------

.. literalinclude:: samples/bgp/bgp_speaker_list_routes-response.json
   :language: javascript

List Dynamic Routing Agents hosting a specific BGP Speaker
==========================================================

.. rest_method:: GET /v2.0/bgp-speakers/{bgp-speaker-id}/bgp-dragents

List all BGP dynamic agents which are hosting the specified BGP Speaker.

.. include:: filtering-list.inc

Normal response codes: 200

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - admin_state_up: admin_state_up
   - agents: agents
   - agent_type: agent_type
   - alive: alive
   - availability_zone: availability_zone
   - binary: binary
   - configurations: configurations
   - created_at: created_at_resource
   - description: description
   - heartbeat_timestamp: heartbeat_timestamp
   - host: host
   - id: id
   - resources_synced: agent_resources_synced
   - started_at: started_at
   - topic: topic

Response Example
----------------

.. literalinclude:: samples/bgp/bgp_speaker_list_dragent_host-response.json
   :language: javascript
