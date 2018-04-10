# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from neutron_lib.tests import _base as base
from neutron_lib.utils import test


class TestUnstableTestDecorator(base.BaseTestCase):

    @test.unstable_test("some bug")
    def test_unstable_pass(self):
        self.assertIsNone(None)

    @test.unstable_test("some other bug")
    def test_unstable_fail(self):
        self.assertIsNotNone(None)
