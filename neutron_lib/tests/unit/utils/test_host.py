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

import multiprocessing
from unittest import mock

from neutron_lib.tests import _base as base
from neutron_lib.utils import host


class TestCpuCount(base.BaseTestCase):

    @mock.patch.object(multiprocessing, 'cpu_count',
                       return_value=7)
    def test_cpu_count(self, mock_cpu_count):
        self.assertEqual(7, host.cpu_count())
        mock_cpu_count.assert_called_once_with()

    @mock.patch.object(multiprocessing, 'cpu_count',
                       side_effect=NotImplementedError())
    def test_cpu_count_not_implemented(self, mock_cpu_count):
        self.assertEqual(1, host.cpu_count())
        mock_cpu_count.assert_called_once_with()
