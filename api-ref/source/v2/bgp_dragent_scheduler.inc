.. -*- rst -*-

=================================================
BGP Speaker and Dynamic Routing Agent interaction
=================================================

Add BGP Speaker to a Dynamic Routing Agent
==========================================

.. rest_method:: POST /v2.0/agents/{bgp-agent-id}/bgp-drinstances

Issue a ``POST`` request to ``/v2.0/agents/{bgp-agent-id}/bgp-drinstances`` to
add a BGP Speaker to the specified Dynamic Routing Agent.

.. note::

    The Dynamic Routing plugin can be configured to use static or dynamic
    (chance) scheduling of BGP Speakers with Dynamic Routing Agents. When using
    the static scheduler, this API must be used to associate a BGP Speaker with
    one or more Dynamic Routing Agents. However, when using the chance
    scheduler, this association happens automatically. As a result, it should
    only be necessary to call this API when you wish to associate a BGP Speaker
    with additional Dynamic Routing Agents (for example, before conducting
    maintenance of a node).
    Refer to the `Agent Scheduler`_ documentation for more information.

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
list all BGP Seakers hosted on the specified Dynamic Routing Agent.

.. include:: filtering-list.inc

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
to delete the BGP Speaker hosted by the specified Dynamic Routing Agent.

.. note::

    The Dynamic Routing plugin can be configured to use static or dynamic
    (chance) scheduling of BGP Speakers with Dynamic Routing Agents. When using
    the static scheduler, this API must be used to diassociate a BGP Speaker
    from Dynamic Routing Agents. However, when using the chance scheduler, this
    disassociation happens automatically. As a result, it should only be
    necessary to call this API when you wish to disassociate a BGP Speaker from
    additional Dynamic Routing Agents (for example, after conducting maintenance
    of a nodes).
    Refer to the `Agent Scheduler`_ documentation for more information.

.. warning:

    If the Dynamic Routing plugin is configured to use the dynamic (chance)
    scheduler and a BGP Speaker is associated with a single Dynamic Routing
    Agent, attempting to delete this association will result in a new
    association being automatically created, potentially against the same
    Dynamic Routing Agent. This can be confusing and may hinder maintenance
    operations. To prevent this, you should either manually create an
    additional association with another Dynamic Routing Agent in advance, or
    you should configure the Dynamic Routing plugin to use the static
    scheduler.

Normal response codes: 204

Request
-------

.. rest_parameters:: parameters.yaml

   - bgp-speaker-id: bgp_speaker_id-path
   - bgp-dragent-id: bgp_dragent_id-path

Response
--------

There is no body content for the response of a successful DELETE request.

.. _Agent Scheduler: https://docs.openstack.org/neutron-dynamic-routing/latest/admin/agent-scheduler.html
