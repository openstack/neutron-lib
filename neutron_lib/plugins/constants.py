# All Rights Reserved.
#
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

# Well-known service type constants:
FIREWALL = "FIREWALL"
VPN = "VPN"
METERING = "METERING"
FLAVORS = "FLAVORS"
QOS = "QOS"
CORE = 'CORE'
L3 = 'L3_ROUTER_NAT'
LOG_API = "LOGGING"
PORTFORWARDING = "PORTFORWARDING"
FLOATINGIPPOOL = "FLOATINGIPPOOL"
NETWORK_SEGMENT_RANGE = "NETWORK_SEGMENT_RANGE"
CONNTRACKHELPER = "CONNTRACKHELPER"

# TODO(johnsom) Remove after these stop being used. Neutron-LBaaS is now
#               retired (train) and these should no longer be necessary.
LOADBALANCER = "LOADBALANCER"
LOADBALANCERV2 = "LOADBALANCERV2"
