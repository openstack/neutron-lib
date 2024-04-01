.. -*- rst -*-

=========================================
Trunk details extended attributes (ports)
=========================================

The trunk_details extension attribute is available when showing a
port resource that participates in a trunk as parent. The extension
is useful for REST clients that may want to access trunk details
when getting the parent port, and it allows them to avoid extra
lookups.

Show trunk details
==================

.. rest_method::  GET /v2.0/ports/{port_id}

Shows details for a port. The details available in the `trunk_details`
attribute contain the trunk ID and the array showing information
about the subports that belong to the trunk: the port UUID, the
segmentation type, the segmentation ID, and the MAC address.

.. include:: filtering-show.inc

Normal response codes: 200

Request
-------

.. rest_parameters:: parameters.yaml

   - port_id: port_id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - trunk_details: trunk_details

Response Example
----------------

.. literalinclude:: ../v2/samples/trunks/trunk-details-show-response.json
   :language: javascript
