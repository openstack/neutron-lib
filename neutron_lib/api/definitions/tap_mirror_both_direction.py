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
from neutron_lib.api.definitions import tap_mirror
from neutron_lib.types import ActionMap, ResourceAttributeMap


ALIAS = 'tap-mirror-both-direction'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = "Tap as a Service mirror with BOTH direction support"
DESCRIPTION = ("Neutron Tap as a Service extension mirroring with support "
               "for BOTH direction.")
UPDATED_TIMESTAMP = "2025-12-15T11:45:00-00:00"

RESOURCE_ATTRIBUTE_MAP: ResourceAttributeMap = {
    tap_mirror.COLLECTION_NAME: {
        'directions': {
            'allow_post': True, 'allow_put': False,
            'validate': {
                'type:dict': {
                    'IN': {
                        'type:integer': None, 'default': None,
                        'required': False},
                    'OUT': {
                        'type:integer': None, 'default': None,
                        'required': False},
                    taas.DIRECTION_BOTH: {
                        'type:integer': None, 'default': None,
                        'required': False},
                }
            },
            'is_visible': True},
    }
}

SUB_RESOURCE_ATTRIBUTE_MAP = None
ACTION_MAP: ActionMap = {}
ACTION_STATUS = {}
REQUIRED_EXTENSIONS = [tap_mirror.ALIAS]
OPTIONAL_EXTENSIONS = []
