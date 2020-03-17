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


_all_log_levels = {'critical', 'error', 'exception', 'info',
                   'warning', 'debug'}
_all_hints = {'_LC', '_LE', '_LI', '_', '_LW'}


_log_warn = re.compile(
    r"(.)*LOG\.(warn)\(\s*('|\")")


_log_translation_hint = re.compile(
    r".*LOG\.(%(levels)s)\(\s*(%(hints)s)\(" % {
        'levels': '|'.join(_all_log_levels),
        'hints': '|'.join(_all_hints),
    })


def _translation_checks_not_enforced(filename):
    # Do not do these validations on tests
    return any(pat in filename for pat in ["/tests/", "rally-jobs/plugins/"])


@core.flake8ext
def check_log_warn_deprecated(logical_line, filename):
    """N532 - Use LOG.warning due to compatibility with py3.

    :param logical_line: The logical line to check.
    :param filename: The file name where the logical line exists.
    :returns: None if the logical line passes the check, otherwise a tuple
        is yielded that contains the offending index in logical line and a
        message describe the check validation failure.
    """
    msg = "N532: Use LOG.warning due to compatibility with py3"
    if _log_warn.match(logical_line):
        yield (0, msg)


@core.flake8ext
def check_raised_localized_exceptions(logical_line, filename):
    """N534 - Untranslated exception message.

    :param logical_line: The logical line to check.
    :param filename: The file name where the logical line exists.
    :returns: None if the logical line passes the check, otherwise a tuple
        is yielded that contains the offending index in logical line and a
        message describe the check validation failure.
    """
    if _translation_checks_not_enforced(filename):
        return

    logical_line = logical_line.strip()
    raised_search = re.compile(
        r"raise (?:\w*)\((.*)\)").match(logical_line)
    if raised_search:
        exception_msg = raised_search.groups()[0]
        if exception_msg.startswith("\"") or exception_msg.startswith("\'"):
            msg = "N534: Untranslated exception message."
            yield (logical_line.index(exception_msg), msg)


@core.flake8ext
def no_translate_logs(logical_line, filename):
    """N537 - Don't translate logs.

    Check for 'LOG.*(_(' and 'LOG.*(_Lx('

    Translators don't provide translations for log messages, and operators
    asked not to translate them.

    * This check assumes that 'LOG' is a logger.

    :param logical_line: The logical line to check.
    :param filename: The file name where the logical line exists.
    :returns: None if the logical line passes the check, otherwise a tuple
        is yielded that contains the offending index in logical line and a
        message describe the check validation failure.
    """
    if _translation_checks_not_enforced(filename):
        return

    msg = "N537: Log messages should not be translated!"
    match = _log_translation_hint.match(logical_line)
    if match:
        yield (logical_line.index(match.group()), msg)
