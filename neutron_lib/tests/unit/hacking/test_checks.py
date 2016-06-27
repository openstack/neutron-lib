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

import contextlib
import math

import mock
import pep8
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

    def test_factory(self):
        def check_callable(fn):
            self.assertTrue(hasattr(fn, '__call__'))
        self.assertIsNone(checks.factory(check_callable))

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

    def test_check_oslo_namespace_imports(self):
        f = checks.check_oslo_namespace_imports
        self.assertLinePasses(f, 'from oslo_utils import importutils')
        self.assertLinePasses(f, 'import oslo_messaging')
        self.assertLineFails(f, 'from oslo.utils import importutils')
        self.assertLineFails(f, 'from oslo import messaging')
        self.assertLineFails(f, 'import oslo.messaging')

    def test_check_contextlib_nested(self):
        f = checks.check_no_contextlib_nested
        self.assertLineFails(f, 'with contextlib.nested():', '')
        self.assertLineFails(f, '    with contextlib.nested():', '')
        self.assertLinePasses(f, '# with contextlib.nested():', '')
        self.assertLinePasses(f, 'print("with contextlib.nested():")', '')

    def test_check_python3_xrange(self):
        f = checks.check_python3_xrange
        self.assertLineFails(f, 'a = xrange(1000)')
        self.assertLineFails(f, 'b =xrange   (   42 )')
        self.assertLineFails(f, 'c = xrange(1, 10, 2)')
        self.assertLinePasses(f, 'd = range(1000)')
        self.assertLinePasses(f, 'e = six.moves.range(1337)')

    def test_no_basestring(self):
        f = checks.check_no_basestring
        self.assertLineFails(f, 'isinstance(x, basestring)')
        self.assertLinePasses(f, 'isinstance(x, BaseString)')

    def test_check_python3_iteritems(self):
        f = checks.check_python3_no_iteritems
        self.assertLineFails(f, "d.iteritems()")
        self.assertLinePasses(f, "six.iteritems(d)")

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

    def test_log_translations(self):
        expected_marks = {
            'error': '_LE',
            'info': '_LI',
            'warning': '_LW',
            'critical': '_LC',
            'exception': '_LE',
        }
        logs = expected_marks.keys()
        debug = "LOG.debug('OK')"
        self.assertEqual(
            0, len(list(tc.validate_log_translations(debug, debug, 'f'))))
        for log in logs:
            bad = 'LOG.%s(_("Bad"))' % log
            self.assertEqual(
                1, len(list(tc.validate_log_translations(bad, bad, 'f'))))
            bad = 'LOG.%s("Bad")' % log
            self.assertEqual(
                1, len(list(tc.validate_log_translations(bad, bad, 'f'))))
            ok = "LOG.%s('OK')    # noqa" % log
            self.assertEqual(
                0, len(list(tc.validate_log_translations(ok, ok, 'f'))))
            ok = "LOG.%s(variable)" % log
            self.assertEqual(
                0, len(list(tc.validate_log_translations(ok, ok, 'f'))))
            # Do not do validations in tests
            ok = 'LOG.%s("OK - unit tests")' % log
            self.assertEqual(
                0, len(list(tc.validate_log_translations(ok, ok,
                                                         'f/tests/f'))))

            for mark in tc._all_hints:
                stmt = "LOG.%s(%s('test'))" % (log, mark)
                self.assertEqual(
                    0 if expected_marks[log] == mark else 1,
                    len(list(tc.validate_log_translations(stmt, stmt, 'f'))))

    def test_no_translate_debug_logs(self):
        for hint in tc._all_hints:
            bad = "LOG.debug(%s('bad'))" % hint
            self.assertEqual(
                1, len(list(tc.no_translate_debug_logs(bad, 'f'))))

    def test_check_log_warn_deprecated(self):
        bad = "LOG.warn(_LW('i am deprecated!'))"
        good = "LOG.warning(_LW('zlatan is the best'))"
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

    @contextlib.contextmanager
    def _mocked_style_guide_checks(self, pep_checks):
        # chunk checks into 3 sub-lists so that each type of check returns
        # approximately 1/3 of the checks
        list_size = int(math.ceil(float(len(pep_checks)) / 3.0))
        chunks = [pep_checks[i:i + list_size]
                  for i in range(0, len(pep_checks), list_size)]
        indexed = [[], [], []]
        for i in range(3):
            for c in range(len(chunks[i])):
                indexed[i].append([chunks[i][c].__name__, chunks[i][c]])

        # each type of check returns about 1/3 of the pep checks
        check_dict = {
            'physical_line': indexed[0],
            'logical_line': indexed[1],
            'tree': indexed[2]
        }
        try:
            class _MockSG(object):
                def get_checks(self, check_type):
                    return check_dict[check_type]

            mock_sg = mock.patch.object(checks.pep8, 'StyleGuide', new=_MockSG)
            mock_sg.start()
            yield mock_sg
        finally:
            mock_sg.stop()

    def _test_register_checks(self, to_register, factory):
        for check in to_register:
            setattr(check, 'off_by_default', True)
        with self._mocked_style_guide_checks(to_register):
            reg = []
            factory(reg.append)
            for check in to_register:
                self.assertIn(check, reg)
                self.assertFalse(getattr(check, 'off_by_default', True))

    def test_latest_adopter_hacking_checks(self):
        self._test_register_checks(list(checks.ADOPTER_CHECKS),
                                   checks.latest_adopter_hacking_checks)

    def test_neutron_lib_project_hacking_checks(self):
        self._test_register_checks(list(checks._LIB_PROJECT_CHECKS),
                                   checks._neutron_lib_project_hacking_checks)

    def test_hacking_check_proxy(self):

        class _MockOpts(object):
            def __init__(self, ignore):
                self.ignore = ignore or []

        all_checks = list(checks.ALL_CHECKS)
        with self._mocked_style_guide_checks(all_checks):
            reg = []
            all_codes = set([])
            for codes in [pep8.ERRORCODE_REGEX.findall(f.__doc__ or '')
                          for f in all_checks]:
                for code in codes:
                    all_codes.add(code)

            self.assertTrue(len(all_codes) > 0)
            opts = _MockOpts(all_codes)

            checks._register_and_enable_checks(reg.append, all_checks)

            checks._ProxyHackingChecks.parse_options(opts)
            # make sure all registered checks are not ignored
            self.assertEqual([], list(opts.ignore))
