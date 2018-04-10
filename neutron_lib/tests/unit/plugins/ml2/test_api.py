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

from neutron_lib.plugins.ml2 import api
from neutron_lib.tests import _base as base


class _MechanismDriver(api.MechanismDriver):
    def bind_port(s, c):
        return c

    def initialize(self):
        pass


class TestMechanismDriver(base.BaseTestCase):

    def test__supports_port_binding(self):
        self.assertTrue(_MechanismDriver()._supports_port_binding)

    def test_get_workers(self):
        self.assertEqual((), _MechanismDriver().get_workers())

    def test_filter_hosts_with_segment_access(self):
        dummy_token = ["X"]
        self.assertEqual(
            dummy_token,
            _MechanismDriver().filter_hosts_with_segment_access(
                dummy_token, dummy_token, dummy_token, dummy_token))
