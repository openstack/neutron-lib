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
DEVICE_OWNER_BAREMETAL_PREFIX = "baremetal:"

DEVICE_OWNER_ROUTER_HA_INTF = (DEVICE_OWNER_NETWORK_PREFIX +
                               "router_ha_interface")
DEVICE_OWNER_HA_REPLICATED_INT = (DEVICE_OWNER_NETWORK_PREFIX +
                                  "ha_router_replicated_interface")
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
DEVICE_OWNER_ROUTED = (DEVICE_OWNER_NETWORK_PREFIX + "routed")
# TODO(johnsom) Remove after these stop being used. Neutron-LBaaS is now
#               retired (train) and these should no longer be necessary.
DEVICE_OWNER_LOADBALANCER = DEVICE_OWNER_NEUTRON_PREFIX + "LOADBALANCER"
DEVICE_OWNER_LOADBALANCERV2 = DEVICE_OWNER_NEUTRON_PREFIX + "LOADBALANCERV2"

# Device owner for distributed services (e.g OVN Metadata/DHCP).
DEVICE_OWNER_DISTRIBUTED = DEVICE_OWNER_NETWORK_PREFIX + "distributed"

DEVICE_OWNER_PREFIXES = (DEVICE_OWNER_NETWORK_PREFIX,
                         DEVICE_OWNER_NEUTRON_PREFIX)

# Collection used to identify devices owned by router interfaces.
# DEVICE_OWNER_ROUTER_HA_INTF is a special case and so is not included.
ROUTER_INTERFACE_OWNERS = (DEVICE_OWNER_ROUTER_INTF,
                           DEVICE_OWNER_HA_REPLICATED_INT,
                           DEVICE_OWNER_DVR_INTERFACE)
ROUTER_INTERFACE_OWNERS_SNAT = (DEVICE_OWNER_ROUTER_INTF,
                                DEVICE_OWNER_HA_REPLICATED_INT,
                                DEVICE_OWNER_DVR_INTERFACE,
                                DEVICE_OWNER_ROUTER_SNAT)

DEVICE_ID_RESERVED_DHCP_PORT = 'reserved_dhcp_port'

FLOATINGIP_KEY = '_floatingips'
PORT_FORWARDING_FLOATINGIP_KEY = '_pf_floatingips'
INTERFACE_KEY = '_interfaces'
HA_INTERFACE_KEY = '_ha_interface'

IPv4 = 'IPv4'
IPv6 = 'IPv6'
IP_VERSION_4 = 4
IP_VERSION_6 = 6
IPv4_BITS = 32
IPv6_BITS = 128

BROADCAST_MAC = 'FF:FF:FF:FF:FF:FF'
INVALID_MAC_ADDRESSES = ['00:00:00:00:00:00', BROADCAST_MAC]

IPv4_ANY = '0.0.0.0/0'
IPv6_ANY = '::/0'
IP_ANY = {IP_VERSION_4: IPv4_ANY, IP_VERSION_6: IPv6_ANY}

IPv6_LLA_PREFIX = 'fe80::/64'

DHCP_CLIENT_PORT = 68
DHCP_RESPONSE_PORT = 67
DHCPV6_CLIENT_PORT = 546
DHCPV6_RESPONSE_PORT = 547

FLOODING_ENTRY = ('00:00:00:00:00:00', '0.0.0.0')

# Agent process name and description
AGENT_PROCESS_DHCP = 'neutron-dhcp-agent'
AGENT_PROCESS_L3 = 'neutron-l3-agent'
AGENT_PROCESS_LINUXBRIDGE = 'neutron-linuxbridge-agent'
AGENT_PROCESS_MACVTAP = 'neutron-macvtap-agent'
AGENT_PROCESS_METADATA = 'neutron-metadata-agent'
AGENT_PROCESS_METERING = 'neutron-metering-agent'
AGENT_PROCESS_NIC_SWITCH = 'neutron-sriov-nic-agent'
AGENT_PROCESS_OVN_METADATA = 'neutron-ovn-metadata-agent'
AGENT_PROCESS_OVS = 'neutron-openvswitch-agent'

AGENT_TYPE_DHCP = 'DHCP agent'
AGENT_TYPE_L3 = 'L3 agent'
AGENT_TYPE_LINUXBRIDGE = 'Linux bridge agent'
AGENT_TYPE_MACVTAP = 'Macvtap agent'
AGENT_TYPE_METADATA = 'Metadata agent'
AGENT_TYPE_METERING = 'Metering agent'
AGENT_TYPE_NIC_SWITCH = 'NIC Switch agent'
AGENT_TYPE_OFA = 'OFA driver agent'
AGENT_TYPE_OVS = 'Open vSwitch agent'

L2_AGENT_TOPIC = 'N/A'

L3_AGENT_MODE_DVR = 'dvr'
L3_AGENT_MODE_DVR_SNAT = 'dvr_snat'
L3_AGENT_MODE_LEGACY = 'legacy'
L3_AGENT_MODE = 'agent_mode'
L3_AGENT_MODE_DVR_NO_EXTERNAL = 'dvr_no_external'

DVR_SNAT_BOUND = 'dvr_snat_bound'
PORT_BINDING_EXT_ALIAS = 'binding'
L3_AGENT_SCHEDULER_EXT_ALIAS = 'l3_agent_scheduler'
DHCP_AGENT_SCHEDULER_EXT_ALIAS = 'dhcp_agent_scheduler'
L3_DISTRIBUTED_EXT_ALIAS = 'dvr'
L3_HA_MODE_EXT_ALIAS = 'l3-ha'
SUBNET_ALLOCATION_EXT_ALIAS = 'subnet_allocation'

# Protocol names and numbers for Security Groups/Firewalls
PROTO_NAME_AH = 'ah'
PROTO_NAME_DCCP = 'dccp'
PROTO_NAME_EGP = 'egp'
PROTO_NAME_ESP = 'esp'
PROTO_NAME_GRE = 'gre'
PROTO_NAME_HOPOPT = 'hopopt'
PROTO_NAME_ICMP = 'icmp'
PROTO_NAME_IGMP = 'igmp'
PROTO_NAME_IP = 'ip'
PROTO_NAME_IPIP = 'ipip'
PROTO_NAME_IPV6_ENCAP = 'ipv6-encap'
PROTO_NAME_IPV6_FRAG = 'ipv6-frag'
PROTO_NAME_IPV6_ICMP = 'ipv6-icmp'
# For backward-compatibility of security group rule API, we keep the old value
# for IPv6 ICMP. It should be clean up in the future.
PROTO_NAME_IPV6_ICMP_LEGACY = 'icmpv6'
PROTO_NAME_IPV6_NONXT = 'ipv6-nonxt'
PROTO_NAME_IPV6_OPTS = 'ipv6-opts'
PROTO_NAME_IPV6_ROUTE = 'ipv6-route'
PROTO_NAME_OSPF = 'ospf'
PROTO_NAME_PGM = 'pgm'
PROTO_NAME_RSVP = 'rsvp'
PROTO_NAME_SCTP = 'sctp'
PROTO_NAME_TCP = 'tcp'
PROTO_NAME_UDP = 'udp'
PROTO_NAME_UDPLITE = 'udplite'
PROTO_NAME_VRRP = 'vrrp'

PROTO_NUM_AH = 51
PROTO_NUM_DCCP = 33
PROTO_NUM_EGP = 8
PROTO_NUM_ESP = 50
PROTO_NUM_GRE = 47
PROTO_NUM_HOPOPT = 0
PROTO_NUM_ICMP = 1
PROTO_NUM_IGMP = 2
PROTO_NUM_IP = 0
PROTO_NUM_IPIP = 4
PROTO_NUM_IPV6_ENCAP = 41
PROTO_NUM_IPV6_FRAG = 44
PROTO_NUM_IPV6_ICMP = 58
PROTO_NUM_IPV6_NONXT = 59
PROTO_NUM_IPV6_OPTS = 60
PROTO_NUM_IPV6_ROUTE = 43
PROTO_NUM_OSPF = 89
PROTO_NUM_PGM = 113
PROTO_NUM_RSVP = 46
PROTO_NUM_SCTP = 132
PROTO_NUM_TCP = 6
PROTO_NUM_UDP = 17
PROTO_NUM_UDPLITE = 136
PROTO_NUM_VRRP = 112

IP_PROTOCOL_MAP = {PROTO_NAME_AH: PROTO_NUM_AH,
                   PROTO_NAME_DCCP: PROTO_NUM_DCCP,
                   PROTO_NAME_EGP: PROTO_NUM_EGP,
                   PROTO_NAME_ESP: PROTO_NUM_ESP,
                   PROTO_NAME_GRE: PROTO_NUM_GRE,
                   PROTO_NAME_HOPOPT: PROTO_NUM_HOPOPT,
                   PROTO_NAME_ICMP: PROTO_NUM_ICMP,
                   PROTO_NAME_IGMP: PROTO_NUM_IGMP,
                   PROTO_NAME_IP: PROTO_NUM_IP,
                   PROTO_NAME_IPIP: PROTO_NUM_IPIP,
                   PROTO_NAME_IPV6_ENCAP: PROTO_NUM_IPV6_ENCAP,
                   PROTO_NAME_IPV6_FRAG: PROTO_NUM_IPV6_FRAG,
                   PROTO_NAME_IPV6_ICMP: PROTO_NUM_IPV6_ICMP,
                   # For backward-compatibility of security group rule API
                   PROTO_NAME_IPV6_ICMP_LEGACY: PROTO_NUM_IPV6_ICMP,
                   PROTO_NAME_IPV6_NONXT: PROTO_NUM_IPV6_NONXT,
                   PROTO_NAME_IPV6_OPTS: PROTO_NUM_IPV6_OPTS,
                   PROTO_NAME_IPV6_ROUTE: PROTO_NUM_IPV6_ROUTE,
                   PROTO_NAME_OSPF: PROTO_NUM_OSPF,
                   PROTO_NAME_PGM: PROTO_NUM_PGM,
                   PROTO_NAME_RSVP: PROTO_NUM_RSVP,
                   PROTO_NAME_SCTP: PROTO_NUM_SCTP,
                   PROTO_NAME_TCP: PROTO_NUM_TCP,
                   PROTO_NAME_UDP: PROTO_NUM_UDP,
                   PROTO_NAME_UDPLITE: PROTO_NUM_UDPLITE,
                   PROTO_NAME_VRRP: PROTO_NUM_VRRP}

# Note that this differs from IP_PROTOCOL_MAP because iptables refers to IPv6
# ICMP as 'icmp6' whereas it is 'ipv6-icmp' in IP_PROTOCOL_MAP.
IPTABLES_PROTOCOL_MAP = {PROTO_NAME_DCCP: 'dccp',
                         PROTO_NAME_ICMP: 'icmp',
                         PROTO_NAME_IPV6_ICMP: 'icmp6',
                         PROTO_NAME_SCTP: 'sctp',
                         PROTO_NAME_TCP: 'tcp',
                         PROTO_NAME_UDP: 'udp'}

# IP header length
IP_HEADER_LENGTH = {
    4: 20,
    6: 40,
}

# ICMPv6 types:
# Destination Unreachable (1)
ICMPV6_TYPE_DEST_UNREACH = 1
# Packet Too Big (2)
ICMPV6_TYPE_PKT_TOOBIG = 2
# Time Exceeded (3)
ICMPV6_TYPE_TIME_EXCEED = 3
# Parameter Problem (4)
ICMPV6_TYPE_PARAMPROB = 4
# Echo Request (128)
ICMPV6_TYPE_ECHO_REQUEST = 128
# Echo Reply (129)
ICMPV6_TYPE_ECHO_REPLY = 129
# Multicast Listener Query (130)
ICMPV6_TYPE_MLD_QUERY = 130
# Multicast Listener Report (131)
ICMPV6_TYPE_MLD_REPORT = 131
# Multicast Listener Done (132)
ICMPV6_TYPE_MLD_DONE = 132
# Router Solicitation (133)
ICMPV6_TYPE_RS = 133
# Router Advertisement (134)
ICMPV6_TYPE_RA = 134
# Neighbor Solicitation (135)
ICMPV6_TYPE_NS = 135
# Neighbor Advertisement (136)
ICMPV6_TYPE_NA = 136
# Multicast Listener v2 Report (143)
ICMPV6_TYPE_MLD2_REPORT = 143

# List of ICMPv6 types that should be allowed from the unspecified address for
# Duplicate Address Detection:
ICMPV6_ALLOWED_UNSPEC_ADDR_TYPES = [ICMPV6_TYPE_MLD_REPORT,
                                    ICMPV6_TYPE_NS,
                                    ICMPV6_TYPE_MLD2_REPORT]

# Human-readable ID to which the subnetpool ID should be set to
# indicate that IPv6 Prefix Delegation is enabled for a given subnetpool
IPV6_PD_POOL_ID = 'prefix_delegation'

# Device names start with "tap"
TAP_DEVICE_PREFIX = 'tap'

# Device names start with "macvtap"
MACVTAP_DEVICE_PREFIX = 'macvtap'

# Linux interface max length
DEVICE_NAME_MAX_LEN = 15

# Time format
ISO8601_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'

DHCPV6_STATEFUL = 'dhcpv6-stateful'
DHCPV6_STATELESS = 'dhcpv6-stateless'
IPV6_SLAAC = 'slaac'
IPV6_MODES = [DHCPV6_STATEFUL, DHCPV6_STATELESS, IPV6_SLAAC]

ACTIVE_PENDING_STATUSES = (
    ACTIVE,
    PENDING_CREATE,
    PENDING_UPDATE
)

# Network Type constants
TYPE_FLAT = 'flat'
TYPE_GENEVE = 'geneve'
TYPE_GRE = 'gre'
TYPE_LOCAL = 'local'
TYPE_VXLAN = 'vxlan'
TYPE_VLAN = 'vlan'
TYPE_NONE = 'none'

# List of supported network segment range types
NETWORK_SEGMENT_RANGE_TYPES = [TYPE_VLAN, TYPE_VXLAN, TYPE_GRE, TYPE_GENEVE]

# Values for network_type

# For VLAN Network
MIN_VLAN_TAG = 1
MAX_VLAN_TAG = 4094

# For Geneve Tunnel
MIN_GENEVE_VNI = 1
MAX_GENEVE_VNI = 2 ** 24 - 1

# For GRE Tunnel
MIN_GRE_ID = 1
MAX_GRE_ID = 2 ** 32 - 1

# For VXLAN Tunnel
MIN_VXLAN_VNI = 1
MAX_VXLAN_VNI = 2 ** 24 - 1
VXLAN_UDP_PORT = 4789

# Overlay (tunnel) protocol overhead
GENEVE_ENCAP_MIN_OVERHEAD = 30
GRE_ENCAP_OVERHEAD = 22
VXLAN_ENCAP_OVERHEAD = 30

# For DNS extension
DNS_DOMAIN_DEFAULT = 'openstacklocal.'
DNS_LABEL_KEYWORDS = ['project_id', 'project_name', 'user_name', 'user_id']
DNS_LABEL_MAX_LEN = 63
DNS_LABEL_REGEX = "^([a-z0-9-]{1,%d}|%s)$" % (
                   DNS_LABEL_MAX_LEN,
                   '<' + '>|<'.join(DNS_LABEL_KEYWORDS) + '>')

# max value for TCP, UDP, SCTP ports
PORT_MAX = 2**16 - 1

VALID_DSCP_MARKS = [0, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34,
                    36, 38, 40, 46, 48, 56]

INGRESS_DIRECTION = 'ingress'
EGRESS_DIRECTION = 'egress'
VALID_DIRECTIONS = (INGRESS_DIRECTION, EGRESS_DIRECTION)

PROVISIONAL_IPV6_PD_PREFIX = '::/64'

# Traffic control
TC_QDISC_TYPE_HTB = 'htb'
TC_QDISC_TYPE_TBF = 'tbf'
TC_QDISC_TYPE_INGRESS = 'ingress'
TC_QDISC_TYPES = (TC_QDISC_TYPE_HTB, TC_QDISC_TYPE_TBF, TC_QDISC_TYPE_INGRESS)

TC_QDISC_INGRESS_ID = 'ffff:'

TC_QDISC_PARENTS = {'root': 0xffffffff,
                    'ingress': 0xfffffff1}


class Sentinel(object):
    """A constant object that does not change even when copied."""
    def __deepcopy__(self, memo):
        # Always return the same object because this is essentially a constant.
        return self

    def __copy__(self):
        # called via copy.copy(x)
        return self


#############################
# Attribute related constants
#############################

ATTR_NOT_SPECIFIED = Sentinel()

DICT_POPULATE_DEFAULTS = 'dict_populate_defaults'

HEX_ELEM = '[0-9A-Fa-f]'
UUID_PATTERN = '-'.join([HEX_ELEM + '{8}', HEX_ELEM + '{4}',
                         HEX_ELEM + '{4}', HEX_ELEM + '{4}',
                         HEX_ELEM + '{12}'])

SHARED = 'shared'


##########################
# Device related constants
##########################
# vhost-user device names start with "vhu"
VHOST_USER_DEVICE_PREFIX = 'vhu'
# The vswitch side of a veth pair for a nova iptables filter setup
VETH_DEVICE_PREFIX = 'qvo'
# prefix for SNAT interface in DVR
SNAT_INT_DEV_PREFIX = 'sg-'


ROUTER_PORT_OWNERS = ROUTER_INTERFACE_OWNERS_SNAT + (DEVICE_OWNER_ROUTER_GW,)

ROUTER_STATUS_ACTIVE = 'ACTIVE'
ROUTER_STATUS_ALLOCATING = 'ALLOCATING'
ROUTER_STATUS_ERROR = 'ERROR'

VALID_ROUTER_STATUS = (ROUTER_STATUS_ACTIVE,
                       ROUTER_STATUS_ALLOCATING,
                       ROUTER_STATUS_ERROR)

HA_ROUTER_STATE_KEY = '_ha_state'
METERING_LABEL_KEY = '_metering_labels'
FLOATINGIP_AGENT_INTF_KEY = '_floatingip_agent_interfaces'
SNAT_ROUTER_INTF_KEY = '_snat_router_interfaces'

HA_NETWORK_NAME = 'HA network tenant %s'
HA_SUBNET_NAME = 'HA subnet tenant %s'
HA_PORT_NAME = 'HA port tenant %s'
HA_ROUTER_STATE_ACTIVE = 'active'
HA_ROUTER_STATE_STANDBY = 'standby'
HA_ROUTER_STATE_UNKNOWN = 'unknown'
VALID_HA_STATES = (HA_ROUTER_STATE_ACTIVE, HA_ROUTER_STATE_STANDBY,
                   HA_ROUTER_STATE_UNKNOWN)

PAGINATION_INFINITE = 'infinite'

SORT_DIRECTION_ASC = 'asc'
SORT_DIRECTION_DESC = 'desc'

ETHERTYPE_NAME_ARP = 'arp'
ETHERTYPE_ARP = 0x0806
ETHERTYPE_RARP = 0x8035
ETHERTYPE_IP = 0x0800
ETHERTYPE_IPV6 = 0x86DD

IP_PROTOCOL_NAME_ALIASES = {PROTO_NAME_IPV6_ICMP_LEGACY:
                            PROTO_NAME_IPV6_ICMP}

# We only want one mapping from '58' to 'ipv6-icmp' since that is the
# normalized string, the name to number mapping can have both
IP_PROTOCOL_NUM_TO_NAME_MAP = ({str(v): k for k, v in IP_PROTOCOL_MAP.items()
                               if k != PROTO_NAME_IPV6_ICMP_LEGACY})

# When using iptables-save we specify '-p {proto}',
# but sometimes those values are not identical.  This is a map
# of known protocol numbers that require a name to be used and
# protocol names that require a different name to be used,
# because that is how iptables-save will display them.
#
# This is how the list was created, so there is a possibility
# it will need to be updated in the future:
#
# $ for num in {0..255}; do iptables -A INPUT -p $num; done
# $ iptables-save
#
# These cases are special, and were found by inspection:
# - 'ipv6-encap' uses 'ipv6'
# - 'icmpv6' uses 'ipv6-icmp'
# - 'pgm' uses '113' instead of its name
# - protocol '0' uses no -p argument
IPTABLES_PROTOCOL_NAME_MAP = {PROTO_NAME_IPV6_ENCAP: 'ipv6',
                              PROTO_NAME_IPV6_ICMP_LEGACY:
                                  'ipv6-icmp',
                              PROTO_NAME_PGM: '113',
                              '0': None,
                              '1': 'icmp',
                              '2': 'igmp',
                              '3': 'ggp',
                              '4': 'ipencap',
                              '5': 'st',
                              '6': 'tcp',
                              '8': 'egp',
                              '9': 'igp',
                              '12': 'pup',
                              '17': 'udp',
                              '20': 'hmp',
                              '22': 'xns-idp',
                              '27': 'rdp',
                              '29': 'iso-tp4',
                              '33': 'dccp',
                              '36': 'xtp',
                              '37': 'ddp',
                              '38': 'idpr-cmtp',
                              '41': 'ipv6',
                              '43': 'ipv6-route',
                              '44': 'ipv6-frag',
                              '45': 'idrp',
                              '46': 'rsvp',
                              '47': 'gre',
                              '50': 'esp',
                              '51': 'ah',
                              '57': 'skip',
                              '58': 'ipv6-icmp',
                              '59': 'ipv6-nonxt',
                              '60': 'ipv6-opts',
                              '73': 'rspf',
                              '81': 'vmtp',
                              '88': 'eigrp',
                              '89': 'ospf',
                              '93': 'ax.25',
                              '94': 'ipip',
                              '97': 'etherip',
                              '98': 'encap',
                              '103': 'pim',
                              '108': 'ipcomp',
                              '112': 'vrrp',
                              '115': 'l2tp',
                              '124': 'isis',
                              '132': 'sctp',
                              '133': 'fc',
                              '135': 'mobility-header',
                              '136': 'udplite',
                              '137': 'mpls-in-ip',
                              '138': 'manet',
                              '139': 'hip',
                              '140': 'shim6',
                              '141': 'wesp',
                              '142': 'rohc'}

# A length of a iptables chain name must be less than or equal to 11
# characters.
# <max length of iptables chain name> - (<binary_name> + '-') = 28-(16+1) = 11
MAX_IPTABLES_CHAIN_LEN_WRAP = 11
MAX_IPTABLES_CHAIN_LEN_NOWRAP = 28

# Timeout in seconds for getting an IPv6 LLA
LLA_TASK_TIMEOUT = 40

# length of all device prefixes (e.g. qvo, tap, qvb)
LINUX_DEV_PREFIX_LEN = 3
# must be shorter than linux IFNAMSIZ (which is 16)
LINUX_DEV_LEN = 14

# Possible prefixes to partial port IDs in interface names used by the OVS,
# Linux Bridge, and IVS VIF drivers in Nova and the neutron agents. See the
# 'get_ovs_interfaceid' method in Nova (nova/virt/libvirt/vif.py) for details.
INTERFACE_PREFIXES = (TAP_DEVICE_PREFIX,
                      VETH_DEVICE_PREFIX,
                      SNAT_INT_DEV_PREFIX)

ATTRIBUTES_TO_UPDATE = 'attributes_to_update'

# TODO(amuller): Re-define the RPC namespaces once Oslo messaging supports
# Targets with multiple namespaces. Neutron will then implement callbacks
# for its RPC clients in order to support rolling upgrades.

# RPC Interface for agents to call DHCP API implemented on the plugin side
RPC_NAMESPACE_DHCP_PLUGIN = None
# RPC interface for the metadata service to get info from the plugin side
RPC_NAMESPACE_METADATA = None
# RPC interface for agent to plugin security group API
RPC_NAMESPACE_SECGROUP = None
# RPC interface for agent to plugin DVR api
RPC_NAMESPACE_DVR = None
# RPC interface for reporting state back to the plugin
RPC_NAMESPACE_STATE = None
# RPC interface for agent to plugin resources API
RPC_NAMESPACE_RESOURCES = None

# Default network MTU value when not configured
DEFAULT_NETWORK_MTU = 1500
IPV6_MIN_MTU = 1280

ROUTER_MARK_MASK = "0xffff"

VALID_ETHERTYPES = (IPv4, IPv6)

IP_ALLOWED_VERSIONS = [IP_VERSION_4, IP_VERSION_6]

PORT_RANGE_MIN = 1
PORT_RANGE_MAX = 65535

ETHERTYPE_MIN = 0
ETHERTYPE_MAX = 65535

# Configuration values for accept_ra sysctl, copied from linux kernel
# networking (netdev) tree, file Documentation/networking/ip-sysctl.txt
#
# Possible values are:
#         0 Do not accept Router Advertisements.
#         1 Accept Router Advertisements if forwarding is disabled.
#         2 Overrule forwarding behaviour. Accept Router Advertisements
#           even if forwarding is enabled.
ACCEPT_RA_DISABLED = 0
ACCEPT_RA_WITHOUT_FORWARDING = 1
ACCEPT_RA_WITH_FORWARDING = 2

# Some components communicate using private address ranges, define
# them all here. These address ranges should not cause any issues
# even if they overlap since they are used in disjoint namespaces,
# but for now they are unique.
# We define the metadata cidr since it falls in the range.
PRIVATE_CIDR_RANGE = '169.254.0.0/16'
DVR_FIP_LL_CIDR = '169.254.64.0/18'
L3_HA_NET_CIDR = '169.254.192.0/18'

# Well-known addresses of the metadata service.
# When binding to an address, used with a port.
METADATA_V4_IP = '169.254.169.254'
# When configuring an address on an interface.
# When adding a route.
METADATA_V4_CIDR = '169.254.169.254/32'
# When checking if a metadata subnet is present.
METADATA_V4_SUBNET = '169.254.0.0/16'

METADATA_V6_IP = 'fe80::a9fe:a9fe'
METADATA_V6_CIDR = 'fe80::a9fe:a9fe/64'

METADATA_PORT = 80

# For backwards compatibility, prefer METADATA_V4_CIDR instead.
METADATA_CIDR = METADATA_V4_CIDR

# The only defined IpamAllocation status at this stage is 'ALLOCATED'.
# More states will be available in the future - e.g.: RECYCLABLE
IPAM_ALLOCATION_STATUS_ALLOCATED = 'ALLOCATED'

VALID_IPAM_ALLOCATION_STATUSES = (IPAM_ALLOCATION_STATUS_ALLOCATED,)

# Port binding states for Live Migration
PORT_BINDING_STATUSES = (ACTIVE,
                         INACTIVE)

VALID_FLOATINGIP_STATUS = (FLOATINGIP_STATUS_ACTIVE,
                           FLOATINGIP_STATUS_DOWN,
                           FLOATINGIP_STATUS_ERROR)

# Floating IP host binding states
FLOATING_IP_HOST_UNBOUND = "FLOATING_IP_HOST_UNBOUND"
FLOATING_IP_HOST_NEEDS_BINDING = "FLOATING_IP_HOST_NEEDS_BINDING"

# Possible types of values (e.g. in QoS rule types)
VALUES_TYPE_CHOICES = "choices"
VALUES_TYPE_RANGE = "range"

# Units base
SI_BASE = 1000
IEC_BASE = 1024

# Port bindings handling
NO_ACTIVE_BINDING = 'no_active_binding'

EXT_PARENT_PREFIX = 'ext_parent'

RP_BANDWIDTHS = 'resource_provider_bandwidths'
RP_INVENTORY_DEFAULTS = 'resource_provider_inventory_defaults'

# Port NUMA affinity policies, matching Nova NUMA affinity policy constants
PORT_NUMA_POLICY_REQUIRED = 'required'
PORT_NUMA_POLICY_PREFERRED = 'preferred'
PORT_NUMA_POLICY_LEGACY = 'legacy'
PORT_NUMA_POLICIES = (PORT_NUMA_POLICY_REQUIRED, PORT_NUMA_POLICY_PREFERRED,
                      PORT_NUMA_POLICY_LEGACY)

# RBAC Sharing Actions
ACCESS_SHARED = 'access_as_shared'
ACCESS_READONLY = 'access_as_readonly'
ACCESS_EXTERNAL = 'access_as_external'
