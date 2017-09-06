.. -*- rst -*-
.. needs:method_verification
.. NOTE(amotoki): method_verification will be removed after sorting methods
   in the recommended order.

========
Networks
========

Lists, shows details for, creates, updates, and deletes networks.

provider extended attributes
============================

The ``provider`` extension allows administrative users to define a physical
binding of a logical network. This extension provides three additional
attributes: ``provider:network_type``, ``provider:physical_network`` and
``provider:segmentation_id``. The validation rules for these attributes
vary across ``provider:network_type``. For example, ``vlan`` and ``flat``
network types require ``provider:physical_network`` attribute, but ``vxlan``
network type does not.

Most Networking plug-ins (e.g. ML2 Plugin) and drivers do not support updating
any provider related attributes. Check your plug-in whether it supports
updating.

multiple provider extension
===========================

The ``multi-provider`` extension allows administrative users to define multiple
physical bindings for a logical network.

To define multiple physical bindings for a network, include a ``segments`` list
in the request body of network creation request.  Each element in the
``segments`` list has the same structure as the provider network
attributes. These attributes are ``provider:network_type``,
``provider:physical_network``, and ``provider:segmentation_id``. The same
validation rules are applied to each element in the ``segments`` list.

Note that you cannot use the provider extension and the multiple provider
extension for a single logical network.

VLAN transparency extension
===========================

The ``vlan-transparent`` extension enables plug-ins that support VLAN
transparency to deliver VLAN transparent trunk networks.
This extension introduces ``vlan_transparent`` attribute to control
a VLAN transparecy of the network. If the service does not support VLAN
transparency and a user requests a VLAN transparent network,
the plug-in refuses to create one and returns an appropriate error to the user.

MTU extensions
==============

The ``net-mtu`` extension allows plug-ins to expose the MTU that is guaranteed
to pass through the data path of the segments in the network. This extension
introduces a read-only ``mtu`` attribute.

A newer ``net-mtu-writable`` extension enhances ``net-mtu`` in that now the
``mtu`` attribute is available for write (both when creating as well as
updating networks).

DNS integration
===============

The ``dns-integration`` extension adds the ``dns_domain`` attribute to networks.
The ``dns_domain`` of a network in conjunction with the ``dns_name`` attribute
of its ports will be published in an external DNS service when Neutron is
configured to integrate with such a service.

Show network details
====================

.. rest_method::  GET /v2.0/networks/{network_id}

Shows details for a network.

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

   - network_id: network_id-path
   - fields: fields

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

Response Example
----------------

.. literalinclude:: samples/networks/network-show-response.json
   :language: javascript

Response Example (admin user; single segment mapping)
-----------------------------------------------------

.. literalinclude:: samples/networks/network-provider-show-response.json
   :language: javascript

Response Example (admin user; multiple segment mappings)
--------------------------------------------------------

.. literalinclude:: samples/networks/network-multi-show-response.json
   :language: javascript

Update network
==============

.. rest_method::  PUT /v2.0/networks/{network_id}

Updates a network.

Normal response codes: 200

Error response codes: 400, 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - network_id: network_id-path
   - network: network
   - admin_state_up: network-admin_state_up-request
   - dns_domain: dns_domain-request
   - mtu: mtu-request
   - name: network-name-request
   - port_security_enabled: network-port_security_enabled-request
   - provider:network_type: provider:network_type
   - provider:physical_network: provider:physical_network
   - provider:segmentation_id: provider:segmentation_id
   - qos_policy_id: qos_policy_id-request
   - router:external: router:external-request
   - segments: segments
   - shared: network-shared-request
   - description: description-request

Request Example
---------------

.. literalinclude:: samples/networks/network-update-request.json
   :language: javascript

Request Example (admin user; single segment mapping)
----------------------------------------------------

.. literalinclude:: samples/networks/network-provider-update-request.json
   :language: javascript

Request Example (admin user; multiple segment mappings)
-------------------------------------------------------

.. literalinclude:: samples/networks/network-multi-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - network: network
   - admin_state_up: network-admin_state_up
   - availability_zone_hints: availability_zone_hints
   - availability_zones: availability_zones
   - dns_domain: dns_domain
   - id: network-id
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
   - description: description

Response Example
----------------

This is an example when a regular user without administrative roles
sends a PUT request. Response examples for administrative users are
similar to responses of `Show network details <#show-network-details>`__
and `Create network <#create-network>`__. See them for details.

.. literalinclude:: samples/networks/network-update-response.json
   :language: javascript

Delete network
==============

.. rest_method::  DELETE /v2.0/networks/{network_id}

Deletes a network and its associated resources.

Normal response codes: 204

Error response codes: 401, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - network_id: network_id-path

Response
--------

There is no body content for the response of a successful DELETE request.

List networks
=============

.. rest_method::  GET /v2.0/networks

Lists networks to which the project has access.

Default policy settings return only networks that the project who submits the
request owns, unless an administrative user submits the request. In addition,
networks shared with the project who submits the request are also returned.

Use the ``fields`` query parameter to control which fields are
returned in the response body. Additionally, you can filter results
by using query string parameters. For information, see `Filtering
and Column Selection <https://wiki.openstack.org/wiki/Neutron/APIv2
-specification#Filtering_and_Column_Selection>`__.

.. TODO(amotoki): Add description on tag filtering to the general API overview.

You can also use the ``tags``, ``tags-any``, ``not-tags``, ``not-tags-any``
query parameter to filter the response with tags. For information,
see `REST API Impact <http://specs.openstack.org/openstack/neutron-
specs/specs/mitaka/add-tags-to-core-resources.html#rest-api-
impact>`__.

Normal response codes: 200

Error response codes: 401

Request
-------

.. rest_parameters:: parameters.yaml

   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - networks: networks
   - admin_state_up: network-admin_state_up
   - availability_zone_hints: availability_zone_hints
   - availability_zones: availability_zones
   - dns_domain: dns_domain
   - id: network-id
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
   - vlan_transparent: vlan_transparent
   - description: description

Response Example
----------------

.. literalinclude:: samples/networks/networks-list-response.json
   :language: javascript

Response Example (admin user)
-----------------------------

When Administrative users request to list networks,
physical segment information bound to the networks are also returned
in a response. In this example, a network ``net1`` is mapped to a single
network segment and a network ``net2`` is mapped to multiple network segments.

.. literalinclude:: samples/networks/networks-provider-list-response.json
   :language: javascript

Create network
==============

.. rest_method::  POST /v2.0/networks

Creates a network.

A request body is optional. An administrative user can specify
another project ID, which is the project that owns the network, in
the request body.

Normal response codes: 201

Error response codes: 400, 401

Request
-------

.. rest_parameters:: parameters.yaml

   - network: network
   - admin_state_up: network-admin_state_up-request
   - dns_domain: dns_domain-request
   - mtu: mtu-request
   - name: network-name-request
   - port_security_enabled: network-port_security_enabled-request
   - project_id: project_id-request
   - provider:network_type: provider:network_type-request
   - provider:physical_network: provider:physical_network-request
   - provider:segmentation_id: provider:segmentation_id-request
   - qos_policy_id: qos_policy_id-request
   - router:external: router:external-request
   - segments: segments-request
   - shared: network-shared-request
   - tenant_id: project_id-request
   - vlan_transparent: vlan_transparent-request
   - description: description-request

Request Example
---------------

.. literalinclude:: samples/networks/network-create-request.json
   :language: javascript

Request Example (admin user; single segment mapping)
----------------------------------------------------

.. literalinclude:: samples/networks/network-provider-create-request.json
   :language: javascript

Request Example (admin user; multiple segment mappings)
-------------------------------------------------------

.. literalinclude:: samples/networks/network-multi-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - network: network
   - admin_state_up: network-admin_state_up
   - availability_zone_hints: availability_zone_hints
   - availability_zones: availability_zones
   - dns_domain: dns_domain
   - id: network-id
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
   - vlan_transparent: vlan_transparent
   - description: description

Response Example
----------------

.. literalinclude:: samples/networks/network-create-response.json
   :language: javascript

Response Example (admin user; single segment mapping)
-----------------------------------------------------

.. literalinclude:: samples/networks/network-provider-create-response.json
   :language: javascript

Response Example (admin user; multiple segment mappings)
--------------------------------------------------------

.. literalinclude:: samples/networks/network-multi-create-response.json
   :language: javascript

Bulk create networks
====================

.. rest_method::  POST /v2.0/networks

Creates multiple networks in a single request.

In the request body, specify a list of networks.

The bulk create operation is always atomic. Either all or no
networks in the request body are created.

Normal response codes: 201

Error response codes: 400, 401

Request
-------

.. rest_parameters:: parameters.yaml

   - networks: networks
   - admin_state_up: network-admin_state_up-request
   - dns_domain: dns_domain-request
   - mtu: mtu-request
   - name: network-name-request
   - port_security_enabled: network-port_security_enabled-request
   - project_id: project_id-request
   - provider:network_type: provider:network_type-request
   - provider:physical_network: provider:physical_network-request
   - provider:segmentation_id: provider:segmentation_id-request
   - qos_policy_id: qos_policy_id-request
   - router:external: router:external-request
   - segments: segments-request
   - shared: network-shared-request
   - tenant_id: project_id-request
   - vlan_transparent: vlan_transparent-request
   - description: description-request

Request Example
---------------

.. literalinclude:: samples/networks/networks-bulk-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - networks: networks
   - admin_state_up: network-admin_state_up
   - availability_zone_hints: availability_zone_hints
   - availability_zones: availability_zones
   - dns_domain: dns_domain
   - id: network-id
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
   - vlan_transparent: vlan_transparent
   - description: description

Response Example
----------------

.. literalinclude:: samples/networks/networks-bulk-create-response.json
   :language: javascript
