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

import collections

from oslo_log import log as logging
from oslo_utils import reflection

from neutron_lib.callbacks import events
from neutron_lib.callbacks import exceptions
from neutron_lib.callbacks import priority_group
from neutron_lib.db import utils as db_utils

LOG = logging.getLogger(__name__)
PriorityCallbacks = collections.namedtuple(
    'PriorityCallbacks', ['priority', 'pri_callbacks', 'cancellable'])
Callback = collections.namedtuple(
    'Callback', ['id', 'method', 'cancellable'])


class CallbacksManager:
    """A callback system that allows objects to cooperate in a loose manner."""

    def __init__(self):
        self.clear()

    def subscribe(self, callback, resource, event,
                  priority=priority_group.PRIORITY_DEFAULT,
                  cancellable=False):
        """Subscribe callback for a resource event.

        The same callback may register for more than one event.

        :param callback: the callback. It must raise or return a boolean.
        :param resource: the resource. It must be a valid resource.
        :param event: the event. It must be a valid event.
        :param priority: the priority. Callbacks are sorted by priority
                         to be called. Smaller one is called earlier.
        :param cancellable: if the callback is "cancellable", in case of
                            returning an exception, the callback manager will
                            raise a ``CallbackFailure`` exception.
        """
        LOG.debug("Subscribe: %(callback)s %(resource)s %(event)s "
                  "%(priority)d, %(cancellable)s",
                  {'callback': callback, 'resource': resource, 'event': event,
                   'priority': priority, 'cancellable': cancellable})

        callback_id = _get_id(callback)
        pri_callbacks_list = self._callbacks[resource].setdefault(event, [])
        for pri_callbacks in pri_callbacks_list:
            if pri_callbacks.priority == priority:
                pri_callbacks = pri_callbacks.pri_callbacks
                break
        else:
            pri_callbacks = {}
            pri_callbacks_list.append(
                PriorityCallbacks(priority, pri_callbacks, cancellable))
            pri_callbacks_list.sort(key=lambda x: x.priority)
        pri_callbacks[callback_id] = callback

        # We keep a copy of callbacks to speed the unsubscribe operation.
        if callback_id not in self._index:
            self._index[callback_id] = collections.defaultdict(set)
        self._index[callback_id][resource].add(event)

    def _del_callback(self, pri_callbacks, callback_id):
        for pri_callback in pri_callbacks:
            if callback_id in pri_callback.pri_callbacks:
                del pri_callback.pri_callbacks[callback_id]
                if not pri_callback.pri_callbacks:
                    pri_callbacks.remove(pri_callback)
                break

    def unsubscribe(self, callback, resource, event):
        """Unsubscribe callback from the registry.

        :param callback: the callback.
        :param resource: the resource.
        :param event: the event.
        """
        LOG.debug("Unsubscribe: %(callback)s %(resource)s %(event)s",
                  {'callback': callback, 'resource': resource, 'event': event})

        callback_id = self._find(callback)
        if not callback_id:
            LOG.debug("Callback %s not found", callback_id)
            return
        if resource and event:
            self._del_callback(self._callbacks[resource][event], callback_id)
            self._index[callback_id][resource].discard(event)
            if not self._index[callback_id][resource]:
                del self._index[callback_id][resource]
                if not self._index[callback_id]:
                    del self._index[callback_id]
        else:
            value = '{},{}'.format(resource, event)
            raise exceptions.Invalid(element='resource,event', value=value)

    def unsubscribe_by_resource(self, callback, resource):
        """Unsubscribe callback for any event associated to the resource.

        :param callback: the callback.
        :param resource: the resource.
        """
        callback_id = self._find(callback)
        if callback_id:
            if resource in self._index[callback_id]:
                for event in self._index[callback_id][resource]:
                    self._del_callback(self._callbacks[resource][event],
                                       callback_id)
                del self._index[callback_id][resource]
                if not self._index[callback_id]:
                    del self._index[callback_id]

    def unsubscribe_all(self, callback):
        """Unsubscribe callback for all events and all resources.


        :param callback: the callback.
        """
        callback_id = self._find(callback)
        if callback_id:
            for resource, resource_events in self._index[callback_id].items():
                for event in resource_events:
                    self._del_callback(self._callbacks[resource][event],
                                       callback_id)
            del self._index[callback_id]

    @db_utils.reraise_as_retryrequest
    def publish(self, resource, event, trigger, payload=None):
        """Notify all subscribed callback(s) with a payload.

        Dispatch the resource's event to the subscribed callbacks.

        :param resource: The resource for the event.
        :param event: The event.
        :param trigger: The trigger. A reference to the sender of the event.
        :param payload: The optional event object to send to subscribers. If
            passed this must be an instance of BaseEvent.
        :raises neutron_lib.callbacks.exceptions.Invalid: if
            the payload object is not an instance of BaseEvent.
        :raises CallbackFailure: if the underlying callback has errors.
        """
        if payload:
            if not isinstance(payload, events.EventPayload):
                raise exceptions.Invalid(element='event payload',
                                         value=type(payload))
        errors = self._notify_loop(resource, event, trigger, payload)
        if errors:
            if event.startswith(events.BEFORE):
                abort_event = event.replace(
                    events.BEFORE, events.ABORT)
                self._notify_loop(resource, abort_event, trigger, payload)

                raise exceptions.CallbackFailure(errors=errors)

            if (event.startswith(events.PRECOMMIT) or
                    any(error.is_cancellable for error in errors)):
                raise exceptions.CallbackFailure(errors=errors)

    def clear(self):
        """Brings the manager to a clean slate."""
        self._callbacks = collections.defaultdict(dict)
        self._index = collections.defaultdict(dict)

    def _notify_loop(self, resource, event, trigger, payload):
        """The notification loop."""
        errors = []
        callbacks = []
        for pri_callbacks in self._callbacks[resource].get(event, []):
            for cb_id, cb_method in pri_callbacks.pri_callbacks.items():
                cb = Callback(cb_id, cb_method, pri_callbacks.cancellable)
                callbacks.append(cb)
        resource_id = getattr(payload, "resource_id", None)
        LOG.debug("Publish callbacks %s for %s (%s), %s",
                  [c.id for c in callbacks], resource, resource_id, event)
        # TODO(armax): consider using a GreenPile
        for callback in callbacks:
            try:
                callback.method(resource, event, trigger, payload=payload)
            except Exception as e:
                if not (events.is_cancellable_event(event) or
                        callback.cancellable):
                    LOG.exception("Error during notification for "
                                  "%(callback)s %(resource)s, %(event)s",
                                  {'callback': callback.id,
                                   'resource': resource, 'event': event})
                else:
                    LOG.debug("Callback %(callback)s raised %(error)s",
                              {'callback': callback.id, 'error': e})
                errors.append(exceptions.NotificationError(
                    callback.id, e, cancellable=callback.cancellable))
        return errors

    def _find(self, callback):
        """Return the callback_id if found, None otherwise."""
        callback_id = _get_id(callback)
        return callback_id if callback_id in self._index else None


def _get_id(callback):
    """Return a unique identifier for the callback."""
    # TODO(armax): consider using something other than names
    # https://www.python.org/dev/peps/pep-3155/, but this
    # might be okay for now.
    parts = (reflection.get_callable_name(callback),
             str(hash(callback)))
    return '-'.join(parts)
