.. -*- rst -*-

==================
L3 agent scheduler
==================

The L3 agent scheduler extension (``l3_agent_scheduler``) allows administrators
to assign Neutron routers to Neutron L3 agents, and retrieve mappings between
Neutron routers and L3 agents.

List routers hosted by an L3 agent
==================================

.. rest_method::  GET /v2.0/agents/{agent_id}/l3-routers

Lists routers that an l3 agent hosts.

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - agent_id: agent_id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - routers: routers
   - id: router-id-body
   - tenant_id: project_id
   - project_id: project_id
   - name: name
   - description: description
   - admin_state_up: admin_state_up
   - status: router-status
   - external_gateway_info: router-external_gateway_info
   - revision_number: revision_number
   - routes: router-routes
   - destination: router-destination
   - nexthop: router-nexthop
   - distributed: router-distributed
   - ha: router-ha
   - availability_zone_hints: router-availability_zone_hints
   - availability_zones: router-availability_zones
   - service_type_id: router-service_type_id
   - flavor_id: router-flavor_id



Response Example
----------------

.. literalinclude:: ../v2/samples/agents/agent-l3-routers-list-response.json
   :language: javascript

Schedule router to an l3 agent
==============================

.. rest_method::  POST /v2.0/agents/{agent_id}/l3-routers

Add a router to an l3 agent.

Normal response codes: 201

Error response codes: 400, 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - agent_id: agent_id-path
   - router_id: router-id-body

Request Example
---------------

.. literalinclude:: ../v2/samples/agents/agent-l3-router-add-request.json
   :language: javascript

Response Parameters
-------------------

null

Response Example
----------------

There is no body content for the response of a successful POST request.


Remove l3 router from an l3 agent
=================================

.. rest_method::  DELETE /v2.0/agents/{agent_id}/l3-routers/{router_id}

Removes a router from an l3 agent.

Normal response codes: 204

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - agent_id: agent_id-path
   - router_id: router_id

Response Example
----------------

There is no body content for the response of a successful DELETE request.

List L3 agents hosting a router
===============================

.. rest_method::  GET /v2.0/routers/{router_id}/l3-agents

Lists l3 agents hosting a specific router.

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - router_id: router_id

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

.. literalinclude:: ../v2/samples/agents/router-l3-agent-list-response.json
   :language: javascript
