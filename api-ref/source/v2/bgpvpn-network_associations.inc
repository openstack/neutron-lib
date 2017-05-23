====================
Network Associations
====================

Associating a BGPVPN to a Network can be done for both BGPVPN of type L2 and of
type L3. For type L3, the semantic is that all Subnets bound to the Network
will be interconnected with the BGP VPN (and thus between themselves).

A given Network can be associated with multiple BGPVPNs.

Associating or disassociating a BGPVPN to a Network is done by manipulating a
Network association API resource as a sub-resource of the BGPVPN resource:

List Network Associations
=========================

.. rest_method::  GET /v2.0/bgpvpn/bgpvpns/{bgpvpn_id}/network_associations

Lists network associations for a given BGP VPN.

Use the ``fields`` query parameter to control which fields are
returned in the response body. Additionally, you can filter results
by using query string parameters. For information, see `Filtering
and Column Selection <https://wiki.openstack.org/wiki/Neutron/APIv2
-specification#Filtering_and_Column_Selection>`__.

Normal response codes: 200

Error response codes: 400, 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - bgpvpn_id: bgpvpn-id-path
   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - network_associations: bgpvpn-network_associations
   - id: bgpvpn-network_association_id
   - network_id: bgpvpn-network_id
   - tenant_id: project_id
   - project_id: project_id

Response Example
----------------

.. literalinclude:: samples/bgpvpn/network_associations/network_association-list-response.json
   :language: javascript

Create Network Association
==========================

.. rest_method::  POST /v2.0/bgpvpn/bgpvpns/{bgpvpn_id}/network_associations

Creates a network association for a given BGP VPN

Normal response codes: 201

Error response codes: 400, 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - bgpvpn_id: bgpvpn-id-path
   - network_association: bgpvpn-network_association
   - network_id: bgpvpn-network_id

Request Example
---------------

.. literalinclude:: samples/bgpvpn/network_associations/network_association-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - network_association: bgpvpn-network_association
   - id: bgpvpn-network_association_id
   - network_id: bgpvpn-network_id
   - tenant_id: project_id
   - project_id: project_id

Response Example
----------------

.. literalinclude:: samples/bgpvpn/network_associations/network_association-create-response.json
   :language: javascript

Show Network Association details
================================

.. rest_method::  GET /v2.0/bgpvpn/bgpvpns/{bgpvpn_id}/network_associations/{network_association_id}

Shows details for a network association.

Normal response codes: 200

Error response codes: 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - bgpvpn_id: bgpvpn-id-path
   - network_association_id: bgpvpn-network_association_id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - network_association: bgpvpn-network_association
   - id: bgpvpn-network_association_id
   - network_id: bgpvpn-network_id
   - tenant_id: project_id
   - project_id: project_id

Response Example
----------------

.. literalinclude:: samples/bgpvpn/network_associations/network_association-show-response.json
   :language: javascript

Delete Network Association
==========================

.. rest_method::  DELETE /v2.0/bgpvpn/bgpvpns/{bgpvpn_id}/network_associations/{network_association_id}

Deletes a network association.

Normal response codes: 204

Error response codes: 400, 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - bgpvpn_id: bgpvpn-id-path
   - network_association_id: bgpvpn-network_association_id-path

Response
--------

There is no body content for the response of a successful DELETE request.
