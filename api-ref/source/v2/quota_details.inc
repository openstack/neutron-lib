.. -*- rst -*-

========================================
Quotas details extension (quota_details)
========================================

Extends the ``quotas`` API to show a quota set for each project that includes
the quota's used, limit and reserved counts per resource.

A quota value of ``-1`` means that quota has no limit.

Show quota details for a tenant
===============================

.. rest_method::  GET /v2.0/quotas/{project_id}/details.json

Shows quota details for a project.

.. include:: filtering-show.inc

Normal response codes: 200

Error response codes: 401, 403

Request
-------

.. rest_parameters:: parameters.yaml

   - project_id: project_id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - quota: quota-detail

Response Example
----------------

.. literalinclude:: samples/quota_details/quota-details-show-for-project-response.json
   :language: javascript
