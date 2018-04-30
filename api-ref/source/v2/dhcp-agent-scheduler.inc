.. -*- rst -*-

====================
DHCP agent scheduler
====================

The DHCP agent scheduler extension (``dhcp_agent_scheduler``)
enables administrators to assign DHCP servers for Neutron networks to given
Neutron DHCP agents, and retrieve mappings between Neutron networks
and DHCP agents.

List networks hosted by a DHCP agent
====================================

.. rest_method::  GET /v2.0/agents/{agent_id}/dhcp-networks


Lists networks that a DHCP agent hosts.

Normal response codes: 200

Error response codes: 401, 403

Request
-------

.. rest_parameters:: parameters.yaml

   - agent_id: agent_id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - network: network
   - admin_state_up: network-admin_state_up
   - availability_zone_hints: availability_zone_hints
   - availability_zones: availability_zones
   - created_at: created_at_resource
   - dns_domain: dns_domain
   - id: network-id
   - ipv4_address_scope: ipv4_address_scope
   - ipv6_address_scope: ipv6_address_scope
   - l2_adjacency: l2_adjacency
   - mtu: mtu
   - name: network-name
   - port_security_enabled: network-port_security_enabled
   - project_id: project_id
   - provider:network_type: provider:network_type
   - provider:physical_network: provider:physical_network
   - provider:segmentation_id: provider:segmentation_id
   - qos_policy_id: qos_policy_id
   - revision_number: revision_number
   - router:external: router:external
   - segments: segments
   - shared: network-shared
   - status: network-status
   - subnets: network-subnets
   - tenant_id: project_id
   - updated_at: updated_at_resource
   - vlan_transparent: vlan_transparent
   - description: description
   - is_default: network_is_default


Response Example
----------------

.. literalinclude:: samples/agents/agent-dhcp-networks-list-response.json
   :language: javascript


Schedule a network to a DHCP agent
==================================

.. rest_method::  POST /v2.0/agents/{agent_id}/dhcp-networks

Add a network to a DHCP agent

Normal response codes: 201

Error response codes: 400, 403, 409, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - agent_id: agent_id-path
   - network_id: network-id

Request Example
---------------

.. literalinclude:: samples/agents/agent-dhcp-network-add-request.json
   :language: javascript

Response Parameters
-------------------

null

Response Example
----------------

There is no body content for the response of a successful POST request.


Remove network from a DHCP agent
================================

.. rest_method::  DELETE /v2.0/agents/{agent_id}/dhcp-networks/{network_id}

Removes a network from a dhcp agent.

Normal response codes: 204

Error response codes: 401, 403, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - agent_id: agent_id-path
   - network_id: network_id

Response Example
----------------

There is no body content for the response of a successful DELETE request.


List DHCP agents hosting a network
==================================

.. rest_method::  GET /v2.0/networks/{network_id}/dhcp-agents


Lists DHCP agents hosting a network.

Normal response codes: 200

Error response codes: 401, 403

Request
-------

.. rest_parameters:: parameters.yaml

   - network_id: network_id

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - admin_state_up: admin_state_up
   - agents: agents
   - agent_type: agent_type
   - alive: alive
   - binary: binary
   - configurations: configurations
   - created_at: created_at_resource
   - description: description
   - heartbeat_timestamp: heartbeat_timestamp
   - host: host
   - id: id
   - started_at: started_at
   - topic: topic

Response Example
----------------

.. literalinclude:: samples/agents/network-dhcp-agent-list-response.json
   :language: javascript