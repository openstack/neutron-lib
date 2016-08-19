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

import errno
import os.path
import stat

import mock

from neutron_lib.tests import _base as base
from neutron_lib.utils import file


class TestEnsureDir(base.BaseTestCase):

    @mock.patch('os.makedirs')
    def test_ensure_dir_no_fail_if_exists(self, makedirs):
        error = OSError()
        error.errno = errno.EEXIST
        makedirs.side_effect = error
        file.ensure_dir("/etc/create/concurrently")

    @mock.patch('os.makedirs')
    def test_ensure_dir_oserr(self, makedirs):
        error = OSError()
        error.errno = errno.EPERM
        makedirs.side_effect = error
        self.assertRaises(OSError,
                          file.ensure_dir,
                          "/etc/create/directory")
        makedirs.assert_called_once_with("/etc/create/directory", 0o755)

    @mock.patch('os.makedirs')
    def test_ensure_dir_calls_makedirs(self, makedirs):
        file.ensure_dir("/etc/create/directory")
        makedirs.assert_called_once_with("/etc/create/directory", 0o755)


class TestReplaceFile(base.BaseTestCase):

    def setUp(self):
        super(TestReplaceFile, self).setUp()
        temp_dir = self.get_default_temp_dir().path
        self.file_name = os.path.join(temp_dir, "new_file")
        self.data = "data to copy"

    def _verify_result(self, file_mode):
        self.assertTrue(os.path.exists(self.file_name))
        with open(self.file_name) as f:
            content = f.read()
        self.assertEqual(self.data, content)
        mode = os.stat(self.file_name).st_mode
        self.assertEqual(file_mode, stat.S_IMODE(mode))

    def test_replace_file_default_mode(self):
        file_mode = 0o644
        file.replace_file(self.file_name, self.data)
        self._verify_result(file_mode)

    def test_replace_file_custom_mode(self):
        file_mode = 0o722
        file.replace_file(self.file_name, self.data, file_mode)
        self._verify_result(file_mode)

    def test_replace_file_custom_mode_twice(self):
        file_mode = 0o722
        file.replace_file(self.file_name, self.data, file_mode)
        self.data = "new data to copy"
        file_mode = 0o777
        file.replace_file(self.file_name, self.data, file_mode)
        self._verify_result(file_mode)
