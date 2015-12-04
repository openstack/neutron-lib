# Copyright (c) 2012 OpenStack Foundation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# TODO(salv-orlando): Verify if a single set of operational
# status constants is achievable
NET_STATUS_ACTIVE = 'ACTIVE'
NET_STATUS_BUILD = 'BUILD'
NET_STATUS_DOWN = 'DOWN'
NET_STATUS_ERROR = 'ERROR'

PORT_STATUS_ACTIVE = 'ACTIVE'
PORT_STATUS_BUILD = 'BUILD'
PORT_STATUS_DOWN = 'DOWN'
PORT_STATUS_ERROR = 'ERROR'
PORT_STATUS_NOTAPPLICABLE = 'N/A'

FLOATINGIP_STATUS_ACTIVE = 'ACTIVE'
FLOATINGIP_STATUS_DOWN = 'DOWN'
FLOATINGIP_STATUS_ERROR = 'ERROR'

# Service operation status constants
ACTIVE = "ACTIVE"
DOWN = "DOWN"
CREATED = "CREATED"
PENDING_CREATE = "PENDING_CREATE"
PENDING_UPDATE = "PENDING_UPDATE"
PENDING_DELETE = "PENDING_DELETE"
INACTIVE = "INACTIVE"
ERROR = "ERROR"

DEVICE_OWNER_COMPUTE_PREFIX = "compute:"
DEVICE_OWNER_NETWORK_PREFIX = "network:"
DEVICE_OWNER_NEUTRON_PREFIX = "neutron:"

DEVICE_OWNER_ROUTER_HA_INTF = (DEVICE_OWNER_NETWORK_PREFIX +
                               "router_ha_interface")
DEVICE_OWNER_ROUTER_INTF = DEVICE_OWNER_NETWORK_PREFIX + "router_interface"
DEVICE_OWNER_ROUTER_GW = DEVICE_OWNER_NETWORK_PREFIX + "router_gateway"
DEVICE_OWNER_FLOATINGIP = DEVICE_OWNER_NETWORK_PREFIX + "floatingip"
DEVICE_OWNER_DHCP = DEVICE_OWNER_NETWORK_PREFIX + "dhcp"
DEVICE_OWNER_DVR_INTERFACE = (DEVICE_OWNER_NETWORK_PREFIX +
                              "router_interface_distributed")
DEVICE_OWNER_AGENT_GW = (DEVICE_OWNER_NETWORK_PREFIX +
                         "floatingip_agent_gateway")
DEVICE_OWNER_ROUTER_SNAT = (DEVICE_OWNER_NETWORK_PREFIX +
                            "router_centralized_snat")
DEVICE_OWNER_LOADBALANCER = DEVICE_OWNER_NEUTRON_PREFIX + "LOADBALANCER"
DEVICE_OWNER_LOADBALANCERV2 = DEVICE_OWNER_NEUTRON_PREFIX + "LOADBALANCERV2"

DEVICE_OWNER_PREFIXES = (DEVICE_OWNER_NETWORK_PREFIX,
                         DEVICE_OWNER_NEUTRON_PREFIX)

# Collection used to identify devices owned by router interfaces.
# DEVICE_OWNER_ROUTER_HA_INTF is a special case and so is not included.
ROUTER_INTERFACE_OWNERS = (DEVICE_OWNER_ROUTER_INTF,
                           DEVICE_OWNER_DVR_INTERFACE)
ROUTER_INTERFACE_OWNERS_SNAT = (DEVICE_OWNER_ROUTER_INTF,
                                DEVICE_OWNER_DVR_INTERFACE,
                                DEVICE_OWNER_ROUTER_SNAT)
FLOATINGIP_KEY = '_floatingips'
INTERFACE_KEY = '_interfaces'
HA_INTERFACE_KEY = '_ha_interface'

IPv4 = 'IPv4'
IPv6 = 'IPv6'
IP_VERSION_4 = 4
IP_VERSION_6 = 6
IPv4_BITS = 32
IPv6_BITS = 128

INVALID_MAC_ADDRESSES = ['00:00:00:00:00:00', 'FF:FF:FF:FF:FF:FF']

IPv4_ANY = '0.0.0.0/0'
IPv6_ANY = '::/0'
IP_ANY = {IP_VERSION_4: IPv4_ANY, IP_VERSION_6: IPv6_ANY}

DHCP_RESPONSE_PORT = 68

FLOODING_ENTRY = ('00:00:00:00:00:00', '0.0.0.0')

AGENT_TYPE_DHCP = 'DHCP agent'
AGENT_TYPE_OVS = 'Open vSwitch agent'
AGENT_TYPE_LINUXBRIDGE = 'Linux bridge agent'
AGENT_TYPE_OFA = 'OFA driver agent'
AGENT_TYPE_L3 = 'L3 agent'
AGENT_TYPE_LOADBALANCER = 'Loadbalancer agent'
AGENT_TYPE_METERING = 'Metering agent'
AGENT_TYPE_METADATA = 'Metadata agent'
AGENT_TYPE_NIC_SWITCH = 'NIC Switch agent'
L2_AGENT_TOPIC = 'N/A'

PORT_BINDING_EXT_ALIAS = 'binding'
L3_AGENT_SCHEDULER_EXT_ALIAS = 'l3_agent_scheduler'
DHCP_AGENT_SCHEDULER_EXT_ALIAS = 'dhcp_agent_scheduler'
LBAAS_AGENT_SCHEDULER_EXT_ALIAS = 'lbaas_agent_scheduler'
L3_DISTRIBUTED_EXT_ALIAS = 'dvr'
L3_HA_MODE_EXT_ALIAS = 'l3-ha'
SUBNET_ALLOCATION_EXT_ALIAS = 'subnet_allocation'

# Protocol names and numbers for Security Groups/Firewalls
PROTO_NAME_TCP = 'tcp'
PROTO_NAME_ICMP = 'icmp'
PROTO_NAME_ICMP_V6 = 'icmpv6'
PROTO_NAME_UDP = 'udp'
PROTO_NUM_TCP = 6
PROTO_NUM_ICMP = 1
PROTO_NUM_ICMP_V6 = 58
PROTO_NUM_UDP = 17

# List of ICMPv6 types that should be allowed by default:
# Multicast Listener Query (130),
# Multicast Listener Report (131),
# Multicast Listener Done (132),
# Neighbor Solicitation (135),
# Neighbor Advertisement (136)
ICMPV6_ALLOWED_TYPES = [130, 131, 132, 135, 136]
ICMPV6_TYPE_RA = 134
ICMPV6_TYPE_NA = 136

# Device names start with "tap"
TAP_DEVICE_PREFIX = 'tap'

# Time format
ISO8601_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'
