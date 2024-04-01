.. -*- rst -*-

=====================================================================
Networking Flavors Framework v2.0 (CURRENT) (flavor, service_profile)
=====================================================================

Extension that allows user selection of operator-curated flavors
during resource creation.

Users can check if flavor available by performing a GET on the
/v2.0/extensions/flavors. If it is unavailable,there is an 404 error
response (itemNotFound).
Refer `Show extension details <#show-extension-details>`__ for more details.

List flavors
============

.. rest_method::  GET /v2.0/flavors

Lists all flavors visible to the project.

The list can be empty.

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: 401

Request
-------

.. rest_parameters:: parameters.yaml

   - id: id-query
   - service_type: flavor-service_type-query
   - name: name-query
   - description: description-query
   - enabled: flavor-enabled-query
   - sort_dir: sort_dir
   - sort_key: flavor-sort_key
   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - flavors: flavors
   - id: flavor-id
   - service_type: flavor-service_type
   - name: flavor-name
   - description: flavor-description
   - enabled: flavor-enabled
   - service_profiles: flavor-service_profiles

Response Example
----------------

.. literalinclude:: samples/flavors/flavors-list-response.json
   :language: javascript

Create flavor
=============

.. rest_method::  POST /v2.0/flavors

Creates a flavor.

This operation establishes a new flavor.

The service_type to which the flavor applies is a required
parameter. The corresponding service plugin must have been
activated as part of the configuration.
Check `Service providers <#list-service-providers>`__ for how to see
currently loaded service types. Additionally the service plugin
needs to support the use of flavors.

Creation currently limited to administrators. Other users will
receive a ``Forbidden 403`` response code with a response body
NeutronError message expressing that creation is disallowed by
policy.

Until one or more service profiles are associated with the flavor
by the operator, attempts to use the flavor during resource
creations will currently return a ``Not Found 404`` with a response
body that indicates no service profile could be found.

If the API cannot fulfill the request due to insufficient data or
data that is not valid, the service returns the HTTP ``Bad Request
(400)`` response code with information about the failure in the
response body. Validation errors require that you correct the error
and submit the request again.

Normal response codes: 201

Error response codes: 400, 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - flavor: flavor
   - service_type: flavor-service_type
   - enabled: flavor-enabled-request
   - description: flavor-description-request
   - name: flavor-name-request

Request Example
---------------

.. literalinclude:: samples/flavors/flavor-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - flavor: flavor
   - id: flavor-id
   - service_type: flavor-service_type
   - name: flavor-name
   - description: flavor-description
   - enabled: flavor-enabled
   - service_profiles: flavor-service_profiles

Response Example
----------------

.. literalinclude:: samples/flavors/flavor-create-response.json
   :language: javascript

Show flavor details
===================

.. rest_method::  GET /v2.0/flavors/{flavor_id}

Shows details for a flavor.

This operation returns a flavor object by ID. If you are not an
administrative user and the flavor object is not visible to your
project account, the service returns the HTTP ``Forbidden (403)``
response code.

.. include:: filtering-show.inc

Normal response codes: 200

Error response codes: 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - flavor_id: flavor_id

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - flavor: flavor
   - id: flavor-id
   - service_type: flavor-service_type
   - name: flavor-name
   - description: flavor-description
   - enabled: flavor-enabled
   - service_profiles: flavor-service_profiles

Response Example
----------------

.. literalinclude:: samples/flavors/flavor-show-response.json
   :language: javascript

Update flavor
=============

.. rest_method::  PUT /v2.0/flavors/{flavor_id}

Updates a flavor.

The service_type cannot be updated as there may be associated
service profiles and consumers depending on the value.

Normal response codes: 200

Error response codes: 400, 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - flavor_id: flavor_id
   - flavor: flavor
   - name: flavor-name-request
   - description: flavor-description-request
   - enabled: flavor-enabled-request

Request Example
---------------

.. literalinclude:: samples/flavors/flavor-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - flavor: flavor
   - id: flavor-id
   - service_type: flavor-service_type
   - name: flavor-name
   - description: flavor-description
   - enabled: flavor-enabled
   - service_profiles: flavor-service_profiles

Response Example
----------------

.. literalinclude:: samples/flavors/flavor-update-response.json
   :language: javascript

Delete flavor
=============

.. rest_method::  DELETE /v2.0/flavors/{flavor_id}

Deletes a flavor.

Normal response codes: 204

Error response codes: 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - flavor_id: flavor_id

Response
--------

No body content is returned on a successful DELETE.

Associate flavor with a service profile
=======================================

.. rest_method::  POST /v2.0/flavors/{flavor_id}/service_profiles

Associate a flavor with a service profile.

A flavor can be associated with more than one profile.

Will return ``409 Conflict`` if association already exists.

Normal response codes: 201

Error response codes: 400, 401, 403, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - flavor_id: flavor_id
   - service_profile: service_profile
   - id: service_profile-id


Request Example
---------------

.. literalinclude:: samples/flavors/flavor-associate-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - service_profile: service_profile
   - id: id

Response Example
----------------

.. literalinclude:: samples/flavors/flavor-associate-response.json
   :language: javascript

Disassociate a flavor.
======================

.. rest_method::  DELETE /v2.0/flavors/{flavor_id}/service_profiles/{profile_id}

Disassociate a flavor from a service profile.

Normal response codes: 204

Error response codes: 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - profile_id: profile_id
   - flavor_id: flavor_id

Response
--------

No body content is returned on a successful disassociation.

List service profiles
=====================

.. rest_method::  GET /v2.0/service_profiles

Lists all service profiles visible for the tenant account.

The list can be empty.

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: 401

Request
-------

.. rest_parameters:: parameters.yaml

   - id: id-query
   - enabled: service_profile-enabled-query
   - driver: service_profile-driver-query
   - description: description-query
   - sort_dir: sort_dir
   - sort_key: service_profile-sort_key

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - service_profiles: service_profiles
   - id: service_profile-id
   - enabled: service_profile-enabled
   - driver: service_profile-driver
   - description: service_profile-description
   - metainfo: service_profile-metainfo

Response Example
----------------

.. literalinclude:: samples/flavors/service-profiles-list-response.json
   :language: javascript

Create service profile
======================

.. rest_method::  POST /v2.0/service_profiles

Creates a service profile.

This operation establishes a new service profile that can be
associated with one or more flavors.

Either metadata or a driver is required.

If a driver is specified but does not exist, call will return a
``Not found 404`` error with the response body explaining that the
driver could not be found.

Creation currently limited to administrators. Other users will
receive a ``Forbidden 403`` response code with a response body
NeutronError message expressing that creation is disallowed by
policy.

If the API cannot fulfill the request due to insufficient data or
data that is not valid, the service returns the HTTP ``Bad Request
(400)`` response code with information about the failure in the
response body. Validation errors require that you correct the error
and submit the request again.

Normal response codes: 201

Error response codes: 400, 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - service_profile: service_profile
   - description: service_profile-description-request
   - metainfo: service_profile-metainfo-request
   - enabled: service_profile-enabled-request
   - driver: service_profile-driver-request

Request Example
---------------

.. literalinclude:: samples/flavors/service-profile-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - service_profile: service_profile
   - id: service_profile-id
   - enabled: service_profile-enabled
   - driver: service_profile-driver
   - description: service_profile-description
   - metainfo: service_profile-metainfo

Response Example
----------------

.. literalinclude:: samples/flavors/service-profile-create-response.json
   :language: javascript

Show service profile details
============================

.. rest_method::  GET /v2.0/service_profiles/{profile_id}

Shows details for a service profile.

This operation returns a service profile object by ID. If you are
not an administrative user and the object is not visible to your
tenant account, the service returns the HTTP ``Forbidden (403)``
response code.

.. include:: filtering-show.inc

Normal response codes: 200

Error response codes: 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - profile_id: profile_id

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - service_profile: service_profile
   - id: service_profile-id
   - enabled: service_profile-enabled
   - driver: service_profile-driver
   - description: service_profile-description
   - metainfo: service_profile-metainfo

Response Example
----------------

.. literalinclude:: samples/flavors/service-profile-show-response.json
   :language: javascript

Update service profile
======================

.. rest_method::  PUT /v2.0/service_profiles/{profile_id}

Updates a service profile.

Normal response codes: 200

Error response codes: 400, 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - profile_id: profile_id
   - service_profile: service_profile
   - enabled: service_profile-enabled-request
   - driver: service_profile-driver-request
   - description: service_profile-description-request
   - metainfo: service_profile-metainfo-request

Request Example
---------------

.. literalinclude:: samples/flavors/service-profile-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - service_profile: service_profile
   - id: service_profile-id
   - enabled: service_profile-enabled
   - driver: service_profile-driver
   - description: service_profile-description
   - metainfo: service_profile-metainfo

Response Example
----------------

.. literalinclude:: samples/flavors/service-profile-update-response.json
   :language: javascript

Delete service profile
======================

.. rest_method::  DELETE /v2.0/service_profiles/{profile_id}

Deletes a service profile.

Attempting to delete a service profile that is currently associated
with a flavor will return a ``Conflict 409`` with a response body
containing an in use message.

Either metadata or a driver is required.

Normal response codes: 204

Error response codes: 401, 403, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - profile_id: profile_id

Response
--------

No body content is returned on a successful DELETE.
