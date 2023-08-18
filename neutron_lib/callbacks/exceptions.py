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

from neutron_lib._i18n import _
from neutron_lib import exceptions


class Invalid(exceptions.NeutronException):
    message = _("The value '%(value)s' for %(element)s is not valid.")


class CallbackFailure(exceptions.MultipleExceptions):

    def __init__(self, errors):
        self.errors = errors

    def __str__(self):
        if isinstance(self.errors, list):
            return ','.join(str(error) for error in self.errors)
        else:
            return str(self.errors)

    @property
    def inner_exceptions(self):
        """The list of unpacked errors for this exception.

        :return: A list of unpacked errors for this exception. An unpacked
            error is the Exception's 'error' attribute if it inherits from
            NotificationError, otherwise it's the exception itself.
        """
        if isinstance(self.errors, list):
            return [self._unpack_if_notification_error(e) for e in self.errors]
        return [self._unpack_if_notification_error(self.errors)]

    @staticmethod
    def _unpack_if_notification_error(exc):
        if isinstance(exc, NotificationError):
            return exc.error
        return exc


class NotificationError(object):

    def __init__(self, callback_id, error, cancellable=False):
        self.callback_id = callback_id
        self.error = error
        self._cancellable = cancellable

    def __str__(self):
        return 'Callback %s failed with "%s"' % (self.callback_id, self.error)

    @property
    def is_cancellable(self):
        return self._cancellable
