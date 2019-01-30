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
from neutron_lib.api.definitions import qos
from neutron_lib.api.definitions import qos_bw_limit_direction
from neutron_lib import constants
from neutron_lib.db import constants as db_const
from neutron_lib.services.qos import constants as q_const


BANDWIDTH_LIMIT_RULES_ALIAS = "alias_bandwidth_limit_rules"
DSCP_MARKING_RULES_ALIAS = 'alias_dscp_marking_rules'
MIN_BANDWIDTH_RULES_ALIAS = 'alias_minimum_bandwidth_rules'

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
        'allow_post': False, 'allow_put': False,
        'required_by_policy': True,
        'is_visible': True
    }
}

ALIAS = 'qos-rules-alias'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Quality of Service rules alias API'
API_PREFIX = '/' + qos.ALIAS
DESCRIPTION = ('API to enable GET, PUT and DELETE operations on QoS policy '
               'rules without specifying policy ID')
UPDATED_TIMESTAMP = '2018-10-07T10:00:00-00:00'
RESOURCE_ATTRIBUTE_MAP = {
    BANDWIDTH_LIMIT_RULES_ALIAS: dict(
        _QOS_RULE_COMMON_FIELDS,
        **{q_const.MAX_KBPS: {
            'allow_post': False, 'allow_put': True,
            'convert_to': converters.convert_to_int,
            'is_visible': True,
            'is_filter': True,
            'is_sort_key': True,
            'validate': {
                'type:range': [0, db_const.DB_INTEGER_MAX_VALUE]
            }
        },
            q_const.DIRECTION: {
                'allow_post': False,
                'allow_put': True,
                'is_visible': True,
                'is_filter': True,
                'is_sort_key': True,
                'default': constants.EGRESS_DIRECTION,
                'validate': {
                    'type:values': constants.VALID_DIRECTIONS
                }
        },
            q_const.MAX_BURST: {
                'allow_post': False, 'allow_put': True,
                'is_visible': True, 'default': 0,
                'is_filter': True,
                'is_sort_key': True,
                'convert_to': converters.convert_to_int,
                'validate': {
                    'type:range': [0, db_const.DB_INTEGER_MAX_VALUE]
                }
        }}),
    DSCP_MARKING_RULES_ALIAS: dict(
        _QOS_RULE_COMMON_FIELDS,
        **{q_const.DSCP_MARK: {
            'allow_post': False, 'allow_put': True,
            'convert_to': converters.convert_to_int,
            'is_visible': True,
            'is_filter': True,
            'is_sort_key': True,
            'validate': {
                'type:values': constants.VALID_DSCP_MARKS
            }
        }}),
    MIN_BANDWIDTH_RULES_ALIAS: dict(
        _QOS_RULE_COMMON_FIELDS,
        **{q_const.MIN_KBPS: {
            'allow_post': False, 'allow_put': True,
            'is_visible': True,
            'is_filter': True,
            'is_sort_key': True,
            'convert_to': converters.convert_to_int,
            'validate': {
                'type:range': [0, db_const.DB_INTEGER_MAX_VALUE]
            }
        },
            q_const.DIRECTION: {
                'allow_post': False, 'allow_put': True,
                'is_visible': True, 'default': constants.EGRESS_DIRECTION,
                'is_filter': True,
                'is_sort_key': True,
                'validate': {
                    'type:values': constants.VALID_DIRECTIONS
                }
            }
        }
    )
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = [qos.ALIAS, qos_bw_limit_direction.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
