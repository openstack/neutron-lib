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

from neutron_lib.api.definitions import taas
from neutron_lib.db import constants as db_const


ALIAS = 'tap-mirror'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = "Tap as a Service GRE or ERSPAN mirror"
DESCRIPTION = "Neutron Tap as a Service extension for GRE or ERSPAN mirroring."
UPDATED_TIMESTAMP = "2023-05-05T11:45:00-00:00"
RESOURCE_NAME = 'tap_mirror'
COLLECTION_NAME = 'tap_mirrors'

mirror_types_list = ['erspanv1', 'gre']
DIRECTION_SPEC = {
    'type:dict': {
        'IN': {'type:integer': None, 'default': None, 'required': False},
        'OUT': {'type:integer': None, 'default': None, 'required': False}
    }
}

RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        'id': {
            'allow_post': False, 'allow_put': False,
            'validate': {'type:uuid': None}, 'is_visible': True,
            'primary_key': True},
        'project_id': {
            'allow_post': True, 'allow_put': False,
            'validate': {'type:string': db_const.PROJECT_ID_FIELD_SIZE},
            'required_by_policy': True, 'is_filter': True,
            'is_sort_key': True, 'is_visible': True},
        'name': {
            'allow_post': True, 'allow_put': True,
            'validate': {'type:string': None},
            'is_visible': True, 'default': ''},
        'description': {
            'allow_post': True, 'allow_put': True,
            'validate': {'type:string': None},
            'is_visible': True, 'default': ''},
        'port_id': {
            'allow_post': True, 'allow_put': False,
            'validate': {'type:uuid': None},
            'enforce_policy': True, 'is_visible': True},
        'directions': {
            'allow_post': True, 'allow_put': False,
            'validate': DIRECTION_SPEC,
            'is_visible': True},
        'remote_ip': {
            'allow_post': True, 'allow_put': False,
            'validate': {'type:ip_address': None},
            'is_visible': True},
        'mirror_type': {
            'allow_post': True, 'allow_put': False,
            'validate': {'type:values': mirror_types_list},
            'is_visible': True},
    }
}

SUB_RESOURCE_ATTRIBUTE_MAP = None
ACTION_MAP = {}
ACTION_STATUS = {}
REQUIRED_EXTENSIONS = [taas.ALIAS]
OPTIONAL_EXTENSIONS = []
