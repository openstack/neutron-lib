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

from unittest import mock

from oslo_db import exception as db_exc
import osprofiler
import sqlalchemy
from sqlalchemy.orm import exc
import testtools

from neutron_lib.db import api as db_api
from neutron_lib import exceptions
from neutron_lib import fixture
from neutron_lib.tests import _base


class TestExceptionToRetryContextManager(_base.BaseTestCase):

    def test_translates_single_exception(self):
        with testtools.ExpectedException(db_exc.RetryRequest):
            with db_api.exc_to_retry(ValueError):
                raise ValueError()

    def test_translates_multiple_exception_types(self):
        with testtools.ExpectedException(db_exc.RetryRequest):
            with db_api.exc_to_retry((ValueError, TypeError)):
                raise TypeError()

    def test_translates_DBerror_inner_exception(self):
        with testtools.ExpectedException(db_exc.RetryRequest):
            with db_api.exc_to_retry(ValueError):
                raise db_exc.DBError(ValueError())

    def test_passes_other_exceptions(self):
        with testtools.ExpectedException(ValueError):
            with db_api.exc_to_retry(TypeError):
                raise ValueError()

    def test_inner_exception_preserved_in_retryrequest(self):
        try:
            exc = ValueError('test')
            with db_api.exc_to_retry(ValueError):
                raise exc
        except db_exc.RetryRequest as e:
            self.assertEqual(exc, e.inner_exc)

    def test_retries_on_multi_exception_containing_target(self):
        with testtools.ExpectedException(db_exc.RetryRequest):
            with db_api.exc_to_retry(ValueError):
                e = exceptions.MultipleExceptions([ValueError(), TypeError()])
                raise e


class TestDeadLockDecorator(_base.BaseTestCase):

    @db_api.retry_db_errors
    def _decorated_function(self, fail_count, exc_to_raise):
        self.fail_count = getattr(self, 'fail_count', fail_count + 1) - 1
        if self.fail_count:
            raise exc_to_raise

    def test_regular_exception_excluded(self):
        with testtools.ExpectedException(ValueError):
            self._decorated_function(1, ValueError)

    def test_staledata_error_caught(self):
        e = exc.StaleDataError()
        self.assertIsNone(self._decorated_function(1, e))

    def test_dbconnection_error_caught(self):
        e = db_exc.DBConnectionError()
        self.assertIsNone(self._decorated_function(1, e))

    def test_multi_exception_contains_retry(self):
        e = exceptions.MultipleExceptions(
            [ValueError(), db_exc.RetryRequest(TypeError())])
        self.assertIsNone(self._decorated_function(1, e))

    def test_multi_exception_contains_deadlock(self):
        e = exceptions.MultipleExceptions([ValueError(), db_exc.DBDeadlock()])
        self.assertIsNone(self._decorated_function(1, e))

    def test_multi_nested_exception_contains_deadlock(self):
        i = exceptions.MultipleExceptions([ValueError(), db_exc.DBDeadlock()])
        e = exceptions.MultipleExceptions([ValueError(), i])
        self.assertIsNone(self._decorated_function(1, e))

    def test_multi_exception_raised_on_exceed(self):
        # limit retries so this doesn't take 40 seconds
        retry_fixture = fixture.DBRetryErrorsFixture(max_retries=2)
        retry_fixture.setUp()
        e = exceptions.MultipleExceptions([ValueError(), db_exc.DBDeadlock()])
        with testtools.ExpectedException(exceptions.MultipleExceptions):
            self._decorated_function(db_api.MAX_RETRIES + 1, e)
        retry_fixture.cleanUp()

    def test_mysql_savepoint_error(self):
        e = db_exc.DBError("(pymysql.err.InternalError) (1305, 'SAVEPOINT "
                           "sa_savepoint_1 does not exist')")
        self.assertIsNone(self._decorated_function(1, e))

    @db_api.retry_if_session_inactive('alt_context')
    def _alt_context_function(self, alt_context, *args, **kwargs):
        return self._decorated_function(*args, **kwargs)

    @db_api.retry_if_session_inactive()
    def _context_function(self, context, list_arg, dict_arg,
                          fail_count, exc_to_raise):
        list_arg.append(1)
        dict_arg[max(dict_arg.keys()) + 1] = True
        self.fail_count = getattr(self, 'fail_count', fail_count + 1) - 1
        if self.fail_count:
            raise exc_to_raise
        return list_arg, dict_arg

    def test_stacked_retries_dont_explode_retry_count(self):
        context = mock.Mock()
        context.session.is_active = False
        e = db_exc.DBConnectionError()
        mock.patch('time.sleep').start()
        with testtools.ExpectedException(db_exc.DBConnectionError):
            # after 20 failures, the inner retry should give up and
            # the exception should be tagged to prevent the outer retry
            self._alt_context_function(context, db_api.MAX_RETRIES + 1, e)

    def _test_retry_time_cost(self, exc_to_raise):
        worst_case = [0.5, 1, 2, 4, 8,
                      10, 10, 10, 10, 10,
                      10, 10, 10, 10, 10,
                      10, 10, 10, 10, 10]

        class FakeTime:
            def __init__(self):
                self.counter = 0

            def sleep(self, t):
                self.counter += t

        fake_timer = FakeTime()

        def fake_sleep(t):
            fake_timer.sleep(t)

        e = exc_to_raise()
        mock.patch('time.sleep', side_effect=fake_sleep).start()
        with testtools.ExpectedException(exc_to_raise):
            self._decorated_function(db_api.MAX_RETRIES + 1, e)
        if exc_to_raise == db_exc.DBDeadlock:
            self.assertEqual(True, (fake_timer.counter <= sum(worst_case)))
        else:
            self.assertGreaterEqual(sum(worst_case), fake_timer.counter)

    def test_all_deadlock_time_elapsed(self):
        self._test_retry_time_cost(db_exc.DBDeadlock)

    def test_not_deadlock_time_elapsed(self):
        self._test_retry_time_cost(db_exc.DBConnectionError)

    def test_retry_if_session_inactive_args_not_mutated_after_retries(self):
        context = mock.Mock()
        context.session.is_active = False
        list_arg = [1, 2, 3, 4]
        dict_arg = {1: 'a', 2: 'b'}
        l, d = self._context_function(context, list_arg, dict_arg,
                                      5, db_exc.DBDeadlock())
        # even though we had 5 failures the list and dict should only
        # be mutated once
        self.assertEqual(5, len(l))
        self.assertEqual(3, len(d))

    def test_retry_if_session_inactive_kwargs_not_mutated_after_retries(self):
        context = mock.Mock()
        context.session.is_active = False
        list_arg = [1, 2, 3, 4]
        dict_arg = {1: 'a', 2: 'b'}
        l, d = self._context_function(context, list_arg=list_arg,
                                      dict_arg=dict_arg,
                                      fail_count=5,
                                      exc_to_raise=db_exc.DBDeadlock())
        # even though we had 5 failures the list and dict should only
        # be mutated once
        self.assertEqual(5, len(l))
        self.assertEqual(3, len(d))

    def test_retry_if_session_inactive_no_retry_in_active_session(self):
        context = mock.Mock()
        context.session.is_active = True
        with testtools.ExpectedException(db_exc.DBDeadlock):
            # retry decorator should have no effect in an active session
            self._context_function(context, [], {1: 2},
                                   fail_count=1,
                                   exc_to_raise=db_exc.DBDeadlock())


class TestDBProfiler(_base.BaseTestCase):

    @mock.patch.object(osprofiler.opts, 'is_trace_enabled',
                       return_value=True)
    @mock.patch.object(osprofiler.opts, 'is_db_trace_enabled',
                       return_value=True)
    def test_set_hook(self, _mock_dbt, _mock_t):
        with mock.patch.object(
                osprofiler.sqlalchemy, 'add_tracing') as add_tracing:
            engine_mock = mock.Mock()
            db_api._set_hook(engine_mock)
            add_tracing.assert_called_once_with(
                sqlalchemy, mock.ANY, "neutron.db")
