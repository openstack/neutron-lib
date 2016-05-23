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

import socket

import mock

from neutron_lib.tests import _base as base
from neutron_lib.utils import net


class TestGetHostname(base.BaseTestCase):

    @mock.patch.object(socket, 'gethostname',
                       return_value='fake-host-name')
    def test_get_hostname(self, mock_gethostname):
        self.assertEqual('fake-host-name',
                         net.get_hostname())
        mock_gethostname.assert_called_once_with()
