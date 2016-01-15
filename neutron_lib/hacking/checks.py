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

# TODO(dougwig)
# add a rule for not importing neutron directly; most will have to ignore

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

oslo_namespace_imports_dot = re.compile(r"import[\s]+oslo[.][^\s]+")
oslo_namespace_imports_from_dot = re.compile(r"from[\s]+oslo[.]")
oslo_namespace_imports_from_root = re.compile(r"from[\s]+oslo[\s]+import[\s]+")
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


def check_oslo_namespace_imports(logical_line):
    if re.match(oslo_namespace_imports_from_dot, logical_line):
        msg = ("N523: '%s' must be used instead of '%s'.") % (
            logical_line.replace('oslo.', 'oslo_'),
            logical_line)
        yield(0, msg)
    elif re.match(oslo_namespace_imports_from_root, logical_line):
        msg = ("N523: '%s' must be used instead of '%s'.") % (
            logical_line.replace('from oslo import ', 'import oslo_'),
            logical_line)
        yield(0, msg)
    elif re.match(oslo_namespace_imports_dot, logical_line):
        msg = ("N523: '%s' must be used instead of '%s'.") % (
            logical_line.replace('import', 'from').replace('.', ' import '),
            logical_line)
        yield(0, msg)


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


def factory(register):
    register(use_jsonutils)
    register(check_oslo_namespace_imports)
    register(check_no_contextlib_nested)
    register(check_python3_xrange)
    register(check_no_basestring)
    register(check_python3_no_iteritems)
    register(no_mutable_default_args)
