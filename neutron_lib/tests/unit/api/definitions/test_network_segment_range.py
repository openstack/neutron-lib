# Copyright (c) 2018 Intel Corporation.
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

from neutron_lib.api.definitions import network_segment_range
from neutron_lib import constants
from neutron_lib.tests.unit.api.definitions import base


class NetworkSegmentRangeDefinitionTestCase(base.DefinitionBaseTestCase):
    extension_module = network_segment_range
    extension_resources = (network_segment_range.COLLECTION_NAME,)
    extension_attributes = ('name', 'default', constants.SHARED,
                            'project_id', 'network_type',
                            'physical_network', 'minimum', 'maximum',
                            'used', 'available',)
