# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from neutron_lib.api.definitions import bgp
from neutron_lib import constants


ALIAS = 'bgp_4byte_asn'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = "BGP 4-byte AS numbers"
DESCRIPTION = "Support bgp 4-byte AS number"
UPDATED_TIMESTAMP = '2017-09-07T00:00:00-00:00'


RESOURCE_ATTRIBUTE_MAP = {
    'bgp-speakers': {
        'local_as': {'allow_post': True, 'allow_put': False,
                     'validate': {'type:range': (constants.MIN_ASNUM,
                                                 constants.MAX_4BYTE_ASNUM)},
                     'is_visible': True, 'default': None,
                     'required_by_policy': False,
                     'enforce_policy': False}
    },
    'bgp-peers': {
        'remote_as': {'allow_post': True, 'allow_put': False,
                      'validate': {'type:range': (constants.MIN_ASNUM,
                                                  constants.MAX_4BYTE_ASNUM)},
                      'is_visible': True, 'default': None,
                      'required_by_policy': False,
                      'enforce_policy': False}
    }
}
SUB_RESOURCE_ATTRIBUTE_MAP = None
ACTION_MAP = {}
ACTION_STATUS = {}
REQUIRED_EXTENSIONS = [bgp.ALIAS]
OPTIONAL_EXTENSIONS = []
