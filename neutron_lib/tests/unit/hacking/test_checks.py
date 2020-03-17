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

import testtools

from neutron_lib.hacking import checks
from neutron_lib.hacking import translation_checks as tc
from neutron_lib.tests import _base as base


class HackingTestCase(base.BaseTestCase):

    def assertLinePasses(self, func, *args):
        with testtools.ExpectedException(StopIteration):
            next(func(*args))

    def assertLineFails(self, func, *args):
        self.assertIsInstance(next(func(*args)), tuple)

    def _get_factory_checks(self, factory):
        check_fns = []

        def _reg(check_fn):
            self.assertTrue(hasattr(check_fn, '__call__'))
            self.assertFalse(check_fn in check_fns)
            check_fns.append(check_fn)

        factory(_reg)
        return check_fns

    def test_factory(self):
        self.assertGreater(len(self._get_factory_checks(checks.factory)), 0)

    def test_use_jsonutils(self):
        def __get_msg(fun):
            msg = ("N521: jsonutils.%(fun)s must be used instead of "
                   "json.%(fun)s" % {'fun': fun})
            return [(0, msg)]

        for method in ('dump', 'dumps', 'load', 'loads'):
            self.assertEqual(
                __get_msg(method),
                list(checks.use_jsonutils("json.%s(" % method,
                                          "./neutron/common/rpc.py")))

            self.assertEqual(
                0,
                len(list(checks.use_jsonutils("jsonx.%s(" % method,
                                              "./neutron/common/rpc.py"))))

            self.assertEqual(
                0,
                len(list(checks.use_jsonutils("json.%sx(" % method,
                                              "./neutron/common/rpc.py"))))

            self.assertEqual(
                0,
                len(list(checks.use_jsonutils(
                    "json.%s" % method,
                    "./neutron/plugins/ml2/drivers/openvswitch/agent/xenapi/"
                    "etc/xapi.d/plugins/netwrap"))))

    def test_check_contextlib_nested(self):
        f = checks.check_no_contextlib_nested
        self.assertLineFails(f, 'with contextlib.nested():', '')
        self.assertLineFails(f, '    with contextlib.nested():', '')
        self.assertLinePasses(f, '# with contextlib.nested():', '')
        self.assertLinePasses(f, 'print("with contextlib.nested():")', '')

    def test_no_mutable_default_args(self):
        self.assertEqual(1, len(list(checks.no_mutable_default_args(
            " def fake_suds_context(calls={}):"))))

        self.assertEqual(1, len(list(checks.no_mutable_default_args(
            "def get_info_from_bdm(virt_type, bdm, mapping=[])"))))

        self.assertEqual(0, len(list(checks.no_mutable_default_args(
            "defined = []"))))

        self.assertEqual(0, len(list(checks.no_mutable_default_args(
            "defined, undefined = [], {}"))))

    def test_check_neutron_namespace_imports(self):
        f = checks.check_neutron_namespace_imports
        self.assertLinePasses(f, 'from neutron_lib import constants')
        self.assertLinePasses(f, 'import neutron_lib.constants')
        self.assertLineFails(f, 'from neutron.common import rpc')
        self.assertLineFails(f, 'from neutron import context')
        self.assertLineFails(f, 'import neutron.common.config')

    def test_no_log_translations(self):
        for log in tc._all_log_levels:
            for hint in tc._all_hints:
                bad = 'LOG.%s(%s("Bad"))' % (log, hint)
                self.assertEqual(
                    1, len(list(tc.no_translate_logs(bad, 'f'))))
                # Catch abuses when used with a variable and not a literal
                bad = 'LOG.%s(%s(msg))' % (log, hint)
                self.assertEqual(
                    1, len(list(tc.no_translate_logs(bad, 'f'))))
                # Do not do validations in tests
                ok = 'LOG.%s(_("OK - unit tests"))' % log
                self.assertEqual(
                    0, len(list(tc.no_translate_logs(ok, 'f/tests/f'))))

    def test_check_log_warn_deprecated(self):
        bad = "LOG.warn('i am deprecated!')"
        good = "LOG.warning('zlatan is the best')"
        f = tc.check_log_warn_deprecated
        self.assertLineFails(f, bad, '')
        self.assertLinePasses(f, good, '')

    def test_check_localized_exception_messages(self):
        f = tc.check_raised_localized_exceptions
        self.assertLineFails(f, "     raise KeyError('Error text')", '')
        self.assertLineFails(f, ' raise KeyError("Error text")', '')
        self.assertLinePasses(f, ' raise KeyError(_("Error text"))', '')
        self.assertLinePasses(f, ' raise KeyError(_ERR("Error text"))', '')
        self.assertLinePasses(f, " raise KeyError(translated_msg)", '')
        self.assertLinePasses(f, '# raise KeyError("Not translated")', '')
        self.assertLinePasses(f, 'print("raise KeyError("Not '
                                 'translated")")', '')

    def test_check_localized_exception_message_skip_tests(self):
        f = tc.check_raised_localized_exceptions
        self.assertLinePasses(f, "raise KeyError('Error text')",
                              'neutron_lib/tests/unit/mytest.py')

    def test_check_eventlet_imports(self):
        f = checks.check_no_eventlet_imports
        self.assertLineFails(f, "import eventlet")
        self.assertLineFails(f, "import eventlet.timeout")
        self.assertLineFails(f, "from eventlet import timeout")
        self.assertLineFails(f, "from eventlet.timeout import Timeout")
        self.assertLineFails(f, "from eventlet.timeout import (Timeout, X)")
        self.assertLinePasses(f, "import is.not.eventlet")
        self.assertLinePasses(f, "from is.not.eventlet")
        self.assertLinePasses(f, "from mymod import eventlet")
        self.assertLinePasses(f, "from mymod.eventlet import amod")
        self.assertLinePasses(f, 'print("eventlet not here")')
        self.assertLinePasses(f, 'print("eventlet.timeout")')
        self.assertLinePasses(f, "from mymod.timeout import (eventlet, X)")

    def test_assert_equal_none(self):
        self.assertEqual(len(list(checks.assert_equal_none(
            "self.assertEqual(A, None)"))), 1)
        self.assertEqual(len(list(checks.assert_equal_none(
            "self.assertEqual(A, None)  # Comment"))), 1)
        self.assertEqual(len(list(checks.assert_equal_none(
            "self.assertEqual(None, A)"))), 1)
        self.assertEqual(len(list(checks.assert_equal_none(
            "self.assertEqual(None, A)  # Comment"))), 1)
        self.assertEqual(len(list(checks.assert_equal_none(
            "self.assertEqual((None, None), A)"))), 0)
        self.assertEqual(len(list(checks.assert_equal_none(
            "self.assertEqual((None, None), A)  # Comment"))), 0)
        self.assertEqual(len(list(checks.assert_equal_none(
            "self.assertEqual(A, (None, None))"))), 0)
        self.assertEqual(len(list(checks.assert_equal_none(
            "self.assertEqual(A, (None, None))  # Comment"))), 0)
        self.assertEqual(len(list(checks.assert_equal_none(
            "assertIsNot(A, None)"))), 1)
        self.assertEqual(len(list(checks.assert_equal_none(
            "assertIsNot(A, None)  # Comment"))), 1)
        self.assertEqual(len(list(checks.assert_equal_none(
            "assertIsNot(None, A)"))), 1)
        self.assertEqual(len(list(checks.assert_equal_none(
            "assertIsNot(None, A)  # Comment"))), 1)
        self.assertEqual(len(list(checks.assert_equal_none(
            "assertIsNot((None, None), A)"))), 0)
        self.assertEqual(len(list(checks.assert_equal_none(
            "assertIsNot((None, None), A)  # Comment"))), 0)
        self.assertEqual(len(list(checks.assert_equal_none(
            "assertIsNot(A, (None, None))"))), 0)
        self.assertEqual(len(list(checks.assert_equal_none(
            "assertIsNot(A, (None, None))  # Comment"))), 0)
        self.assertEqual(
            len(list(checks.assert_equal_none("self.assertIsNone(A)"))), 0)
        self.assertEqual(
            len(list(checks.assert_equal_none("self.assertIsNotNone(A)"))), 0)
