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
from neutron_lib.tests import _base as base


class HackingTestCase(base.BaseTestCase):

    def assertLinePasses(self, func, line):
        with testtools.ExpectedException(StopIteration):
            next(func(line))

    def assertLineFails(self, func, line):
        self.assertIsInstance(next(func(line)), tuple)

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

            self.assertEqual(0,
                len(list(checks.use_jsonutils("jsonx.%s(" % method,
                                              "./neutron/common/rpc.py"))))

            self.assertEqual(0,
                len(list(checks.use_jsonutils("json.%sx(" % method,
                                              "./neutron/common/rpc.py"))))

            self.assertEqual(0,
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

    def test_check_python3_xrange(self):
        f = checks.check_python3_xrange
        self.assertLineFails(f, 'a = xrange(1000)')
        self.assertLineFails(f, 'b =xrange   (   42 )')
        self.assertLineFails(f, 'c = xrange(1, 10, 2)')
        self.assertLinePasses(f, 'd = range(1000)')
        self.assertLinePasses(f, 'e = six.moves.range(1337)')

    def test_no_basestring(self):
        self.assertEqual(1,
            len(list(checks.check_no_basestring("isinstance(x, basestring)"))))

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
