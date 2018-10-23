# Copyright (C) 2013 eNovance SAS <licensing@enovance.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from neutron_lib.api import converters
from neutron_lib import constants
from neutron_lib.db import constants as db_const
from neutron_lib.services.qos import constants as qos_consts


METERING_LABELS = 'metering_labels'
METERING_LABEL_RULES = 'metering_label_rules'

ALIAS = 'metering'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Neutron Metering'
API_PREFIX = ''
DESCRIPTION = 'Neutron Metering extension.'
UPDATED_TIMESTAMP = '2013-06-12T10:00:00-00:00'
RESOURCE_ATTRIBUTE_MAP = {
    METERING_LABELS: {
        'id': {
            'allow_post': False, 'allow_put': False,
            'is_visible': True,
            'is_filter': True,
            'is_sort_key': True,
            'primary_key': True
        },
        'name': {
            'allow_post': True, 'allow_put': False,
            'validate': {'type:string': db_const.NAME_FIELD_SIZE},
            'is_filter': True, 'is_sort_key': True,
            'is_visible': True, 'default': ''
        },
        'description': {
            'allow_post': True, 'allow_put': False,
            'validate': {
                'type:string': db_const.LONG_DESCRIPTION_FIELD_SIZE},
            'is_filter': True, 'is_sort_key': True,
            'is_visible': True, 'default': ''
        },
        'tenant_id': {
            'allow_post': True, 'allow_put': False,
            'required_by_policy': True,
            'validate': {
                'type:string': db_const.PROJECT_ID_FIELD_SIZE},
            'is_filter': True, 'is_sort_key': True,
            'is_visible': True
        },
        constants.SHARED: {
            'allow_post': True, 'allow_put': False,
            'is_filter': True, 'is_sort_key': True,
            'is_visible': True, 'default': False,
            'convert_to': converters.convert_to_boolean
        }
    },
    METERING_LABEL_RULES: {
        'id': {
            'allow_post': False, 'allow_put': False,
            'is_visible': True, 'is_filter': True,
            'is_sort_key': True, 'primary_key': True
        },
        'metering_label_id': {
            'allow_post': True, 'allow_put': False,
            'validate': {'type:uuid': None},
            'is_filter': True, 'is_sort_key': True,
            'is_visible': True, 'required_by_policy': True
        },
        qos_consts.DIRECTION: {
            'allow_post': True, 'allow_put': False,
            'is_visible': True, 'is_filter': True,
            'is_sort_key': True,
            'validate': {'type:values': constants.VALID_DIRECTIONS}
        },
        'excluded': {
            'allow_post': True, 'allow_put': False,
            'is_visible': True, 'default': False,
            'is_filter': True, 'is_sort_key': True,
            'convert_to': converters.convert_to_boolean
        },
        'remote_ip_prefix': {
            'allow_post': True, 'allow_put': False,
            'is_visible': True, 'required_by_policy': True,
            'is_filter': True, 'is_sort_key': True,
            'validate': {'type:subnet': None}
        },
        'tenant_id': {
            'allow_post': True, 'allow_put': False,
            'required_by_policy': True,
            'validate': {'type:string': db_const.PROJECT_ID_FIELD_SIZE},
            'is_visible': True
        }
    }
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = []
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
