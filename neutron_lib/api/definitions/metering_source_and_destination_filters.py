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

from neutron_lib.api.definitions import metering

ALIAS = 'metering_source_and_destination_fields'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Neutron Metering with source and destination filtering'
API_PREFIX = ''
DESCRIPTION = 'Neutron Metering extension that enables the use of source ' \
              'and destination IP prefixes to create metering label rules.'
UPDATED_TIMESTAMP = '2020-08-21T08:12:00-00:00'

RESOURCE_ATTRIBUTE_MAP = {}

REQUIRED_EXTENSIONS = [metering.ALIAS]

_PARENT = {
    'collection_name': metering.METERING_LABEL_RULES,
    'member_name': metering.METERING_LABEL_RULES
}
SUB_RESOURCE_ATTRIBUTE_MAP = {
    metering.METERING_LABEL_RULES: {
        'parent': _PARENT,
        'parameters': {
            'remote_ip_prefix': {
                'allow_post': True, 'allow_put': False,
                'is_visible': True, 'required_by_policy': False,
                'is_filter': True, 'is_sort_key': True, 'default': None
            },
            'source_ip_prefix': {
                'allow_post': True, 'allow_put': True,
                'is_visible': True, 'required_by_policy': False,
                'is_filter': True, 'is_sort_key': True, 'default': None
            },
            'destination_ip_prefix': {
                'allow_post': True, 'allow_put': True,
                'is_visible': True, 'required_by_policy': False,
                'is_filter': True, 'is_sort_key': True, 'default': None
            }
        }
    }
}
ACTION_MAP = {}
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
