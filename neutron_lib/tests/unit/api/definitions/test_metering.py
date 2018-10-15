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

from neutron_lib.api.definitions import metering
from neutron_lib.services.qos import constants as qos_consts
from neutron_lib.tests.unit.api.definitions import base


class MeteringDefinitionTestCase(base.DefinitionBaseTestCase):
    extension_module = metering
    extension_resources = (metering.METERING_LABEL_RULES,
                           metering.METERING_LABELS)
    extension_attributes = ('remote_ip_prefix',
                            'excluded',
                            'metering_label_id',
                            qos_consts.DIRECTION)
