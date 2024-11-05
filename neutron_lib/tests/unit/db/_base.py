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

"""
Base classes for unit tests needing DB backend.
Only sqlite is supported in neutron-lib.
"""

from neutron_lib import fixture
from neutron_lib.tests import _base as base


class SqlTestCase(base.BaseTestCase):

    def setUp(self):
        super().setUp()
        self.useFixture(fixture.SqlFixture())
