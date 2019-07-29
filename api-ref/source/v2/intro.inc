.. -*- rst -*-
.. needs:method_verification
.. needs:parameter_verification
.. needs:example_verification
.. needs:body_verification

=========
API guide
=========

This section introduces readers to OpenStack Networking (v2) API, provides
guidelines on how to use it, and describes common features available to users
throughout all Networking APIs.

General information
===================

The Networking API v2.0 is a RESTful HTTP service that uses all aspects of the
HTTP protocol including methods, URIs, media types, response codes, and so on.
Providers can use existing features of the protocol including caching,
persistent connections, and content compression. For example, providers who
employ a caching layer can respond with a ``203`` code instead of a ``200`` code
when a request is served from the cache.  Additionally, providers can offer support
for conditional ``GET`` requests by using ETags, or they may send a redirect in
response to a ``GET`` request. Create clients so that these differences are
accounted for.

Authentication and authorization
================================

The Networking API v2.0 uses the `OpenStack Identity service
<https://docs.openstack.org/keystone/latest/>`_ as the default authentication
service. When Keystone is enabled, users that submit requests to the OpenStack
Networking service must provide an authentication token in ``X-Auth-Token``
request header. You obtain the token by authenticating to the Keystone
endpoint.

When Keystone is enabled, the ``project_id`` attribute is not required in create
requests because the project ID is derived from the authentication token.

NOTE: Currently the Networking API accepts the deprecated ``tenant_id``
attribute for the project ID for backward compatibility.

The default authorization settings allow only administrative users to create
resources on behalf of a different project.

OpenStack Networking uses information received from Keystone to authorize user
requests. OpenStack Networking handles the following types of authorization
policies:

-  **Operation-based policies** specify access criteria for specific
   operations, possibly with fine-grained control over specific attributes.

-  **Resource-based policies** access a specific resource. Permissions might or
   might not be granted depending on the permissions configured for the
   resource.  Currently available for only the network resource.

The actual authorization policies enforced in OpenStack Networking might vary
from deployment to deployment.

Request and response formats
============================

The Networking API v2.0 supports JSON data serialization request and response
formats only.

Request format
--------------

The Networking API v2.0 only accepts requests with the JSON data serialization
format. The ``Content-Type`` header is ignored.

Tenant and project attributes in requests
-----------------------------------------

Starting with the Newton release of the Networking service, the Networking API
accepts the ``project_id`` attribute in addition to the ``tenant_id`` attribute
in requests. The ``tenant_id`` attribute is accepted for backward compatibility.
If both the ``project_id`` and the ``tenant_id`` attribute are provided in the
same request, their values must be identical.

To determine whether a Networking API v2.0 endpoint supports the ``project_id``
attribute in requests, check that the ``project-id`` API extension is enabled
(see Extensions_).


Response format
---------------

The Networking API v2.0 always responds with the JSON data serialization
format. The ``Accept`` header is ignored.

Query extension
A ``.json`` extension can be added to the request URI. For example, the
``.json`` extension in the following requests are equivalent:

- GET *publicURL*/networks

- GET *publicURL*/networks.json

Tenant and project attributes in responses
------------------------------------------

Starting with the Newton release of the Networking service, the Networking API
returns a ``project_id`` attribute in responses, while still returning a
``tenant_id`` attribute for backward compatibility. The values will always be
identical.

To determine whether a Networking API v2.0 endpoint returns the ``project_id``
attribute in responses, check that the ``project-id`` API extension is enabled
(see Extensions_).


.. _filtering:

Filtering and column selection
==============================

The Networking API v2.0 supports filtering based on all top level attributes of
a resource. Filters are applicable to all list requests.

For example, the following request returns all networks named ``foobar``:

.. code::

    GET /v2.0/networks?name=foobar

When you specify multiple filters using different fields, the Networking API
v2.0 returns only objects that meet all filtering criteria. The operation
applies an AND condition among different filter fields.

OpenStack Networking offers an OR mechanism for filters by repeating the field
with the different OR criteria. For example, to find all networks named
``foobar`` OR ``bizbaz``:

.. code::

    GET /v2.0/networks?name=foobar&name=bizbaz


ORs and ANDs can be combined. For example, if you want all networks with
admin_state_up=True and shared=True and named ``foobar`` or ``bizbaz``:

.. code::

    GET /v2.0/networks?name=foobar&name=bizbaz&admin_state_up=True&shared=True

List of resources is supported in GET requests. For example, if you want the
information of two specific ports that ``id`` is ``port_id_A`` or ``port_id_B``:

.. code::

    GET /v2.0/ports?id=port_id_A&id=port_id_B

It treats ID filters as list and return ports with those 2 IDs.

Starting from Rocky release, the Networking API might support filtering
attributes with empty value. For example, the request below lists all ports
that have ``device_id`` attribute with empty value (which are unbound ports).

.. code::

    GET /v2.0/networks?device_id=

To determine if this feature is supported, a user can check whether the
``empty-string-filtering`` extension API is available.

Starting from Rocky release, the Networking API will perform validation
on filtering attributes if the API extension ``filter-validation`` is
available. If an API request contains an unknown or unsupported
parameter, the server will return a ``400`` response instead of silently
ignoring the invalid input.

Note
----

By default, OpenStack Networking returns all attributes for any show or list
call. The Networking API v2.0 has a mechanism to limit the set of attributes
returned. For example, return ``id``.

You can use the ``fields`` query parameter to control the attributes returned
from the Networking API v2.0.

For example, the following request returns only ``id`` and ``name`` for each
network:

.. code::

    GET /v2.0/networks.json?fields=id&fields=name

Synchronous versus asynchronous plug-in behavior
================================================

The Networking API v2.0 presents a logical model of network connectivity
consisting of networks, ports, and subnets. It is up to the OpenStack
Networking plug-in to communicate with the underlying infrastructure to ensure
packet forwarding is consistent with the logical model. A plug-in might perform
these operations asynchronously.

When an API client modifies the logical model by issuing an HTTP ``POST``,
``PUT``, or ``DELETE`` request, the API call might return before the plug-in
modifies underlying virtual and physical switching devices. However, an API
client is guaranteed that all subsequent API calls properly reflect the changed
logical model.

For example, if a client issues an HTTP ``PUT`` request to set the attachment
for a port, there is no guarantee that packets sent by the interface named in
the attachment are forwarded immediately when the HTTP call returns. However,
it is guaranteed that a subsequent HTTP ``GET`` request to view the attachment
on that port returns the new attachment value.

You can use the ``status`` attribute with the network and port resources to
determine whether the OpenStack Networking plug-in has successfully completed
the configuration of the resource.

Bulk-create
===========

The Networking API v2.0 enables you to create several objects of the same type
in the same API request. Bulk create operations use exactly the same API syntax
as single create operations except that you specify a list of objects rather
than a single object in the request body.

Bulk operations are always performed atomically, meaning that either all or
none of the objects in the request body are created. If a particular plug-in
does not support atomic operations, the Networking API v2.0 emulates the atomic
behavior so that users can expect the same behavior regardless of the
particular plug-in running in the background.

OpenStack Networking might be deployed without support for bulk operations and
when the client attempts a bulk create operation, a ``400`` Bad request error is
returned.

Pagination
==========

To reduce load on the service, list operations will return a maximum number of
items at a time. To navigate the collection, the parameters ``limit``, ``marker``
and ``page_reverse`` can be set in the URI. For example:

.. code::

    ?limit=100&marker=1234&page_reverse=False

The ``marker`` parameter is the ID of the last item in the previous list. The
``limit`` parameter sets the page size. The ``page_reverse`` parameter sets
the page direction. These parameters are optional. If the client requests a
limit beyond the maximum limit configured by the deployment, the server returns
the maximum limit number of items.

For convenience, list responses contain atom ``next`` links and ``previous``
links. The last page in the list requested with ``page_reverse=False`` will not
contain ``next`` link, and the last page in the list requested with
``page_reverse=True`` will not contain ``previous`` link. The following examples
illustrate two pages with three items. The first page was retrieved through:

.. code::

    GET http://127.0.0.1:9696/v2.0/networks.json?limit=2

Pagination is an optional feature of OpenStack Networking API, and it might be
disabled. If pagination is disabled, the pagination parameters will be ignored
and return all the items.

If a particular plug-in does not support pagination operations, and pagination
is enabled, the Networking API v2.0 will emulate the pagination behavior so
that users can expect the same behavior regardless of the particular plug-in
running in the background.

To determine if pagination is supported, a user can check whether the
'pagination' extension API is available.

**Example Network collection, first page: JSON request**

.. code::

    GET /v2.0/networks.json?limit=2 HTTP/1.1
    Host: 127.0.0.1:9696
    Content-Type: application/json
    Accept: application/json



**Example Network collection, first page: JSON response**

.. code::

    {
        "networks": [
            {
                "admin_state_up": true,
                "id": "396f12f8-521e-4b91-8e21-2e003500433a",
                "name": "net3",
                "provider:network_type": "vlan",
                "provider:physical_network": "physnet1",
                "provider:segmentation_id": 1002,
                "router:external": false,
                "shared": false,
                "status": "ACTIVE",
                "subnets": [],
                "tenant_id": "20bd52ff3e1b40039c312395b04683cf"
                "project_id": "20bd52ff3e1b40039c312395b04683cf"
            },
            {
                "admin_state_up": true,
                "id": "71c1e68c-171a-4aa2-aca5-50ea153a3718",
                "name": "net2",
                "provider:network_type": "vlan",
                "provider:physical_network": "physnet1",
                "provider:segmentation_id": 1001,
                "router:external": false,
                "shared": false,
                "status": "ACTIVE",
                "subnets": [],
                "tenant_id": "20bd52ff3e1b40039c312395b04683cf"
                "project_id": "20bd52ff3e1b40039c312395b04683cf"
            }
        ],
        "networks_links": [
            {
                "href": "http://127.0.0.1:9696/v2.0/networks.json?limit=2&marker=71c1e68c-171a-4aa2-aca5-50ea153a3718",
                "rel": "next"
            },
            {
                "href": "http://127.0.0.1:9696/v2.0/networks.json?limit=2&marker=396f12f8-521e-4b91-8e21-2e003500433a&page_reverse=True",
                "rel": "previous"
            }
        ]
    }


The last page won't show the ``next`` links

**Example Network collection, last page: JSON request**

.. code::

    GET /v2.0/networks.json?limit=2&marker=71c1e68c-171a-4aa2-aca5-50ea153a3718 HTTP/1.1
    Host: 127.0.0.1:9696
    Content-Type: application/json
    Accept: application/json



**Example Network collection, last page: JSON response**

.. code::

    {
        "networks": [
            {
                "admin_state_up": true,
                "id": "b3680498-03da-4691-896f-ef9ee1d856a7",
                "name": "net1",
                "provider:network_type": "vlan",
                "provider:physical_network": "physnet1",
                "provider:segmentation_id": 1000,
                "router:external": false,
                "shared": false,
                "status": "ACTIVE",
                "subnets": [],
                "tenant_id": "c05140b3dc7c4555afff9fab6b58edc2"
                "project_id": "c05140b3dc7c4555afff9fab6b58edc2"
            }
        ],
        "networks_links": [
            {
                "href": "http://127.0.0.1:9696/v2.0/networks.json?limit=2&marker=b3680498-03da-4691-896f-ef9ee1d856a7&page_reverse=True",
                "rel": "previous"
            }
        ]
    }


Sorting
=======

You can use the ``sort_key`` and ``sort_dir`` parameters to sort the
results of list operations. Currently sorting does not work with extended
attributes of resource. The ``sort_key`` and ``sort_dir`` can be repeated,
and the number of ``sort_key`` and ``sort_dir`` provided must be same. The
``sort_dir`` parameter indicates in which direction to sort. Acceptable
values are ``asc`` (ascending) and ``desc`` (descending).

Sorting is optional feature of OpenStack Networking API, and it might be
disabled. If sorting is disabled, the sorting parameters are ignored.

If a particular plug-in does not support sorting operations and sorting is
enabled, the Networking API v2.0 emulates the sorting behavior so that users
can expect the same behavior regardless of the particular plug-in that runs in
the background.

To determine if sorting is supported, a user can check whether the 'sorting'
extension API is available.

Starting from Rocky release, the Networking API performs validation on
sorting attributes if the API extension ``sort-key-validation`` is available.
If an API request contains an unknown or unsupported sort key,
the server will return a ``400`` response instead of silently ignoring
the invalid input.


.. _Extensions:

Extensions
==========

The Networking API v2.0 is extensible.

The purpose of Networking API v2.0 extensions is to:

-  Introduce new features in the API without requiring a version change.

-  Introduce vendor-specific niche functionality.

-  Act as a proving ground for experimental functionalities that might be
   included in a future version of the API.

To programmatically determine which extensions are available, issue a ``GET``
request on the ``v2.0/extensions`` URI.

To query extensions individually by unique alias, issue a ``GET`` request on
the ``/v2.0/extensions/*alias_name*`` URI. Use this method to easily
determine if an extension is available. If the extension is not available, a
``404 Not Found`` response is returned.

You can extend existing core API resources with new actions or extra
attributes. Also, you can add new resources as extensions. Extensions usually
have tags that prevent conflicts with other extensions that define attributes
or resources with the same names, and with core resources and attributes.
Because an extension might not be supported by all plug-ins, the availability
of an extension varies with deployments and the specific plug-in in use.


Faults
======

The Networking API v2.0 returns an error response if a failure occurs while
processing a request. OpenStack Networking uses only standard HTTP error codes.
``4nn`` errors indicate problems in the particular request being sent from
the client.

+-------+--------------------------------------------------------------+
| Error | Description                                                  |
+=======+==============================================================+
|``400``| Bad request                                                  |
|       | Malformed request URI or body requested admin state invalid  |
|       | Invalid values entered                                       |
|       | Bulk operations disallowed                                   |
|       | Validation failed                                            |
|       | Method not allowed for request body (such as trying to       |
|       | update attributes that can be specified at create-time only) |
+-------+--------------------------------------------------------------+
|``404``| Not Found                                                    |
|       | Non existent URI                                             |
|       | Resource not found                                           |
+-------+--------------------------------------------------------------+
|``409``| Conflict                                                     |
|       | Port configured on network                                   |
|       | IP allocated on subnet                                       |
|       | Conflicting IP allocation pools for subnet                   |
+-------+--------------------------------------------------------------+
|``412``| Precondition failed                                          |
|       | The revision number is mismatched                            |
+-------+--------------------------------------------------------------+
|``500``| Internal server error                                        |
|       | Internal OpenStack Networking error                          |
+-------+--------------------------------------------------------------+
|``503``| Service unavailable                                          |
|       | Failure in Mac address generation                            |
+-------+--------------------------------------------------------------+

Users submitting requests to the Networking API v2.0 might also receive the
following errors:

-  ``401 Unauthorized`` - If invalid credentials are provided.

-  ``403 Forbidden`` - If the user cannot access a specific resource or perform
   the requested operation.


Revisions
=========

The ``Resource revision numbers`` extension (``standard-attr-revisions``) adds
the ``revision_number`` attribute to all API resources that support standard
attributes. This includes networks, ports, subnets, subnet pools, floating IPs,
routers, logs, security groups/rules, network segments, QoS policies and trunks.
As you'd expect, the ``revision_number`` indicates the number of updates a
particular resource has undergone and is read-only.

In addition, the ``If-Match constraints based on revision_number`` extension
(``revision-if-match``) allows API consumers to leverage the ``If-Match`` HTTP
header to conditionally update/delete a resource when the HTTP ``If-Match``
header matches the ``revision_number`` of the said resource.

If the HTTP ``If-Match`` header doesn't match the ``revision_number`` of the
resource, users will receive the following errors:

-  ``412 Precondition failed`` - Update/Delete the target resource has been
   denied due to the mismatch of revision number.
