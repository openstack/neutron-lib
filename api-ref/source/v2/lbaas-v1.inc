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
Error response codes:400,401,413,503,500,

Request
-------

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - lb_algorithm: lb_algorithm
   - status: status
   - protocol: protocol
   - description: description
   - health_monitors: health_monitors
   - subnet_id: subnet_id
   - tenant_id: project_id
   - project_id: project_id
   - admin_state_up: admin_state_up
   - vip_id: vip_id
   - health_monitors_status: health_monitors_status
   - members: members
   - provider: provider
   - pools: pools
   - status_description: status_description
   - id: id
   - name: name

Response Example
----------------

.. literalinclude:: samples/lbaas/pools-list-response.json
   :language: javascript

Create a load balancer pool
===========================

.. rest_method::  POST /v2.0/lb/pools

Creates a load balancer pool.

Error response codes:201,400,401,413,503,500,

Request
-------

.. rest_parameters:: parameters.yaml

   - lb_method: lb_method
   - protocol: protocol
   - description: description
   - admin_state_up: admin_state_up
   - subnet_id: subnet_id
   - tenant_id: project_id
   - project_id: project_id
   - pool: pool
   - name: name

Request Example
---------------

.. literalinclude:: samples/lbaas/pool-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - lb_algorithm: lb_algorithm
   - status: status
   - protocol: protocol
   - description: description
   - health_monitors: health_monitors
   - subnet_id: subnet_id
   - tenant_id: project_id
   - project_id: project_id
   - admin_state_up: admin_state_up
   - vip_id: vip_id
   - health_monitors_status: health_monitors_status
   - members: members
   - provider: provider
   - status_description: status_description
   - id: id
   - pool: pool
   - name: name

Show pool details
=================

.. rest_method::  GET /v2.0/lb/pools/{pool_id}

Shows details for a pool.

Normal response codes: 200
Error response codes:400,401,413,503,500,

Request
-------

.. rest_parameters:: parameters.yaml

   - pool_id: pool_id

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - lb_algorithm: lb_algorithm
   - status: status
   - protocol: protocol
   - description: description
   - health_monitors: health_monitors
   - subnet_id: subnet_id
   - tenant_id: project_id
   - project_id: project_id
   - admin_state_up: admin_state_up
   - vip_id: vip_id
   - health_monitors_status: health_monitors_status
   - members: members
   - provider: provider
   - status_description: status_description
   - id: id
   - pool: pool
   - name: name

Response Example
----------------

.. literalinclude:: samples/lbaas/pool-show-response.json
   :language: javascript

Update pool
===========

.. rest_method::  PUT /v2.0/lb/pools/{pool_id}

Updates a load balancer pool.

Normal response codes: 200
Error response codes:400,401,413,503,500,

Request
-------

.. rest_parameters:: parameters.yaml

   - pool: pool
   - lb_method: lb_method
   - description: description
   - name: name
   - admin_state_up: admin_state_up
   - pool_id: pool_id

Request Example
---------------

.. literalinclude:: samples/lbaas/pool-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - lb_algorithm: lb_algorithm
   - status: status
   - protocol: protocol
   - description: description
   - health_monitors: health_monitors
   - subnet_id: subnet_id
   - tenant_id: project_id
   - project_id: project_id
   - admin_state_up: admin_state_up
   - vip_id: vip_id
   - health_monitors_status: health_monitors_status
   - members: members
   - provider: provider
   - status_description: status_description
   - id: id
   - pool: pool
   - name: name

Response Example
----------------

.. literalinclude:: samples/lbaas/pool-update-response.json
   :language: javascript

Delete pool
===========

.. rest_method::  DELETE /v2.0/lb/pools/{pool_id}

Deletes a load balancer pool.

Error response codes:204,400,401,413,503,500,

Request
-------

.. rest_parameters:: parameters.yaml

   - pool_id: pool_id

.. ============================================================

List VIPs
=========

.. rest_method::  GET /v2.0/lb/vips

Lists VIPs.

The list might be empty.

Normal response codes: 200
Error response codes:500,401,503,

Request
-------

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - status: status
   - status_description: status_description
   - protocol: protocol
   - description: description
   - admin_state_up: admin_state_up
   - subnet_id: subnet_id
   - tenant_id: project_id
   - project_id: project_id
   - connection_limit: connection_limit
   - pool_id: pool_id
   - session_persistence: session_persistence
   - address: address
   - vips: vips
   - protocol_port: protocol_port
   - port_id: port_id
   - id: id
   - name: name

Response Example
----------------

.. literalinclude:: samples/lbaas/vips-list-response.json
   :language: javascript

Create a load balancer VIP
==========================

.. rest_method::  POST /v2.0/lb/vips

Creates a load balancer VIP.

Error response codes:201,400,404,500,401,413,503,409,

Request
-------

.. rest_parameters:: parameters.yaml

   - protocol: protocol
   - description: description
   - admin_state_up: admin_state_up
   - subnet_id: subnet_id
   - tenant_id: project_id
   - project_id: project_id
   - connection_limit: connection_limit
   - pool_id: pool_id
   - session_persistence: session_persistence
   - vip: vip
   - address: address
   - protocol_port: protocol_port
   - name: name

Request Example
---------------

.. literalinclude:: samples/lbaas/vip-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - status: status
   - status_description: status_description
   - protocol: protocol
   - description: description
   - admin_state_up: admin_state_up
   - subnet_id: subnet_id
   - tenant_id: project_id
   - project_id: project_id
   - connection_limit: connection_limit
   - pool_id: pool_id
   - session_persistence: session_persistence
   - vip: vip
   - address: address
   - protocol_port: protocol_port
   - port_id: port_id
   - id: id
   - name: name

Show VIP details
================

.. rest_method::  GET /v2.0/lb/vips/{vip_id}

Shows details for a VIP.

Normal response codes: 200
Error response codes:404,403,500,401,413,503,409,

Request
-------

.. rest_parameters:: parameters.yaml

   - vip_id: vip_id

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - status: status
   - status_description: status_description
   - protocol: protocol
   - description: description
   - admin_state_up: admin_state_up
   - subnet_id: subnet_id
   - tenant_id: project_id
   - project_id: project_id
   - connection_limit: connection_limit
   - pool_id: pool_id
   - session_persistence: session_persistence
   - vip: vip
   - address: address
   - protocol_port: protocol_port
   - port_id: port_id
   - id: id
   - name: name

Response Example
----------------

.. literalinclude:: samples/lbaas/vip-show-response.json
   :language: javascript

Update VIP
==========

.. rest_method::  PUT /v2.0/lb/vips/{vip_id}

Updates a load balancer VIP.

Normal response codes: 200
Error response codes:400,401,413,503,500,

Request
-------

.. rest_parameters:: parameters.yaml

   - description: description
   - admin_state_up: admin_state_up
   - connection_limit: connection_limit
   - pool_id: pool_id
   - session_persistence: session_persistence
   - vip: vip
   - name: name
   - vip_id: vip_id

Request Example
---------------

.. literalinclude:: samples/lbaas/vip-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - status: status
   - status_description: status_description
   - protocol: protocol
   - description: description
   - admin_state_up: admin_state_up
   - subnet_id: subnet_id
   - tenant_id: project_id
   - project_id: project_id
   - connection_limit: connection_limit
   - pool_id: pool_id
   - session_persistence: session_persistence
   - vip: vip
   - address: address
   - protocol_port: protocol_port
   - port_id: port_id
   - id: id
   - name: name

Response Example
----------------

.. literalinclude:: samples/lbaas/vip-update-response.json
   :language: javascript

Delete VIP
==========

.. rest_method::  DELETE /v2.0/lb/vips/{vip_id}

Deletes a load balancer VIP.

Error response codes:204,400,401,413,503,500,

Request
-------

.. rest_parameters:: parameters.yaml

   - vip_id: vip_id

.. ============================================================

List members
============

.. rest_method::  GET /v2.0/lb/members

Lists members.

Normal response codes: 200
Error response codes:400,401,413,503,500,

Request
-------

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - status: status
   - status_description: status_description
   - weight: weight
   - admin_state_up: admin_state_up
   - tenant_id: project_id
   - project_id: project_id
   - pool_id: pool_id
   - members: members
   - address: address
   - protocol_port: protocol_port
   - id: id

Response Example
----------------

.. literalinclude:: samples/lbaas/members-list-response.json
   :language: javascript

Create a load balancer member
=============================

.. rest_method::  POST /v2.0/lb/members

Creates a load balancer member.

Error response codes:201,400,401,413,503,500,

Request
-------

.. rest_parameters:: parameters.yaml

   - weight: weight
   - admin_state_up: admin_state_up
   - tenant_id: project_id
   - project_id: project_id
   - pool_id: pool_id
   - member: member
   - address: address
   - protocol_port: protocol_port

Request Example
---------------

.. literalinclude:: samples/lbaas/member-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - status: status
   - status_description: status_description
   - weight: weight
   - admin_state_up: admin_state_up
   - tenant_id: project_id
   - project_id: project_id
   - pool_id: pool_id
   - member: member
   - address: address
   - protocol_port: protocol_port
   - id: id

Show member details
===================

.. rest_method::  GET /v2.0/lb/members/{member_id}

Shows details for a member.

Normal response codes: 200
Error response codes:400,401,413,503,500,

Request
-------

.. rest_parameters:: parameters.yaml

   - member_id: member_id

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - status: status
   - status_description: status_description
   - weight: weight
   - admin_state_up: admin_state_up
   - tenant_id: project_id
   - project_id: project_id
   - pool_id: pool_id
   - member: member
   - address: address
   - protocol_port: protocol_port
   - id: id

Response Example
----------------

.. literalinclude:: samples/lbaas/member-show-response.json
   :language: javascript

Update member
=============

.. rest_method::  PUT /v2.0/lb/members/{member_id}

Updates a load balancer member.

Normal response codes: 200
Error response codes:400,401,413,503,500,

Request
-------

.. rest_parameters:: parameters.yaml

   - member: member
   - pool_id: pool_id
   - weight: weight
   - admin_state_up: admin_state_up
   - member_id: member_id

Request Example
---------------

.. literalinclude:: samples/lbaas/member-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - status: status
   - status_description: status_description
   - weight: weight
   - admin_state_up: admin_state_up
   - tenant_id: project_id
   - project_id: project_id
   - pool_id: pool_id
   - member: member
   - address: address
   - protocol_port: protocol_port
   - id: id

Response Example
----------------

.. literalinclude:: samples/lbaas/member-update-response.json
   :language: javascript

Delete member
=============

.. rest_method::  DELETE /v2.0/lb/members/{member_id}

Deletes a load balancer member.

Error response codes:204,400,401,413,503,500,

Request
-------

.. rest_parameters:: parameters.yaml

   - member_id: member_id

.. ============================================================

List health monitors
====================

.. rest_method::  GET /v2.0/lb/health_monitors

Lists health monitors.

Normal response codes: 200
Error response codes:400,401,413,503,500,

Request
-------

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - health_monitors: health_monitors
   - tenant_id: project_id
   - project_id: project_id
   - admin_state_up: admin_state_up
   - delay: delay
   - expected_codes: expected_codes
   - max_retries: max_retries
   - http_method: http_method
   - timeout: timeout
   - pools: pools
   - url_path: url_path
   - type: type
   - id: id

Response Example
----------------

.. literalinclude:: samples/lbaas/healthmonitors-list-response.json
   :language: javascript

Create a load balancer health monitor
=====================================

.. rest_method::  POST /v2.0/lb/health_monitors

Creates a load balancer health monitor.

Error response codes:201,400,401,413,503,500,

Request
-------

.. rest_parameters:: parameters.yaml

   - health_monitor: health_monitor
   - tenant_id: project_id
   - project_id: project_id
   - admin_state_up: admin_state_up
   - delay: delay
   - expected_codes: expected_codes
   - max_retries: max_retries
   - http_method: http_method
   - timeout: timeout
   - url_path: url_path
   - type: type

Request Example
---------------

.. literalinclude:: samples/lbaas/healthmonitor-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - health_monitor: health_monitor
   - tenant_id: project_id
   - project_id: project_id
   - admin_state_up: admin_state_up
   - delay: delay
   - expected_codes: expected_codes
   - max_retries: max_retries
   - http_method: http_method
   - timeout: timeout
   - pools: pools
   - url_path: url_path
   - type: type
   - id: id

Show health monitor details
===========================

.. rest_method::  GET /v2.0/lb/health_monitors/{health_monitor_id}

Shows details for a health monitor.

Normal response codes: 200
Error response codes:400,401,413,503,500,

Request
-------

.. rest_parameters:: parameters.yaml

   - health_monitor_id: health_monitor_id

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - health_monitor: health_monitor
   - tenant_id: project_id
   - project_id: project_id
   - admin_state_up: admin_state_up
   - delay: delay
   - expected_codes: expected_codes
   - max_retries: max_retries
   - http_method: http_method
   - timeout: timeout
   - pools: pools
   - url_path: url_path
   - type: type
   - id: id

Response Example
----------------

.. literalinclude:: samples/lbaas/healthmonitor-show-response.json
   :language: javascript

Update health monitor
=====================

.. rest_method::  PUT /v2.0/lb/health_monitors/{health_monitor_id}

Updates a load balancer health monitor.

Normal response codes: 200
Error response codes:400,401,413,503,500,

Request
-------

.. rest_parameters:: parameters.yaml

   - health_monitor: health_monitor
   - admin_state_up: admin_state_up
   - delay: delay
   - expected_codes: expected_codes
   - max_retries: max_retries
   - http_method: http_method
   - timeout: timeout
   - url_path: url_path
   - health_monitor_id: health_monitor_id

Request Example
---------------

.. literalinclude:: samples/lbaas/healthmonitor-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - health_monitor: health_monitor
   - tenant_id: project_id
   - project_id: project_id
   - admin_state_up: admin_state_up
   - delay: delay
   - expected_codes: expected_codes
   - max_retries: max_retries
   - http_method: http_method
   - timeout: timeout
   - pools: pools
   - url_path: url_path
   - type: type
   - id: id

Response Example
----------------

.. literalinclude:: samples/lbaas/healthmonitor-update-response.json
   :language: javascript

Delete health monitor
=====================

.. rest_method::  DELETE /v2.0/lb/health_monitors/{health_monitor_id}

Deletes a load balancer health monitor.

Error response codes:204,400,401,413,503,500,

Request
-------

.. rest_parameters:: parameters.yaml

   - health_monitor_id: health_monitor_id

Associate health monitor with pool
==================================

.. rest_method::  POST /v2.0/lb/pools/{pool_id}/health_monitors

Associates a health monitor with a pool.

Error response codes:201,400,401,413,503,500,

Request
-------

.. rest_parameters:: parameters.yaml

   - id: id
   - health_monitor: health_monitor
   - pool_id: pool_id

Request Example
---------------

.. literalinclude:: samples/lbaas/healthmonitor-associate-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - health_monitor: health_monitor

Disassociate health monitor from pool
=====================================

.. rest_method::  DELETE /v2.0/lb/pools/{pool_id}/health_monitors/{health_monitor_id}

Disassociates a health monitor from a pool.

Error response codes:204,400,401,413,503,500,

Request
-------

.. rest_parameters:: parameters.yaml

   - health_monitor_id: health_monitor_id
   - pool_id: pool_id

