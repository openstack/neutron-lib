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

from neutron_lib import constants


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
    'enable_ndp_proxy',
    'external_gateways',
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
    'qos_policy_id',
    'service_types',
    constants.SHARED,
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
    'subnetpools',
    'security_groups'
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
    'agent-resources-synced',
    'allowed-address-pairs',
    'allowed-address-pairs-atomic',
    'auto-allocated-topology',
    'availability_zone',
    'binding',
    'data-plane-status',
    'project-default-networks',
    'default-subnetpools',
    'dhcp_agent_scheduler',
    'dns-domain-ports',
    'dns-integration',
    'dvr',
    'enable-default-route-ecmp',
    'enable-default-route-bfd',
    'empty-string-filtering',
    'expose-l3-conntrack-helper',
    'expose-port-forwarding-in-fip',
    'ext-gw-mode',
    'external-net',
    'extra_dhcp_opt',
    'extraroute',
    'extraroute-atomic',
    'filter-validation',
    'fip-port-details',
    'flavors',
    'floating-ip-port-forwarding',
    'floating-ip-port-forwarding-description',
    'floatingip-autodelete-internal',
    'floatingip-pools',
    'ip-substring-filtering',
    'l3-conntrack-helper',
    'l3-ha',
    'l3_agent_scheduler',
    'l3-ext-ndp-proxy',
    'l3-ndp-proxy',
    'l3-port-ip-change-not-allowed',
    'logging',
    'metering',
    'metering_source_and_destination_filters',
    'multi-provider',
    'external-gateway-multihoming',
    'net-mtu',
    'network-ip-availability',
    'network-segment-range',
    'network_availability_zone',
    'pagination',
    'port-mac-address-override',
    'port-resource-request',
    'port-security',
    'project-id',
    'provider',
    'qos',
    'qos-bw-limit-direction',
    'qos-fip',
    'qos-fip-network-policy',
    'qos-gateway-ip',
    'qos-port-network-policy',
    'qos-pps-minimum',
    'qos-pps-minimum-rule-alias',
    'qos-rule-type-filter',
    'qos-rules-alias',
    'quotas',
    'quota-check-limit',
    'quota-check-limit-default',
    'port-hints',
    'port-hint-ovs-tx-steering',
    'port-numa-affinity-policy',
    'port-numa-affinity-policy-socket',
    'rbac-address-group',
    'rbac-address-scope',
    'rbac-bgpvpn',
    'rbac-policies',
    'rbac-security-groups',
    'rbac-subnetpool',
    'router',
    'router_availability_zone',
    'security-group',
    'segment',
    'service-type',
    'sort-key-validation',
    'sorting',
    'standard-attr-description',
    'standard-attr-fwaas-v2',
    'standard-attr-revisions',
    'standard-attr-segment',
    'standard-attr-timestamp',
    'subnet',
    'subnet_allocation',
    'subnet_dns_publish_fixed_ip',
    'subnet_onboard',
    'subnetpool-prefix-ops',
    'subnet-segmentid-enforce',
    'subnet-segmentid-writable',
    'tag',
    'tag-creation',
    'trunk',
    'trunk-details',
    'uplink-status-propagation',
    'uplink-status-propagation-updatable',
    # Add here list of extensions with pointers to the project repo, e.g.
    'bgp',  # https://opendev.org/openstack/neutron-dynamic-routing

    # https://opendev.org/openstack/neutron-fwaas
    'fwaas',
    'fwaasrouterinsertion',
    'fwaas_v2',
    'bgpvpn',  # https://opendev.org/openstack/networking-bgpvpn
    'bgpvpn-routes-control',
    'bgpvpn-vni',

    # https://opendev.org/openstack/neutron-vpnaas
    'vpnaas',
    'vpn-endpoint-groups',
    'vpn-flavors',

    # https://opendev.org/openstack/networking-sfc:
    'flow_classifier',
    'sfc',

    # https://opendev.org/openstack/tap-as-a-service
    'taas',
    'tap_mirrors',
    'taas-vlan-filter',
)

KNOWN_KEYWORDS = (
    'allow_post',
    'allow_put',
    'convert_to',
    'convert_list_to',
    'default',
    'enforce_policy',
    'is_filter',
    'is_sort_key',
    'is_visible',
    'primary_key',
    'required_by_policy',
    'validate',
    'default_overrides_none',
    'dict_populate_defaults',
)
