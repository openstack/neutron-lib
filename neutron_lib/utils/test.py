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

"""Test functions."""

import functools


def unstable_test(reason):
    """Decorator used to mark test as unstable, on failure test will be skipped

    :param reason: String used in explanation, for example, 'bug 123456'.
    """
    def decor(f):
        @functools.wraps(f)
        def inner(self, *args, **kwargs):
            try:
                return f(self, *args, **kwargs)
            except Exception as e:
                msg = ("%s was marked as unstable because of %s, "
                       "failure was: %s") % (self.id(), reason, e)
                raise self.skipTest(msg)
        return inner
    return decor
