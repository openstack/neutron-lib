.. -*- rst -*-

======
Agents
======

Lists, shows details for, updates, and deletes agents.

Agent Resources Synced Extension
================================

The ``agent-resources-synced`` extension adds the ``resources_synced`` attribute
to agents.

Availability Zone Extension
===========================

The ``availability_zone`` extension adds the ``availability_zone`` attribute
to agents. ``availability_zone`` is the name of the availability zone that
the agent is running on.

List all agents
===============

.. rest_method::  GET /v2.0/agents

Shows details for an agent.

Use the ``fields`` query parameter to control which fields are
returned in the response body. For information, see `Filtering and
Column Selection <http://specs.openstack.org/openstack/neutron-
specs/specs/api/networking_general_api_information.html#filtering-
and-column-selection>`__.

Normal response codes: 200

Error response codes: 401

Request
-------

.. rest_parameters:: parameters.yaml

   - admin_state_up: admin_state_up-query
   - agent_type: agent_type-query
   - alive: alive-query
   - availability_zone: availability_zone-query
   - binary: binary-query
   - description: description-query
   - host: host-query
   - id: id-query
   - topic: topic-query
   - fields: fields
   - sort_dir: sort_dir
   - sort_key: agent-sort_key

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

.. literalinclude:: samples/agents/agents-list-response.json
   :language: javascript


Show agent details
==================

.. rest_method::  GET /v2.0/agents/{agent_id}

Shows details for an agent.

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - agent_id: agent_id-path
   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - admin_state_up: admin_state_up
   - agent: agent
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

.. literalinclude:: samples/agents/agent-show-response.json
   :language: javascript

Update agent
==============

.. rest_method::  PUT /v2.0/agents/{agent_id}

Updates an agent.

Normal response codes: 200

Error response codes: 400, 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - agent_id: agent_id-path
   - admin_state_up: admin_state_up-request
   - description: description-request

Request Example
---------------

.. literalinclude:: samples/agents/agent-update-request.json
   :language: javascript


Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - admin_state_up: admin_state_up
   - agent: agent
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

.. literalinclude:: samples/agents/agent-update-response.json
   :language: javascript

Delete agent
============

.. rest_method::  DELETE /v2.0/agents/{agent_id}

Agents that won't be used anymore can be removed. Before deleting agents via
API, the agent should be stopped/disabled.

Normal response codes: 204

Error response codes: 401, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - agent_id: agent_id-path

Response
--------

There is no body content for the response of a successful DELETE request.
