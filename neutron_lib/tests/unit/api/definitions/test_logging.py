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

from neutron_lib.api.definitions import logging as log_api
from neutron_lib.tests.unit.api.definitions import base

EXTENSION_ATTRIBUTES = (
    'event',
    'target_id',
    'resource_type',
    'enabled',
    'resource_id',
    'type',
)


class LoggingApiTestCase(base.DefinitionBaseTestCase):
    extension_module = log_api
    extension_attributes = EXTENSION_ATTRIBUTES
    extension_resources = (log_api.LOGS,
                           log_api.LOG_TYPES,)
