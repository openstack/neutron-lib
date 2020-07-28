# Copyright (c) 2013 OpenStack Foundation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from neutron_lib.api.definitions import agent

ALIAS = 'agent_sort_key'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Agents Sort Key'
API_PREFIX = ''
DESCRIPTION = 'Enabling the keyword sort_key for sorting in agents.'
UPDATED_TIMESTAMP = '2013-02-03T10:00:00-00:00'
is_sort_key = {'is_sort_key': True}
agents_collection = agent.RESOURCE_ATTRIBUTE_MAP[agent.COLLECTION_NAME]
RESOURCE_ATTRIBUTE_MAP = {
    agent.COLLECTION_NAME: {
        k: {**v, **is_sort_key} for k, v in agents_collection.items() if
        k != "configurations"}
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = []
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
