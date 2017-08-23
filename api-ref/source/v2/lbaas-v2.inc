.. -*- rst -*-

==================
LBaaS 2.0 (STABLE)
==================

The Load-Balancer-as-a-Service (LBaaS) version 2.0 extension pairs with the
Networking 2.0 API to enable OpenStack projects to manage load balancers for
their VMs. With this extension you can load-balance client traffic from one
network to application services, such as VMs, on the same network.

Use this extension to create and manage load balancers, listeners, pools,
members of a pool, and health monitors and view status of a resource.

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

List load balancers
===================

.. rest_method::  GET /v2.0/lbaas/loadbalancers

Lists all load balancers for the project.

Use the ``fields`` query parameter to control which fields are
returned in the response body. Additionally, you can filter results
by using query string parameters. For information, see `Filtering
and Column Selection <https://wiki.openstack.org/wiki/Neutron/APIv2
-specification#Filtering_and_Column_Selection>`__.

The list might be empty.

Normal response codes: 200

Error response codes: 401

Request
-------

.. rest_parameters:: parameters.yaml

   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - loadbalancers: loadbalancers
   - admin_state_up: admin_state_up
   - description: description
   - flavor: flavor-id-response
   - id: loadbalancer-id
   - listeners: listeners
   - name: name
   - operating_status: operating_status
   - project_id: project_id
   - provider: loadbalancer-provider
   - provisioning_status: provisioning_status
   - tenant_id: project_id
   - vip_address: vip_address
   - vip_subnet_id: vip_subnet_id
   - pools: pools-obj

Response Example
----------------

.. literalinclude:: samples/lbaas/loadbalancers-list-response.json
   :language: javascript

Create a load balancer
======================

.. rest_method::  POST /v2.0/lbaas/loadbalancers

Creates a load balancer.

This operation provisions a new load balancer by using the
configuration that you define in the request object. After the API
validates the request and starts the provisioning process, the API
returns a response object that contains a unique ID and the status
of provisioning the load balancer.

In the response, the load balancer provisioning status is
``ACTIVE``, ``PENDING_CREATE``, or ``ERROR``.

If the status is ``PENDING_CREATE``, issue GET
``/lbaas/loadbalancers/loadbalancer_id`` to view the progress of
the provisioning operation. When the load balancer status changes
to ``ACTIVE``, the load balancer is successfully provisioned and
operational for traffic handling.

If the API cannot fulfill the request due to insufficient data or
data that is not valid, the service returns the HTTP ``Bad Request
(400)`` response code with information about the failure in the
response body. Validation errors require that you correct the error
and submit the request again.

You can configure all documented features of the load balancer at
creation time by specifying the additional elements or attributes
in the request.

Administrative users can specify a project ID that is different than
their own to create load balancers for other projects.

**Example: Create a load balancer**

- ``project_id``. Admin only. Required to create a load balancer for
  another project.

- ``vip_subnet_id``. The network on which to allocate the VIP
  address for the load balancer. A project can only create load
  balancer VIPs on networks that the policy authorizes, such as her
  own networks or shared or provider networks.

Some attributes receive default values if you omit them from the
request:

- ``admin_state_up``. Default is ``true``.

- ``name``. Default is an empty string.

- ``description``. Default is an empty string.

If you own the subnet where you want to create the load balancer
VIP, you can specify a ``vip_address`` attribute. If you omit the
``vip_address`` attribute from the payload, the LBaaS service
allocates a VIP address from the subnet of the load balancer VIP.

An optional ``flavor`` attribute can be passed to enable dynamic
selection of an appropriate provider if configured by the operator.
The basic selection algorithm chooses the provider in the first
service profile currently associated with flavor.

You can also specify the ``provider`` attribute when you create a
load balancer. You can set this attribute to any service provider
with a ``LOADBALANCER`` service type. Setting both a flavor and a
provider will result in a conflict error.

Finally, ``vip_network_id`` can be used in place of
``vip_subnet_id``. When this option is used, the VIP port is
created on the given network using the default behavior. If
assigned multiple fixed IPs, an IPv4 addresses is chosen as the
VIP in preference to IPv6 addresses.

Normal response codes: 201

Error response codes: 400, 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - loadbalancer: loadbalancer
   - admin_state_up: admin_state_up-request
   - description: description-request
   - flavor: flavor-id-request
   - name: name-request
   - project_id: project_id-request
   - provider: loadbalancer-provider-request
   - tenant_id: project_id-request
   - vip_address: vip_address
   - vip_subnet_id: vip_subnet_id

Request Example
---------------

.. literalinclude:: samples/lbaas/loadbalancer-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - loadbalancer: loadbalancer
   - admin_state_up: admin_state_up
   - description: description
   - flavor: flavor-id-response
   - id: loadbalancer-id
   - listeners: listeners
   - name: name
   - operating_status: operating_status
   - project_id: project_id
   - provider: loadbalancer-provider
   - provisioning_status: provisioning_status
   - tenant_id: project_id
   - vip_address: vip_address
   - vip_network_id: vip_network_id
   - vip_subnet_id: vip_subnet_id
   - pools: pools-obj

Response Example
----------------

.. literalinclude:: samples/lbaas/loadbalancer-create-response.json
   :language: javascript

Show load balancer details
==========================

.. rest_method::  GET /v2.0/lbaas/loadbalancers/{loadbalancer_id}

Shows details for a load balancer.

This operation returns a load balancer object, by ID. If you are
not an administrative user and the load balancer object does not
belong to your project, the service returns the HTTP
``Forbidden (403)`` response code.

Normal response codes: 200

Error response codes: 401, 403

Request
-------

.. rest_parameters:: parameters.yaml

   - loadbalancer_id: loadbalancer-id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - loadbalancer: loadbalancer
   - admin_state_up: admin_state_up
   - description: description
   - id: loadbalancer-id
   - listeners: listeners
   - name: name
   - operating_status: operating_status
   - project_id: project_id
   - provisioning_status: provisioning_status
   - tenant_id: project_id
   - vip_address: vip_address
   - vip_subnet_id: vip_subnet_id
   - pools: pools-obj

Response Example
----------------

.. literalinclude:: samples/lbaas/loadbalancer-show-response.json
   :language: javascript

Update load balancer
====================

.. rest_method::  PUT /v2.0/lbaas/loadbalancers/{loadbalancer_id}

Updates a load balancer.

If the request is valid, the service returns the ``Accepted (202)``
response code. To confirm the update, check that the load balancer
provisioning status is ``ACTIVE``. If the status is
``PENDING_UPDATE``, use a GET operation to poll the load balancer
object for changes.

This operation returns the updated load balancer object with the
``ACTIVE``, ``PENDING_UPDATE``, or ``ERROR`` provisioning status.

Normal response codes: 202

Error response codes: 400, 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - loadbalancer_id: loadbalancer-id-path
   - loadbalancer: loadbalancer
   - admin_state_up: admin_state_up-request
   - name: name-request
   - description: description-request

Request Example
---------------

.. literalinclude:: samples/lbaas/loadbalancer-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - loadbalancer: loadbalancer
   - admin_state_up: admin_state_up
   - description: description
   - flavor: flavor-id-response
   - id: loadbalancer-id
   - listeners: listeners
   - name: name
   - operating_status: operating_status
   - project_id: project_id
   - provider: loadbalancer-provider
   - provisioning_status: provisioning_status
   - tenant_id: project_id
   - vip_address: vip_address
   - vip_subnet_id: vip_subnet_id
   - pools: pools-obj

Response Example
----------------

.. literalinclude:: samples/lbaas/loadbalancer-update-response.json
   :language: javascript

Remove load balancer
====================

.. rest_method::  DELETE /v2.0/lbaas/loadbalancers/{loadbalancer_id}

Removes a load balancer and its associated configuration from the project.

The API immediately purges any and all configuration data. You
cannot recover it.

Example: Delete a load balancer

Normal response codes: 204

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - loadbalancer_id: loadbalancer-id-path

Response
--------

There is no body content for the response of a successful DELETE request.

Show load balancer status tree
==============================

.. rest_method::  GET /v2.0/lbaas/loadbalancers/{loadbalancer_id}/statuses

Shows the status tree for a load balancer.

This operation returns a status tree for a load balancer object, by
load balancer ID. If you are not an administrative user and the
load balancer object does not belong to the project, the API
returns the ``Forbidden (403)`` response code.

If the operation succeeds, the returned element is a status tree
that contains the load balancer and all provisioning and operating
statuses for its children.

Normal response codes: 200

Error response codes: 401, 403

Request
-------

.. rest_parameters:: parameters.yaml

   - loadbalancer_id: loadbalancer-id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - statuses: loadbalancer-statuses
   - loadbalancer: loadbalancer
   - listeners: listeners
   - pools: pools
   - healthmonitor: healthmonitor
   - id: loadbalancer-id
   - members: members
   - operating_status: operating_status
   - provisioning_status: provisioning_status

Response Example
----------------

.. literalinclude:: samples/lbaas/loadbalancer-status-tree.json
   :language: javascript

.. ============================================================

List listeners
==============

.. rest_method::  GET /v2.0/lbaas/listeners

Lists all listeners.

Use the ``fields`` query parameter to control which fields are
returned in the response body. Additionally, you can filter results
by using query string parameters. For information, see `Filtering
and Column Selection <https://wiki.openstack.org/wiki/Neutron/APIv2
-specification#Filtering_and_Column_Selection>`__.

This operation lists all listeners that are associated with your
project.

The list might be empty.

Example: List listeners

Normal response codes: 200

Error response codes: 401

Request
-------

.. rest_parameters:: parameters.yaml

   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - listeners: listeners-response
   - admin_state_up: admin_state_up
   - connection_limit: connection_limit-response
   - default_pool_id: default_pool_id-response
   - default_tls_container_ref: default_tls_container_ref-response
   - description: description
   - id: listener-id-response
   - loadbalancers: loadbalancers
   - name: name
   - project_id: project_id
   - protocol: protocol-response
   - protocol_port: protocol_port
   - sni_container_refs: sni_container_refs-response
   - tenant_id: project_id

Response Example
----------------

.. literalinclude:: samples/lbaas/listeners-list-response.json
   :language: javascript

Create listener
===============

.. rest_method::  POST /v2.0/lbaas/listeners

Creates a listener.

This operation provisions a new listener by using the configuration
that you define in the request object. After the request is
validated and the provisioning process begins, a response object is
returned. The object contains a unique identifier.

At a minimum, you must specify these listener attributes:

- ``project_id``. Admin only. Required to create a listener for
  another project.

- ``loadbalancer_id``. The load balancer on which to provision this
  listener. A project can only create listeners on load balancers
  that the policy authorizes. For example, her own load balancers.

- ``description``. The load balancer description.

- ``protocol``. The protocol for which the front end listens. Must
  be ``HTTP``, ``HTTPS``, ``TCP``, or ``TERMINATED_HTTPS``.

- ``protocol_port``. The port on which the front end listens. Must
  be an integer from 1 to 65535.

Some attributes receive default values if you omit them from the
request:

- ``default_tls_container_ref``. The reference to a container that
  holds TLS secrets. If you also specify ``sni_container_refs``,
  this container is the default. This parameter is required for the
  ``TERMINATED_HTTPS`` protocol.

- ``sni_container_refs``. A list of references to containers that
  hold TLS secrets for server name indication (SNI). This parameter
  is required for the ``TERMINATED_HTTPS`` protocol.

- ``admin_state_up``. Default is ``true``.

- ``name``. Default is an empty string.

- ``description``. Default is an empty string.

- ``connection_limit``. Default is ``-1``, which indicates an
  infinite limit.

If the API cannot fulfill the request due to insufficient data or
data that is not valid, the service returns the HTTP ``Bad Request
(400)`` response code with information about the failure in the
response body. Validation errors require that you correct the error
and submit the request again.

You can configure all documented features of the listener at
creation time by specifying the additional elements or attributes
in the request.

Administrative users can specify a project ID that is different than
their own to create listeners for other projects.

To update a listener, the load balancer to which to attach must
have an ``ACTIVE`` provisioning status.

Normal response codes: 201

Error response codes: 400, 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - listener: listener
   - admin_state_up: admin_state_up-request
   - connection_limit: connection_limit
   - default_pool_id: default_pool_id
   - default_tls_container_ref: default_tls_container_ref
   - description: description
   - loadbalancer_id: loadbalancer-id
   - name: name
   - project_id: project_id-request
   - protocol: protocol-response
   - protocol_port: protocol_port-request
   - sni_container_refs: sni_container_refs
   - tenant_id: project_id-request

Request Example
---------------

.. literalinclude:: samples/lbaas/listener-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - listener: listener
   - admin_state_up: admin_state_up
   - connection_limit: connection_limit-response
   - default_pool_id: default_pool_id-response
   - default_tls_container_ref: default_tls_container_ref-response
   - description: description
   - id: listener-id-response
   - loadbalancers: loadbalancers
   - name: name
   - project_id: project_id
   - protocol: protocol-response
   - protocol_port: protocol_port
   - sni_container_refs: sni_container_refs-response
   - tenant_id: project_id

Response Example
----------------

.. literalinclude:: samples/lbaas/listener-create-response.json
   :language: javascript

Show listener details
=====================

.. rest_method::  GET /v2.0/lbaas/listeners/{listener_id}

Shows details for a listener.

This operation returns a listener object, by ID. If you are not an
administrative user and the listener object does not belong to your
account, the API returns the HTTP ``Forbidden (403)`` response
code.

Example: Show listener details

Normal response codes: 200

Error response codes: 401, 403

Request
-------

.. rest_parameters:: parameters.yaml

   - listener_id: listener-id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - listener: listener
   - admin_state_up: admin_state_up
   - connection_limit: connection_limit-response
   - id: listener-id-response
   - default_pool_id: default_pool_id-response
   - default_tls_container_ref: default_tls_container_ref-response
   - description: description
   - loadbalancers: loadbalancers
   - name: name
   - project_id: project_id
   - protocol: protocol-response
   - protocol_port: protocol_port
   - sni_container_refs: sni_container_refs-response
   - tenant_id: project_id

Response Example
----------------

.. literalinclude:: samples/lbaas/listener-show-response.json
   :language: javascript

Update listener
===============

.. rest_method::  PUT /v2.0/lbaas/listeners/{listener_id}

Updates a listener.

This operation updates the attributes of a listener. Upon
successful validation of the request, the service returns the HTTP
``Accepted (202)`` response code.

Note: You cannot update the ``listener_id``, ``project_id``,
``loadbalancer_id``, ``loadbalancers``, ``default_pool_id``,
``protocol``, and ``protocol_port`` attributes. Attempting to
update an immutable attribute results in the HTTP ``Immutable
(422)`` response code.

Note: You cannot update a listener if the load balancer to which
the listener is attached does not have an ``ACTIVE`` provisioning
status.

Normal response codes: 202

Error response codes: 401, 404, 422

Request
-------

.. rest_parameters:: parameters.yaml

   - listener_id: listener-id-path
   - listener: listener
   - admin_state_up: admin_state_up-request
   - connection_limit: connection_limit
   - default_tls_container_ref: default_tls_container_ref
   - description: description
   - name: name
   - sni_container_refs: sni_container_refs

Request Example
---------------

.. literalinclude:: samples/lbaas/listener-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - listener: listener
   - admin_state_up: admin_state_up
   - connection_limit: connection_limit-response
   - default_pool_id: default_pool_id-response
   - default_tls_container_ref: default_tls_container_ref-response
   - description: description
   - id: listener-id-response
   - loadbalancers: loadbalancers
   - name: name
   - project_id: project_id
   - protocol: protocol-response
   - protocol_port: protocol_port
   - sni_container_refs: sni_container_refs-response
   - tenant_id: project_id

Response Example
----------------

.. literalinclude:: samples/lbaas/listener-update-response.json
   :language: javascript

Remove listener
===============

.. rest_method::  DELETE /v2.0/lbaas/listeners/{listener_id}

Removes a listener.

This operation removes a listener and its associated configuration
from the project. The API immediately purges any and all
configuration data. You cannot recover it.

You cannot delete a listener if the load balancer to which it is
attached does not have an ``ACTIVE`` provisioning status.

Example: Delete a listener

Normal response codes: 204

Error response codes: 401, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - listener_id: listener-id-path

Response
--------

There is no body content for the response of a successful DELETE request.

.. ============================================================

List pools
==========

.. rest_method::  GET /v2.0/lbaas/pools

Lists all pools that are associated with your project.

Use the ``fields`` query parameter to control which fields are
returned in the response body. Additionally, you can filter results
by using query string parameters. For information, see `Filtering
and Column Selection <https://wiki.openstack.org/wiki/Neutron/APIv2
-specification#Filtering_and_Column_Selection>`__.

The list might be empty.

Example: List pools

Normal response codes: 200

Error response codes: 401

Request
-------

.. rest_parameters:: parameters.yaml

   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - pools: pools-obj
   - admin_state_up: admin_state_up
   - description: description
   - healthmonitors: healthmonitors-response
   - healthmonitors_status: healthmonitors_status
   - id: pool-id-response
   - lb_algorithm: lb_algorithm
   - members: members
   - name: name
   - project_id: project_id
   - protocol: protocol-response
   - provider: loadbalancer-provider
   - status: pool-status
   - status_description: status_description
   - subnet_id: pool-subnet_id
   - tenant_id: project_id
   - vip_id: vip_id

Response Example
----------------

.. literalinclude:: samples/lbaas/pools-list-response.json
   :language: javascript

Create pool
===========

.. rest_method::  POST /v2.0/lbaas/pools

Creates a pool.

This operation provisions a pool by using the configuration that
you define in the request object. After the API validates the
request and starts the provisioning process, the API returns a
response object, which contains a unique ID.

At a minimum, you must specify these pool attributes:

- ``project_id``. Admin only. Required to create a pool for another
  project.

- ``protocol``. The protocol for which this pool and its members
  listen. A valid value is ``TCP``, ``HTTP``, or ``HTTPS``.

- ``lb_algorithm``. The load-balancer algorithm, such as
  ``ROUND_ROBIN``, ``LEAST_CONNECTIONS``, and ``SOURCE_IP``, that
  distributes traffic to the pool members. The load-balancer
  provider must support this algorithm.

- ``listener_id``. The ID of the listener in which this pool
  becomes the default pool. Each listener has only one default
  pool.

Some attributes receive default values if you omit them from the
request:

- ``admin_state_up``. Default is ``true``.

- ``name``. Default is an empty string.

- ``description``. Default is an empty string.

- ``session_persistence``. Default is an empty dictionary.

If the API cannot fulfill the request due to insufficient data or
data that is not valid, the service returns the HTTP ``Bad Request
(400)`` response code with information about the failure in the
response body. Validation errors require that you correct the error
and submit the request again.

Users can configure all documented features at creation time by
providing the additional elements or attributes in the request.

Administrative users can specify a project ID that is different than
their own to create pools for other projects.

To update a pool, the load balancer to which to attach must have an
``ACTIVE`` provisioning status.

Normal response codes: 201

Error response codes: 400, 401

Request
-------

.. rest_parameters:: parameters.yaml

   - pool: pool
   - admin_state_up: admin_state_up-request
   - description: description-request
   - lb_algorithm: lb_algorithm
   - listener_id: listener-id-response
   - name: name
   - project_id: project_id-request
   - protocol: protocol
   - subnet_id: pool-subnet_id
   - tenant_id: project_id-request

Request Example
---------------

.. literalinclude:: samples/lbaas/pool-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - pool: pool
   - admin_state_up: admin_state_up
   - description: description
   - healthmonitors: healthmonitors-response
   - healthmonitors_status: healthmonitors_status
   - id: pool-id-response
   - lb_algorithm: lb_algorithm
   - members: members
   - name: name
   - project_id: project_id
   - protocol: protocol-response
   - provider: loadbalancer-provider
   - status: pool-status
   - status_description: status_description
   - subnet_id: pool-subnet_id
   - tenant_id: project_id
   - vip_id: vip_id

Response Example
----------------

.. literalinclude:: samples/lbaas/pool-create-response.json
   :language: javascript

Show pool details
=================

.. rest_method::  GET /v2.0/lbaas/pools/{pool_id}

Shows details for a pool.

This operation shows details for a pool, by ID. If you are not an
administrative user and the pool object does not belong to your
project, the call returns the HTTP ``Forbidden (403)``
response code.

If this operation succeeds, it returns a ``pool`` element.

Example: Show pool details

Normal response codes: 200

Error response codes: 403

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
   - healthmonitors: healthmonitors-response
   - healthmonitors_status: healthmonitors_status
   - lb_algorithm: lb_algorithm
   - members: members
   - id: pool-id-response
   - name: name
   - status: pool-status
   - status_description: status_description
   - project_id: project_id
   - protocol: protocol-response
   - provider: loadbalancer-provider
   - subnet_id: pool-subnet_id
   - tenant_id: project_id
   - vip_id: vip_id

Response Example
----------------

.. literalinclude:: samples/lbaas/pool-show-response.json
   :language: javascript

Update pool
===========

.. rest_method::  PUT /v2.0/lbaas/pools/{pool_id}

Updates a pool.

This operation updates the attributes of a pool. Upon successful
validation of the request, the service returns the HTTP ``Accepted
(202)`` response code.

Note: You cannot update the pool ID, ``project_id``,
``listener_id``, ``listeners``, ``healthmonitor_id``,
``protocol``, and ``members`` immutable attributes. If you try to
update any of these attributes, the service returns the HTTP
``Immutable (422)`` response code   .

Note: You cannot update a pool if the load balancer to which it is
attached does not have an ``ACTIVE`` provisioning status.

Normal response codes: 202

Error response codes: 401, 404, 422

Request
-------

.. rest_parameters:: parameters.yaml

   - pool_id: pool_id-path
   - pool: pool
   - admin_state_up: admin_state_up-request
   - description: description-request
   - lb_algorithm: lb_algorithm
   - name: name

Request Example
---------------

.. literalinclude:: samples/lbaas/pool-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - pool: pool
   - admin_state_up: admin_state_up
   - description: description
   - healthmonitors: healthmonitors-response
   - healthmonitors_status: healthmonitors_status
   - id: pool-id-response
   - lb_algorithm: lb_algorithm
   - members: members
   - name: name
   - status: pool-status
   - status_description: status_description
   - project_id: project_id
   - protocol: protocol-response
   - provider: loadbalancer-provider
   - subnet_id: pool-subnet_id
   - tenant_id: project_id
   - vip_id: vip_id

Response Example
----------------

.. literalinclude:: samples/lbaas/pool-update-response.json
   :language: javascript

Remove pool
===========

.. rest_method::  DELETE /v2.0/lbaas/pools/{pool_id}

Removes a pool.

This operation removes a pool and its associated configuration from
the project. The API immediately purges any and all
configuration data. You cannot recover it.

You cannot delete a pool if the load balancer to which it is
attached does not have an ``ACTIVE`` provisioning status.

Normal response codes: 204

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - pool_id: pool_id-path

Response
--------

There is no body content for the response of a successful DELETE request.

.. ============================================================

List pool members
=================

.. rest_method::  GET /v2.0/lbaas/pools/{pool_id}/members

Lists members of a pool.

Lists all members that are associated with a pool that is
associated with your project. The list of members includes
only members that belong to the pool object identified by
``pool_id``.

The list might be empty.

Example: List pool members

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - pool_id: pool_id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - members: members
   - address: address
   - admin_state_up: admin_state_up
   - id: member-id-response
   - project_id: project_id
   - protocol_port: protocol_port
   - subnet_id: pool-subnet_id
   - tenant_id: project_id
   - weight: member-weight

Response Example
----------------

.. literalinclude:: samples/lbaas/pool-members-list-response.json
   :language: javascript

Add member to pool
==================

.. rest_method::  POST /v2.0/lbaas/pools/{pool_id}/members

Adds a member to a pool.

This operation provisions a member and adds it to a pool by using
the configuration that you define in the request object. After the
API validates the request and starts the provisioning process, it
returns a response object, which contains a unique ID.

At a minimum, you must specify these pool attributes:

- ``project_id``. Admin only. Required to create a pool for another
  project.

- ``address``. The IP address of the member to receive traffic from
  the load balancer.

- ``protocol_port`` The port on which the member listens for
  traffic.

Some attributes receive default values if you omit them from the
request:

- ``admin_state_up``. Default is ``true``.

- ``weight``. Default is ``1``.

If you omit the ``subnet_id`` parameter, LBaaS uses the
``vip_subnet_id`` parameter value for the subnet UUID.

If the request fails due to incorrect data, the service returns the
HTTP ``Bad Request (400)`` response code with information about the
failure in the response body. Validation errors require that you
correct the error and submit the request again.

To configure all documented member features at creation time,
specify additional elements or attributes in the request.

Administrative users can specify a project ID that is different than
their own to create members for other projects.

To update a member, the load balancer must have an ``ACTIVE``
provisioning status.

Normal response codes: 201

Error response codes: 400, 401

Request
-------

.. rest_parameters:: parameters.yaml

   - pool_id: pool_id-path
   - address: address
   - member: member
   - project_id: project_id-request
   - protocol_port: protocol_port
   - subnet_id: pool-subnet_id-request
   - tenant_id: project_id-request

Request Example
---------------

.. literalinclude:: samples/lbaas/member-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - member: member
   - address: address
   - admin_state_up: admin_state_up
   - id: member-id-response
   - project_id: project_id
   - protocol_port: protocol_port
   - subnet_id: pool-subnet_id
   - tenant_id: project_id
   - weight: member-weight

Response Example
----------------

.. literalinclude:: samples/lbaas/member-create-response.json
   :language: javascript

Show pool member details
========================

.. rest_method::  GET /v2.0/lbaas/pools/{pool_id}/members/{member_id}

Shows details for a pool member.

This operation returns a member object identified by ``member_id``
that belongs to a pool object identified by ``pool_id``. If you are
not an administrative user and the pool or member object does not
belong to your project, the service returns the HTTP
``Forbidden (403)`` response code.

If this operation succeeds, it returns a pool element.

Example: Show pool member details

Normal response codes: 200

Error response codes: 401, 403

Request
-------

.. rest_parameters:: parameters.yaml

   - pool_id: pool_id-path
   - member_id: member_id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - member: member
   - address: address
   - admin_state_up: admin_state_up
   - id: member-id-response
   - project_id: project_id
   - protocol_port: protocol_port
   - subnet_id: pool-subnet_id
   - tenant_id: project_id
   - weight: member-weight

Response Example
----------------

.. literalinclude:: samples/lbaas/member-show-response.json
   :language: javascript

Update pool member
==================

.. rest_method::  PUT /v2.0/lbaas/pools/{pool_id}/members/{member_id}

Updates attributes for a pool member.

Upon successful validation of the request, the service returns the
HTTP ``OK (200)`` response code.

Note: You cannot update the member ID, ``project_id``,
``address``, ``protocol_port``, and ``subnet_id`` attributes. If
you attempt to update any of these attributes, the service returns
the HTTP ``Immutable (422)`` response code.

Note: You cannot update a member if the attached load balancer does
not have an ``ACTIVE`` provisioning status.

Normal response codes: 200

Error response codes: 401, 404, 422

Request
-------

.. rest_parameters:: parameters.yaml

   - pool_id: pool_id-path
   - member_id: member_id-path
   - member: member
   - admin_state_up: admin_state_up
   - weight: member-weight-request

Request Example
---------------

.. literalinclude:: samples/lbaas/member-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - member: member
   - address: address
   - admin_state_up: admin_state_up
   - id: member-id-response
   - project_id: project_id
   - protocol_port: protocol_port
   - subnet_id: pool-subnet_id
   - tenant_id: project_id
   - weight: member-weight

Response Example
----------------

.. literalinclude:: samples/lbaas/member-update-response.json
   :language: javascript

Remove member from pool
=======================

.. rest_method::  DELETE /v2.0/lbaas/pools/{pool_id}/members/{member_id}

Removes a member from a pool and its associated configuration from the project.

The API immediately purges any and all configuration data. You
cannot recover it.

You cannot delete a member if the attached load balancer does not
have an ``ACTIVE`` provisioning status.

Example: Remove a member from a pool

Normal response codes: 204

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - pool_id: pool_id-path
   - member_id: member_id-path

Response
--------

There is no body content for the response of a successful DELETE request.

.. ============================================================

List health monitors
====================

.. rest_method::  GET /v2.0/lbaas/healthmonitors

Lists health monitors.

This operation lists all health monitors that are associated with
your project.

Use the ``fields`` query parameter to control which fields are
returned in the response body. Additionally, you can filter results
by using query string parameters. For information, see `Filtering
and Column Selection <https://wiki.openstack.org/wiki/Neutron/APIv2
-specification#Filtering_and_Column_Selection>`__.

This operation returns a list, which might be empty.

Normal response codes: 200

Error response codes: 401

Request
-------

.. rest_parameters:: parameters.yaml

   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - healthmonitors: healthmonitors-obj
   - admin_state_up: admin_state_up
   - delay: delay
   - expected_codes: expected_codes-response
   - http_method: http_method
   - id: healthmonitor-id
   - max_retries: max_retries
   - pools: pools
   - project_id: project_id
   - tenant_id: project_id
   - timeout: timeout
   - type: type
   - url_path: url_path-response

Response Example
----------------

.. literalinclude:: samples/lbaas/healthmonitors-list-response.json
   :language: javascript

Create health monitor
=====================

.. rest_method::  POST /v2.0/lbaas/healthmonitors

Creates a health monitor.

This operation provisions a health monitor by using the
configuration that you define in the request object. After the API
validates the request and start the provisioning process, it
returns a response object. The object contains a unique identifier.

At a minimum, you must specify these health monitor attributes:

- ``project_id``. Admin only. Required to create a health monitor for
  another project.

- ``type``. The type of health monitor. A valid value is ``TCP``,
  ``HTTP``, or ``HTTPS``.

- ``delay``. The interval, in seconds, between health checks.

- ``timeout``. The time, in seconds, after which a health check
  times out.

- ``max_retries``. Number of failed health checks before marked as
  OFFLINE.

- ``pool_id``. The pool to monitor.

Some attributes receive default values if you omit them from the
request, and are only useful when you specify a health monitor type
of HTTP(S):

- ``http_method``. Default is ``GET``.

- ``url_path``. Default is ``/``.

- ``expected_codes``. The expected HTTP status codes to get from a
  successful health check. Default is ``200``.

- ``admin_state_up``. Default is ``true``.

If the API cannot fulfill the request due to insufficient data or
data that is not valid, it returns the ``Bad Request (400)``
response code with information about the nature of the failure in
the response body. Failures in the validation process are non-
recoverable and require that you correct the cause of the failure
and submit the request again.

You can configure all documented features of the health monitor at
creation time by specifying the additional elements or attributes
in the request.

Administrative users can specify a project ID that is different than
their own to create health monitors for other projects.

To update a health monitor, the load balancer to which to attach
must have an ``ACTIVE`` provisioning status.

Normal response codes: 201

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - healthmonitor: healthmonitor
   - admin_state_up: admin_state_up
   - delay: delay
   - expected_codes: expected_codes
   - http_method: http_method
   - max_retries: max_retries
   - pool_id: pool_id-request
   - project_id: project_id
   - tenant_id: project_id
   - timeout: timeout
   - type: type
   - url_path: url_path

Request Example
---------------

.. literalinclude:: samples/lbaas/healthmonitor-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - healthmonitor: healthmonitor
   - admin_state_up: admin_state_up
   - delay: delay
   - expected_codes: expected_codes-response
   - http_method: http_method
   - id: healthmonitor-id
   - max_retries: max_retries
   - pools: pools
   - project_id: project_id
   - tenant_id: project_id
   - timeout: timeout
   - type: type
   - url_path: url_path-response

Response Example
----------------

.. literalinclude:: samples/lbaas/healthmonitor-show-response.json
   :language: javascript

Show health monitor details
===========================

.. rest_method::  GET /v2.0/lbaas/healthmonitors/{healthmonitor_id}

Shows details for a health monitor.

This operation returns a health monitor object, by health monitor
ID. If you are not an administrative user and the health monitor
object does not belong to your project, the service returns
the HTTP ``Forbidden (403)`` response code.

Example: Show health monitor details

Normal response codes: 200

Error response codes: 401, 403

Request
-------

.. rest_parameters:: parameters.yaml

   - healthmonitor_id: healthmonitor_id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - healthmonitor: healthmonitor
   - admin_state_up: admin_state_up
   - delay: delay
   - expected_codes: expected_codes-response
   - http_method: http_method
   - max_retries: max_retries
   - id: healthmonitor-id
   - pools: pools
   - project_id: project_id
   - tenant_id: project_id
   - timeout: timeout
   - type: type
   - url_path: url_path-response

Response Example
----------------

.. literalinclude:: samples/lbaas/healthmonitor-show-response.json
   :language: javascript

Update health monitor
=====================

.. rest_method::  PUT /v2.0/lbaas/healthmonitors/{healthmonitor_id}

Updates a health monitor.

Upon successful validation of the request, the service returns the
HTTP ``Accepted (202)`` response code.

Note: The health monitor ID, ``project_id``, ``pool_id``, and type
are immutable attributes and cannot be updated. If you specify an
unsupported attribute, the service returns the HTTP ``Immutable
(422)`` response code.

Normal response codes: 202

Error response codes: 401, 404, 422

Request
-------

.. rest_parameters:: parameters.yaml

   - healthmonitor_id: healthmonitor_id-path
   - healthmonitor: healthmonitor
   - admin_state_up: admin_state_up
   - delay: delay
   - expected_codes: expected_codes
   - http_method: http_method
   - max_retries: max_retries
   - timeout: timeout
   - url_path: url_path

Request Example
---------------

.. literalinclude:: samples/lbaas/healthmonitor-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - healthmonitor: healthmonitor
   - admin_state_up: admin_state_up
   - delay: delay
   - expected_codes: expected_codes-response
   - http_method: http_method
   - max_retries: max_retries
   - id: healthmonitor-id
   - pools: pools
   - project_id: project_id
   - tenant_id: project_id
   - timeout: timeout
   - type: type
   - url_path: url_path-response

Response Example
----------------

.. literalinclude:: samples/lbaas/healthmonitor-update-response.json
   :language: javascript

Remove health monitor
=====================

.. rest_method::  DELETE /v2.0/lbaas/healthmonitors/{healthmonitor_id}

Removes a health monitor and its associated configuration from the project.

The API immediately purges any and all configuration data. You
cannot recover it.

You cannot delete a health monitor if the attached load balancer
does not have an ``ACTIVE`` provisioning status.

Example: Delete a health monitor

Normal response codes: 204

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - healthmonitor_id: healthmonitor_id-path

Response
--------

There is no body content for the response of a successful DELETE request.
