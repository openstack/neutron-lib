# Copyright 2010-2011 OpenStack Foundation
# All Rights Reserved.
#
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

import logging as std_logging
import os
import os.path
import random

import fixtures
import mock
from oslo_config import cfg
from oslo_db import options as db_options
from oslo_utils import strutils
import six
import testtools

from neutron_lib._i18n import _
from neutron_lib import constants
from neutron_lib.tests import _post_mortem_debug as post_mortem_debug
from neutron_lib.tests import _tools as tools


CONF = cfg.CONF
LOG_FORMAT = "%(asctime)s %(levelname)8s [%(name)s] %(message)s"

ROOTDIR = os.path.dirname(__file__)
ETCDIR = os.path.join(ROOTDIR, 'etc')


def etcdir(*p):
    return os.path.join(ETCDIR, *p)


def fake_use_fatal_exceptions(*args):
    return True


def get_rand_name(max_length=None, prefix='test'):
    """Return a random string.

    The string will start with 'prefix' and will be exactly 'max_length'.
    If 'max_length' is None, then exactly 8 random characters, each
    hexadecimal, will be added. In case len(prefix) <= len(max_length),
    ValueError will be raised to indicate the problem.
    """

    if max_length:
        length = max_length - len(prefix)
        if length <= 0:
            raise ValueError("'max_length' must be bigger than 'len(prefix)'.")

        suffix = ''.join(str(random.randint(0, 9)) for i in range(length))
    else:
        suffix = hex(random.randint(0x10000000, 0x7fffffff))[2:]
    return prefix + suffix


def get_rand_device_name(prefix='test'):
    return get_rand_name(
        max_length=constants.DEVICE_NAME_MAX_LEN, prefix=prefix)


def bool_from_env(key, strict=False, default=False):
    value = os.environ.get(key)
    return strutils.bool_from_string(value, strict=strict, default=default)


def get_test_timeout(default=0):
    return int(os.environ.get('OS_TEST_TIMEOUT', default))


def sanitize_log_path(path):
    # Sanitize the string so that its log path is shell friendly
    return path.replace(' ', '-').replace('(', '_').replace(')', '_')


class AttributeDict(dict):

    """Provide attribute access (dict.key) to dictionary values."""

    def __getattr__(self, name):
        """Allow attribute access for all keys in the dict."""
        if name in self:
            return self[name]
        raise AttributeError(_("Unknown attribute '%s'.") % name)


class BaseTestCase(testtools.TestCase):

    def setUp(self):
        super(BaseTestCase, self).setUp()

        # Update the default QueuePool parameters. These can be tweaked by the
        # conf variables - max_pool_size, max_overflow and pool_timeout
        db_options.set_defaults(
            cfg.CONF,
            connection='sqlite://',
            sqlite_db='', max_pool_size=10,
            max_overflow=20, pool_timeout=10)

        # Configure this first to ensure pm debugging support for setUp()
        debugger = os.environ.get('OS_POST_MORTEM_DEBUGGER')
        if debugger:
            self.addOnException(post_mortem_debug.get_exception_handler(
                debugger))

        # Make sure we see all relevant deprecation warnings when running tests
        self.useFixture(tools.WarningsFixture())

        if bool_from_env('OS_DEBUG'):
            _level = std_logging.DEBUG
        else:
            _level = std_logging.INFO
        capture_logs = bool_from_env('OS_LOG_CAPTURE')
        if not capture_logs:
            std_logging.basicConfig(format=LOG_FORMAT, level=_level)
        self.log_fixture = self.useFixture(
            fixtures.FakeLogger(
                format=LOG_FORMAT,
                level=_level,
                nuke_handlers=capture_logs,
            ))

        test_timeout = get_test_timeout()
        if test_timeout == -1:
            test_timeout = 0
        if test_timeout > 0:
            self.useFixture(fixtures.Timeout(test_timeout, gentle=True))

        # If someone does use tempfile directly, ensure that it's cleaned up
        self.useFixture(fixtures.NestedTempfile())
        self.useFixture(fixtures.TempHomeDir())

        self.addCleanup(mock.patch.stopall)

        if bool_from_env('OS_STDOUT_CAPTURE'):
            stdout = self.useFixture(fixtures.StringStream('stdout')).stream
            self.useFixture(fixtures.MonkeyPatch('sys.stdout', stdout))
        if bool_from_env('OS_STDERR_CAPTURE'):
            stderr = self.useFixture(fixtures.StringStream('stderr')).stream
            self.useFixture(fixtures.MonkeyPatch('sys.stderr', stderr))

        self.addOnException(self.check_for_systemexit)
        self.orig_pid = os.getpid()

    def check_for_systemexit(self, exc_info):
        if isinstance(exc_info[1], SystemExit):
            if os.getpid() != self.orig_pid:
                # Subprocess - let it just exit
                raise
            # This makes sys.exit(0) still a failure
            self.force_failure = True

    def assertOrderedEqual(self, expected, actual):
        expect_val = self.sort_dict_lists(expected)
        actual_val = self.sort_dict_lists(actual)
        self.assertEqual(expect_val, actual_val)

    def sort_dict_lists(self, dic):
        for key, value in six.iteritems(dic):
            if isinstance(value, list):
                dic[key] = sorted(value)
            elif isinstance(value, dict):
                dic[key] = self.sort_dict_lists(value)
        return dic

    def assertDictSupersetOf(self, expected_subset, actual_superset):
        """Checks that actual dict contains the expected dict.

        After checking that the arguments are of the right type, this checks
        that each item in expected_subset is in, and matches, what is in
        actual_superset. Separate tests are done, so that detailed info can
        be reported upon failure.
        """
        if not isinstance(expected_subset, dict):
            self.fail("expected_subset (%s) is not an instance of dict" %
                      type(expected_subset))
        if not isinstance(actual_superset, dict):
            self.fail("actual_superset (%s) is not an instance of dict" %
                      type(actual_superset))
        for k, v in expected_subset.items():
            self.assertIn(k, actual_superset)
            self.assertEqual(v, actual_superset[k],
                             "Key %(key)s expected: %(exp)r, actual %(act)r" %
                             {'key': k, 'exp': v, 'act': actual_superset[k]})
