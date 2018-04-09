.. -*- rst -*-

================
Trunk networking
================

The trunk extension can be used to multiplex packets coming from and going to
multiple neutron logical networks using a single neutron logical port. A trunk
is modeled in neutron as a collection of neutron logical ports. One port,
called parent port, must be associated to a trunk and it is *the* port to
be used to connect instances with neutron. A sequence of subports (or
sub_ports) each typically belonging to distinct neutron networks, is also
associated to a trunk, and each subport may have a segmentation type and ID
used to mux/demux the traffic coming in and out of the parent port.

In more details, the extension introduces the following resources:

- **trunk**. A top level logical entity to model the group of neutron
  logical networks whose traffic flows through the trunk.

- **sub_port**. An association to a neutron logical port with attributes
  segmentation_id and segmentation_type.

Resource timestamps
===================

The ``standard-attr-timestamp`` extension adds the ``created_at`` and
``updated_at`` attributes to all resources that have standard attributes.


Tag extension
=============

The ``standard-attr-tag`` adds Tag support for resources with
standard attributes by adding the ``tags`` attribute
allowing consumers to associate tags with resources.


List trunks
===========

.. rest_method::  GET /v2.0/trunks

Lists trunks that are accessible to the user who submits the request.

Default policy settings return only those trunks that are
owned by the user who submits the request, unless an admin user
submits the request.

Use the ``fields`` query parameter to control which fields are
returned in the response body. Additionally, you can filter results
by using query string parameters. For information, see the Filtering_
section for more details.

Normal response codes: 200

Error response codes: 401, 404

Request Parameters
------------------

.. rest_parameters:: parameters.yaml

   - admin_state_up: admin_state_up_trunk-query
   - description: description-query
   - id: id-query
   - name: name-query
   - port_id: trunk_port_id-query
   - revision_number: revision_number-query
   - status: trunk-status-query
   - tenant_id: project_id-query
   - project_id: project_id-query
   - sort_dir: sort_dir
   - sort_key: trunk-sort_key
   - tags: tags-query
   - tags-any: tags-any-query
   - not-tags: not-tags-query
   - not-tags-any: not-tags-any-query

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - admin_state_up: admin_state_up_trunk
   - created_at: created_at_resource
   - description: description_resource
   - id: id_resource
   - name: name_resource
   - port_id: trunk_port_id
   - revision_number: revision_number
   - status: trunk-status
   - tenant_id: project_id-request
   - project_id: project_id-request
   - sub_ports: sub_ports
   - updated_at: updated_at_resource
   - tags: tags

Response Example
----------------

.. literalinclude:: ../v2/samples/trunks/trunks-list-response.json
   :language: javascript


Create trunk
============

.. rest_method::  POST /v2.0/trunks

Error codes:

- ``400`` The operation returns this error code if the request is malformed,
  e.g. there are missing or invalid parameters in the request.

- ``401`` The operation is not authorized.

- ``404`` If the extension is not available or the port UUID of any of the
  specified ports is not found.

- ``409`` The operation returns this error code for one of these
  reasons:

  - A port to be used as subport is in use by another trunk.

  - The segmentation type and segmentation ID are already in use in the trunk.

  - A port to be used as parent port is in use by another trunk or cannot be trunked.

  - A system configuration prevents the operation from succeeding.


Normal response codes: 201

Error response codes: 400, 401, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - tenant_id: project_id
   - project_id: project_id
   - port_id: trunk_port_id
   - name: name_resource
   - description: description_resource
   - admin_state_up: admin_state_up_trunk
   - sub_ports: sub_ports

Request Example
---------------

.. literalinclude:: ../v2/samples/trunks/trunk-create-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - admin_state_up: admin_state_up_trunk
   - created_at: created_at_resource
   - description: description_resource
   - id: id_resource
   - name: name_resource
   - port_id: trunk_port_id
   - revision_number: revision_number
   - status: trunk-status
   - tenant_id: project_id
   - project_id: project_id
   - sub_ports: sub_ports
   - updated_at: updated_at_resource
   - tags: tags

Response Example
----------------

.. literalinclude:: ../v2/samples/trunks/trunks-create-response.json
   :language: javascript

Add subports to trunk
=====================

.. rest_method::  PUT /v2.0/trunks/{trunk_id}/add_subports

Normal response codes: 200

Error response codes: 400, 401, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - trunk_id: trunk_id
   - segmentation_id: segmentation_id
   - segmentation_type: segmentation_type-request
   - port_id: port_id_subport

Request Example
---------------

.. literalinclude:: ../v2/samples/trunks/trunk-add-subports-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - admin_state_up: admin_state_up_trunk
   - created_at: created_at_resource
   - description: description_resource
   - id: id_resource
   - name: name_resource
   - port_id: trunk_port_id
   - revision_number: revision_number
   - status: trunk-status
   - tenant_id: project_id
   - project_id: project_id
   - sub_ports: sub_ports
   - updated_at: updated_at_resource
   - tags: tags

Response Example
----------------

.. literalinclude:: ../v2/samples/trunks/trunk-add-subports-response.json
   :language: javascript


Delete subports from trunk
==========================

.. rest_method::  PUT /v2.0/trunks/{trunk_id}/remove_subports

Normal response codes: 200

Error response codes: 400, 401, 404, 409

Request
-------

.. rest_parameters:: parameters.yaml

   - trunk_id: trunk_id
   - port_id: port_id

Request Example
---------------

.. literalinclude:: ../v2/samples/trunks/trunk-remove-subports-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - admin_state_up: admin_state_up_trunk
   - created_at: created_at_resource
   - description: description_resource
   - id: id_resource
   - name: name_resource
   - port_id: trunk_port_id
   - revision_number: revision_number
   - status: trunk-status
   - tenant_id: project_id
   - project_id: project_id
   - sub_ports: sub_ports
   - updated_at: updated_at_resource
   - tags: tags

Response Example
----------------

.. literalinclude:: ../v2/samples/trunks/trunk-remove-subports-response.json
   :language: javascript


List subports for trunk
=======================

.. rest_method::  GET /v2.0/trunks/{trunk_id}/get_subports

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - trunk_id: trunk_id

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - port_id: port_id_subport
   - segmentation_type: segmentation_type
   - segmentation_id: segmentation_id
   - tags: tags

Response Example
----------------

.. literalinclude:: ../v2/samples/trunks/trunk-list-subports-response.json
   :language: javascript


Update trunk
============

.. rest_method::  PUT /v2.0/trunks/{trunk_id}

The update request is only for changing fields like name, description or
admin_state_up. Setting the admin_state_up to False locks the trunk in
that it prevents operations such as as adding/removing subports.

Normal response codes: 200

Error response codes: 400, 401, 404, 409, 412

Request
-------

.. rest_parameters:: parameters.yaml

   - name_resource: name_resource
   - admin_state_up_trunk: admin_state_up
   - description_resource: description_resource
   - trunk_id: trunk_id

Request Example
---------------

.. literalinclude:: ../v2/samples/trunks/trunk-update-request.json
   :language: javascript

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml


   - admin_state_up: admin_state_up_trunk
   - created_at: created_at_resource
   - description: description_resource
   - id: id_resource
   - name: name_resource
   - port_id: trunk_port_id
   - revision_number: revision_number
   - status: trunk-status
   - tenant_id: project_id
   - project_id: project_id
   - sub_ports: sub_ports
   - updated_at: updated_at_resource
   - tags: tags

Response Example
----------------

.. literalinclude:: ../v2/samples/trunks/trunk-update-response.json
   :language: javascript


Show trunk
==========

.. rest_method::  GET /v2.0/trunks/{trunk_id}

Shows details for a trunk.

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

   - trunk_id: trunk_id

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - admin_state_up: admin_state_up_trunk
   - created_at: created_at_resource
   - description: description_resource
   - id: id_resource
   - name: name_resource
   - port_id: trunk_port_id
   - revision_number: revision_number
   - status: trunk-status
   - tenant_id: project_id
   - project_id: project_id
   - sub_ports: sub_ports
   - updated_at: updated_at_resource
   - tags: tags

Response Example
----------------

.. literalinclude:: ../v2/samples/trunks/trunk-show-response.json
   :language: javascript


Delete trunk
============

.. rest_method::  DELETE /v2.0/trunks/{trunk_id}

Deletes a trunk, if its state allows it.

Normal response codes: 204

Error response codes: 401, 404, 409, 412

Request
-------

.. rest_parameters:: parameters.yaml

   - trunk_id: trunk_id
