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

from neutron_lib.api import converters
from neutron_lib.api.definitions import l3
from neutron_lib.api import validators
from neutron_lib.api.validators import bfd as bfd_validator
from neutron_lib import constants
from neutron_lib.db import constants as db_const


ALIAS = 'bfd-monitor'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'BFD monitors for Neutron'
DESCRIPTION = "Provides support for BFD monitors"
UPDATED_TIMESTAMP = "2021-07-26T11:00:00-00:00"
BFD_MONITOR = 'bfd_monitor'
BFD_MONITORS = 'bfd_monitors'
BFD_SESSION_STATUS = 'bfd_session_status'

BFD_MODE_ASYNC = 'asynchronous'
BFD_MODE_DEMAND = 'demand'
BFD_MODE_ONE_ARM = 'one_arm_echo'

AUTH_TYPE_PWD = 'password'  # nosec
AUTH_TYPE_MD5 = 'MD5'
AUTH_TYPE_METIC_MD5 = 'MeticulousMD5'
AUTH_TYPE_SHA1 = 'SHA1'
AUTH_TYPE_METIC_SHA1 = 'MeticulousSHA1'

VALID_AUTH_TYPES = (AUTH_TYPE_PWD, AUTH_TYPE_MD5, AUTH_TYPE_METIC_MD5,
                    AUTH_TYPE_SHA1, AUTH_TYPE_METIC_SHA1)
VALID_MODES = (BFD_MODE_ASYNC, BFD_MODE_DEMAND, BFD_MODE_ONE_ARM)

validators.add_validator('bfd_mode_validator',
                         bfd_validator.validate_bfd_mode)
validators.add_validator('bfd_auth_type_validator',
                         bfd_validator.validate_bfd_auth_type)

RESOURCE_ATTRIBUTE_MAP = {
    BFD_MONITORS: {
        'id': {'allow_post': False, 'allow_put': False,
               'validate': {'type:uuid': None},
               'is_visible': True,
               'primary_key': True,
               'enforce_policy': True},
        'name': {'allow_post': True, 'allow_put': True,
                 'validate': {'type:string': db_const.NAME_FIELD_SIZE},
                 'default': '', 'is_filter': True, 'is_sort_key': True,
                 'is_visible': True},
        'description': {'allow_post': True, 'allow_put': True,
                        'is_visible': True, 'default': '',
                        'validate': {
                            'type:string': db_const.DESCRIPTION_FIELD_SIZE}},
        'project_id': {'allow_post': True, 'allow_put': False,
                       'validate': {
                           'type:string': db_const.PROJECT_ID_FIELD_SIZE},
                       'required_by_policy': True,
                       'is_visible': True, 'enforce_policy': True},
        'mode': {'allow_post': True, 'allow_put': False,
                 'validate': {'type:bfd_mode_validator': VALID_MODES},
                 'default': BFD_MODE_ASYNC, 'is_filter': True,
                 'is_sort_key': True, 'is_visible': True},
        'dst_ip': {'allow_post': True, 'allow_put': False,
                   'validate': {'type:ip_address': None},
                   'is_sort_key': True, 'is_filter': True,
                   'is_visible': True, 'default': None,
                   'enforce_policy': True},
        'src_ip': {'allow_post': True, 'allow_put': False,
                   'validate': {'type:ip_address_or_none': None},
                   'is_sort_key': True, 'is_filter': True,
                   'is_visible': True, 'default': None,
                   'enforce_policy': True},
        'min_rx': {'allow_post': True, 'allow_put': True,
                   'validate': {'type:non_negative': None},
                   'convert_to': converters.convert_to_int,
                   'default': 1000,
                   'is_visible': True, 'enforce_policy': True},
        'min_tx': {'allow_post': True, 'allow_put': True,
                   'validate': {'type:non_negative': None},
                   'convert_to': converters.convert_to_int,
                   'default': 100,
                   'is_visible': True, 'enforce_policy': True},
        'multiplier': {'allow_post': True, 'allow_put': True,
                       'validate': {'type:non_negative': None},
                       'convert_to': converters.convert_to_int,
                       'default': 3,
                       'is_visible': True, 'enforce_policy': True},
        'status': {'allow_post': False, 'allow_put': False,
                   'is_filter': True, 'is_sort_key': True,
                   'is_visible': True},
        'auth_type': {'allow_post': True, 'allow_put': False,
                      'validate': {'type:bfd_auth_type_validator':
                                   VALID_AUTH_TYPES},
                      'default': constants.ATTR_NOT_SPECIFIED,
                      'is_visible': True},
        'auth_key': {'allow_post': True, 'allow_put': False,
                     'validate': {'type:dict_or_none': None},
                     'default': constants.ATTR_NOT_SPECIFIED,
                     'is_visible': True},
    },
}

SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {
    BFD_MONITOR: {
        'get_bfd_session_status': 'GET',
        'get_bfd_monitor_associations': 'GET',
    }
}
ACTION_STATUS = {}
REQUIRED_EXTENSIONS = [l3.ALIAS]
OPTIONAL_EXTENSIONS = []
