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
import weakref

from oslo_log import log as logging
from oslo_utils import timeutils
from oslo_utils import uuidutils

from neutron_lib._i18n import _


LOG = logging.getLogger(__name__)


def parse_mappings(mapping_list, unique_values=True, unique_keys=True):
    """Parse a list of mapping strings into a dictionary.

    :param mapping_list: A list of strings of the form '<key>:<value>'.
    :param unique_values: Values must be unique if True.
    :param unique_keys: Keys must be unique if True, else implies that keys
        and values are not unique.
    :returns: A dict mapping keys to values or to list of values.
    :raises ValueError: Upon malformed data or duplicate keys.
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

    This method doesn't consider ordering.

    :param a: The first item to compare.
    :param b: The second item to compare.
    :returns: True if a and b have the same elements, False otherwise.
    """
    return set(a or []) == set(b or [])


def safe_sort_key(value):
    """Return value hash or build one for dictionaries.

    :param value: The value to build a hash for.
    :returns: The value sorted.
    """
    if isinstance(value, collections.Mapping):
        return sorted(value.items())
    return value


def dict2str(dic):
    """Build a str representation of a dict.

    :param dic: The dict to build a str representation for.
    :returns: The dict in str representation that is a k=v command list for
        each item in dic.
    """
    return ','.join("%s=%s" % (key, val)
                    for key, val in sorted(dic.items()))


def str2dict(string):
    """Parse a str representation of a dict into its dict form.

    This is the inverse of dict2str()

    :param string: The string to parse.
    :returns: A dict constructed from the str representation in string.
    """
    res_dict = {}
    for keyvalue in string.split(','):
        (key, value) = keyvalue.split('=', 1)
        res_dict[key] = value
    return res_dict


def dict2tuple(d):
    """Build a tuple from a dict.

    :param d: The dict to coherence into a tuple.
    :returns: The dict d in tuple form.
    """
    items = list(d.items())
    items.sort()
    return tuple(items)


def diff_list_of_dict(old_list, new_list):
    """Given 2 lists of dicts, return a tuple containing the diff.

    :param old_list: The old list of dicts to diff.
    :param new_list: The new list of dicts to diff.
    :returns: A tuple where the first item is a list of the added dicts in
        the diff and the second item is the removed dicts.
    """
    new_set = set([dict2str(i) for i in new_list])
    old_set = set([dict2str(i) for i in old_list])
    added = new_set - old_set
    removed = old_set - new_set
    return [str2dict(a) for a in added], [str2dict(r) for r in removed]


def get_random_string(length):
    """Get a random hex string of the specified length.

    :param length: The length for the hex string.
    :returns: A random hex string of the said length.
    """
    return "{0:0{1}x}".format(random.getrandbits(length * 4), length)


def camelize(s):
    """Camelize a str that uses _ as a camelize token.

    :param s: The str to camelize that contains a _ at each index where a new
        camelized word starts.
    :returns: The camelized str.
    """
    return ''.join(s.replace('_', ' ').title().split())


def round_val(val):
    """Round the value.

    :param val: The value to round.
    :returns: The value rounded using the half round up scheme.
    """
    # we rely on decimal module since it behaves consistently across Python
    # versions (2.x vs. 3.x)
    return int(decimal.Decimal(val).quantize(decimal.Decimal('1'),
                                             rounding=decimal.ROUND_HALF_UP))


def safe_decode_utf8(s):
    """Safe decode a str from UTF.

    :param s: The str to decode.
    :returns: The decoded str.
    """
    if isinstance(s, bytes):
        return s.decode('utf-8', 'surrogateescape')
    return s


weak_method = weakref.WeakMethod


def make_weak_ref(f):
    """Make a weak reference to a function accounting for bound methods.

    :param f: The callable to make a weak ref for.
    :returns: A weak ref to f.
    """
    return weak_method(f) if hasattr(f, '__self__') else weakref.ref(f)


def resolve_ref(ref):
    """Handles dereference of weakref.

    :param ref: The weak ref to resolve.
    :returns: The resolved reference.
    """
    if isinstance(ref, weakref.ref):
        ref = ref()
    return ref


def timecost(f):
    call_id = uuidutils.generate_uuid()
    message_base = ("Time-cost: call %(call_id)s function %(fname)s ") % {
                    "call_id": call_id, "fname": f.__name__}
    end_message = (message_base + "took %(seconds).3fs seconds to run")

    @timeutils.time_it(LOG, message=end_message, min_duration=None)
    def wrapper(*args, **kwargs):
        LOG.debug(message_base + "start")
        ret = f(*args, **kwargs)
        return ret
    return wrapper
