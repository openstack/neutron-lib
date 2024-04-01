.. -*- rst -*-

==============================
Router NDP proxy (ndp_proxies)
==============================

A ``ndp_proxy`` is a logical entity for annunciate a unique IPv6 address to
external network. It depends on a ``router`` entity on which external gateway
is enabled.

List ndp proxies
================

.. rest_method::  GET /v2.0/ndp_proxies

Lists logical ndp_proxies that the project who submits the request can
access.

Default policy settings return only those ndp_proxies that the project
who submits the request owns, unless an administrative user submits
the request.

.. include:: filtering-list.inc

Normal response codes: 200

Error response codes: 401

Request
-------

.. rest_parameters:: parameters.yaml

   - id: id-query
   - tenant_id: project_id-query
   - project_id: project_id-query
   - name: name-query
   - description: description-query
   - router_id: ndp_proxy-router-id-query
   - port_id: ndp_proxy-port-id-query
   - ip_address: ndp_proxy-ip-address-query
   - revision_number: revision_number-query
   - sort_dir: sort_dir
   - sort_key: ndp_proxy-sort_key
   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - ndp_proxies: ndp_proxies
   - name: name
   - id: ndp_proxy_id-body
   - description: description
   - tenant_id: project_id
   - project_id: project_id
   - revision_number: revision_number
   - router_id: ndp_proxy_router_id-body
   - port_id: ndp_proxy_port_id-body
   - ip_address: ndp_proxy_ip_address-body
   - created_at: created_at_resource
   - updated_at: updated_at_resource

Response Example
----------------

.. literalinclude:: samples/ndp_proxies/ndp-proxies-list-response.json
   :language: javascript


Show ndp proxy details
======================

.. rest_method::  GET /v2.0/ndp_proxies/{ndp_proxy_id}

Shows information for a ndp proxy

.. include:: filtering-show.inc

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - ndp_proxy_id: ndp_proxy_id-path
   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - ndp_proxy: ndp_proxy
   - name: name
   - id: ndp_proxy_id-body
   - description: description
   - tenant_id: project_id
   - project_id: project_id
   - revision_number: revision_number
   - router_id: ndp_proxy_router_id-body
   - port_id: ndp_proxy_port_id-body
   - ip_address: ndp_proxy_ip_address-body
   - created_at: created_at_resource
   - updated_at: updated_at_resource

Response Example
----------------

.. literalinclude:: samples/ndp_proxies/ndp-proxy-show-response.json
   :language: javascript


Update a ndp proxy
==================

.. rest_method:: PUT /v2.0/ndp_proxies/{ndp_proxy_id}

Updates a ndp proxy

Normal response codes: 200

Error response codes: 400, 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - ndp_proxy_id: ndp_proxy_id-path
   - ndp_proxy: ndp_proxy
   - name: name
   - description: description-request-put

Request Example
---------------

.. literalinclude:: samples/ndp_proxies/ndp-proxy-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - ndp_proxy: ndp_proxy
   - name: name
   - id: ndp_proxy_id-body
   - description: description
   - tenant_id: project_id
   - project_id: project_id
   - revision_number: revision_number
   - router_id: ndp_proxy_router_id-body
   - port_id: ndp_proxy_port_id-body
   - ip_address: ndp_proxy_ip_address-body
   - created_at: created_at_resource
   - updated_at: updated_at_resource

Response Example
----------------

.. literalinclude:: samples/ndp_proxies/ndp-proxy-update-response.json
   :language: javascript


Create ndp proxy
================

.. rest_method::  POST /v2.0/ndp_proxies

Creates a ndp proxy

Normal response codes: 201

Error response codes: 400, 401

Request
-------

.. rest_parameters:: parameters.yaml

    - ndp_proxy: ndp_proxy
    - name: name-request
    - router_id: ndp_proxy_router_id-body
    - port_id: ndp_proxy_port_id-body
    - ip_address: ndp_proxy_ip_address-body-request
    - description: description-request

Request Example
---------------

.. literalinclude:: samples/ndp_proxies/ndp-proxy-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - ndp_proxy: ndp_proxy
   - name: name
   - id: ndp_proxy_id-body
   - description: description
   - tenant_id: project_id
   - project_id: project_id
   - revision_number: revision_number
   - router_id: ndp_proxy_router_id-body
   - port_id: ndp_proxy_port_id-body
   - ip_address: ndp_proxy_ip_address-body
   - created_at: created_at_resource
   - updated_at: updated_at_resource

Response Example
----------------

.. literalinclude:: samples/ndp_proxies/ndp-proxy-create-response.json
   :language: javascript


Delete a ndp proxy
==================

.. rest_method::  DELETE /v2.0/ndp_proxies/{ndp_proxy_id}

Deletes a ndp proxy.

Normal response codes: 204

Error response codes: 404

Request
-------

.. rest_parameters:: parameters.yaml

   - ndp_proxy_id: ndp_proxy_id-path

Response
--------

There is no body content for the response of a successful DELETE request.
