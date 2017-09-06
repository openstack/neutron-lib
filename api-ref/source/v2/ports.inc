.. -*- rst -*-

=====
Ports
=====

Lists, shows details for, creates, updates, and deletes ports.

Port binding extended attributes
================================

The port binding extension (``binding``) allows administrative users
to specify and retrieve physical binding information of ports.
The extension defines several attributes whose names have a prefix
``binding:`` including ``binding:host_id``, ``binding:vnic_type``,
``binding:vif_type``, ``binding:vif_details``, and ``binding:profile``.

|

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
   - created_at: created_at
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
   - mac_address: mac_address
   - name: name
   - network_id: network_id
   - port_security_enabled: port_security_enabled
   - project_id: project_id
   - revision_number: revision_number
   - security_groups: port-security_groups
   - status: port-status
   - tenant_id: project_id
   - updated_at: updated_at

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

Only admins and users with a specific role can update the data plane status
(default role: ``data_plane_integrator``).


Normal response codes: 200

Error response codes: 400, 401, 403, 404, 409

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
   - port_security_enabled: port_security_enabled-request
   - security_groups: port-security_groups-request

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
   - created_at: created_at
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
   - mac_address: mac_address
   - name: name
   - network_id: network_id
   - port_security_enabled: port_security_enabled
   - project_id: project_id
   - revision_number: revision_number
   - security_groups: port-security_groups
   - status: port-status
   - tenant_id: project_id
   - updated_at: updated_at

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

Error response codes: 401, 403, 404

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

Normal response codes: 200

Error response codes: 401

Request
-------

.. rest_parameters:: parameters.yaml

   - fields: fields

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
   - created_at: created_at
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
   - mac_address: mac_address
   - name: name
   - network_id: network_id
   - port_security_enabled: port_security_enabled
   - project_id: project_id
   - revision_number: revision_number
   - security_groups: port-security_groups
   - status: port-status
   - tenant_id: project_id
   - updated_at: updated_at

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
   - port_security_enabled: port_security_enabled-request
   - project_id: project_id-request
   - security_groups: port-security_groups-request
   - tenant_id: project_id-request

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
   - created_at: created_at
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
   - mac_address: mac_address
   - name: name
   - network_id: network_id
   - port_security_enabled: port_security_enabled
   - project_id: project_id
   - revision_number: revision_number
   - security_groups: port-security_groups
   - status: port-status
   - tenant_id: project_id
   - updated_at: updated_at

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
   - port_security_enabled: port_security_enabled-request
   - project_id: project_id-request
   - security_groups: port-security_groups-request
   - tenant_id: project_id-request

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
   - created_at: created_at
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
   - mac_address: mac_address
   - name: name
   - network_id: network_id
   - port_security_enabled: port_security_enabled
   - project_id: project_id
   - revision_number: revision_number
   - security_groups: port-security_groups
   - status: port-status
   - tenant_id: project_id
   - updated_at: updated_at

Response Example
----------------

.. literalinclude:: samples/ports/ports-bulk-create-response.json
   :language: javascript
