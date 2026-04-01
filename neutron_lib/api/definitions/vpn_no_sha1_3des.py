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

from neutron_lib.api.definitions import vpn


ALIAS = 'vpn-no-sha1-3des'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'VPN remove deprecated sha1 and 3des'
DESCRIPTION = 'Remove sha1 auth and 3des encryption from VPN policies'
UPDATED_TIMESTAMP = '2025-03-30T09:00:00-00:00'
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = [vpn.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}

VPN_SUPPORTED_AUTH_ALGORITHMS_V2 = [
    alg for alg in vpn.VPN_SUPPORTED_AUTH_ALGORITHMS
    if alg != vpn.VPN_AUTH_ALGORITHM_SHA1
]

VPN_SUPPORTED_ENCRYPTION_ALGORITHMS_V2 = [
    alg for alg in vpn.VPN_SUPPORTED_ENCRYPTION_ALGORITHMS
    if alg != vpn.VPN_ENCRYPTION_ALGORITHM_3DES
]


RESOURCE_ATTRIBUTE_MAP = {
    vpn.IKE_POLICIES: {
        'auth_algorithm': {
            'allow_post': True,
            'allow_put': True,
            'default': vpn.VPN_AUTH_ALGORITHM_SHA256,
            'validate': {
                'type:values': VPN_SUPPORTED_AUTH_ALGORITHMS_V2},
            'is_visible': True},
        vpn.ENCRYPTION_ALGORITHM: {
            'allow_post': True,
            'allow_put': True,
            'default': vpn.VPN_ENCRYPTION_ALGORITHM_AES_128,
            'validate': {
                'type:values': VPN_SUPPORTED_ENCRYPTION_ALGORITHMS_V2},
            'is_visible': True},
    },
    vpn.IPSEC_POLICIES: {
        'auth_algorithm': {
            'allow_post': True,
            'allow_put': True,
            'default': vpn.VPN_AUTH_ALGORITHM_SHA256,
            'validate': {
                'type:values': VPN_SUPPORTED_AUTH_ALGORITHMS_V2},
            'is_visible': True},
        vpn.ENCRYPTION_ALGORITHM: {
            'allow_post': True,
            'allow_put': True,
            'default': vpn.VPN_ENCRYPTION_ALGORITHM_AES_128,
            'validate': {
                'type:values': VPN_SUPPORTED_ENCRYPTION_ALGORITHMS_V2},
            'is_visible': True},
    },
}
