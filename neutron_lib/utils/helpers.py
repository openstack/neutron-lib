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

import collections
import decimal
import random

import six

from neutron_lib._i18n import _


def parse_mappings(mapping_list, unique_values=True, unique_keys=True):
    """Parse a list of mapping strings into a dictionary.

    :param mapping_list: a list of strings of the form '<key>:<value>'
    :param unique_values: values must be unique if True
    :param unique_keys: keys must be unique if True, else implies that keys
    and values are not unique
    :returns: a dict mapping keys to values or to list of values
    """
    mappings = {}
    for mapping in mapping_list:
        mapping = mapping.strip()
        if not mapping:
            continue
        split_result = mapping.split(':')
        if len(split_result) != 2:
            raise ValueError(_("Invalid mapping: '%s'") % mapping)
        key = split_result[0].strip()
        if not key:
            raise ValueError(_("Missing key in mapping: '%s'") % mapping)
        value = split_result[1].strip()
        if not value:
            raise ValueError(_("Missing value in mapping: '%s'") % mapping)
        if unique_keys:
            if key in mappings:
                raise ValueError(_("Key %(key)s in mapping: '%(mapping)s' not "
                                   "unique") % {'key': key,
                                                'mapping': mapping})
            if unique_values and value in mappings.values():
                raise ValueError(_("Value %(value)s in mapping: '%(mapping)s' "
                                   "not unique") % {'value': value,
                                                    'mapping': mapping})
            mappings[key] = value
        else:
            mappings.setdefault(key, [])
            if value not in mappings[key]:
                mappings[key].append(value)
    return mappings


def compare_elements(a, b):
    """Compare elements if a and b have same elements.

    This method doesn't consider ordering
    """
    return set(a or []) == set(b or [])


def safe_sort_key(value):
    """Return value hash or build one for dictionaries."""
    if isinstance(value, collections.Mapping):
        return sorted(value.items())
    return value


def dict2str(dic):
    return ','.join("%s=%s" % (key, val)
                    for key, val in sorted(six.iteritems(dic)))


def str2dict(string):
    res_dict = {}
    for keyvalue in string.split(','):
        (key, value) = keyvalue.split('=', 1)
        res_dict[key] = value
    return res_dict


def dict2tuple(d):
    items = list(d.items())
    items.sort()
    return tuple(items)


def diff_list_of_dict(old_list, new_list):
    new_set = set([dict2str(l) for l in new_list])
    old_set = set([dict2str(l) for l in old_list])
    added = new_set - old_set
    removed = old_set - new_set
    return [str2dict(a) for a in added], [str2dict(r) for r in removed]


def get_random_string(length):
    """Get a random hex string of the specified length."""
    return "{0:0{1}x}".format(random.getrandbits(length * 4), length)


def camelize(s):
    return ''.join(s.replace('_', ' ').title().split())


def round_val(val):
    # we rely on decimal module since it behaves consistently across Python
    # versions (2.x vs. 3.x)
    return int(decimal.Decimal(val).quantize(decimal.Decimal('1'),
                                             rounding=decimal.ROUND_HALF_UP))


def safe_decode_utf8(s):
    if six.PY3 and isinstance(s, bytes):
        return s.decode('utf-8', 'surrogateescape')
    return s
