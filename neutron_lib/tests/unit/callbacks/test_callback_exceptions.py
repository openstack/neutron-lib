# -*- coding: utf-8 -*-

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

"""
test_callback_exceptions
----------------------------------

Tests for `neutron_lib.callback.exceptions` module.
"""

import functools

import neutron_lib._callbacks.exceptions as ex
from neutron_lib.tests.unit import test_exceptions


class TestCallbackExceptions(test_exceptions.TestExceptions):

    def _check_exception(self, exc_class, expected_msg, **kwargs):
        raise_exc_class = functools.partial(test_exceptions._raise, exc_class)
        e = self.assertRaises(exc_class, raise_exc_class, **kwargs)
        self.assertEqual(expected_msg, str(e))

    def test_invalid(self):
        self._check_exception(
            ex.Invalid,
            "The value 'foo' for bar is not valid.",
            value='foo', element='bar')

    def test_callback_failure(self):
        self._check_exception(
            ex.CallbackFailure,
            'one',
            errors='one')

    def test_callback_failure_with_list(self):
        self._check_exception(
            ex.CallbackFailure,
            '1,2,3',
            errors=[1, 2, 3])

    def test_notification_error(self):
        '''Test that correct message is create for this error class.'''
        error = ex.NotificationError('abc', 'boom')
        self.assertEqual('Callback abc failed with "boom"', str(error))
