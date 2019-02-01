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

from neutron_lib.api.definitions import dvr as dvr_apidef

ALIAS = 'router-admin-state-down-before-update'
IS_SHIM_EXTENSION = True
IS_STANDARD_ATTR_EXTENSION = False
NAME = "Enforce Router's Admin State Down Before Update Extension"
DESCRIPTION = ('Ensure that the admin state of a router is DOWN '
               '(admin_state_up=False) before updating the distributed '
               'attribute')
UPDATED_TIMESTAMP = '2019-07-02T15:56:00'
RESOURCE_ATTRIBUTE_MAP = {}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = [dvr_apidef.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
