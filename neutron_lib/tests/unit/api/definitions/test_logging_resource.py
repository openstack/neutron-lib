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

from neutron_lib.api.definitions import logging_resource
from neutron_lib.tests.unit.api.definitions import base


class LoggingResourceDefinitionTestCase(base.DefinitionBaseTestCase):
    extension_module = logging_resource
    extension_resources = (logging_resource.COLLECTION_NAME,)
    extension_subresources = (logging_resource.FIREWALL_LOGS,)
    extension_attributes = (logging_resource.ENABLED,
                            logging_resource.FIREWALL_LOGS,
                            logging_resource.LOGGING_RESOURCE_ID,
                            logging_resource.FW_EVENT,
                            logging_resource.FIREWALL_ID,)
