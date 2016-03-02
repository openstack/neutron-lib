# Copyright (c) 2014 OpenStack Foundation.
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

import re

# Guidelines for writing new hacking checks
#
#  - Use only for Neutron specific tests. OpenStack general tests
#    should be submitted to the common 'hacking' module.
#  - Pick numbers in the range N5xx. Find the current test with
#    the highest allocated number and then pick the next value.
#  - Keep the test method code in the source file ordered based
#    on the N5xx value.
#  - List the new rule in the top level HACKING.rst file
#  - Add test cases for each new rule to
#    neutron_lib/tests/unit/hacking/test_checks.py

mutable_default_args = re.compile(r"^\s*def .+\((.+=\{\}|.+=\[\])")

namespace_imports_dot = re.compile(r"import[\s]+([\w]+)[.][^\s]+")
namespace_imports_from_dot = re.compile(r"from[\s]+([\w]+)[.]")
namespace_imports_from_root = re.compile(r"from[\s]+([\w]+)[\s]+import[\s]+")
contextlib_nested = re.compile(r"^with (contextlib\.)?nested\(")


def use_jsonutils(logical_line, filename):
    msg = "N521: jsonutils.%(fun)s must be used instead of json.%(fun)s"

    # Some files in the tree are not meant to be run from inside Neutron
    # itself, so we should not complain about them not using jsonutils
    json_check_skipped_patterns = [
        "neutron/plugins/ml2/drivers/openvswitch/agent/xenapi/etc/xapi.d/"
        "plugins/netwrap",
    ]

    for pattern in json_check_skipped_patterns:
        if pattern in filename:
            return

    if "json." in logical_line:
        json_funcs = ['dumps(', 'dump(', 'loads(', 'load(']
        for f in json_funcs:
            pos = logical_line.find('json.%s' % f)
            if pos != -1:
                yield (pos, msg % {'fun': f[:-1]})


def _check_imports(regex, submatch, logical_line):
    m = re.match(regex, logical_line)
    if m and m.group(1) == submatch:
        return True


def _check_namespace_imports(failure_code, namespace, new_ns, logical_line,
                             message_override=None):
    if message_override is not None:
        msg_o = "%s: %s" % (failure_code, message_override)
    else:
        msg_o = None

    if _check_imports(namespace_imports_from_dot, namespace, logical_line):
        msg = ("%s: '%s' must be used instead of '%s'.") % (
            failure_code,
            logical_line.replace('%s.' % namespace, new_ns),
            logical_line)
        return (0, msg_o or msg)
    elif _check_imports(namespace_imports_from_root, namespace, logical_line):
        msg = ("%s: '%s' must be used instead of '%s'.") % (
            failure_code,
            logical_line.replace(
                'from %s import ' % namespace, 'import %s' % new_ns),
            logical_line)
        return (0, msg_o or msg)
    elif _check_imports(namespace_imports_dot, namespace, logical_line):
        msg = ("%s: '%s' must be used instead of '%s'.") % (
            failure_code,
            logical_line.replace('import', 'from').replace('.', ' import '),
            logical_line)
        return (0, msg_o or msg)


def check_oslo_namespace_imports(logical_line):
    x = _check_namespace_imports('N523', 'oslo', 'oslo_', logical_line)
    if x is not None:
        yield x


def check_no_contextlib_nested(logical_line, filename):
    msg = ("N524: contextlib.nested is deprecated. With Python 2.7 and later "
           "the with-statement supports multiple nested objects. See https://"
           "docs.python.org/2/library/contextlib.html#contextlib.nested for "
           "more information.")

    if contextlib_nested.match(logical_line):
        yield(0, msg)


def check_python3_xrange(logical_line):
    if re.search(r"\bxrange\s*\(", logical_line):
        yield(0, "N525: Do not use xrange. Use range, or six.moves.range for "
                 "large loops.")


def check_no_basestring(logical_line):
    if re.search(r"\bbasestring\b", logical_line):
        msg = ("N526: basestring is not Python3-compatible, use "
               "six.string_types instead.")
        yield(0, msg)


def check_python3_no_iteritems(logical_line):
    if re.search(r".*\.iteritems\(\)", logical_line):
        msg = ("N527: Use six.iteritems() instead of dict.iteritems().")
        yield(0, msg)


def no_mutable_default_args(logical_line):
    msg = "N529: Method's default argument shouldn't be mutable!"
    if mutable_default_args.match(logical_line):
        yield (0, msg)


# Chances are that most projects will need to put an ignore on this rule
# until they can fully migrate to the lib.

def check_neutron_namespace_imports(logical_line):
    x = _check_namespace_imports(
        'N530', 'neutron', 'neutron_lib.', logical_line,
        message_override="direct neutron imports not allowed")
    if x is not None:
        yield x


def factory(register):
    register(use_jsonutils)
    register(check_oslo_namespace_imports)
    register(check_no_contextlib_nested)
    register(check_python3_xrange)
    register(check_no_basestring)
    register(check_python3_no_iteritems)
    register(no_mutable_default_args)
    register(check_neutron_namespace_imports)
