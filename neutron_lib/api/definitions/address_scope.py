# Copyright (c) 2015 Huawei Technologies Co.,LTD.
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

from neutron_lib.api import converters
from neutron_lib import constants
from neutron_lib.db import constants as db_constants


ADDRESS_SCOPE = 'address_scope'
ADDRESS_SCOPE_ID = 'address_scope_id'
IPV4_ADDRESS_SCOPE = 'ipv4_%s' % ADDRESS_SCOPE
IPV6_ADDRESS_SCOPE = 'ipv6_%s' % ADDRESS_SCOPE

ALIAS = 'address-scope'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Address scope'
API_PREFIX = ''
DESCRIPTION = 'Address scopes extension.'
UPDATED_TIMESTAMP = '2015-07-26T10:00:00-00:00'
RESOURCE_NAME = ADDRESS_SCOPE
COLLECTION_NAME = RESOURCE_NAME + 's'
RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        'id': {'allow_post': False,
               'allow_put': False,
               'validate': {'type:uuid': None},
               'is_filter': True,
               'is_sort_key': True,
               'is_visible': True,
               'primary_key': True},
        'name': {'allow_post': True,
                 'allow_put': True,
                 'default': '',
                 'validate': {'type:string': db_constants.NAME_FIELD_SIZE},
                 'is_filter': True,
                 'is_sort_key': True,
                 'is_visible': True},
        'tenant_id': {'allow_post': True,
                      'allow_put': False,
                      'validate': {
                          'type:string': db_constants.PROJECT_ID_FIELD_SIZE},
                      'required_by_policy': True,
                      'is_filter': True,
                      'is_sort_key': True,
                      'is_visible': True},
        constants.SHARED: {'allow_post': True,
                           'allow_put': True,
                           'default': False,
                           'convert_to': converters.convert_to_boolean,
                           'is_visible': True,
                           'is_filter': True,
                           'is_sort_key': True,
                           'required_by_policy': True,
                           'enforce_policy': True},
        'ip_version': {'allow_post': True, 'allow_put': False,
                       'convert_to': converters.convert_to_int,
                       'validate': {'type:values': [4, 6]},
                       'is_filter': True,
                       'is_sort_key': True,
                       'is_visible': True},
    },
    'subnetpools': {
        ADDRESS_SCOPE_ID: {'allow_post': True,
                           'allow_put': True,
                           'default': constants.ATTR_NOT_SPECIFIED,
                           'validate': {'type:uuid_or_none': None},
                           'is_filter': True,
                           'is_sort_key': True,
                           'is_visible': True}
    },
    'networks': {
        IPV4_ADDRESS_SCOPE: {'allow_post': False,
                             'allow_put': False,
                             'is_visible': True},
        IPV6_ADDRESS_SCOPE: {'allow_post': False,
                             'allow_put': False,
                             'is_visible': True},
    }
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = []
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
