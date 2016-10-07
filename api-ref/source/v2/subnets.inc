.. -*- rst -*-
.. needs:method_verification
.. needs:parameter_verification
.. needs:example_verification
.. needs:body_verification

=======
Subnets
=======

Lists, shows details for, creates, updates, and deletes subnet
resources.

List subnets
============

.. rest_method::  GET /v2.0/subnets

Lists subnets that the project has access to.

Default policy settings return only subnets owned by the
project of the user submitting the request, unless the
user has administrative role. You can control which attributes
are returned by using the fields query parameter. You can filter
results by using query string parameters.

Normal response codes: 200

Error response codes: 401

Request
-------

Response Example
----------------

.. literalinclude:: samples/subnets/subnets-list-response.json
   :language: javascript

Create subnet
=============

.. rest_method::  POST /v2.0/subnets

Creates a subnet on a network.

OpenStack Networking does not try to derive the correct IP version
from the CIDR. If you do not specify the ``gateway_ip`` attribute,
OpenStack Networking allocates an address from the CIDR for the
gateway for the subnet.

To specify a subnet without a gateway, set the ``gateway_ip``
attribute to ``null`` in the request body. If you do not specify
the ``allocation_pools`` attribute, OpenStack Networking
automatically allocates pools for covering all IP addresses in the
CIDR, excluding the address reserved for the subnet gateway.
Otherwise, you can explicitly specify allocation pools as shown in
the following example.

When you specify both the ``allocation_pools`` and ``gateway_ip``
attributes, you must ensure that the gateway IP does not overlap
with the allocation pools; otherwise, the call returns the
``Conflict (409)`` response code.

A subnet can have one or more name servers and host routes. Hosts
in this subnet use the name servers. Devices with IP addresses from
this subnet, not including the local subnet route, use the host
routes.

Specify the ``ipv6_ra_mode`` and ``ipv6_address_mode`` attributes
to create subnets that support IPv6 configurations, such as
stateless address autoconfiguration (SLAAC), DHCPv6 stateful, and
DHCPv6 stateless configurations.

A subnet can optionally be associated with a network segment when
it is created by specifying the ``segment_id`` of a valid segment
on the specified network. A network with subnets associated in this
way is called a routed network. On any given network, all of the
subnets must be associated with segments or none of them can be.
Neutron enforces this invariant. Currently, routed networks are
only supported for provider networks.

Error response codes: 201,404,403,401,400,409

Request
-------

.. .. rest_parameters:: parameters.yaml

Request Example
---------------

.. literalinclude:: samples/subnets/subnet-create-request.json
   :language: javascript

Bulk create subnet
==================

.. rest_method::  POST /v2.0/subnets

Creates multiple subnets in a single request. Specify a list of subnets in the request body.

The bulk create operation is always atomic. Either all or no
subnets in the request body are created.

Error response codes: 201,404,403,401,400,409

Request
-------

.. .. rest_parameters:: parameters.yaml

Request Example
---------------

.. literalinclude:: samples/subnets/subnets-create-bulk-request.json
   :language: javascript

Show subnet details
===================

.. rest_method::  GET /v2.0/subnets/{subnet_id}

Shows details for a subnet.

Use the fields query parameter to filter the results.

Normal response codes: 200

Error response codes: 404,401

Request
-------

.. rest_parameters:: parameters.yaml

   - subnet_id: subnet_id

Response Example
----------------

.. literalinclude:: samples/subnets/subnet-show-response.json
   :language: javascript

Update subnet
=============

.. rest_method::  PUT /v2.0/subnets/{subnet_id}

Updates a subnet.

Some attributes, such as IP version (ip_version), CIDR (cidr), and
segment (segment_id) cannot be updated. Attempting to update these
attributes results in a ``400 Bad Request`` error.

Normal response codes: 200

Error response codes: 404,403,401,400

Request
-------

.. rest_parameters:: parameters.yaml

   - subnet_id: subnet_id

Request Example
---------------

.. literalinclude:: samples/subnets/subnet-update-request.json
   :language: javascript

Response Example
----------------

.. literalinclude:: samples/subnets/subnet-update-response.json
   :language: javascript

Delete subnet
=============

.. rest_method::  DELETE /v2.0/subnets/{subnet_id}

Deletes a subnet.

The operation fails if subnet IP addresses are still allocated.

Error response codes: 409,404,204,401

Request
-------

.. rest_parameters:: parameters.yaml

   - subnet_id: subnet_id

