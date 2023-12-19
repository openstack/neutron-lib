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


ALIAS = 'vpn-aes-ctr'
IS_SHIM_EXTENSION = True
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'VPN support for AES CTR mode'
DESCRIPTION = 'Add AES CTR choices for encryption algorithm'
UPDATED_TIMESTAMP = '2024-01-09T09:00:00-00:00'
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = [vpn.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}

# Additional VPN encryption algorithm constants
VPN_ENCRYPTION_ALGORITHM_AES_128_CTR = 'aes-128-ctr'
VPN_ENCRYPTION_ALGORITHM_AES_192_CTR = 'aes-192-ctr'
VPN_ENCRYPTION_ALGORITHM_AES_256_CTR = 'aes-256-ctr'

VPN_SUPPORTED_ENCRYPTION_ALGORITHMS_WITH_CTR = (
    vpn.VPN_SUPPORTED_ENCRYPTION_ALGORITHMS + [
        VPN_ENCRYPTION_ALGORITHM_AES_128_CTR,
        VPN_ENCRYPTION_ALGORITHM_AES_192_CTR,
        VPN_ENCRYPTION_ALGORITHM_AES_256_CTR,
    ]
)


RESOURCE_ATTRIBUTE_MAP = {
    vpn.IKE_POLICIES: {
        vpn.ENCRYPTION_ALGORITHM: {
            'allow_post': True,
            'allow_put': True,
            'default': vpn.VPN_ENCRYPTION_ALGORITHM_AES_128,
            'validate': {
                'type:values': VPN_SUPPORTED_ENCRYPTION_ALGORITHMS_WITH_CTR},
            'is_visible': True},
    },
    vpn.IPSEC_POLICIES: {
        vpn.ENCRYPTION_ALGORITHM: {
            'allow_post': True,
            'allow_put': True,
            'default': vpn.VPN_ENCRYPTION_ALGORITHM_AES_128,
            'validate': {
                'type:values': VPN_SUPPORTED_ENCRYPTION_ALGORITHMS_WITH_CTR},
            'is_visible': True},
    },
}
