# Copyright (c) 2015 Red Hat Inc.
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

from neutron_lib.api import converters
from neutron_lib.api.definitions import network
from neutron_lib.api.definitions import port
from neutron_lib import constants
from neutron_lib.db import constants as db_const
from neutron_lib.services.qos import constants as qos_const


BANDWIDTH_LIMIT_RULES = "bandwidth_limit_rules"
RULE_TYPES = "rule_types"
POLICIES = 'policies'
POLICY = 'policy'
DSCP_MARKING_RULES = 'dscp_marking_rules'
MIN_BANDWIDTH_RULES = 'minimum_bandwidth_rules'
_QOS_RULE_COMMON_FIELDS = {
    'id': {
        'allow_post': False, 'allow_put': False,
        'validate': {'type:uuid': None},
        'is_visible': True,
        'is_filter': True,
        'is_sort_key': True,
        'primary_key': True
    },
    'tenant_id': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': True,
        'is_visible': True
    }
}

ALIAS = 'qos'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Quality of Service'
API_PREFIX = '/' + ALIAS
DESCRIPTION = 'The Quality of Service extension.'
UPDATED_TIMESTAMP = '2015-06-08T10:00:00-00:00'
RESOURCE_ATTRIBUTE_MAP = {
    POLICIES: {
        'id': {
            'allow_post': False, 'allow_put': False,
            'validate': {'type:uuid': None},
            'is_filter': True, 'is_sort_key': True,
            'is_visible': True, 'primary_key': True
        },
        'name': {
            'allow_post': True, 'allow_put': True,
            'is_visible': True, 'default': '',
            'is_filter': True, 'is_sort_key': True,
            'validate': {'type:string': db_const.NAME_FIELD_SIZE}},
        constants.SHARED: {
            'allow_post': True, 'allow_put': True,
            'is_visible': True, 'default': False,
            'is_filter': True,
            'convert_to': converters.convert_to_boolean
        },
        'tenant_id': {
            'allow_post': True, 'allow_put': False,
            'required_by_policy': True,
            'validate': {'type:string': db_const.PROJECT_ID_FIELD_SIZE},
            'is_filter': True, 'is_sort_key': True,
            'is_visible': True
        },
        'rules': {
            'allow_post': False,
            'allow_put': False,
            'is_visible': True
        }
    },
    RULE_TYPES: {
        'type': {
            'allow_post': False, 'allow_put': False,
            'is_visible': True
        }
    },
    port.COLLECTION_NAME: {
        qos_const.QOS_POLICY_ID: {
            'allow_post': True,
            'allow_put': True,
            'is_visible': True,
            'default': None,
            'validate': {'type:uuid_or_none': None}
        }
    },
    network.COLLECTION_NAME: {
        qos_const.QOS_POLICY_ID: {
            'allow_post': True,
            'allow_put': True,
            'is_visible': True,
            'default': None,
            'validate': {'type:uuid_or_none': None}
        }
    }
}
_PARENT = {
    'collection_name': POLICIES,
    'member_name': POLICY
}
SUB_RESOURCE_ATTRIBUTE_MAP = {
    BANDWIDTH_LIMIT_RULES: {
        'parent': _PARENT,
        'parameters': dict(
            _QOS_RULE_COMMON_FIELDS,
            **{qos_const.MAX_KBPS: {
                'allow_post': True, 'allow_put': True,
                'convert_to': converters.convert_to_int,
                'is_visible': True,
                'is_filter': True,
                'is_sort_key': True,
                'validate': {
                    'type:range': [0, db_const.DB_INTEGER_MAX_VALUE]}
            },
                qos_const.MAX_BURST: {
                    'allow_post': True, 'allow_put': True,
                    'is_visible': True, 'default': 0,
                    'is_filter': True,
                    'is_sort_key': True,
                    'convert_to': converters.convert_to_int,
                    'validate': {
                        'type:range': [0, db_const.DB_INTEGER_MAX_VALUE]}}}),
    },
    DSCP_MARKING_RULES: {
        'parent': _PARENT,
        'parameters': dict(
            _QOS_RULE_COMMON_FIELDS,
            **{qos_const.DSCP_MARK: {
                'allow_post': True, 'allow_put': True,
                'convert_to': converters.convert_to_int,
                'is_visible': True,
                'is_filter': True,
                'is_sort_key': True,
                'validate': {
                    'type:values': constants.VALID_DSCP_MARKS}}})
    },
    MIN_BANDWIDTH_RULES: {
        'parent': _PARENT,
        'parameters': dict(
            _QOS_RULE_COMMON_FIELDS,
            **{qos_const.MIN_KBPS: {
                'allow_post': True, 'allow_put': True,
                'is_visible': True,
                'is_filter': True,
                'is_sort_key': True,
                'convert_to': converters.convert_to_int,
                'validate': {
                    'type:range': [0, db_const.DB_INTEGER_MAX_VALUE]}},
                qos_const.DIRECTION: {
                    'allow_post': True, 'allow_put': True,
                    'is_visible': True, 'default': constants.EGRESS_DIRECTION,
                    'is_filter': True,
                    'is_sort_key': True,
                    'validate': {
                        'type:values': [constants.EGRESS_DIRECTION]}}})
    }
}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = []
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
