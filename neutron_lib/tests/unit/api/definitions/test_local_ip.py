# Copyright 2021 Huawei, Inc.
# All rights reserved.
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

from neutron_lib.api.definitions import local_ip
from neutron_lib.tests.unit.api.definitions import base


class LocalIPDefinitionTestCase(base.DefinitionBaseTestCase):
    extension_module = local_ip
    extension_resources = (local_ip.COLLECTION_NAME,)
    extension_subresources = (local_ip.LOCAL_IP_ASSOCIATIONS,)
    extension_attributes = ('local_port_id', 'local_ip_address', 'ip_mode',
                            'local_ip_id', 'fixed_port_id', 'fixed_ip', 'host')
