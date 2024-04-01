.. -*- rst -*-

==================================================================================================
VPNaaS 2.0 (vpn, vpnservices, ikepolicies, ipsecpolicies, endpoint-groups, ipsec-site-connections)
==================================================================================================

The Virtual-Private-Network-as-a-Service (VPNaaS) extension enables
OpenStack projects to extend private networks across the public
telecommunication infrastructure.

This initial implementation of the VPNaaS extension provides:

- Site-to-site VPN that connects two private networks.

- Multiple VPN connections per project.

- IKEv1 policy support with 3des, aes-128, aes-256, or aes-192
  encryption.

- IPsec policy support with 3des, aes-128, aes-192, or aes-256
  encryption, sha1 authentication, ESP, AH, or AH-ESP transform
  protocol, and tunnel or transport mode encapsulation.

- Dead Peer Detection (DPD) with hold, clear, restart, disabled, or
  restart-by-peer actions.

This extension introduces these resources:

- ``service``. A parent object that associates VPN with a specific
  subnet and router.

- ``ikepolicy``. The Internet Key Exchange (IKE) policy that
  identifies the authentication and encryption algorithm to use
  during phase one and two negotiation of a VPN connection.

- ``ipsecpolicy``. The IP security policy that specifies the
  authentication and encryption algorithm and encapsulation mode to
  use for the established VPN connection.

- ``ipsec-site-connection``. Details for the site-to-site IPsec
  connection, including the peer CIDRs, MTU, authentication mode,
  peer address, DPD settings, and status.

VPN Endpoint Groups
===================

The ``endpoint-groups`` extension adds support for defining one or more
endpoints of a specific type, and can be used to specify both local
and peer endpoints for IPsec connections.

VPN Flavors
===========

The ``vpn-flavors`` extension adds the ``flavor_id`` attribute
to ``vpnservices`` resources. During vpnservice creation, if a ``flavor_id``
is passed, it is used to find the provider for the driver which would
handle the newly created vpnservice.

List IKE policies
=================

.. rest_method::  GET /v2.0/vpn/ikepolicies

Lists IKE policies.

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: 401, 403

Request
-------

.. rest_parameters:: parameters.yaml

   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - ikepolicies: ikepolicies
   - name: name-request
   - description: description-request
   - tenant_id: project_id
   - project_id: project_id
   - auth_algorithm: auth_algorithm
   - encryption_algorithm: encryption_algorithm
   - pfs: pfs
   - value: value
   - phase1_negotiation_mode: phase1_negotiation_mode
   - units: units
   - lifetime: lifetime
   - id: ikepolicy_id-body-response
   - ike_version: ike_version

Response Example
----------------

.. literalinclude:: samples/vpn/ikepolicies-list-response.json
   :language: javascript

Create IKE policy
=================

.. rest_method::  POST /v2.0/vpn/ikepolicies

Creates an IKE policy.

The IKE policy is used for phases one and two negotiation of the
VPN connection. You can specify both the authentication and
encryption algorithms for connections.

Normal response codes: 201

Error response codes: 400, 401

Request
-------

.. rest_parameters:: parameters.yaml

   - ikepolicy: ikepolicy
   - name: name-request
   - description: description-request
   - tenant_id: project_id
   - project_id: project_id
   - auth_algorithm: auth_algorithm
   - encryption_algorithm: encryption_algorithm
   - pfs: pfs
   - value: value
   - phase1_negotiation_mode: phase1_negotiation_mode
   - units: units
   - lifetime: lifetime
   - ike_version: ike_version

Request Example
---------------

.. literalinclude:: samples/vpn/ikepolicy-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - ikepolicies: ikepolicies
   - ikepolicy: ikepolicy
   - name: name-request
   - description: description-request
   - tenant_id: project_id
   - project_id: project_id
   - auth_algorithm: auth_algorithm
   - encryption_algorithm: encryption_algorithm
   - pfs: pfs
   - value: value
   - phase1_negotiation_mode: phase1_negotiation_mode
   - units: units
   - lifetime: lifetime
   - id: ikepolicy_id-body-response
   - ike_version: ike_version

Response Example
----------------

.. literalinclude:: samples/vpn/ikepolicy-create-response.json
   :language: javascript

Show IKE policy details
=======================

.. rest_method::  GET /v2.0/vpn/ikepolicies/{ikepolicy_id}

Shows details for an IKE policy.

.. include:: filtering-show.inc

Normal response codes: 200

Error response codes: 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - ikepolicy_id: ikepolicy_id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - ikepolicies: ikepolicies
   - ikepolicy: ikepolicy
   - name: name-request
   - description: description-request
   - tenant_id: project_id
   - project_id: project_id
   - auth_algorithm: auth_algorithm
   - encryption_algorithm: encryption_algorithm
   - pfs: pfs
   - value: value
   - phase1_negotiation_mode: phase1_negotiation_mode
   - units: units
   - lifetime: lifetime
   - id: ikepolicy_id-body-response
   - ike_version: ike_version

Response Example
----------------

.. literalinclude:: samples/vpn/ikepolicy-show-response.json
   :language: javascript

Update IKE policy
=================

.. rest_method::  PUT /v2.0/vpn/ikepolicies/{ikepolicy_id}

Updates policy settings in an IKE policy.

Normal response codes: 200

Error response codes: 400, 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - ikepolicy_id: ikepolicy_id-path
   - ikepolicy: ikepolicy
   - description: description-request
   - auth_algorithm: auth_algorithm
   - name: name-request
   - encryption_algorithm: encryption_algorithm
   - pfs: pfs
   - value: value
   - phase1_negotiation_mode: phase1_negotiation_mode
   - units: units
   - lifetime: lifetime
   - ike_version: ike_version

Request Example
---------------

.. literalinclude:: samples/vpn/ikepolicy-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - ikepolicies: ikepolicies
   - ikepolicy: ikepolicy
   - description: description-request
   - tenant_id: project_id
   - project_id: project_id
   - auth_algorithm: auth_algorithm
   - name: name-request
   - encryption_algorithm: encryption_algorithm
   - pfs: pfs
   - value: value
   - phase1_negotiation_mode: phase1_negotiation_mode
   - units: units
   - lifetime: lifetime
   - id: ikepolicy_id-body-response
   - ike_version: ike_version

Response Example
----------------

.. literalinclude:: samples/vpn/ikepolicy-update-response.json
   :language: javascript

Remove IKE policy
=================

.. rest_method::  DELETE /v2.0/vpn/ikepolicies/{ikepolicy_id}

Removes an IKE policy.

Normal response codes: 204

Error response codes: 401, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - ikepolicy_id: ikepolicy_id-path

Response
--------

There is no body content for the response of a successful DELETE request.

List IPsec policies
===================

.. rest_method::  GET /v2.0/vpn/ipsecpolicies

Lists all IPsec policies.

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: 401, 403

Request
-------

.. rest_parameters:: parameters.yaml

   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - ipsecpolicies: ipsecpolicies
   - description: description-request
   - tenant_id: project_id
   - project_id: project_id
   - auth_algorithm: auth_algorithm
   - encapsulation_mode: encapsulation_mode
   - encryption_algorithm: encryption_algorithm
   - pfs: pfs
   - value: value
   - transform_protocol: transform_protocol
   - units: units
   - lifetime: lifetime
   - id: ipsecpolicy_id-body-response
   - name: name-request

Response Example
----------------

.. literalinclude:: samples/vpn/ipsecpolicies-list-response.json
   :language: javascript

Create IPsec policy
===================

.. rest_method::  POST /v2.0/vpn/ipsecpolicies

Creates an IP security (IPsec) policy.

The IPsec policy specifies the authentication and encryption
algorithms and encapsulation mode to use for the established VPN
connection.

Normal response codes: 201

Error response codes: 400, 401

Request
-------

.. rest_parameters:: parameters.yaml

   - ipsecpolicy: ipsecpolicy
   - description: description-request
   - tenant_id: project_id
   - project_id: project_id
   - auth_algorithm: auth_algorithm
   - encapsulation_mode: encapsulation_mode
   - encryption_algorithm: encryption_algorithm
   - pfs: pfs
   - value: value
   - transform_protocol: transform_protocol
   - units: units
   - lifetime: lifetime
   - name: name-request

Request Example
---------------

.. literalinclude:: samples/vpn/ipsecpolicy-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - ipsecpolicies: ipsecpolicies
   - ipsecpolicy: ipsecpolicy
   - description: description-request
   - tenant_id: project_id
   - project_id: project_id
   - auth_algorithm: auth_algorithm
   - encapsulation_mode: encapsulation_mode
   - encryption_algorithm: encryption_algorithm
   - pfs: pfs
   - value: value
   - transform_protocol: transform_protocol
   - units: units
   - lifetime: lifetime
   - id: ipsecpolicy_id-body-response
   - name: name-request

Response Example
----------------

.. literalinclude:: samples/vpn/ipsecpolicy-create-response.json
   :language: javascript

Show IPsec policy
=================

.. rest_method::  GET /v2.0/vpn/ipsecpolicies/{ipsecpolicy_id}

Shows details for an IPsec policy.

.. include:: filtering-show.inc

Normal response codes: 200

Error response codes: 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - ipsecpolicy_id: ipsecpolicy_id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - ipsecpolicies: ipsecpolicies
   - ipsecpolicy: ipsecpolicy
   - description: description-request
   - tenant_id: project_id
   - project_id: project_id
   - auth_algorithm: auth_algorithm
   - encapsulation_mode: encapsulation_mode
   - encryption_algorithm: encryption_algorithm
   - pfs: pfs
   - value: value
   - transform_protocol: transform_protocol
   - units: units
   - lifetime: lifetime
   - id: ipsecpolicy_id-body-response
   - name: name-request

Response Example
----------------

.. literalinclude:: samples/vpn/ipsecpolicy-show-response.json
   :language: javascript

Update IPsec policy
===================

.. rest_method::  PUT /v2.0/vpn/ipsecpolicies/{ipsecpolicy_id}

Updates policy settings in an IPsec policy.

Normal response codes: 200

Error response codes: 400, 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - ipsecpolicy_id: ipsecpolicy_id-path
   - ipsecpolicy: ipsecpolicy
   - description: description-request
   - transform_protocol: transform_protocol
   - auth_algorithm: auth_algorithm
   - encapsulation_mode: encapsulation_mode
   - encryption_algorithm: encryption_algorithm
   - pfs: pfs
   - value: value
   - units: units
   - lifetime: lifetime
   - name: name-request

Request Example
---------------

.. literalinclude:: samples/vpn/ipsecpolicy-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - ipsecpolicies: ipsecpolicies
   - ipsecpolicy: ipsecpolicy
   - description: description-request
   - tenant_id: project_id
   - project_id: project_id
   - auth_algorithm: auth_algorithm
   - encapsulation_mode: encapsulation_mode
   - encryption_algorithm: encryption_algorithm
   - pfs: pfs
   - value: value
   - transform_protocol: transform_protocol
   - units: units
   - lifetime: lifetime
   - id: ipsecpolicy_id-body-response
   - name: name-request

Response Example
----------------

.. literalinclude:: samples/vpn/ipsecpolicy-update-response.json
   :language: javascript

Remove IPsec policy
===================

.. rest_method::  DELETE /v2.0/vpn/ipsecpolicies/{ipsecpolicy_id}

Removes an IPsec policy.

Normal response codes: 204

Error response codes: 401, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - ipsecpolicy_id: ipsecpolicy_id-path

Response
--------

There is no body content for the response of a successful DELETE request.

List IPsec connections
======================

.. rest_method::  GET /v2.0/vpn/ipsec-site-connections

Lists all IPsec connections.

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: 401, 403

Request
-------

.. rest_parameters:: parameters.yaml

   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - auth_mode: auth_mode
   - ikepolicy_id: ikepolicy_id-body-response
   - vpnservice_id: vpnservice_id-body-response
   - local_ep_group_id: local_ep_group_id
   - peer_address: peer_address
   - id: connection_id-body-response
   - route_mode: route_mode
   - ipsecpolicy_id: ipsecpolicy_id-body-response
   - peer_id: peer_id
   - status: ipsec_site_connection-status
   - psk: psk
   - description: description-request
   - initiator: initiator
   - peer_cidrs: peer_cidrs
   - name: name-request
   - admin_state_up: admin_state_up
   - tenant_id: project_id
   - project_id: project_id
   - interval: interval
   - mtu: mtu
   - peer_ep_group_id: peer_ep_group_id
   - dpd: dpd
   - timeout: ipsec_site_connection-timeout
   - action: ipsec_site_connection-action
   - local_id: local_id

Response Example
----------------

.. literalinclude:: samples/vpn/ipsec-site-connections-list-response.json
   :language: javascript

Create IPsec connection
=======================

.. rest_method::  POST /v2.0/vpn/ipsec-site-connections

Creates a site-to-site IPsec connection for a service.

Normal response codes: 201

Error response codes: 400, 401

Request
-------

.. rest_parameters:: parameters.yaml

   - ipsec_site_connection: ipsec_site_connection
   - auth_mode: auth_mode
   - ikepolicy_id: ikepolicy_id-body-request
   - vpnservice_id: vpnservice_id-body-request
   - local_ep_group_id: local_ep_group_id
   - peer_address: peer_address
   - route_mode: route_mode
   - ipsecpolicy_id: ipsecpolicy_id-body-request
   - peer_id: peer_id
   - psk: psk
   - description: description-request
   - initiator: initiator
   - peer_cidrs: peer_cidrs
   - name: name-request
   - admin_state_up: admin_state_up
   - tenant_id: project_id
   - project_id: project_id
   - interval: interval
   - mtu: mtu
   - peer_ep_group_id: peer_ep_group_id
   - dpd: dpd
   - timeout: ipsec_site_connection-timeout
   - action: ipsec_site_connection-action
   - local_id: local_id

Request Example
---------------

.. literalinclude:: samples/vpn/ipsec-site-connection-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - ipsec_site_connection: ipsec_site_connection
   - auth_mode: auth_mode
   - ikepolicy_id: ikepolicy_id-body-response
   - vpnservice_id: vpnservice_id-body-response
   - local_ep_group_id: local_ep_group_id
   - peer_address: peer_address
   - id: connection_id-body-response
   - route_mode: route_mode
   - ipsecpolicy_id: ipsecpolicy_id-body-response
   - peer_id: peer_id
   - status: ipsec_site_connection-status
   - psk: psk
   - description: description-request
   - initiator: initiator
   - peer_cidrs: peer_cidrs
   - name: name-request
   - admin_state_up: admin_state_up
   - tenant_id: project_id
   - project_id: project_id
   - interval: interval
   - mtu: mtu
   - peer_ep_group_id: peer_ep_group_id
   - dpd: dpd
   - timeout: ipsec_site_connection-timeout
   - action: ipsec_site_connection-action
   - local_id: local_id

Response Example
----------------

.. literalinclude:: samples/vpn/ipsec-site-connection-create-response.json
   :language: javascript

Show IPsec connection
=====================

.. rest_method::  GET /v2.0/vpn/ipsec-site-connections/{connection_id}

Shows details for an IPsec connection.

.. include:: filtering-show.inc

Normal response codes: 200

Error response codes: 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - connection_id: connection_id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - auth_mode: auth_mode
   - ikepolicy_id: ikepolicy_id-body-response
   - vpnservice_id: vpnservice_id-body-response
   - local_ep_group_id: local_ep_group_id
   - peer_address: peer_address
   - id: connection_id-body-response
   - ipsec_site_connection: ipsec_site_connection
   - route_mode: route_mode
   - ipsecpolicy_id: ipsecpolicy_id-body-response
   - peer_id: peer_id
   - status: ipsec_site_connection-status
   - psk: psk
   - description: description-request
   - initiator: initiator
   - peer_cidrs: peer_cidrs
   - name: name-request
   - admin_state_up: admin_state_up
   - tenant_id: project_id
   - project_id: project_id
   - interval: interval
   - mtu: mtu
   - peer_ep_group_id: peer_ep_group_id
   - dpd: dpd
   - timeout: ipsec_site_connection-timeout
   - action: ipsec_site_connection-action
   - local_id: local_id

Response Example
----------------

.. literalinclude:: samples/vpn/ipsec-site-connection-show-response.json
   :language: javascript

Update IPsec connection
=======================

.. rest_method::  PUT /v2.0/vpn/ipsec-site-connections/{connection_id}

Updates connection settings for an IPsec connection.

Normal response codes: 200

Error response codes: 400, 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - connection_id: connection_id-path
   - ipsec_site_connection: ipsec_site_connection
   - psk: psk
   - initiator: initiator
   - description: description-request
   - admin_state_up: admin_state_up
   - interval: interval
   - peer_cidrs: peer_cidrs
   - mtu: mtu
   - peer_ep_group_id: peer_ep_group_id
   - local_ep_group_id: local_ep_group_id
   - dpd: dpd
   - timeout: ipsec_site_connection-timeout
   - action: ipsec_site_connection-action
   - peer_address: peer_address
   - peer_id: peer_id
   - name: name-request
   - local_id: local_id

Request Example
---------------

.. literalinclude:: samples/vpn/ipsec-site-connection-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - auth_mode: auth_mode
   - ikepolicy_id: ikepolicy_id-body-response
   - vpnservice_id: vpnservice_id-body-response
   - local_ep_group_id: local_ep_group_id
   - peer_address: peer_address
   - id: connection_id-body-response
   - ipsec_site_connection: ipsec_site_connection
   - route_mode: route_mode
   - ipsecpolicy_id: ipsecpolicy_id-body-response
   - peer_id: peer_id
   - status: ipsec_site_connection-status
   - psk: psk
   - description: description-request
   - initiator: initiator
   - peer_cidrs: peer_cidrs
   - name: name-request
   - admin_state_up: admin_state_up
   - tenant_id: project_id
   - project_id: project_id
   - interval: interval
   - mtu: mtu
   - peer_ep_group_id: peer_ep_group_id
   - dpd: dpd
   - timeout: ipsec_site_connection-timeout
   - action: ipsec_site_connection-action
   - local_id: local_id

Response Example
----------------

.. literalinclude:: samples/vpn/ipsec-site-connection-update-response.json
   :language: javascript

Remove IPsec connection
=======================

.. rest_method::  DELETE /v2.0/vpn/ipsec-site-connections/{connection_id}

Removes an IPsec connection.

Normal response codes: 204

Error response codes: 401, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - connection_id: connection_id-path

Response
--------

There is no body content for the response of a successful DELETE request.

List VPN endpoint groups
========================

.. rest_method::  GET /v2.0/vpn/endpoint-groups

Lists VPN endpoint groups.

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: 401, 403

Request
-------

.. rest_parameters:: parameters.yaml

   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - endpoints: endpoints
   - name: name-request
   - description: description-request
   - tenant_id: project_id
   - project_id: project_id
   - type: vpn_endpoint_type
   - id: endpoint_group_id-body-response

Response Example
----------------

.. literalinclude:: samples/vpn/vpn-endpoint-groups-list-response.json
   :language: javascript

Create VPN endpoint group
=========================

.. rest_method::  POST /v2.0/vpn/endpoint-groups

Creates a VPN endpoint group.

The endpoint group contains one or more endpoints of a specific
type that you can use to create a VPN connections.

Normal response codes: 201

Error response codes: 400, 401

Request
-------

.. rest_parameters:: parameters.yaml

   - tenant_id: project_id
   - project_id: project_id
   - endpoints: endpoints
   - type: vpn_endpoint_type
   - description: description-request
   - name: name-request

Request Example
---------------

.. literalinclude:: samples/vpn/vpn-endpoint-group-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - endpoints: endpoints
   - description: description-request
   - tenant_id: project_id
   - project_id: project_id
   - type: vpn_endpoint_type
   - id: endpoint_group_id-body-response
   - name: name-request

Response Example
----------------

.. literalinclude:: samples/vpn/vpn-endpoint-group-create-response.json
   :language: javascript

Show VPN endpoint group
=======================

.. rest_method::  GET /v2.0/vpn/endpoint-groups/{endpoint_group_id}

Shows details for a VPN endpoint group.

.. include:: filtering-show.inc

Normal response codes: 200

Error response codes: 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - endpoint_group_id: endpoint_group_id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - endpoints: endpoints
   - description: description-request
   - tenant_id: project_id
   - project_id: project_id
   - type: vpn_endpoint_type
   - id: endpoint_group_id-body-response
   - name: name-request

Response Example
----------------

.. literalinclude:: samples/vpn/vpn-endpoint-group-show-response.json
   :language: javascript

Update VPN endpoint group
=========================

.. rest_method::  PUT /v2.0/vpn/endpoint-groups/{endpoint_group_id}

Updates settings for a VPN endpoint group.

Normal response codes: 200

Error response codes: 400, 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - description: description-request
   - name: name-request
   - endpoint_group_id: endpoint_group_id-path

Request Example
---------------

.. literalinclude:: samples/vpn/vpn-endpoint-group-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - endpoints: endpoints
   - description: description-request
   - tenant_id: project_id
   - project_id: project_id
   - type: vpn_endpoint_type
   - id: endpoint_group_id-body-response
   - name: name-request

Response Example
----------------

.. literalinclude:: samples/vpn/vpn-endpoint-group-update-response.json
   :language: javascript

Remove VPN endpoint group
=========================

.. rest_method::  DELETE /v2.0/vpn/endpoint-groups/{endpoint_group_id}

Removes a VPN endpoint group.

Normal response codes: 204

Error response codes: 401, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - endpoint_group_id: endpoint_group_id-path

Response
--------

There is no body content for the response of a successful DELETE request.

List VPN services
=================

.. rest_method::  GET /v2.0/vpn/vpnservices

Lists all VPN services.

The list might be empty.

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: 401, 403

Request
-------

.. rest_parameters:: parameters.yaml

   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - vpnservices: vpnservices
   - router_id: router_id
   - status: vpnservice-status
   - name: name-request
   - external_v6_ip: external_v6_ip
   - admin_state_up: admin_state_up
   - subnet_id: subnet_id
   - tenant_id: project_id
   - project_id: project_id
   - external_v4_ip: external_v4_ip
   - id: vpnservice_id-body-response
   - description: description-request
   - flavor_id: flavor-id-response

Response Example
----------------

.. literalinclude:: samples/vpn/vpnservices-list-response.json
   :language: javascript

Create VPN service
==================

.. rest_method::  POST /v2.0/vpn/vpnservices

Creates a VPN service.

The service is associated with a router. After you create the
service, it can contain multiple VPN connections.

An optional ``flavor_id`` attribute can be passed to enable dynamic
selection of an appropriate provider if configured by the operator.
It is only available when ``vpn-flavors`` extension is enabled.
The basic selection algorithm chooses the provider in the first
service profile currently associated with flavor. This option can
only be set in ``POST`` operation.

Normal response codes: 201

Error response codes: 400, 401

Request
-------

.. rest_parameters:: parameters.yaml

   - vpnservice: vpnservice
   - router_id: router_id
   - description: description-request
   - admin_state_up: admin_state_up
   - subnet_id: subnet_id
   - tenant_id: project_id
   - project_id: project_id
   - name: name-request
   - flavor_id: flavor-id-request

Request Example
---------------

.. literalinclude:: samples/vpn/vpnservice-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - vpnservice: vpnservice
   - router_id: router_id
   - status: vpnservice-status
   - name: name-request
   - external_v6_ip: external_v6_ip
   - admin_state_up: admin_state_up
   - subnet_id: subnet_id
   - tenant_id: project_id
   - project_id: project_id
   - external_v4_ip: external_v4_ip
   - id: vpnservice_id-body-response
   - description: description-request
   - flavor_id: flavor-id-response

Response Example
----------------

.. literalinclude:: samples/vpn/vpnservice-create-response.json
   :language: javascript

Show VPN service details
========================

.. rest_method::  GET /v2.0/vpn/vpnservices/{service_id}

Shows details for a VPN service.

If the user is not an administrative user and the VPN service
object does not belong to the tenant account for the user, the
operation returns the ``Forbidden (403)`` response code.

.. include:: filtering-show.inc

Normal response codes: 200

Error response codes: 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - service_id: vpnservice_id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - vpnservice: vpnservice
   - router_id: router_id
   - status: vpnservice-status
   - name: name-request
   - external_v6_ip: external_v6_ip
   - admin_state_up: admin_state_up
   - subnet_id: subnet_id
   - tenant_id: project_id
   - project_id: project_id
   - external_v4_ip: external_v4_ip
   - id: vpnservice_id-body-response
   - description: description-request
   - flavor_id: flavor-id-response

Response Example
----------------

.. literalinclude:: samples/vpn/vpnservice-show-response.json
   :language: javascript

Update VPN service
==================

.. rest_method::  PUT /v2.0/vpn/vpnservices/{service_id}

Updates a VPN service.

Updates the attributes of a VPN service. You cannot update a
service with a ``PENDING_*`` status.

Normal response codes: 200

Error response codes: 400, 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - vpnservice: vpnservice
   - description: description-request
   - name: name-request
   - admin_state_up: admin_state_up
   - service_id: vpnservice_id-path

Request Example
---------------

.. literalinclude:: samples/vpn/vpnservice-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - vpnservice: vpnservice
   - router_id: router_id
   - status: vpnservice-status
   - name: name-request
   - external_v6_ip: external_v6_ip
   - admin_state_up: admin_state_up
   - subnet_id: subnet_id
   - tenant_id: project_id
   - project_id: project_id
   - external_v4_ip: external_v4_ip
   - id: vpnservice_id-body-response
   - description: description-request
   - flavor_id: flavor-id-response

Response Example
----------------

.. literalinclude:: samples/vpn/vpnservice-update-response.json
   :language: javascript

Remove VPN service
==================

.. rest_method::  DELETE /v2.0/vpn/vpnservices/{service_id}

Removes a VPN service.

If the service has connections, the request is rejected.

Normal response codes: 204

Error response codes: 401, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - service_id: vpnservice_id-path

Response
--------

There is no body content for the response of a successful DELETE request.
