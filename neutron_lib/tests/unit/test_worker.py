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

import mock

from neutron_lib.callbacks import events
from neutron_lib.callbacks import resources
from neutron_lib import fixture
from neutron_lib import worker

from neutron_lib.tests import _base as base


class _BaseWorker(worker.BaseWorker):

    def reset(self):
        pass

    def stop(self):
        pass

    def wait(self):
        pass


class TestBaseWorker(base.BaseTestCase):

    def setUp(self):
        super(TestBaseWorker, self).setUp()
        self._reg = mock.Mock()
        self.useFixture(fixture.CallbackRegistryFixture(
            callback_manager=self._reg))

    def test_worker_process_count(self):
        self.assertEqual(9, _BaseWorker(
            worker_process_count=9).worker_process_count)

    def test_start_callback_event(self):
        base_worker = _BaseWorker()
        base_worker.start()
        self._reg.notify.assert_called_once_with(
            resources.PROCESS, events.AFTER_INIT, base_worker.start)
