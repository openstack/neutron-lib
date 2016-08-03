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

from debtcollector import moves
from debtcollector import removals
from hacking import core
import pep8

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


@core.flake8ext
@core.off_by_default
def use_jsonutils(logical_line, filename):
    """N521 - jsonutils must be used instead of json."""
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


@removals.remove(removal_version='P release')
@core.flake8ext
@core.off_by_default
def check_oslo_namespace_imports(logical_line):
    """N523 - Import oslo_ rather than oslo."""
    x = _check_namespace_imports('N523', 'oslo', 'oslo_', logical_line)
    if x is not None:
        yield x


@core.flake8ext
@core.off_by_default
def check_no_contextlib_nested(logical_line, filename):
    """N524 - Use of contextlib.nested is deprecated."""
    msg = ("N524: contextlib.nested is deprecated. With Python 2.7 and later "
           "the with-statement supports multiple nested objects. See https://"
           "docs.python.org/2/library/contextlib.html#contextlib.nested for "
           "more information.")

    if contextlib_nested.match(logical_line):
        yield(0, msg)


@core.flake8ext
@core.off_by_default
def check_python3_xrange(logical_line):
    """N525 - Do not use xrange."""
    if re.search(r"\bxrange\s*\(", logical_line):
        yield(0, "N525: Do not use xrange. Use range, or six.moves.range for "
                 "large loops.")


@core.flake8ext
@core.off_by_default
def check_no_basestring(logical_line):
    """N526 - basestring is not Python3-compatible."""
    if re.search(r"\bbasestring\b", logical_line):
        msg = ("N526: basestring is not Python3-compatible, use "
               "six.string_types instead.")
        yield(0, msg)


@core.flake8ext
@core.off_by_default
def check_python3_no_iteritems(logical_line):
    """N527 - Use dict.items() instead of dict.iteritems()."""
    if re.search(r".*\.iteritems\(\)", logical_line):
        msg = ("N527: Use dict.items() instead of dict.iteritems() to be "
               "compatible with both Python 2 and Python 3. In Python 2, "
               "dict.items() may be inefficient for very large dictionaries. "
               "If you can prove that you need the optimization of an "
               "iterator for Python 2, then you can use six.iteritems(dict).")
        yield(0, msg)


@core.flake8ext
@core.off_by_default
def no_mutable_default_args(logical_line):
    """N529 - Method's default argument shouldn't be mutable."""
    msg = "N529: Method's default argument shouldn't be mutable!"
    if mutable_default_args.match(logical_line):
        yield (0, msg)


# Chances are that most projects will need to put an ignore on this rule
# until they can fully migrate to the lib.
@core.flake8ext
@core.off_by_default
def check_neutron_namespace_imports(logical_line):
    """N530 - Direct neutron imports not allowed."""
    x = _check_namespace_imports(
        'N530', 'neutron', 'neutron_lib.', logical_line,
        message_override="direct neutron imports not allowed")
    if x is not None:
        yield x


@core.flake8ext
@core.off_by_default
def check_no_eventlet_imports(logical_line):
    """N535 - Usage of Python eventlet module not allowed."""
    if re.match(r'(import|from)\s+[(]?eventlet', logical_line):
        msg = 'N535: Usage of Python eventlet module not allowed'
        yield logical_line.index('eventlet'), msg


ALL_CHECKS = set([use_jsonutils,
                  check_no_contextlib_nested,
                  check_python3_xrange,
                  check_no_basestring,
                  check_python3_no_iteritems,
                  no_mutable_default_args,
                  check_neutron_namespace_imports,
                  translation_checks.validate_log_translations,
                  translation_checks.no_translate_debug_logs,
                  translation_checks.check_log_warn_deprecated,
                  translation_checks.check_raised_localized_exceptions,
                  check_no_eventlet_imports])

_LIB_PROJECT_CHECKS = ALL_CHECKS

ADOPTER_CHECKS = ALL_CHECKS - set([check_no_eventlet_imports])


def _get_pep8_checks():
    check_types = ['physical_line', 'logical_line', 'tree']
    style_guide = pep8.StyleGuide()
    check_reg = {}

    for check_type in check_types:
        for registered_check in style_guide.get_checks(check_type):
            check_reg[registered_check[0]] = registered_check
    return check_reg


def _register_and_enable_checks(register, checks):
    """Call register for each check; ensuring its enabled."""
    check_reg = _get_pep8_checks()

    for check in checks:
        # NOTE(boden): checks registered via entry points already exist
        # and must be enabled programmatically
        check = (check_reg[check.__name__][1]
                 if check.__name__ in check_reg
                 else check)
        setattr(check, 'off_by_default', False)
        register(check)


def latest_adopter_hacking_checks(register):
    """Hacking check factory for neutron-lib adopter compliant checks.

    This factory registers all checks neutron-lib adopters should seek to
    pass. The set of checks registered is the latest set of adopter checks
    and is thus subject to change from release to release.

    As neutron-lib hacking checks are registered as entry points and default
    to disabled, consumers have more granular control over checks by not using
    this factory function and instead selecting individual checks via their
    flake8/tox configuration.

    This function should only be used with tox flake8 hacking targets.

    :param register: The register function to call for each check.
    :return: None
    """
    _register_and_enable_checks(register, ADOPTER_CHECKS)


# TODO(boden): update removal_version once naming determined
factory = moves.moved_function(latest_adopter_hacking_checks,
                               'factory', __name__,
                               message='function renamed to reflect '
                                       'explicit usage',
                               version='newton',
                               removal_version='P release')


def _neutron_lib_project_hacking_checks(register):
    """neutron-lib project specific hacking checks."""
    _register_and_enable_checks(register, _LIB_PROJECT_CHECKS)


class _ProxyHackingChecks(core.GlobalCheck):
    """Flake8 extension to ensure latest off_by_default is used.

    Hacking checks registered via entry point are typically set
    off_by_default to True so that consumers can selectively enable them.
    Subsequent factory method calls to register and enable hacking checks
    go unnoticed; the check registered via entry point takes precedence by
    default.

    This flake8 extension is registered via entry point and performs option
    handling to ensure any changes to hacking check off_by_default are
    reflected in the checks ignored in the options. This allows consumers
    to use our hacking check factory methods to enable checks pragmatically.

    Note that if consumers use flake8 CLI with the --ignore option, the ignored
    checks are not even in the list of checks returned by pep8. Therefore CLI
    select/ignore still functions as expected regardless of the off_by_default
    logic contained herein.
    """
    name = 'enabled-hacking-check-proxy'

    @classmethod
    def parse_options(cls, opts):
        ignore = list(opts.ignore)

        # NOTE(boden): make sure options.ignore has the latest off_by_default
        # from pep8 registered checks that may be set post entry-point loading
        for fn_name, check_data in _get_pep8_checks().items():
            check_fn = check_data[1]

            enabled = not getattr(check_fn, 'off_by_default', False)
            if enabled:
                check_codes = pep8.ERRORCODE_REGEX.findall(
                    check_fn.__doc__ or '')
                # Remove check's codes from default ignore list
                for code in check_codes:
                    if code in ignore:
                        ignore.remove(code)
        opts.ignore = tuple(ignore)
