# Copyright 2018 Ericsson
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# trait prefixes to be used after CUSTOM_
TRAIT_PREFIX_VNIC_TYPE = 'VNIC_TYPE_'
TRAIT_PREFIX_PHYSNET = 'PHYSNET_'

# resource classes
CLASS_NET_BW_EGRESS_KBPS = 'NET_BW_EGR_KILOBIT_PER_SEC'
CLASS_NET_BW_INGRESS_KBPS = 'NET_BW_IGR_KILOBIT_PER_SEC'

# Optionally reported inventory parameters. Mandatory parameters like 'total'
# are left out intentionally. See also:
# https://docs.openstack.org/api-ref/placement
#        /#update-resource-provider-inventory
INVENTORY_OPTIONS = set([
    'allocation_ratio',
    'max_unit',
    'min_unit',
    'reserved',
    'step_size',
    ])
