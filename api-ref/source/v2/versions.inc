.. -*- rst -*-
.. needs:example_verification

============
API versions
============

Lists information for all Networking API versions.

List API versions
=================

.. rest_method::  GET /

Lists information about all Networking API versions.

Normal response codes: 200

Request
-------

.. .. rest_parameters:: parameters.yaml

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - versions: versions
   - status: version-status
   - id: version-id
   - links: version-links
   - href: version-href
   - rel: version-rel

Response Example
----------------

.. literalinclude:: samples/networks/versions-list-response.json
   :language: javascript

Show API v2 details
===================

.. rest_method::  GET /v2.0/

Shows details for Networking API v2.0.

Normal response codes: 200

Error response codes: 401

Request
-------

.. .. rest_parameters:: parameters.yaml

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - resources: resources
   - name: resource-name
   - collection: resource-collection
   - links: resource-links
   - href: resource-href
   - rel: resource-rel

Response Example
----------------

.. literalinclude:: samples/networks/version-show-response.json
   :language: javascript
