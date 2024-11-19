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

from unittest import mock

import neutron_lib.exceptions.l3_ext_ha_mode as lehm
from neutron_lib.tests.unit.exceptions import test_exceptions


class TestHANetworkConcurrentDeletion(test_exceptions.TestExceptionsBase):

    # NOTE(haleyb) We only test HANetworkConcurrentDeletion because it is
    # the only one with an __init__() section.
    def test_ha_network_concurrent_deletion(self):
        self._check_nexc(
            lehm.HANetworkConcurrentDeletion,
            _('Network for project project_id concurrently deleted.'),
            project_id='project_id')

    @mock.patch.object(lehm, 'LOG')
    def test_ha_network_concurrent_deletion_tenant_id(self, mock_log):
        self._check_nexc(
            lehm.HANetworkConcurrentDeletion,
            _('Network for project tenant_id concurrently deleted.'),
            tenant_id='tenant_id')
        mock_log.warning.assert_called_once_with(
            'Keyword tenant_id has been deprecated, use project_id instead')

    @mock.patch.object(lehm, 'LOG')
    def test_ha_network_concurrent_deletion_both(self, mock_log):
        self._check_nexc(
            lehm.HANetworkConcurrentDeletion,
            _('Network for project project_id concurrently deleted.'),
            project_id='project_id', tenant_id='tenant_id')
        mock_log.warning.assert_called_once_with(
            'Keyword tenant_id has been deprecated, use project_id instead')
