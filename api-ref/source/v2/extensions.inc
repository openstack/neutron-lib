.. -*- rst -*-

==========
Extensions
==========


Extensions introduce features and vendor-specific functionality to
the API.

List extensions
===============

.. rest_method::  GET /v2.0/extensions

Lists available extensions.

Lists available Networking API v2.0 extensions.

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: 401

Request
-------

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - extensions: extensions
   - name: extension-name
   - links: extension-links
   - alias: extension-alias-body
   - updated: extension-updated
   - description: extension-description

Response Example
----------------

.. literalinclude:: samples/extensions/extensions-list-response.json
   :language: javascript

Show extension details
======================

.. rest_method::  GET /v2.0/extensions/{alias}

Shows details for an extension, by alias.
The response shows the extension name and its alias. To show
details for an extension, you specify the alias.

.. include:: filtering-show.inc

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - alias: extensions-alias-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - extension: extension
   - name: extension-name
   - links: extension-links
   - alias: extension-alias-body
   - updated: extension-updated
   - description: extension-description

Response Example
----------------

.. literalinclude:: samples/extensions/extension-show-response.json
   :language: javascript

