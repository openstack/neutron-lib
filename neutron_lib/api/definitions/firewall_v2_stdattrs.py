# Copyright 2023 EasyStack Limited
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

from neutron_lib.api.definitions import firewall_v2


ALIAS = 'standard-attr-fwaas-v2'
IS_SHIM_EXTENSION = True
IS_STANDARD_ATTR_EXTENSION = True
NAME = 'Standard Attribute FWaaS v2 Extension'
DESCRIPTION = 'Add standard attributes to FWaaS v2 resources'
UPDATED_TIMESTAMP = '2023-04-027T01:00:00-00:00'
RESOURCE_ATTRIBUTE_MAP = {}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = [firewall_v2.ALIAS]
OPTIONAL_EXTENSIONS = [
    'standard-attr-description',
    'standard-attr-timestamp',
    'standard-attr-revisions'
]
ACTION_STATUS = {}
