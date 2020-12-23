.. -*- rst -*-

=====
Ports
=====

Lists, shows details for, creates, updates, and deletes ports.

Allowed address pairs
=====================

The ``allowed-address-pairs`` extension adds an ``allowed_address_pairs``
attribute to ports. The value of ``allowed_address_pairs`` is an array of
allowed address pair objects, each having an ``ip_address`` and a
``mac_address``. The set of allowed address pairs defines IP and MAC address
that the port can use when sending packets if ``port_security_enabled`` is
``true`` (see the ``port-security`` extension). Note that while the
``ip_address`` is required in each allowed address pair, the ``mac_address``
is optional and will be taken from the port if not specified.

.. warning::

    If a security group with a ``remote_group_id`` rule is used by a port, adding
    an address pair with IP address ``0.0.0.0/0`` (``ANY``) will bypass all rules
    with source IP address restrictions for all ports which use the same security
    group.

Data plane status extension
===========================

The data plane port extension (``data-plane-status``) adds a new attribute
``data_plane_status`` to represent the status of the underlying data plane.
This attribute is to be managed by entities outside of the Networking service,
while the ``status`` attribute is managed by Networking service. Both status
attributes are independent from one another.

Supported data plane status values:

- ``null``: no status being reported; default value
- ``ACTIVE``: the underlying data plane is up and running
- ``DOWN``: no traffic can flow from/to the port

DNS integration
===============

The ``dns-integration`` extension adds the ``dns_name`` and ``dns_assignment``
attributes to port resources. While the ``dns_name`` can be set on create and
update operations, the ``dns_assignment`` is read-only and shows the
``hostname``, ``ip_address`` and ``fqdn`` for the port's internal DNS
assignment.

To enable the ``dns_domain`` on port resources, the ``dns-domain-ports``
extension must be used in conjunction with the ``dns-integration`` extension.
When enabled and set, a port level ``dns_domain`` take precedence over a
``dns_domain`` specified in the port's network allowing per-port DNS domains.

Device profile
==============

The port device profile extension (``port-device-profile``) defines a named set
of user requirements for one or more acceletators. This parameter is a
reference for Cyborg project, read by Nova when a port is requested. If this
parameter is populated, Nova makes a request to Cyborg.
https://docs.openstack.org/api-ref/accelerator/v2/index.html#device-profiles

Extra DHCP option (``extra_dhcp_opt``) extension
================================================

The extra DHCP option (``extra_dhcp_opt``) extension enables extra
DHCP configuration options on ``ports``. For example, PXE boot
options to DHCP clients can be specified (e.g. tftp-server, server-ip-address,
bootfile-name). The value of the ``extra_dhcp_opt`` attribute is an array of
DHCP option objects, where each object contains an ``opt_name`` and
``opt_value`` (string values) as well as an optional ``ip_version``
(the acceptable values are either the integer ``4`` or ``6``).

IP allocation extension
=======================

The IP allocation extension (``ip_allocation``) adds a new read-only attribute
``ip_allocation`` that indicates when ports use deferred, immediate or
no IP allocation.

IP Substring Filtering
======================

The ``ip-substring-filtering`` extension adds support for filtering ports by
using part of an IP address.

Mac learning extension
======================

The ``mac_learning_enabled`` extension extends neutron ports providing the
ability to enable MAC learning on the associated port via the
```mac_learning_enabled``` attribute.

NUMA affinity policy
====================

The NUMA affinity policy extension (``port-numa-affinity-policy``) defines
the Nova scheduling strategy according to the network backend NUMA topology.
This parameter could be ``required``, ``preferred``, ``legacy`` or ``None``.

Port binding extended attributes
================================

The port binding extension (``binding``) allows administrative users
to specify and retrieve physical binding information of ports.
The extension defines several attributes whose names have a prefix
``binding:`` including ``binding:host_id``, ``binding:vnic_type``,
``binding:vif_type``, ``binding:vif_details``, and ``binding:profile``.

Port resource request
=====================

The port resource request extension (``port-resource-request``) allows
administrative users (including Nova) to retrieve the Placement resources and
traits needed by a port by introducing the ``resource_request`` to ``port`` resources.

Port security
=============

The ``port-security`` extension adds the ``port_security_enabled`` boolean
attribute to ports. If a ``port-security`` value is not specified during
port creation, a port will inherit the ``port_security_enabled`` from the
network its connected to.

QoS extension
=============

The :ref:`QoS <quality-of-service>` extension (``qos``) makes it possible to
define QoS policies and associate these to the ports by introducing the
``qos_policy_id`` attribute. The policies should be created before they are
associated to the ports.

QoS network policy
==================

The ``qos-port-network-policy`` extension adds the read only parameter
``qos_network_policy_id`` to the port responses. This parameter contains the
QoS policy ID of the network where this port is plugged.

Regenerate mac address extension
================================

The Port MAC address regenerate extension (``port-mac-address-regenerate``)
makes it possible to regenerate the mac address of a port. When passing
``'null'`` (``None``) as the ``mac_address`` on port update, a new mac address
will be generated and set on the port.

Resource timestamps
===================

The ``standard-attr-timestamp`` extension adds the ``created_at`` and
``updated_at`` attributes to all resources that have standard attributes.

Tag extension
=============

The ``standard-attr-tag`` adds Tag support for resources with
standard attributes by adding the ``tags`` attribute
allowing consumers to associate tags with resources.

Uplink status propagation
=========================

The ``uplink-status-propagation`` extension adds ``propagate_uplink_status``
attribute to port. If this attribute is set to ``false``, uplink status
propagation is disabled. If this attribute is not specified, it is default to
``true`` which indicates uplink status propagation is enabled.

Show port details
=================

.. rest_method::  GET /v2.0/ports/{port_id}

Shows details for a port.

Use the ``fields`` query parameter to control which fields are
returned in the response body. For information, see `Filtering and
Column Selection <http://specs.openstack.org/openstack/neutron-
specs/specs/api/networking_general_api_information.html#filtering-
and-column-selection>`__.

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - port_id: port_id-path
   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - port: port
   - admin_state_up: admin_state_up
   - allowed_address_pairs: allowed_address_pairs
   - binding:host_id: binding:host_id
   - binding:profile: binding:profile
   - binding:vif_details: binding:vif_details
   - binding:vif_type: binding:vif_type
   - binding:vnic_type: binding:vnic_type
   - created_at: created_at_resource
   - data_plane_status: data_plane_status
   - description: description
   - device_id: device_id
   - device_owner: device_owner
   - dns_assignment: dns_assignment
   - dns_domain: dns_domain
   - dns_name: dns_name
   - extra_dhcp_opts: extra_dhcp_opts
   - fixed_ips: fixed_ips
   - id: id
   - ip_allocation: ip_allocation
   - mac_address: mac_address
   - name: name
   - network_id: network_id
   - numa_affinity_policy: numa_affinity_policy
   - port_security_enabled: port_security_enabled
   - project_id: project_id
   - qos_network_policy_id: qos_network_policy_id-port-response
   - qos_policy_id: qos_policy_id-port-response
   - revision_number: revision_number
   - resource_request: port-resource
   - security_groups: port-security_groups
   - status: port-status
   - tags: tags
   - tenant_id: project_id
   - updated_at: updated_at_resource
   - propagate_uplink_status: propagate_uplink_status
   - mac_learning_enabled: mac_learning_enabled

Response Example
----------------

.. literalinclude:: samples/ports/port-show-response.json
   :language: javascript

Response Example (admin user)
-----------------------------

.. literalinclude:: samples/ports/port-bind-show-response.json
   :language: javascript

Update port
===========

.. rest_method::  PUT /v2.0/ports/{port_id}

Updates a port.

You can update information for a port, such as its symbolic name
and associated IPs. When you update IPs for a port, any previously
associated IPs are removed, returned to the respective subnet
allocation pools, and replaced by the IPs in the request body.
Therefore, this operation replaces the ``fixed_ip`` attribute when
you specify it in the request body. If the updated IP addresses are
not valid or are already in use, the operation fails and the
existing IP addresses are not removed from the port.

When you update security groups for a port and the operation
succeeds, any associated security groups are removed and replaced
by the security groups in the request body. Therefore, this
operation replaces the ``security_groups`` attribute when you
specify it in the request body. If the security groups are not
valid, the operation fails and the existing security groups are not
removed from the port.

When you update ``binding:profile`` of a port with null it is treated as {}
in the response.

Only admins and users with a specific role can update the data plane status
(default role: ``data_plane_integrator``).


Normal response codes: 200

Error response codes: 400, 401, 403, 404, 409, 412

Request
-------

.. rest_parameters:: parameters.yaml

   - port_id: port_id-path
   - port: port
   - admin_state_up: admin_state_up-request
   - allowed_address_pairs: allowed_address_pairs-request
   - binding:host_id: binding:host_id-request
   - binding:profile: binding:profile-request
   - binding:vnic_type: binding:vnic_type-request
   - data_plane_status: data_plane_status-request
   - description: description-request
   - device_id: device_id-request
   - device_owner: device_owner-request
   - dns_domain: dns_domain-request
   - dns_name: dns_name-request
   - extra_dhcp_opts: extra_dhcp_opts-request
   - fixed_ips: fixed_ips-request
   - mac_address: mac_address-request-put
   - name: name-request
   - numa_affinity_policy: numa_affinity_policy-request
   - port_security_enabled: port_security_enabled-request
   - qos_policy_id: qos_policy_id-port-request
   - security_groups: port-security_groups-request
   - mac_learning_enabled: mac_learning_enabled-request

Request Example
---------------

.. literalinclude:: samples/ports/port-update-request.json
   :language: javascript

Request Example (admin user)
----------------------------

.. literalinclude:: samples/ports/port-bind-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - port: port
   - admin_state_up: admin_state_up
   - allowed_address_pairs: allowed_address_pairs
   - binding:host_id: binding:host_id
   - binding:profile: binding:profile
   - binding:vif_details: binding:vif_details
   - binding:vif_type: binding:vif_type
   - binding:vnic_type: binding:vnic_type
   - created_at: created_at_resource
   - data_plane_status: data_plane_status
   - description: description
   - device_id: device_id
   - device_owner: device_owner
   - dns_assignment: dns_assignment
   - dns_domain: dns_domain
   - dns_name: dns_name
   - extra_dhcp_opts: extra_dhcp_opts
   - fixed_ips: fixed_ips
   - id: id
   - ip_allocation: ip_allocation
   - mac_address: mac_address
   - name: name
   - network_id: network_id
   - numa_affinity_policy: numa_affinity_policy
   - port_security_enabled: port_security_enabled
   - project_id: project_id
   - qos_network_policy_id: qos_network_policy_id-port-response
   - qos_policy_id: qos_policy_id-port-response
   - revision_number: revision_number
   - resource_request: port-resource
   - security_groups: port-security_groups
   - status: port-status
   - tags: tags
   - tenant_id: project_id
   - updated_at: updated_at_resource
   - propagate_uplink_status: propagate_uplink_status
   - mac_learning_enabled: mac_learning_enabled

Response Example
----------------

.. literalinclude:: samples/ports/port-update-response.json
   :language: javascript

Response Example (admin user)
-----------------------------

.. literalinclude:: samples/ports/port-bind-update-response.json
   :language: javascript

Delete port
===========

.. rest_method::  DELETE /v2.0/ports/{port_id}

Deletes a port.

Any IP addresses that are associated with the port are returned to
the respective subnets allocation pools.

Normal response codes: 204

Error response codes: 401, 403, 404, 412

Request
-------

.. rest_parameters:: parameters.yaml

   - port_id: port_id-path

Response
--------

There is no body content for the response of a successful DELETE request.

List ports
==========

.. rest_method::  GET /v2.0/ports

Lists ports to which the user has access.

Default policy settings return only those ports that are owned by
the project of the user who submits the request, unless the request is submitted
by a user with administrative rights.

Use the ``fields`` query parameter to control which fields are
returned in the response body. Additionally, you can filter results
by using query string parameters. For information, see `Filtering
and Column Selection <https://wiki.openstack.org/wiki/Neutron/APIv2
-specification#Filtering_and_Column_Selection>`__.

If the ``ip-substring-filtering`` extension is enabled, the Neutron API
supports IP address substring filtering on the ``fixed_ips`` attribute.
If you specify an IP address substring (``ip_address_substr``) in
an entry of the ``fixed_ips`` attribute, the Neutron API will list all
ports that have an IP address matching the substring.

Normal response codes: 200

Error response codes: 401

Request
-------

.. rest_parameters:: parameters.yaml

   - admin_state_up: admin_state_up-query
   - binding:host_id: binding:host_id-query
   - description: description-query
   - device_id: device_id-query
   - device_owner: device_owner-query
   - fixed_ips: fixed_ips-query
   - id: id-query
   - ip_allocation: ip_allocation-query
   - mac_address: mac_address-query
   - name: name-query
   - network_id: network_id-query
   - project_id: project_id-query
   - revision_number: revision_number-query
   - sort_dir: sort_dir
   - sort_key: port-sort_key
   - status: port-status-query
   - tenant_id: project_id-query
   - tags: tags-query
   - tags-any: tags-any-query
   - not-tags: not-tags-query
   - not-tags-any: not-tags-any-query
   - fields: fields
   - mac_learning_enabled: mac_learning_enabled-query

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - ports: ports
   - admin_state_up: admin_state_up
   - allowed_address_pairs: allowed_address_pairs
   - binding:host_id: binding:host_id
   - binding:profile: binding:profile
   - binding:vif_details: binding:vif_details
   - binding:vif_type: binding:vif_type
   - binding:vnic_type: binding:vnic_type
   - created_at: created_at_resource
   - data_plane_status: data_plane_status
   - description: description
   - device_id: device_id
   - device_owner: device_owner
   - dns_assignment: dns_assignment
   - dns_domain: dns_domain
   - dns_name: dns_name
   - extra_dhcp_opts: extra_dhcp_opts
   - fixed_ips: fixed_ips
   - id: id
   - ip_allocation: ip_allocation
   - mac_address: mac_address
   - name: name
   - network_id: network_id
   - numa_affinity_policy: numa_affinity_policy
   - port_security_enabled: port_security_enabled
   - project_id: project_id
   - qos_network_policy_id: qos_network_policy_id-port-response
   - qos_policy_id: qos_policy_id-port-response
   - revision_number: revision_number
   - resource_request: port-resource
   - security_groups: port-security_groups
   - status: port-status
   - tags: tags
   - tenant_id: project_id
   - updated_at: updated_at_resource
   - propagate_uplink_status: propagate_uplink_status
   - mac_learning_enabled: mac_learning_enabled

Response Example
----------------

.. literalinclude:: samples/ports/ports-list-response.json
   :language: javascript

Response Example (admin user)
-----------------------------

.. literalinclude:: samples/ports/ports-bind-list-response.json
   :language: javascript

Create port
===========

.. rest_method::  POST /v2.0/ports

Creates a port on a network.

To define the network in which to create the port, specify the
``network_id`` attribute in the request body.

Normal response codes: 201

Error response codes: 400, 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - port: port
   - admin_state_up: admin_state_up-request
   - allowed_address_pairs: allowed_address_pairs-request
   - binding:host_id: binding:host_id-request
   - binding:profile: binding:profile-request
   - binding:vnic_type: binding:vnic_type-request
   - description: description-request
   - device_id: device_id-request
   - device_owner: device_owner-request
   - dns_domain: dns_domain-request
   - dns_name: dns_name-request
   - extra_dhcp_opts: extra_dhcp_opts-request
   - fixed_ips: fixed_ips-request
   - mac_address: mac_address-request
   - name: name-request
   - network_id: network_id
   - numa_affinity_policy: numa_affinity_policy-request
   - port_security_enabled: port_security_enabled-request
   - project_id: project_id-request
   - qos_policy_id: qos_policy_id-port-request
   - security_groups: port-security_groups-request
   - tenant_id: project_id-request
   - propagate_uplink_status: propagate_uplink_status-request
   - mac_learning_enabled: mac_learning_enabled-request

Request Example
---------------

.. literalinclude:: samples/ports/port-create-request.json
   :language: javascript

Request Example (admin user)
----------------------------

.. literalinclude:: samples/ports/port-bind-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - port: port
   - admin_state_up: admin_state_up
   - allowed_address_pairs: allowed_address_pairs
   - binding:host_id: binding:host_id
   - binding:profile: binding:profile
   - binding:vif_details: binding:vif_details
   - binding:vif_type: binding:vif_type
   - binding:vnic_type: binding:vnic_type
   - created_at: created_at_resource
   - data_plane_status: data_plane_status
   - description: description
   - device_id: device_id
   - device_owner: device_owner
   - dns_assignment: dns_assignment
   - dns_domain: dns_domain
   - dns_name: dns_name
   - extra_dhcp_opts: extra_dhcp_opts
   - fixed_ips: fixed_ips
   - id: id
   - ip_allocation: ip_allocation
   - mac_address: mac_address
   - name: name
   - network_id: network_id
   - numa_affinity_policy: numa_affinity_policy
   - port_security_enabled: port_security_enabled
   - project_id: project_id
   - qos_network_policy_id: qos_network_policy_id-port-response
   - qos_policy_id: qos_policy_id-port-response
   - revision_number: revision_number
   - resource_request: port-resource
   - security_groups: port-security_groups
   - status: port-status
   - tags: tags
   - tenant_id: project_id
   - updated_at: updated_at_resource
   - propagate_uplink_status: propagate_uplink_status
   - mac_learning_enabled: mac_learning_enabled

Response Example
----------------

.. literalinclude:: samples/ports/port-create-response.json
   :language: javascript

Response Example (admin user)
-----------------------------

.. literalinclude:: samples/ports/port-bind-create-response.json
   :language: javascript

Bulk create ports
=================

.. rest_method::  POST /v2.0/ports

Creates multiple ports in a single request. Specify a list of ports in the request body.

Guarantees the atomic completion of the bulk operation.

Normal response codes: 201

Error response codes: 400, 401, 403, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - ports: ports
   - admin_state_up: admin_state_up-request
   - allowed_address_pairs: allowed_address_pairs-request
   - binding:host_id: binding:host_id-request
   - binding:profile: binding:profile-request
   - binding:vnic_type: binding:vnic_type-request
   - description: description-request
   - device_id: device_id-request
   - device_owner: device_owner-request
   - dns_domain: dns_domain-request
   - dns_name: dns_name-request
   - extra_dhcp_opts: extra_dhcp_opts-request
   - fixed_ips: fixed_ips-request
   - mac_address: mac_address-request
   - name: name-request
   - network_id: network_id
   - numa_affinity_policy: numa_affinity_policy-request
   - port_security_enabled: port_security_enabled-request
   - project_id: project_id-request
   - qos_policy_id: qos_policy_id-port-request
   - security_groups: port-security_groups-request
   - tenant_id: project_id-request
   - propagate_uplink_status: propagate_uplink_status-request
   - mac_learning_enabled: mac_learning_enabled-request

Request Example
---------------

.. literalinclude:: samples/ports/ports-bulk-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - ports: ports
   - admin_state_up: admin_state_up
   - allowed_address_pairs: allowed_address_pairs
   - binding:host_id: binding:host_id
   - binding:profile: binding:profile
   - binding:vif_details: binding:vif_details
   - binding:vif_type: binding:vif_type
   - binding:vnic_type: binding:vnic_type
   - created_at: created_at_resource
   - data_plane_status: data_plane_status
   - description: description
   - device_id: device_id
   - device_owner: device_owner
   - dns_assignment: dns_assignment
   - dns_domain: dns_domain
   - dns_name: dns_name
   - extra_dhcp_opts: extra_dhcp_opts
   - fixed_ips: fixed_ips
   - id: id
   - ip_allocation: ip_allocation
   - mac_address: mac_address
   - name: name
   - network_id: network_id
   - numa_affinity_policy: numa_affinity_policy
   - port_security_enabled: port_security_enabled
   - project_id: project_id
   - qos_network_policy_id: qos_network_policy_id-port-response
   - qos_policy_id: qos_policy_id-port-response
   - revision_number: revision_number
   - security_groups: port-security_groups
   - status: port-status
   - tags: tags
   - tenant_id: project_id
   - updated_at: updated_at_resource
   - propagate_uplink_status: propagate_uplink_status
   - mac_learning_enabled: mac_learning_enabled

Response Example
----------------

.. literalinclude:: samples/ports/ports-bulk-create-response.json
   :language: javascript
