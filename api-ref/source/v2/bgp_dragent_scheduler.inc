.. -*- rst -*-

=================================================
BGP Speaker and Dynamic Routing Agent interaction
=================================================

Add BGP Speaker to a Dynamic Routing Agent
==========================================

.. rest_method:: POST /v2.0/agents/{bgp-agent-id}/bgp-drinstances

Issue a ``POST`` request to ``/v2.0/agents/{bgp-agent-id}/bgp-drinstances`` to
add a BGP Speaker to the specified dynamic routing agent.

Normal response codes: 201

Request
-------

.. rest_parameters:: parameters.yaml

   - bgp_speaker_id: bgp_speaker-id-body

Request Example
---------------

.. literalinclude:: samples/bgp/dragent_add_speaker-request.json
   :language: javascript

Response
--------

There is no body content for the response of a successful add
BGP Speaker to a Dynamic Routing Agent.

List BGP speakers hosted by a Dynamic Routing Agent
===================================================

.. rest_method:: GET /v2.0/agents/{bgp-dragent-id}/bgp-drinstances

Issue a ``GET`` request to ``/v2.0/agents/{bgp-dragent-id}/bgp-drinstances`` to
list all BGP Seakers hosted on the specified dynamic routing agent.

Normal response codes: 200

Request
-------

.. rest_parameters:: parameters.yaml

   - bgp-dragent-id: bgp_dragent_id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - bgp_speakers: bgp_speakers
   - id: bgp_speaker-id-body
   - peers: bgp_peers
   - name: bgp_speaker-name-body
   - ip_version: bgp_speaker_ip_version-body
   - advertise_floating_ip_host_routes: bgp_speaker_advertise_fip_host_routes-body
   - advertise_tenant_networks: bgp_speaker_advertise_tenant_net-body
   - local_as: bgp_speaker_local_as_body
   - networks: bgp_speaker-networks-body
   - project_id: project_id

Response Example
----------------

.. literalinclude:: samples/bgp/dragent_list_speakers-response.json
   :language: javascript

Delete BGP Speaker from a Dynamic Routing Agent
===============================================

.. rest_method:: DELETE /v2.0/agents/{bgp-agent-id}/bgp-drinstances/{bgp-speaker-id}

Issue a ``DELETE`` request to ``/v2.0/agents/{bgp-agent-id}/bgp-drinstances/{bgp-speaker-id}``
to delete the BGP Speaker hosted by the specified dynamic routing agent.

Normal response codes: 204

Request
-------

.. rest_parameters:: parameters.yaml

   - bgp-speaker-id: bgp_speaker_id-path
   - bgp-dragent-id: bgp_dragent_id-path

Response
--------

There is no body content for the response of a successful DELETE request.

