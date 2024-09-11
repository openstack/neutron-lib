# Copyright 2024 Red Hat, Inc.
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

from neutron_lib.api.definitions import port_trusted_vif
from neutron_lib.tests.unit.api.definitions import base


class PortTrustedVifDefinitionTestCase(base.DefinitionBaseTestCase):
    extension_module = port_trusted_vif
    extension_resources = (port_trusted_vif.COLLECTION_NAME,)
    extension_attributes = (port_trusted_vif.TRUSTED_VIF,)
