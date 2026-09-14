# Copyright (C) 2015 Ericsson AB
# Copyright (c) 2015 Gigamon
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


from neutron_lib.types import ActionMap, ResourceAttributeMap

DIRECTION_IN = 'IN'
DIRECTION_OUT = 'OUT'
DIRECTION_BOTH = 'BOTH'
DIRECTION_ENUM = [DIRECTION_IN, DIRECTION_OUT, DIRECTION_BOTH]
DIRECTION_IN_BOTH = [DIRECTION_IN, DIRECTION_BOTH]
DIRECTION_OUT_BOTH = [DIRECTION_OUT, DIRECTION_BOTH]

'''
Resource Attribute Map:

Note:

'tap_services' data model refers to the Tap Service created.
port_id specifies destination port to which the mirrored data is sent.
'''

ALIAS = 'taas'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = "Neutron Tap as a Service"
DESCRIPTION = "Neutron Tap as a Service Extension."
UPDATED_TIMESTAMP = "2015-01-14T10:00:00-00:00"
RESOURCE_NAME = 'tap_service'
COLLECTION_NAME = 'tap_services'
TAP_FLOW = 'tap_flow'
TAP_FLOWS = 'tap_flows'

RESOURCE_ATTRIBUTE_MAP: ResourceAttributeMap = {
    COLLECTION_NAME: {
        'id': {
            'allow_post': False,
            'allow_put': False,
            'validate': {'type:uuid': None},
            'is_visible': True,
            'is_filter': True,
            'is_sort_key': True,
            'primary_key': True
        },
        'tenant_id': {
            'allow_post': True,
            'allow_put': False,
            'validate': {'type:string': None},
            'required_by_policy': True,
            'is_visible': True,
            'is_filter': True,
            'is_sort_key': True
        },
        'name': {
            'allow_post': True,
            'allow_put': True,
            'validate': {'type:name_string': None},
            'default': '',
            'is_visible': True,
            'is_filter': True,
            'is_sort_key': True
        },
        'description': {
            'allow_post': True,
            'allow_put': True,
            'validate': {'type:string': None},
            'default': '',
            'is_visible': True,
            'is_filter': True
        },
        'port_id': {
            'allow_post': True,
            'allow_put': False,
            'validate': {'type:uuid': None},
            'is_visible': True,
            'is_filter': True
        },
        'status': {
            'allow_post': False,
            'allow_put': False,
            'is_visible': True,
            'is_filter': True
        },
    },
    TAP_FLOWS: {
        'id': {
            'allow_post': False,
            'allow_put': False,
            'validate': {'type:uuid': None},
            'is_visible': True,
            'is_filter': True,
            'is_sort_key': True,
            'primary_key': True
        },
        'tenant_id': {
            'allow_post': True,
            'allow_put': False,
            'validate': {'type:string': None},
            'required_by_policy': True,
            'is_visible': True,
            'is_filter': True,
            'is_sort_key': True
        },
        'name': {
            'allow_post': True,
            'allow_put': True,
            'validate': {'type:string': None},
            'default': '',
            'is_visible': True,
            'is_filter': True,
            'is_sort_key': True
        },
        'description': {
            'allow_post': True,
            'allow_put': True,
            'validate': {'type:string': None},
            'default': '',
            'is_visible': True,
            'is_filter': True
        },
        'tap_service_id': {
            'allow_post': True,
            'allow_put': False,
            'validate': {'type:uuid': None},
            'required_by_policy': True,
            'is_visible': True,
            'is_filter': True
        },
        'source_port': {
            'allow_post': True,
            'allow_put': False,
            'validate': {'type:uuid': None},
            'required_by_policy': True,
            'is_visible': True,
            'is_filter': True
        },
        'direction': {
            'allow_post': True,
            'allow_put': False,
            'validate': {'type:values': DIRECTION_ENUM},
            'is_visible': True,
            'is_filter': True
        },
        'status': {
            'allow_post': False,
            'allow_put': False,
            'is_visible': True,
            'is_filter': True
        },
    }
}
SUB_RESOURCE_ATTRIBUTE_MAP = None
ACTION_MAP: ActionMap = {}
ACTION_STATUS = {}
REQUIRED_EXTENSIONS = []
OPTIONAL_EXTENSIONS = []
