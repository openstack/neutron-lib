# Copyright 2016 Hewlett Packard Development Coompany LP
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
#

from neutron_lib.api import converters as n_conv
from neutron_lib import constants
from neutron_lib.db import constants as db_const


ALIAS = 'bgp'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = "Neutron BGP Dynamic Routing Extension"
DESCRIPTION = ("Discover and advertise routes for Neutron prefixes "
               "dynamically via BGP")
UPDATED_TIMESTAMP = '2016-05-10T15:37:00-00:00'
BGP_SPEAKER_RESOURCE_NAME = 'bgp-speaker'
BGP_SPEAKER_BODY_KEY_NAME = 'bgp_speaker'
BGP_SPEAKERS = '%ss' % BGP_SPEAKER_BODY_KEY_NAME
BGP_PEER_BODY_KEY_NAME = 'bgp_peer'


RESOURCE_ATTRIBUTE_MAP = {
    BGP_SPEAKER_RESOURCE_NAME + 's': {
        'id': {'allow_post': False, 'allow_put': False,
               'validate': {'type:uuid': None},
               'is_visible': True, 'primary_key': True},
        'name': {'allow_post': True, 'allow_put': True,
                 'validate': {'type:string': db_const.NAME_FIELD_SIZE},
                 'is_visible': True, 'default': ''},
        'local_as': {'allow_post': True, 'allow_put': False,
                     'validate': {'type:range': (constants.MIN_ASNUM,
                                                 constants.MAX_ASNUM)},
                     'is_visible': True, 'default': None,
                     'required_by_policy': False,
                     'enforce_policy': False},
        'ip_version': {'allow_post': True, 'allow_put': False,
                       'validate': {'type:values': [4, 6]},
                       'is_visible': True, 'default': None,
                       'required_by_policy': False,
                       'enforce_policy': False},
        'tenant_id': {'allow_post': True, 'allow_put': False,
                      'required_by_policy': False,
                      'validate': {
                          'type:string': db_const.PROJECT_ID_FIELD_SIZE},
                      'is_visible': True},
        'peers': {'allow_post': False, 'allow_put': False,
                  'validate': {'type:uuid_list': None},
                  'is_visible': True, 'default': [],
                  'required_by_policy': False,
                  'enforce_policy': True},
        'networks': {'allow_post': False, 'allow_put': False,
                     'validate': {'type:uuid_list': None},
                     'is_visible': True, 'default': [],
                     'required_by_policy': False,
                     'enforce_policy': True},
        'advertise_floating_ip_host_routes': {
                                      'allow_post': True,
                                      'allow_put': True,
                                      'convert_to': n_conv.convert_to_boolean,
                                      'validate': {'type:boolean': None},
                                      'is_visible': True, 'default': True,
                                      'required_by_policy': False,
                                      'enforce_policy': True},
        'advertise_tenant_networks': {
                                      'allow_post': True,
                                      'allow_put': True,
                                      'convert_to': n_conv.convert_to_boolean,
                                      'validate': {'type:boolean': None},
                                      'is_visible': True, 'default': True,
                                      'required_by_policy': False,
                                      'enforce_policy': True},
    },
    'bgp-peers': {
        'id': {'allow_post': False, 'allow_put': False,
               'validate': {'type:uuid': None},
               'is_visible': True, 'primary_key': True},
        'name': {'allow_post': True, 'allow_put': True,
                 'validate': {'type:string': db_const.NAME_FIELD_SIZE},
                 'is_visible': True, 'default': ''},
        'peer_ip': {'allow_post': True, 'allow_put': False,
                    'required_by_policy': True,
                    'validate': {'type:ip_address': None},
                    'is_visible': True},
        'remote_as': {'allow_post': True, 'allow_put': False,
                      'validate': {'type:range': (constants.MIN_ASNUM,
                                                  constants.MAX_ASNUM)},
                      'is_visible': True, 'default': None,
                      'required_by_policy': False,
                      'enforce_policy': False},
        'auth_type': {'allow_post': True, 'allow_put': False,
                      'required_by_policy': True,
                      'validate': {'type:values':
                                   constants.SUPPORTED_AUTH_TYPES},
                      'is_visible': True},
        'password': {'allow_post': True, 'allow_put': True,
                     'required_by_policy': True,
                     'validate': {'type:string_or_none': None},
                     'is_visible': False,
                     'default': None},
        'tenant_id': {'allow_post': True, 'allow_put': False,
                      'required_by_policy': False,
                      'validate': {
                          'type:string': db_const.PROJECT_ID_FIELD_SIZE},
                      'is_visible': True}
    }
}
SUB_RESOURCE_ATTRIBUTE_MAP = None
ACTION_MAP = {
    BGP_SPEAKER_RESOURCE_NAME: {
        'add_bgp_peer': 'PUT',
        'remove_bgp_peer': 'PUT',
        'add_gateway_network': 'PUT',
        'remove_gateway_network': 'PUT',
        'get_advertised_routes': 'GET'
    }
}
ACTION_STATUS = {}
REQUIRED_EXTENSIONS = []
OPTIONAL_EXTENSIONS = []
