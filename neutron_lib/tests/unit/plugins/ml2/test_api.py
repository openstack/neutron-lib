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

from unittest import mock

from neutron_lib.plugins.ml2 import api
from neutron_lib.tests import _base as base


class _MechanismDriver(api.MechanismDriver):
    def bind_port(self, context):
        return context

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


class _TypeDriver_Base:
    def get_type(self):
        pass

    def initialize(self):
        pass

    def is_partial_segment(self, segment):
        pass

    def validate_provider_segment(self, segment):
        pass

    def get_mtu(self, physical):
        pass

    def reserve_provider_segment(self, session, segment, filters=None):
        pass

    def allocate_tenant_segment(self, session, filters=None):
        pass

    def release_segment(self, session, segment):
        pass


class _TypeDriver_NoProject(_TypeDriver_Base, api.TypeDriver):
    pass


class _TypeDriver_WithProject(_TypeDriver_NoProject):

    def allocate_project_segment(self, session, filters=None):
        pass


class TestTypeDriver(base.BaseTestCase):

    def test_typedriver_noproject(self):
        drv = _TypeDriver_NoProject()
        drv.allocate_tenant_segment = mock.Mock()
        drv.allocate_project_segment('session', filters='filters')
        drv.allocate_tenant_segment.assert_called_once_with(
            'session', filters='filters')

    def test_typedriver_withproject(self):
        drv = _TypeDriver_WithProject()
        drv.allocate_tenant_segment = mock.Mock()
        drv.allocate_project_segment('session', filters='filters')
        drv.allocate_tenant_segment.assert_not_called()


class _ML2TypeDriver_NoProject(_TypeDriver_Base, api.ML2TypeDriver):

    def initialize_network_segment_range_support(self):
        pass

    def update_network_segment_range_allocations(self):
        pass


class _ML2TypeDriver_WithProject(_ML2TypeDriver_NoProject):

    def allocate_project_segment(self, context, filters=None):
        pass


class TestML2TypeDriver(base.BaseTestCase):

    def test_ml2typedriver_noproject(self):
        drv = _ML2TypeDriver_NoProject()
        drv.allocate_tenant_segment = mock.Mock()
        drv.allocate_project_segment('context', filters='filters')
        drv.allocate_tenant_segment.assert_called_once_with(
            'context', filters='filters')

    def test_ml2typedriver_withproject(self):
        drv = _ML2TypeDriver_WithProject()
        drv.allocate_tenant_segment = mock.Mock()
        drv.allocate_project_segment('context', filters='filters')
        drv.allocate_tenant_segment.assert_not_called()
