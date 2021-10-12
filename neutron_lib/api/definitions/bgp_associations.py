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

from neutron_lib.api import converters as n_conv
from neutron_lib.api.definitions import bgp
from neutron_lib.db import constants as db_const

ALIAS = 'bgp-associations'
DESCRIPTION = "Allow adding router, peer association objects to BGP extension"
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'BGP Associations'
UPDATED_TIMESTAMP = "2021-07-01T11:00:00-00:00"

BGP_ASSOC_EXT_ALIAS = 'bgp-associations'
ROUTER_ASSOCIATIONS = 'router_associations'
ROUTER_ASSOCIATION = 'router_association'
PEER_ASSOCIATIONS = 'peer_associations'
PEER_ASSOCIATION = 'peer_association'

RESOURCE_ATTRIBUTE_MAP = {
    bgp.BGP_SPEAKERS: {}
}

SUB_RESOURCE_ATTRIBUTE_MAP = {
    ROUTER_ASSOCIATIONS: {
        'parent': {'collection_name': bgp.BGP_SPEAKERS,
                   'member_name': bgp.BGP_SPEAKER_BODY_KEY_NAME},
        'parameters': {
            'id': {'allow_post': False, 'allow_put': False,
                   'validate': {'type:uuid': None},
                   'is_visible': True,
                   'primary_key': True},
            'name': {'allow_post': True, 'allow_put': True,
                     'validate': {'type:string': db_const.NAME_FIELD_SIZE},
                     'default': '', 'is_filter': True, 'is_sort_key': True,
                     'is_visible': True},
            'project_id': {'allow_post': True, 'allow_put': False,
                           'validate': {
                               'type:string': db_const.PROJECT_ID_FIELD_SIZE},
                           'required_by_policy': True,
                           'is_visible': True},
            'router_id': {'allow_post': True, 'allow_put': False,
                          'validate': {'type:uuid': None},
                          'is_visible': True},
            'advertise_extra_routes': {
                                      'allow_post': True,
                                      'allow_put': True,
                                      'convert_to': n_conv.convert_to_boolean,
                                      'validate': {'type:boolean': None},
                                      'is_visible': True, 'default': True,
                                      'required_by_policy': False},
            'status': {'allow_post': False, 'allow_put': False,
                       'is_filter': True, 'is_sort_key': True,
                       'is_visible': True},
            }
    },
    PEER_ASSOCIATIONS: {
        'parent': {'collection_name': bgp.BGP_SPEAKERS,
                   'member_name': bgp.BGP_SPEAKER_BODY_KEY_NAME},
        'parameters': {
            'id': {'allow_post': False, 'allow_put': False,
                   'validate': {'type:uuid': None},
                   'is_visible': True,
                   'primary_key': True},
            'name': {'allow_post': True, 'allow_put': True,
                     'validate': {'type:string': db_const.NAME_FIELD_SIZE},
                     'default': '', 'is_filter': True, 'is_sort_key': True,
                     'is_visible': True},
            'project_id': {'allow_post': True, 'allow_put': False,
                           'validate': {
                               'type:string': db_const.PROJECT_ID_FIELD_SIZE},
                           'required_by_policy': True,
                           'is_visible': True},
            'peer_id': {'allow_post': True, 'allow_put': False,
                        'validate': {'type:uuid': None},
                        'is_visible': True},
            'status': {'allow_post': False, 'allow_put': False,
                       'is_filter': True, 'is_sort_key': True,
                       'is_visible': True},
        }
    }
}

REQUIRED_EXTENSIONS = [bgp.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_MAP = bgp.ACTION_MAP
ACTION_MAP[bgp.BGP_SPEAKER_RESOURCE_NAME].update({
    'get_routes': 'GET',
})
ACTION_STATUS = {}
