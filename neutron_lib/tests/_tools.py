# Copyright (c) 2013 NEC Corporation
# All Rights Reserved.
#
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

import collections
import fixtures
import warnings


def _safe_sort_key(value):
    """Return value hash or build one for dictionaries."""
    if isinstance(value, collections.Mapping):
        return sorted(value.items())
    return value


class UnorderedList(list):
    """A list that is equals to any permutation of itself."""

    def __eq__(self, other):
        if not isinstance(other, list):
            return False
        return (sorted(self, key=_safe_sort_key) ==
                sorted(other, key=_safe_sort_key))

    def __neq__(self, other):
        return not self == other


class WarningsFixture(fixtures.Fixture):
    """Filters out warnings during test runs."""

    warning_types = (
        DeprecationWarning, PendingDeprecationWarning, ImportWarning
    )

    def _setUp(self):
        self.addCleanup(warnings.resetwarnings)
        for wtype in self.warning_types:
            warnings.filterwarnings(
                "always", category=wtype, module='^neutron_lib\\.')
