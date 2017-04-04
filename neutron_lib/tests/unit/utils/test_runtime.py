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

import mock

from neutron_lib.tests import _base as base
from neutron_lib.utils import runtime


class _DummyDriver(object):
    driver = mock.sentinel.dummy_driver


class TestRunTime(base.BaseTestCase):

    @mock.patch.object(runtime, 'LOG')
    def test_load_class_by_alias_or_classname_no_name(self, mock_log):
        self.assertRaises(
            ImportError,
            runtime.load_class_by_alias_or_classname, 'ns', None)

    @mock.patch.object(runtime.driver, 'DriverManager',
                       return_value=_DummyDriver)
    @mock.patch.object(runtime, 'LOG')
    def test_load_class_by_alias_or_classname_dummy_driver(
            self, mock_log, mock_driver):
        self.assertEqual(_DummyDriver.driver,
                         runtime.load_class_by_alias_or_classname('ns', 'n'))

    @mock.patch.object(runtime, 'LOG')
    def test_load_class_by_alias_or_classname_bad_classname(self, mock_log):
        self.assertRaises(
            ImportError,
            runtime.load_class_by_alias_or_classname, 'ns', '_NoClass')

    @mock.patch.object(runtime.importutils, 'import_class',
                       return_value=mock.sentinel.dummy_class)
    @mock.patch.object(runtime, 'LOG')
    def test_load_class_by_alias_or_classname_with_classname(
            self, mock_log, mock_import):
        self.assertEqual(
            mock.sentinel.dummy_class,
            runtime.load_class_by_alias_or_classname('ns', 'n'))
