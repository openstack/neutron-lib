# Copyright 2021 Huawei, Inc.
# All rights reserved.
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

from neutron_lib import constants
from neutron_lib.db import constants as db_const

RESOURCE_NAME = 'local_ip'
COLLECTION_NAME = RESOURCE_NAME + 's'

LOCAL_IP_ASSOCIATION = 'port_association'
LOCAL_IP_ASSOCIATIONS = LOCAL_IP_ASSOCIATION + 's'

ALIAS = RESOURCE_NAME
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Local IP'
DESCRIPTION = 'Support Node Local Virtual IP'
UPDATED_TIMESTAMP = '2021-07-26T10:00:00-00:00'

IP_MODE_TRANSLATE = 'translate'
IP_MODE_PASSTHROUGH = 'passthrough'
VALID_IP_MODES = [IP_MODE_TRANSLATE, IP_MODE_PASSTHROUGH]

RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        'id': {
            'allow_post': False,
            'allow_put': False,
            'validate': {'type:uuid': None},
            'is_visible': True,
            'is_filter': True,
            'is_sort_key': True,
            'primary_key': True},
        'name': {
            'allow_post': True,
            'allow_put': True,
            'default': '',
            'validate': {'type:string': db_const.NAME_FIELD_SIZE},
            'is_filter': True,
            'is_sort_key': True,
            'is_visible': True},
        'description': {
            'allow_post': True,
            'allow_put': True,
            'default': '',
            'validate': {'type:string': db_const.LONG_DESCRIPTION_FIELD_SIZE},
            'is_filter': True,
            'is_sort_key': True,
            'is_visible': True},
        'project_id': {
            'allow_post': True,
            'allow_put': False,
            'validate': {'type:string': db_const.PROJECT_ID_FIELD_SIZE},
            'required_by_policy': True,
            'is_filter': True,
            'is_sort_key': True,
            'is_visible': True},
        'local_port_id': {
            'allow_post': True,
            'allow_put': False,
            'validate': {'type:uuid': None},
            'default': constants.ATTR_NOT_SPECIFIED,
            'is_filter': True,
            'is_sort_key': True,
            'is_visible': True},
        'network_id': {
            'allow_post': True,
            'allow_put': False,
            'validate': {'type:uuid': None},
            'default': constants.ATTR_NOT_SPECIFIED,
            'is_filter': True,
            'is_sort_key': True,
            'is_visible': True},
        'local_ip_address': {
            'allow_post': True,
            'allow_put': False,
            'default': constants.ATTR_NOT_SPECIFIED,
            'validate': {'type:ip_address_or_none': None},
            'is_filter': True,
            'is_sort_key': True,
            'is_visible': True,
            'enforce_policy': True},
        'ip_mode': {
            'allow_post': True,
            'allow_put': False,
            'default': IP_MODE_TRANSLATE,
            'validate': {'type:values': VALID_IP_MODES},
            'is_filter': True,
            'is_sort_key': True,
            'is_visible': True},
    }
}

SUB_RESOURCE_ATTRIBUTE_MAP = {
    LOCAL_IP_ASSOCIATIONS: {
        'parent': {'collection_name': COLLECTION_NAME,
                   'member_name': RESOURCE_NAME},
        'parameters': {
            'local_ip_id': {
                'allow_post': False,
                'allow_put': False,
                'is_visible': True},
            'local_ip_address': {
                'allow_post': False,
                'allow_put': False,
                'is_filter': True,
                'is_sort_key': True,
                'is_visible': True},
            'fixed_port_id': {
                'allow_post': True,
                'allow_put': False,
                'validate': {'type:uuid': None},
                'is_filter': True,
                'is_sort_key': True,
                'is_visible': True},
            'fixed_ip': {
                'allow_post': True,
                'allow_put': False,
                'validate': {'type:ip_address_or_none': None},
                'is_filter': True,
                'is_sort_key': True,
                'is_visible': True,
                'default': None},
            'host': {
                'allow_post': False,
                'allow_put': False,
                'is_filter': True,
                'is_sort_key': True,
                'is_visible': True},
            'project_id': {
                'allow_post': True,
                'allow_put': False,
                'validate': {'type:string': db_const.PROJECT_ID_FIELD_SIZE},
                'required_by_policy': True,
                'is_visible': False},
        }
    }
}

ACTION_MAP = {}

ACTION_STATUS = {}

REQUIRED_EXTENSIONS = []

OPTIONAL_EXTENSIONS = []
