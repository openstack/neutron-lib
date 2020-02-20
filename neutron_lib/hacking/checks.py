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

from hacking import core

from neutron_lib.hacking import translation_checks

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
contextlib_nested = re.compile(r"^\s*with (contextlib\.)?nested\(")

assert_equal_none_re = re.compile(
    r"assertEqual\(.*?,\s+None\)(( |\t)*#.*)?$|assertEqual\(None,")
assert_is_none_re = re.compile(
    r"assertIs(Not)?\(.*,\s+None\)(( |\t)*#.*)?$|assertIs(Not)?\(None,")


@core.flake8ext
def use_jsonutils(logical_line, filename):
    """N521 - jsonutils must be used instead of json.

    :param logical_line: The logical line to check.
    :param filename: The file name where the logical line exists.
    :returns: None if the logical line passes the check, otherwise a tuple
        is yielded that contains the offending index in logical line and a
        message describe the check validation failure.
    """
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


@core.flake8ext
def check_no_contextlib_nested(logical_line, filename):
    """N524 - Use of contextlib.nested is deprecated.

    :param logical_line: The logical line to check.
    :param filename: The file name where the logical line exists.
    :returns: None if the logical line passes the check, otherwise a tuple
        is yielded that contains the offending index in logical line and a
        message describe the check validation failure.
    """
    msg = ("N524: contextlib.nested is deprecated. With Python 2.7 and later "
           "the with-statement supports multiple nested objects. See https://"
           "docs.python.org/2/library/contextlib.html#contextlib.nested for "
           "more information.")

    if contextlib_nested.match(logical_line):
        yield(0, msg)


@core.flake8ext
def no_mutable_default_args(logical_line):
    """N529 - Method's default argument shouldn't be mutable.

    :param logical_line: The logical line to check.
    :returns: None if the logical line passes the check, otherwise a tuple
        is yielded that contains the offending index in logical line and a
        message describe the check validation failure.
    """
    msg = "N529: Method's default argument shouldn't be mutable!"
    if mutable_default_args.match(logical_line):
        yield (0, msg)


# Chances are that most projects will need to put an ignore on this rule
# until they can fully migrate to the lib.

@core.flake8ext
def check_neutron_namespace_imports(logical_line):
    """N530 - Direct neutron imports not allowed.

    :param logical_line: The logical line to check.
    :returns: None if the logical line passes the check, otherwise a tuple
        is yielded that contains the offending index in logical line and a
        message describe the check validation failure.
    """
    x = _check_namespace_imports(
        'N530', 'neutron', 'neutron_lib.', logical_line,
        message_override="direct neutron imports not allowed")
    if x is not None:
        yield x


@core.flake8ext
def check_no_eventlet_imports(logical_line):
    """N535 - Usage of Python eventlet module not allowed.

    :param logical_line: The logical line to check.
    :returns: None if the logical line passes the check, otherwise a tuple
        is yielded that contains the offending index in logical line and a
        message describe the check validation failure.
    """
    if re.match(r'(import|from)\s+[(]?eventlet', logical_line):
        msg = 'N535: Usage of Python eventlet module not allowed'
        yield logical_line.index('eventlet'), msg


@core.flake8ext
def assert_equal_none(logical_line):
    """N536 - Use assertIsNone."""
    if assert_equal_none_re.search(logical_line):
        msg = ("N536: Use assertIsNone rather than assertEqual "
               "to check for None values")
        yield logical_line.index('assert'), msg

    if assert_is_none_re.search(logical_line):
        msg = ("N536: Use assertIsNone or assertIsNotNone rather than "
               "assertIs or assertIsNone to check for None values.")
        yield logical_line.index('assert'), msg


# TODO(amotoki): Drop this once all neutron related projects
# have switched to hacking 2.x
def factory(register):
    """Hacking check factory for neutron-lib adopter compliant checks.

    Hacking check factory for use with tox.ini. This factory registers all
    neutron-lib adopter checks consumers should seek to comply with.

    :param register: The function to register the check functions with.
    :returns: None.
    """
    register(use_jsonutils)
    register(check_no_contextlib_nested)
    register(no_mutable_default_args)
    register(check_neutron_namespace_imports)
    register(translation_checks.no_translate_logs)
    register(translation_checks.check_log_warn_deprecated)
    register(translation_checks.check_raised_localized_exceptions)
    register(assert_equal_none)
