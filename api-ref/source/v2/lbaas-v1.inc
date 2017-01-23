.. -*- rst -*-
.. needs:method_verification
.. needs:parameter_verification
.. needs:example_verification
.. needs:body_verification

======================
LBaaS 1.0 (DEPRECATED)
======================

The Load-Balancer-as-a-Service (LBaaS) v1.0 extension pairs with
the Networking v2.0 API to enable OpenStack projects to manage load
balancers for their VMs. With this extension, you can load-balance
client traffic from one network to application services, such as
VMs, on the same network.

Use this extension to create and manage virtual IP addresses
(VIPs), pools, members of a pool, health monitors, and view status
of a resource.

.. note::

    LBaaS 1.0 support was removed in Newton release. It's no longer available
    in any installations starting from this release.

**Load balancer statuses**

+----------------+--------------------------------------------------------------------+
| Status         | Description                                                        |
+----------------+--------------------------------------------------------------------+
| ACTIVE         | The resource is ready and active.                                  |
+----------------+--------------------------------------------------------------------+
| PENDING_CREATE | The resource is being created.                                     |
+----------------+--------------------------------------------------------------------+
| PENDING_UPDATE | The resource is being updated.                                     |
+----------------+--------------------------------------------------------------------+
| PENDING_DELETE | The resource is pending deletion.                                  |
+----------------+--------------------------------------------------------------------+
| INACTIVE       | The resource is not active.                                        |
+----------------+--------------------------------------------------------------------+
| ERROR          | An object within the service is not working. The ``error_details`` |
|                | attribute provides an explanation for the error, its cause, and    |
|                | possibly a solution.                                               |
+----------------+--------------------------------------------------------------------+

.. ============================================================

List pools
==========

.. rest_method::  GET /v2.0/lb/pools

Lists pools.

Normal response codes: 200

Error response codes: 401

Request
-------

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - pools: pools-obj
   - admin_state_up: admin_state_up
   - description: description
   - health_monitors: health_monitors-response
   - health_monitors_status: health_monitors_status
   - id: pool-id-response
   - lb_method: lb_method
   - members: members
   - name: name
   - protocol: pool-protocol
   - provider: pool-provider
   - status: pool-status
   - status_description: status_description
   - subnet_id: pool-subnet_id
   - tenant_id: project_id
   - vip_id: vip_id

Response Example
----------------

.. literalinclude:: samples/lbaas-v1/pools-list-response.json
   :language: javascript

Create a load balancer pool
===========================

.. rest_method::  POST /v2.0/lb/pools

Creates a load balancer pool.

Normal response codes: 201

Error response codes: 400, 401

Request
-------

.. rest_parameters:: parameters.yaml

   - pool: pool
   - admin_state_up: admin_state_up-request
   - description: description-request
   - health_monitors: health_monitors-request
   - lb_method: lb_method
   - name: name-request
   - protocol: pool-protocol
   - provider: pool-provider-request
   - subnet_id: pool-subnet_id
   - tenant_id: project_id-request

Request Example
---------------

.. literalinclude:: samples/lbaas-v1/pool-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - pool: pool
   - admin_state_up: admin_state_up
   - description: description
   - health_monitors: health_monitors-response
   - health_monitors_status: health_monitors_status
   - id: pool-id-response
   - lb_method: lb_method
   - members: members
   - name: name
   - protocol: pool-protocol
   - provider: pool-provider
   - status: pool-status
   - status_description: status_description
   - subnet_id: pool-subnet_id
   - tenant_id: project_id
   - vip_id: vip_id

Response Example
----------------

.. literalinclude:: samples/lbaas-v1/pool-create-response.json
   :language: javascript

Show pool details
=================

.. rest_method::  GET /v2.0/lb/pools/{pool_id}

Shows details for a pool.

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - pool_id: pool_id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - pool: pool
   - admin_state_up: admin_state_up
   - description: description
   - health_monitors: health_monitors-response
   - health_monitors_status: health_monitors_status
   - id: pool-id-response
   - lb_method: lb_method
   - members: members
   - name: name
   - protocol: pool-protocol
   - provider: pool-provider
   - status: pool-status
   - status_description: status_description
   - subnet_id: pool-subnet_id
   - tenant_id: project_id
   - vip_id: vip_id

Response Example
----------------

.. literalinclude:: samples/lbaas-v1/pool-show-response.json
   :language: javascript

Update pool
===========

.. rest_method::  PUT /v2.0/lb/pools/{pool_id}

Updates a load balancer pool.

Normal response codes: 200

Error response codes: 400, 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - pool_id: pool_id-path
   - pool: pool
   - admin_state_up: admin_state_up-request
   - description: description-request
   - health_monitors: health_monitors-request
   - lb_method: lb_method-request-put
   - name: name-request

Request Example
---------------

.. literalinclude:: samples/lbaas-v1/pool-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - pool: pool
   - admin_state_up: admin_state_up
   - description: description
   - health_monitors: health_monitors-response
   - health_monitors_status: health_monitors_status
   - id: pool-id-response
   - lb_method: lb_method
   - members: members
   - name: name
   - protocol: pool-protocol
   - provider: pool-provider
   - status: pool-status
   - status_description: status_description
   - subnet_id: pool-subnet_id
   - tenant_id: project_id
   - vip_id: vip_id

Response Example
----------------

.. literalinclude:: samples/lbaas-v1/pool-update-response.json
   :language: javascript

Delete pool
===========

.. rest_method::  DELETE /v2.0/lb/pools/{pool_id}

Deletes a load balancer pool.

Normal response codes: 204

Error response codes: 401, 404, 409

When a requested load balancer pool has a VIP,
``Conflict (409)`` is returned.

Request
-------

.. rest_parameters:: parameters.yaml

   - pool_id: pool_id-path

Response
--------

There is no body content for the response of a successful DELETE request.

.. ============================================================

List VIPs
=========

.. rest_method::  GET /v2.0/lb/vips

Lists VIPs.

The list might be empty.

Normal response codes: 200

Error response codes: 401

Request
-------

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - vips: vips
   - address: vip-address
   - admin_state_up: admin_state_up
   - connection_limit: connection_limit-response
   - description: description
   - id: vip-id
   - name: name
   - pool_id: vip-pool_id
   - port_id: vip-port_id
   - protocol: vip-protocol
   - protocol_port: protocol_port
   - session_persistence: vip-session_persistence
   - status: vip-status
   - status_description: status_description
   - subnet_id: vip-subnet_id
   - tenant_id: project_id

Response Example
----------------

.. literalinclude:: samples/lbaas-v1/vips-list-response.json
   :language: javascript

Create a load balancer VIP
==========================

.. rest_method::  POST /v2.0/lb/vips

Creates a load balancer VIP.

Normal response codes: 201

Error response codes: 400, 401, 404, 409

When a specified pool already has a VIP, ``Conflict (409)`` is
returned.
When a specified pool or a specified subnet is not found,
``Not Found (404)`` is returned.

Request
-------

.. rest_parameters:: parameters.yaml

   - vip: vip
   - address: vip-address-request
   - admin_state_up: admin_state_up-request
   - connection_limit: connection_limit
   - description: description-request
   - name: name-request
   - pool_id: vip-pool_id
   - protocol: vip-protocol
   - protocol_port: protocol_port
   - session_persistence: vip-session_persistence-request
   - subnet_id: vip-subnet_id
   - tenant_id: project_id-request

Request Example
---------------

.. literalinclude:: samples/lbaas-v1/vip-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - vip: vip
   - address: vip-address
   - admin_state_up: admin_state_up
   - connection_limit: connection_limit-response
   - description: description
   - id: vip-id
   - name: name
   - pool_id: vip-pool_id
   - port_id: vip-port_id
   - protocol: vip-protocol
   - protocol_port: protocol_port
   - session_persistence: vip-session_persistence
   - status: vip-status
   - status_description: status_description
   - subnet_id: vip-subnet_id
   - tenant_id: project_id

Response Example
----------------

.. literalinclude:: samples/lbaas-v1/vip-create-response.json
   :language: javascript

Show VIP details
================

.. rest_method::  GET /v2.0/lb/vips/{vip_id}

Shows details for a VIP.

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - vip_id: vip_id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - vip: vip
   - address: vip-address
   - admin_state_up: admin_state_up
   - connection_limit: connection_limit-response
   - description: description
   - id: vip-id
   - name: name
   - pool_id: vip-pool_id
   - port_id: vip-port_id
   - protocol: vip-protocol
   - protocol_port: protocol_port
   - session_persistence: vip-session_persistence
   - status: vip-status
   - status_description: status_description
   - subnet_id: vip-subnet_id
   - tenant_id: project_id

Response Example
----------------

.. literalinclude:: samples/lbaas-v1/vip-show-response.json
   :language: javascript

Update VIP
==========

.. rest_method::  PUT /v2.0/lb/vips/{vip_id}

Updates a load balancer VIP.

Normal response codes: 200

Error response codes: 400, 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - vip_id: vip_id-path
   - vip: vip
   - admin_state_up: admin_state_up-request
   - connection_limit: connection_limit
   - description: description-request
   - name: name-request
   - pool_id: vip-pool_id-request
   - session_persistence: vip-session_persistence-request

Request Example
---------------

.. literalinclude:: samples/lbaas-v1/vip-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - vip: vip
   - address: vip-address
   - admin_state_up: admin_state_up
   - connection_limit: connection_limit-response
   - description: description
   - id: vip-id
   - name: name
   - pool_id: vip-pool_id
   - port_id: vip-port_id
   - protocol: vip-protocol
   - protocol_port: protocol_port
   - session_persistence: vip-session_persistence
   - status: vip-status
   - status_description: status_description
   - subnet_id: vip-subnet_id
   - tenant_id: project_id

Response Example
----------------

.. literalinclude:: samples/lbaas-v1/vip-update-response.json
   :language: javascript

Delete VIP
==========

.. rest_method::  DELETE /v2.0/lb/vips/{vip_id}

Deletes a load balancer VIP.

Normal response codes: 204

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - vip_id: vip_id-path

Response
--------

There is no body content for the response of a successful DELETE request.

.. ============================================================

List members
============

.. rest_method::  GET /v2.0/lb/members

Lists members.

Normal response codes: 200

Error response codes: 401

Request
-------

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - members: members-obj
   - address: address
   - admin_state_up: admin_state_up
   - id: member-id-response
   - pool_id: member-pool_id
   - protocol_port: protocol_port
   - status: member-status
   - status_description: status_description
   - tenant_id: project_id
   - weight: member-weight

Response Example
----------------

.. literalinclude:: samples/lbaas-v1/members-list-response.json
   :language: javascript

Create a load balancer member
=============================

.. rest_method::  POST /v2.0/lb/members

Creates a load balancer member.

Normal response codes: 201

Error response codes: 400, 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - member: member
   - address: address
   - admin_state_up: admin_state_up-request
   - pool_id: member-pool_id
   - protocol_port: protocol_port
   - tenant_id: project_id-request
   - weight: member-weight-request

Request Example
---------------

.. literalinclude:: samples/lbaas-v1/member-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - member: member
   - address: address
   - admin_state_up: admin_state_up
   - id: member-id-response
   - pool_id: member-pool_id
   - protocol_port: protocol_port
   - status: member-status
   - status_description: status_description
   - tenant_id: project_id
   - weight: member-weight

Response Example
----------------

.. literalinclude:: samples/lbaas-v1/member-create-response.json
   :language: javascript

Show member details
===================

.. rest_method::  GET /v2.0/lb/members/{member_id}

Shows details for a member.

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - member_id: member_id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - member: member
   - address: address
   - admin_state_up: admin_state_up
   - id: member-id-response
   - pool_id: member-pool_id
   - protocol_port: protocol_port
   - status: member-status
   - status_description: status_description
   - tenant_id: project_id
   - weight: member-weight

Response Example
----------------

.. literalinclude:: samples/lbaas-v1/member-show-response.json
   :language: javascript

Update member
=============

.. rest_method::  PUT /v2.0/lb/members/{member_id}

Updates a load balancer member.

Normal response codes: 200

Error response codes: 400, 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - member_id: member_id-path
   - member: member
   - admin_state_up: admin_state_up-request
   - pool_id: member-pool_id-request
   - weight: member-weight-request

Request Example
---------------

.. literalinclude:: samples/lbaas-v1/member-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - member: member
   - address: address
   - admin_state_up: admin_state_up
   - id: member-id-response
   - pool_id: member-pool_id
   - protocol_port: protocol_port
   - status: member-status
   - status_description: status_description
   - tenant_id: project_id
   - weight: member-weight

Response Example
----------------

.. literalinclude:: samples/lbaas-v1/member-update-response.json
   :language: javascript

Delete member
=============

.. rest_method::  DELETE /v2.0/lb/members/{member_id}

Deletes a load balancer member.

Normal response codes: 204

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - member_id: member_id-path

Response
--------

There is no body content for the response of a successful DELETE request.

.. ============================================================

List health monitors
====================

.. rest_method::  GET /v2.0/lb/health_monitors

Lists health monitors.

Normal response codes: 200

Error response codes: 401

Request
-------

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - health_monitors: health_monitors-obj
   - admin_state_up: admin_state_up
   - delay: delay
   - expected_codes: expected_codes-response
   - http_method: http_method
   - id: health_monitor-id
   - max_retries: max_retries
   - pools: pools
   - tenant_id: project_id
   - timeout: timeout
   - type: type
   - url_path: url_path-response

Response Example
----------------

.. literalinclude:: samples/lbaas-v1/healthmonitors-list-response.json
   :language: javascript

Create a load balancer health monitor
=====================================

.. rest_method::  POST /v2.0/lb/health_monitors

Creates a load balancer health monitor.

Normal response codes: 201

Error response codes: 400, 401

Request
-------

.. rest_parameters:: parameters.yaml

   - health_monitor: health_monitor
   - admin_state_up: admin_state_up-request
   - delay: delay
   - expected_codes: expected_codes
   - http_method: http_method-request
   - max_retries: max_retries
   - tenant_id: project_id-request
   - timeout: timeout
   - type: type
   - url_path: url_path

Request Example
---------------

.. literalinclude:: samples/lbaas-v1/healthmonitor-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - health_monitor: health_monitor
   - admin_state_up: admin_state_up
   - delay: delay
   - expected_codes: expected_codes-response
   - http_method: http_method
   - id: health_monitor-id
   - max_retries: max_retries
   - pools: pools
   - tenant_id: project_id
   - timeout: timeout
   - type: type
   - url_path: url_path-response

Response Example
----------------

.. literalinclude:: samples/lbaas-v1/healthmonitor-create-response.json
   :language: javascript

Show health monitor details
===========================

.. rest_method::  GET /v2.0/lb/health_monitors/{health_monitor_id}

Shows details for a health monitor.

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - health_monitor_id: health_monitor_id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - health_monitor: health_monitor
   - admin_state_up: admin_state_up
   - delay: delay
   - expected_codes: expected_codes-response
   - http_method: http_method
   - id: health_monitor-id
   - max_retries: max_retries
   - pools: pools
   - tenant_id: project_id
   - timeout: timeout
   - type: type
   - url_path: url_path-response

Response Example
----------------

.. literalinclude:: samples/lbaas-v1/healthmonitor-show-response.json
   :language: javascript

Update health monitor
=====================

.. rest_method::  PUT /v2.0/lb/health_monitors/{health_monitor_id}

Updates a load balancer health monitor.

Normal response codes: 200

Error response codes: 400, 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - health_monitor_id: health_monitor_id-path
   - health_monitor: health_monitor
   - admin_state_up: admin_state_up-request
   - delay: delay
   - expected_codes: expected_codes
   - http_method: http_method-request
   - max_retries: max_retries
   - timeout: timeout
   - url_path: url_path

Request Example
---------------

.. literalinclude:: samples/lbaas-v1/healthmonitor-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - health_monitor: health_monitor
   - admin_state_up: admin_state_up
   - delay: delay
   - expected_codes: expected_codes-response
   - http_method: http_method
   - id: health_monitor-id
   - max_retries: max_retries
   - pools: pools
   - tenant_id: project_id
   - timeout: timeout
   - type: type
   - url_path: url_path-response

Response Example
----------------

.. literalinclude:: samples/lbaas-v1/healthmonitor-update-response.json
   :language: javascript

Delete health monitor
=====================

.. rest_method::  DELETE /v2.0/lb/health_monitors/{health_monitor_id}

Deletes a load balancer health monitor.

Normal response codes: 204

Error response codes: 401, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - health_monitor_id: health_monitor_id-path

Response
--------

There is no body content for the response of a successful DELETE request.

Associate health monitor with pool
==================================

.. rest_method::  POST /v2.0/lb/pools/{pool_id}/health_monitors

Associates a health monitor with a pool.

Normal response codes: 201

Error response codes: 400, 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - pool_id: pool_id-path
   - health_monitor: health_monitor
   - id: health_monitor-id

Request Example
---------------

.. literalinclude:: samples/lbaas-v1/healthmonitor-associate-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - health_monitor: health_monitor

Response Example
----------------

.. literalinclude:: samples/lbaas-v1/healthmonitor-associate-response.json
   :language: javascript

Disassociate health monitor from pool
=====================================

.. rest_method::  DELETE /v2.0/lb/pools/{pool_id}/health_monitors/{health_monitor_id}

Disassociates a health monitor from a pool.

Normal response codes: 201

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - pool_id: pool_id-path
   - health_monitor_id: health_monitor_id-path

Response
--------

There is no body content for the response of a successful DELETE request.
