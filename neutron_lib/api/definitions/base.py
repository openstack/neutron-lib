#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

KNOWN_ATTRIBUTES = (
    'admin_state_up',
    'id',
    'description',
    'name',
    'network_id',
    'port_id',
    'project_id',
    'shared',
    'status',
    'tenant_id',
)

KNOWN_RESOURCES = (
    'networks',
    'ports',
    'subnets',
    'routers',
)

KNOWN_HTTP_ACTIONS = (
    'DELETE',
    'GET',
    'POST',
    'PUT',
)

KNOWN_EXTENSIONS = (
    'address-scope',
    'agent',
    'allowed-address-pairs',
    'auto-allocated-topology',
    'availability_zone',
    'binding',
    'default-subnetpools',
    'dhcp_agent_scheduler',
    'dns-integration',
    'dvr',
    'ext-gw-mode',
    'external-net',
    'extra_dhcp_opt',
    'extraroute',
    'flavors',
    'l3-ha',
    'l3_agent_scheduler',
    'metering',
    'multi-provider',
    'net-mtu',
    'network-ip-availability',
    'network_availability_zone',
    'pagination',
    'port-security',
    'project-id',
    'provider',
    'qos',
    'quotas',
    'rbac-policies',
    'router',
    'router_availability_zone',
    'security-group',
    'service-type',
    'sorting',
    'standard-attr-description',
    'standard-attr-revisions',
    'standard-attr-timestamp',
    'subnet_allocation',
    'tag',
    'trunk',
    'trunk-details',
    # Add here list of extensions with pointers to the project repo, e.g.
    # 'bgp',  # http://git.openstack.org/cgit/openstack/neutron-dynamic-routing
    'fw',  # http://git.openstack.org/cgit/openstack/neutron-fwaas
    'fwaas',  # http://git.openstack.org/cgit/openstack/neutron-fwaas
)

# The following is a short reference for understanding attribute info:
# allow_post: the attribute can be used on POST requests.
# allow_put: the attribute can be used on PUT requests.
# convert_to: transformation to apply to the value before it is returned
# default: default value of the attribute (if missing, the attribute
# becomes mandatory.
# enforce_policy: the attribute is actively part of the policy enforcing
# mechanism, ie: there might be rules which refer to this attribute.
# is_visible: the attribute is returned in GET responses.
# required_by_policy: the attribute is required by the policy engine and
# should therefore be filled by the API layer even if not present in
# request body.
# validate: specifies rules for validating data in the attribute.
KNOWN_KEYWORDS = (
    'allow_post',
    'allow_put',
    'convert_to',
    'convert_list_to',
    'default',
    'enforce_policy',
    'is_visible',
    'primary_key',
    'required_by_policy',
    'validate',
)
