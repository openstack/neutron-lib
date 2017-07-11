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
    'allocation_pools',
    'cidr',
    'default_prefixlen',
    'default_quota',
    'description',
    'device_id',
    'device_owner',
    'dns_nameservers',
    'enable_dhcp',
    'fixed_ips',
    'gateway_ip',
    'host_routes',
    'id',
    'ip_version',
    'ipv6_address_mode',
    'ipv6_ra_mode',
    'is_default',
    'mac_address',
    'max_prefixlen',
    'min_prefixlen',
    'name',
    'network_id',
    'port_id',
    'prefixes',
    'prefixlen',
    'project_id',
    'shared',
    'status',
    'subnets',
    'subnetpool_id',
    'tenant_id'
)

KNOWN_RESOURCES = (
    'networks',
    'ports',
    'routers',
    'subnets',
    'subnetpools'
)

KNOWN_HTTP_ACTIONS = (
    'DELETE',
    'GET',
    'POST',
    'PUT',
)

KNOWN_ACTION_STATUSES = (
    200,
    201,
    202,
    203,
    204,
    205,
    206,
)

KNOWN_EXTENSIONS = (
    'address-scope',
    'agent',
    'allowed-address-pairs',
    'auto-allocated-topology',
    'availability_zone',
    'binding',
    'data-plane-status',
    'default-subnetpools',
    'dhcp_agent_scheduler',
    'dns-domain-ports',
    'dns-integration',
    'dvr',
    'ext-gw-mode',
    'external-net',
    'extra_dhcp_opt',
    'extraroute',
    'flavors',
    'l3-ha',
    'l3_agent_scheduler',
    'logging',
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

    # http://git.openstack.org/cgit/openstack/neutron-fwaas
    'fwaas',
    'fwaasrouterinsertion',
    'fwaas_v2',
    'bgpvpn',  # https://git.openstack.org/cgit/openstack/networking-bgpvpn
    'bgpvpn-routes-control',
)

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
