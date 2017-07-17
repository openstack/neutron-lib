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

import webob.exc

from neutron_lib.api import faults
from neutron_lib.tests import _base as base


class TestFaultMap(base.BaseTestCase):

    def test_extend_fault_map(self):
        fault_map_dict = {NotImplemented: webob.exc.HTTPServiceUnavailable}
        faults.FAULT_MAP.update(fault_map_dict)
        self.assertIn(NotImplemented, faults.FAULT_MAP)
