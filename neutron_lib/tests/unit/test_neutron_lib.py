# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import copy

from neutron_lib import constants

from neutron_lib.tests import _base as base


class TestNeutronLib(base.BaseTestCase):

    def test_sentinel_constant(self):
        foo = constants.Sentinel()
        bar = copy.deepcopy(foo)
        self.assertEqual(id(foo), id(bar))

    def test_sentinel_copy(self):
        singleton = constants.Sentinel()
        self.assertEqual(copy.deepcopy(singleton), copy.copy(singleton))
