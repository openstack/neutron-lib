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

import pep8

_all_log_levels = {
    'critical': '_LC',
    'error': '_LE',
    'exception': '_LE',
    'info': '_LI',
    'reserved': '_',  # this should never be used with a log unless
                      # it is a variable used for a log message and
                      # a exception
    'warning': '_LW',
}
_all_hints = set(_all_log_levels.values())
_log_warn = re.compile(
    r"(.)*LOG\.(warn)\(\s*('|\"|_)")


def _regex_for_level(level, hint):
    return r".*LOG\.%(level)s\(\s*((%(wrong_hints)s)\(|'|\")" % {
        'level': level,
        'wrong_hints': '|'.join(_all_hints - set([hint])),
    }


_log_translation_hint = re.compile(
    '|'.join('(?:%s)' % _regex_for_level(level, hint)
             for level, hint in _all_log_levels.items()))
_log_string_interpolation = re.compile(
    r".*LOG\.(error|warning|info|critical|exception|debug)\([^,]*%[^,]*[,)]")


def _translation_is_not_expected(filename):
    # Do not do these validations on tests
    return any(pat in filename for pat in ["/tests/", "rally-jobs/plugins/"])


def validate_log_translations(logical_line, physical_line, filename):
    if _translation_is_not_expected(filename):
        return

    if pep8.noqa(physical_line):
        return

    msg = "N531: Log messages require translation hints!"
    if _log_translation_hint.match(logical_line):
        yield (0, msg)


def check_log_warn_deprecated(logical_line, filename):
    msg = "N532: Use LOG.warning due to compatibility with py3"
    if _log_warn.match(logical_line):
        yield (0, msg)


def no_translate_debug_logs(logical_line, filename):
    """Check for 'LOG.debug(_(' and 'LOG.debug(_Lx('

    As per our translation policy,
    https://wiki.openstack.org/wiki/LoggingStandards#Log_Translation
    we shouldn't translate debug level logs.

    * This check assumes that 'LOG' is a logger.
    N533
    """
    for hint in _all_hints:
        if logical_line.startswith("LOG.debug(%s(" % hint):
            yield(0, "N533 Don't translate debug level logs")


def check_raised_localized_exceptions(logical_line, filename):
    if _translation_is_not_expected(filename):
        return

    logical_line = logical_line.strip()
    raised_search = re.compile(
        r"raise (?:\w*)\((.*)\)").match(logical_line)
    if raised_search:
        exception_msg = raised_search.groups()[0]
        if exception_msg.startswith("\"") or exception_msg.startswith("\'"):
            msg = "N534: Untranslated exception message."
            yield (logical_line.index(exception_msg), msg)


def check_delayed_string_interpolation(logical_line, filename, noqa):
    """N536 String interpolation should be delayed at logging calls.

    N536: LOG.debug('Example: %s' % 'bad')
    Okay: LOG.debug('Example: %s', 'good')
    """
    msg = ("N536 String interpolation should be delayed to be "
           "handled by the logging code, rather than being done "
           "at the point of the logging call. "
           "Use ',' instead of '%'.")

    if noqa:
        return

    if '/tests/' in filename:
        return

    if _log_string_interpolation.match(logical_line):
        yield(logical_line.index('%'), msg)
