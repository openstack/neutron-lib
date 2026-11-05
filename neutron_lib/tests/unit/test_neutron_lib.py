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

import copy
import subprocess
import sys

from neutron_lib import constants

from neutron_lib.tests import _base as base


class TestNeutronLib(base.BaseTestCase):

    def test_sentinel_constant(self):
        singleton = constants.Sentinel()
        sing_copy = copy.deepcopy(singleton)
        self.assertEqual(id(singleton), id(sing_copy))

    def test_sentinel_copy(self):
        singleton = constants.Sentinel()
        self.assertEqual(copy.deepcopy(singleton), copy.copy(singleton))

    def test_agent_modules_do_not_load_db_api(self):
        # Run in a fresh interpreter: the test process has already imported
        # neutron_lib.db.api.
        modules = ('neutron_lib.agent.topics', 'neutron_lib.api.definitions',
                   'neutron_lib.context')
        forbidden = ('neutron_lib.db.api', 'pecan')
        code = ('import importlib, sys\n'
                'for m in %r:\n'
                '    importlib.import_module(m)\n'
                'print(",".join(m for m in %r if m in sys.modules))\n'
                % (modules, forbidden))
        cmd = [sys.executable, '-c', code]
        out = subprocess.check_output(cmd, text=True)  # noqa: S603
        self.assertEqual('', out.strip())
