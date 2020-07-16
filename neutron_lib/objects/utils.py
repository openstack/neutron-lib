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

import abc
import copy

from neutron_lib import exceptions


def convert_filters(**kwargs):
    result = copy.deepcopy(kwargs)
    if 'tenant_id' in result:
        if 'project_id' in result:
            raise exceptions.TenantIdProjectIdFilterConflict()

        result['project_id'] = result.pop('tenant_id')
    return result


class FilterObj(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def filter(self, column):
        pass


class StringMatchingFilterObj(FilterObj):
    @property
    def is_contains(self):
        return bool(getattr(self, "contains", False))

    @property
    def is_starts(self):
        return bool(getattr(self, "starts", False))

    @property
    def is_ends(self):
        return bool(getattr(self, "ends", False))


class StringContains(StringMatchingFilterObj):

    def __init__(self, matching_string):
        super().__init__()
        self.contains = matching_string

    def filter(self, column):
        return column.contains(self.contains)


class StringStarts(StringMatchingFilterObj):

    def __init__(self, matching_string):
        super().__init__()
        self.starts = matching_string

    def filter(self, column):
        return column.startswith(self.starts)


class StringEnds(StringMatchingFilterObj):

    def __init__(self, matching_string):
        super().__init__()
        self.ends = matching_string

    def filter(self, column):
        return column.endswith(self.ends)


class NotIn(FilterObj):

    def __init__(self, value):
        super().__init__()
        self.value = value

    def filter(self, column):
        return ~column.in_(self.value)


class NotEqual(FilterObj):

    def __init__(self, value):
        super().__init__()
        self.value = value

    def filter(self, column):
        return column != self.value


def get_updatable_fields(cls, fields):
    fields = fields.copy()
    for field in cls.fields_no_update:
        if field in fields:
            del fields[field]
    return fields
