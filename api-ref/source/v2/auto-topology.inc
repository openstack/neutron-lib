.. -*- rst -*-

=========================
Auto Allocated Topologies
=========================

Show details and delete the auto allocated topology for a given project.
This API is only available when the ``auto-allocated-topology`` extension
is enabled.


Show auto allocated topology details
====================================

.. rest_method::  GET /v2.0/auto-allocated-topology/{project_id}

Shows details for an auto allocated topology.

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

   - project_id: project_id-path
   - fields: fields

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - id: id_autotopology
   - tenant_id: project_id-autotopology

Response Example
----------------

.. literalinclude:: samples/auto-topology/topo-show-response.json
   :language: javascript


Delete the auto allocated topology
==================================

.. rest_method::  DELETE /v2.0/auto-allocated-topology/{project_id}

Deletes the auto allocated topology.

Normal response codes: 204

Error response codes: 401, 403, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - project_id: project_id-path

Response
--------

There is no body content for the response of a successful DELETE request.
