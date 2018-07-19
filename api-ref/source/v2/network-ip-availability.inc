.. -*- rst -*-

=======================================
Network IP availability and usage stats
=======================================

The extension ``network-ip-availability`` allows users to list and show the
network IP usage stats of all networks or of a specified network.
By default policy configuration, only administrative users can use this API.

Show Network IP Availability
============================

.. rest_method::  GET /v2.0/network-ip-availabilities/{network_id}

Shows network IP availability details for a network.

By default policy configuration, only administrative users can retrieve
IP availability. Otherwise, ``Not Found (404)`` will be returned.

Normal response codes: 200

Error response codes: 401, 404

Request
-------

.. rest_parameters:: parameters.yaml

   - network_id: network_id-path

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - network_ip_availability: network_ip_availability
   - network_id: network_ip_availability-network_id
   - network_name: network-name
   - tenant_id: project_id
   - project_id: project_id
   - total_ips: total_ips
   - used_ips: used_ips
   - subnet_ip_availability: subnet_ip_availability
   - subnet_id: network_ip_availability-subnet_id
   - subnet_name: subnet_name
   - ip_version: subnet-ip_version
   - cidr: cidr

Response Example
----------------

.. literalinclude:: samples/network-ip-availability/network-ip-availability-show.json
   :language: javascript

List Network IP Availability
============================

.. rest_method::  GET /v2.0/network-ip-availabilities

Lists network IP availability of all networks.

By default policy configuration, only administrative users can retrieve
IP availabilities. Otherwise, an empty list will be returned.

Normal response codes: 200

Error response codes: 401

Request
-------

.. rest_parameters:: parameters.yaml

   - network_id: network_ip_availability-network_id-query
   - network_name: network-name-query
   - tenant_id: project_id-query
   - project_id: project_id-query
   - ip_version: ip_version-query

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - network_ip_availabilities: network_ip_availabilities
   - network_id: network_ip_availability-network_id
   - network_name: network-name
   - tenant_id: project_id
   - project_id: project_id
   - total_ips: total_ips
   - used_ips: used_ips
   - subnet_ip_availability: subnet_ip_availability
   - subnet_id: network_ip_availability-subnet_id
   - subnet_name: subnet_name
   - ip_version: subnet-ip_version
   - cidr: cidr

Response Example
----------------

.. literalinclude:: samples/network-ip-availability/network-ip-availability-list.json
   :language: javascript

