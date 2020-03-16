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


# Same as _BaseWorker, but looks like a process launch instead of eventlet
class _ProcWorker(_BaseWorker):

    def __init__(self, worker_process_count=1, set_proctitle='on'):
        super(_ProcWorker, self).__init__(worker_process_count, set_proctitle)
        self._my_pid = -1  # make it appear to be a separate process


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

    # Forked workers, should call setproctitle

    def test_proctitle_default(self):
        with mock.patch('setproctitle.setproctitle') as spt:
            _ProcWorker().start()
            self.assertRegex(spt.call_args[0][0],
                             '^neutron-server: _ProcWorker \\(.*python.*\\)$')

    def test_proctitle_custom_desc(self):
        with mock.patch('setproctitle.setproctitle') as spt:
            _ProcWorker().start(desc="fancy title")
            self.assertRegex(spt.call_args[0][0],
                             '^neutron-server: fancy title \\(.*python.*\\)$')

    def test_proctitle_custom_name(self):
        with mock.patch('setproctitle.setproctitle') as spt:
            _ProcWorker().start(name="tardis")
            self.assertRegex(spt.call_args[0][0],
                             '^tardis: _ProcWorker \\(.*python.*\\)$')

    def test_proctitle_empty(self):
        with mock.patch('setproctitle.setproctitle') as spt:
            _ProcWorker().start(desc="")
            self.assertRegex(spt.call_args[0][0],
                             '^neutron-server: _ProcWorker \\(.*python.*\\)$')

    def test_proctitle_nonstring(self):
        with mock.patch('setproctitle.setproctitle') as spt:
            _ProcWorker().start(desc=2)
            self.assertRegex(spt.call_args[0][0],
                             '^neutron-server: 2 \\(.*python.*\\)$')

    def test_proctitle_both_empty(self):
        with mock.patch('setproctitle.setproctitle') as spt:
            _ProcWorker().start(name="", desc="")
            self.assertRegex(spt.call_args[0][0],
                             '^: _ProcWorker \\(.*python.*\\)$')

    def test_proctitle_name_none(self):
        with mock.patch('setproctitle.setproctitle') as spt:
            _ProcWorker().start(name=None)
            self.assertRegex(spt.call_args[0][0],
                             '^None: _ProcWorker \\(.*python.*\\)$')

    # Forked, but proctitle disabled

    def test_proctitle_off(self):
        with mock.patch('setproctitle.setproctitle') as spt:
            _ProcWorker(set_proctitle='off').start()
            self.assertIsNone(spt.call_args)

    # Eventlet style worker, should never call setproctitle

    def test_proctitle_same_process(self):
        with mock.patch('setproctitle.setproctitle') as spt:
            _BaseWorker().start()
            self.assertIsNone(spt.call_args)

    def test_setproctitle_on(self):
        with mock.patch('setproctitle.setproctitle') as spt:
            _ProcWorker(set_proctitle='on').start(name="foo", desc="bar")
            self.assertRegex(spt.call_args[0][0],
                             '^foo: bar \\(.*python.*\\)$')

    def test_setproctitle_off(self):
        with mock.patch('setproctitle.setproctitle') as spt:
            _ProcWorker(set_proctitle='off').start(name="foo", desc="bar")
            self.assertIsNone(spt.call_args)

    def test_setproctitle_brief(self):
        with mock.patch('setproctitle.setproctitle') as spt:
            _ProcWorker(set_proctitle='brief').start(name="foo", desc="bar")
            self.assertEqual(spt.call_args[0][0], 'foo: bar')
