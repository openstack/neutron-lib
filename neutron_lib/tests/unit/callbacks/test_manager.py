# Copyright 2015 OpenStack Foundation
#
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

from unittest import mock

from oslo_db import exception as db_exc
from oslotest import base

from neutron_lib.callbacks import events
from neutron_lib.callbacks import exceptions
from neutron_lib.callbacks import manager
from neutron_lib.callbacks import priority_group
from neutron_lib.callbacks import resources


PRI_HIGH = 0
PRI_MED = 5000
PRI_LOW = 10000


class ObjectWithCallback:

    def __init__(self):
        self.counter = 0

    def callback(self, *args, **kwargs):
        self.counter += 1


class GloriousObjectWithCallback(ObjectWithCallback):
    pass


def callback_1(*args, **kwargs):
    callback_1.counter += 1


callback_id_1 = manager._get_id(callback_1)


def callback_2(*args, **kwargs):
    callback_2.counter += 1


callback_id_2 = manager._get_id(callback_2)


def callback_raise(*args, **kwargs):
    raise Exception()


def callback_raise_retriable(*args, **kwargs):
    raise db_exc.DBDeadlock()


def callback_raise_not_retriable(*args, **kwargs):
    raise Exception()


def callback_3(resource, event, trigger, payload):
    callback_3.counter += 1


class CallBacksManagerTestCase(base.BaseTestCase):

    def setUp(self):
        super().setUp()
        self.manager = manager.CallbacksManager()
        self.event_payload = events.EventPayload(object())
        callback_1.counter = 0
        callback_2.counter = 0
        callback_3.counter = 0

    def test_subscribe_cancellable(self):
        self._test_subscribe(True)

    def test_subscribe_uncancellable(self):
        self._test_subscribe(False)

    def _test_subscribe(self, cancellable):
        self.manager.subscribe(
            callback_1, resources.PORT, events.BEFORE_CREATE,
            cancellable=cancellable)
        self.assertIsNotNone(
            self.manager._callbacks[resources.PORT][events.BEFORE_CREATE])
        self.assertIn(callback_id_1, self.manager._index)
        self.assertEqual(self.__module__ + '.callback_1-%s' %
                         hash(callback_1), callback_id_1)
        self.assertEqual(cancellable,
                         self.manager._callbacks[resources.PORT]
                         [events.BEFORE_CREATE][0][2])

    def test_subscribe_unknown(self):
        self.manager.subscribe(
            callback_1, 'my_resource', 'my-event')
        self.assertIsNotNone(
            self.manager._callbacks['my_resource']['my-event'])
        self.assertIn(callback_id_1, self.manager._index)

    def test_subscribe_is_idempotent(self):
        for cancellable in (True, False):
            self.manager.subscribe(
                callback_1, resources.PORT, events.BEFORE_CREATE,
                cancellable=cancellable)
            self.manager.subscribe(
                callback_1, resources.PORT, events.BEFORE_CREATE,
                cancellable=cancellable)
        self.assertEqual(
            1,
            len(self.manager._callbacks[resources.PORT][events.BEFORE_CREATE]))
        # The first event registered had cancellable=True.
        self.assertTrue(self.manager._callbacks[resources.PORT]
                        [events.BEFORE_CREATE][0][2])
        callbacks = self.manager._index[callback_id_1][resources.PORT]
        self.assertEqual(1, len(callbacks))

    def test_subscribe_multiple_callbacks(self):
        self.manager.subscribe(
            callback_1, resources.PORT, events.BEFORE_CREATE)
        self.manager.subscribe(
            callback_2, resources.PORT, events.BEFORE_CREATE)
        self.assertEqual(2, len(self.manager._index))
        self.assertEqual(
            1,
            len(self.manager._callbacks[resources.PORT][events.BEFORE_CREATE]))
        self.assertEqual(
            2,
            len(self.manager._callbacks
                [resources.PORT][events.BEFORE_CREATE][0][1]))

    def test_unsubscribe_during_iteration(self):
        def unsub(r, e, *a, **k):
            return self.manager.unsubscribe(unsub, r, e)

        self.manager.subscribe(unsub, resources.PORT,
                               events.BEFORE_CREATE)
        self.manager.publish(resources.PORT, events.BEFORE_CREATE, mock.ANY,
                             payload=self.event_payload)
        self.assertNotIn(unsub, self.manager._index)

    def test_unsubscribe_cancellable(self):
        self._test_unsubscribe(True)

    def test_unsubscribe_uncancellable(self):
        self._test_unsubscribe(False)

    def _test_unsubscribe(self, cancellable):
        self.manager.subscribe(
            callback_1, resources.PORT, events.BEFORE_CREATE,
            cancellable=cancellable)
        self.manager.unsubscribe(
            callback_1, resources.PORT, events.BEFORE_CREATE)
        self.assertNotIn(
            callback_id_1,
            self.manager._callbacks[resources.PORT][events.BEFORE_CREATE])
        self.assertNotIn(callback_id_1, self.manager._index)

    def test_unsubscribe_unknown_callback(self):
        self.manager.subscribe(
            callback_2, resources.PORT, events.BEFORE_CREATE)
        self.manager.unsubscribe(callback_1, mock.ANY, mock.ANY)
        self.assertEqual(1, len(self.manager._index))

    def test_fail_to_unsubscribe(self):
        self.manager.subscribe(
            callback_1, resources.PORT, events.BEFORE_CREATE)
        self.assertRaises(exceptions.Invalid,
                          self.manager.unsubscribe,
                          callback_1, resources.PORT, None)
        self.assertRaises(exceptions.Invalid,
                          self.manager.unsubscribe,
                          callback_1, None, events.BEFORE_CREATE)

    def test_unsubscribe_is_idempotent_cancellable(self):
        self._test_unsubscribe_is_idempotent(True)

    def test_unsubscribe_is_idempotent_uncancellable(self):
        self._test_unsubscribe_is_idempotent(False)

    def _test_unsubscribe_is_idempotent(self, cancellable):
        self.manager.subscribe(
            callback_1, resources.PORT, events.BEFORE_CREATE,
            cancellable=cancellable)
        self.manager.unsubscribe(
            callback_1, resources.PORT, events.BEFORE_CREATE)
        self.manager.unsubscribe(
            callback_1, resources.PORT, events.BEFORE_CREATE)
        self.assertNotIn(callback_id_1, self.manager._index)
        self.assertNotIn(callback_id_1,
                         self.manager._callbacks[resources.PORT]
                                                [events.BEFORE_CREATE])

    def test_unsubscribe_by_resource(self):
        self.manager.subscribe(
            callback_1, resources.PORT, events.BEFORE_CREATE)
        self.manager.subscribe(
            callback_1, resources.PORT, events.BEFORE_DELETE)
        self.manager.subscribe(
            callback_2, resources.PORT, events.BEFORE_DELETE)
        self.manager.unsubscribe_by_resource(callback_1, resources.PORT)
        self.assertEqual(
            0,
            len(self.manager._callbacks
                [resources.PORT][events.BEFORE_CREATE]))
        self.assertEqual(
            1,
            len(self.manager._callbacks[resources.PORT][events.BEFORE_DELETE]))
        self.assertIn(
            callback_id_2,
            self.manager._callbacks
            [resources.PORT][events.BEFORE_DELETE][0][1])
        self.assertNotIn(callback_id_1, self.manager._index)

    def test_unsubscribe_all(self):
        self.manager.subscribe(
            callback_1, resources.PORT, events.BEFORE_CREATE)
        self.manager.subscribe(
            callback_1, resources.PORT, events.BEFORE_DELETE)
        self.manager.subscribe(
            callback_1, resources.ROUTER, events.BEFORE_CREATE)
        self.manager.unsubscribe_all(callback_1)
        self.assertNotIn(
            callback_id_1,
            self.manager._callbacks[resources.PORT][events.BEFORE_CREATE])
        self.assertNotIn(callback_id_1, self.manager._index)

    def test_publish_none(self):
        self.manager.publish(resources.PORT, events.BEFORE_CREATE, mock.ANY,
                             payload=self.event_payload)
        self.assertEqual(0, callback_1.counter)
        self.assertEqual(0, callback_2.counter)

    def test_feebly_referenced_callback(self):
        self.manager.subscribe(lambda *x, **y: None, resources.PORT,
                               events.BEFORE_CREATE)
        self.manager.publish(resources.PORT, events.BEFORE_CREATE, mock.ANY,
                             payload=self.event_payload)

    def test_publish_with_exception(self):
        with mock.patch.object(self.manager, '_notify_loop') as n:
            n.return_value = ['error']
            self.assertRaises(exceptions.CallbackFailure,
                              self.manager.publish,
                              mock.ANY, events.BEFORE_CREATE, mock.ANY,
                              payload=self.event_payload)
            expected_calls = [
                mock.call(mock.ANY, 'before_create', mock.ANY,
                          self.event_payload),
                mock.call(mock.ANY, 'abort_create', mock.ANY,
                          self.event_payload)
            ]
            n.assert_has_calls(expected_calls)

    def test_publish_with_precommit_exception(self):
        with mock.patch.object(self.manager, '_notify_loop') as n:
            n.return_value = ['error']
            self.assertRaises(exceptions.CallbackFailure,
                              self.manager.publish,
                              mock.ANY, events.PRECOMMIT_UPDATE, mock.ANY,
                              payload=self.event_payload)
            expected_calls = [
                mock.call(mock.ANY, 'precommit_update', mock.ANY,
                          self.event_payload),
            ]
            n.assert_has_calls(expected_calls)

    def test_publish_handle_exception(self):
        self.manager.subscribe(
            callback_raise, resources.PORT, events.BEFORE_CREATE)
        e = self.assertRaises(exceptions.CallbackFailure, self.manager.publish,
                              resources.PORT, events.BEFORE_CREATE, self,
                              payload=self.event_payload)
        self.assertIsInstance(e.errors[0], exceptions.NotificationError)

    def test_publish_handle_retriable_exception(self):
        self.manager.subscribe(
            callback_raise_retriable, resources.PORT, events.BEFORE_CREATE)
        self.assertRaises(db_exc.RetryRequest, self.manager.publish,
                          resources.PORT, events.BEFORE_CREATE, self,
                          payload=self.event_payload)

    def test_publish_handle_not_retriable_exception(self):
        self.manager.subscribe(
            callback_raise_not_retriable, resources.PORT, events.BEFORE_CREATE)
        self.assertRaises(exceptions.CallbackFailure, self.manager.publish,
                          resources.PORT, events.BEFORE_CREATE, self,
                          payload=self.event_payload)

    def test_publish_handle_not_retriable_exception_no_cancellable_flag(self):
        self.manager.subscribe(
            callback_raise_not_retriable, resources.PORT, events.AFTER_INIT)
        # No exception is raised.
        self.manager.publish(resources.PORT, events.AFTER_INIT, self,
                             payload=self.event_payload)

    def test_publish_handle_not_retriable_exception_cancellable_flag(self):
        self.manager.subscribe(
            callback_raise_not_retriable, resources.PORT, events.AFTER_INIT,
            cancellable=True)
        self.assertRaises(exceptions.CallbackFailure, self.manager.publish,
                          resources.PORT, events.AFTER_INIT, self,
                          payload=self.event_payload)

    def test_publish_called_once_with_no_failures(self):
        with mock.patch.object(self.manager, '_notify_loop') as n:
            n.return_value = False
            self.manager.publish(resources.PORT, events.BEFORE_CREATE,
                                 mock.ANY,
                                 payload=self.event_payload)
            n.assert_called_once_with(
                resources.PORT, events.BEFORE_CREATE, mock.ANY,
                self.event_payload)

    def test__notify_loop_single_event(self):
        self.manager.subscribe(
            callback_1, resources.PORT, events.BEFORE_CREATE)
        self.manager.subscribe(
            callback_2, resources.PORT, events.BEFORE_CREATE)
        self.manager._notify_loop(
            resources.PORT, events.BEFORE_CREATE, mock.ANY,
            payload=mock.ANY)
        self.assertEqual(1, callback_1.counter)
        self.assertEqual(1, callback_2.counter)

    def test__notify_loop_multiple_events(self):
        self.manager.subscribe(
            callback_1, resources.PORT, events.BEFORE_CREATE)
        self.manager.subscribe(
            callback_1, resources.ROUTER, events.BEFORE_DELETE)
        self.manager.subscribe(
            callback_2, resources.PORT, events.BEFORE_CREATE)
        self.manager._notify_loop(
            resources.PORT, events.BEFORE_CREATE, mock.ANY,
            payload=mock.ANY)
        self.manager._notify_loop(
            resources.ROUTER, events.BEFORE_DELETE, mock.ANY,
            payload=mock.ANY)
        self.assertEqual(2, callback_1.counter)
        self.assertEqual(1, callback_2.counter)

    def test_clearing_subscribers(self):
        self.manager.subscribe(
            callback_1, resources.PORT, events.BEFORE_CREATE)
        self.manager.subscribe(
            callback_2, resources.PORT, events.AFTER_CREATE)
        self.assertEqual(2, len(self.manager._callbacks[resources.PORT]))
        self.assertEqual(2, len(self.manager._index))
        self.manager.clear()
        self.assertEqual(0, len(self.manager._callbacks))
        self.assertEqual(0, len(self.manager._index))

    def test_callback_priority(self):
        pri_first = priority_group.PRIORITY_DEFAULT - 100
        pri_last = priority_group.PRIORITY_DEFAULT + 100
        # lowest priority value should be first in the _callbacks
        self.manager.subscribe(callback_1, 'my-resource', 'my-event')
        self.manager.subscribe(callback_2, 'my-resource',
                               'my-event', pri_last)
        self.manager.subscribe(callback_3, 'my-resource',
                               'my-event', pri_first)
        callbacks = self.manager._callbacks['my-resource']['my-event']
        # callbacks should be sorted based on priority for resource and event
        self.assertEqual(3, len(callbacks))
        self.assertEqual(pri_first, callbacks[0][0])
        self.assertEqual(priority_group.PRIORITY_DEFAULT, callbacks[1][0])
        self.assertEqual(pri_last, callbacks[2][0])

    @mock.patch('neutron_lib.callbacks.manager.CallbacksManager._del_callback')
    def test_del_callback_called_on_unsubscribe(self, mock_cb):
        self.manager.subscribe(callback_1, 'my-resource', 'my-event')
        callback_id = self.manager._find(callback_1)
        callbacks = self.manager._callbacks['my-resource']['my-event']
        self.assertEqual(1, len(callbacks))
        self.manager.unsubscribe(callback_1, 'my-resource', 'my-event')
        mock_cb.assert_called_once_with(callbacks, callback_id)

    @mock.patch("neutron_lib.callbacks.manager.LOG")
    def test_callback_order(self, _logger):
        self.manager.subscribe(callback_1, 'my-resource', 'my-event', PRI_MED)
        self.manager.subscribe(callback_2, 'my-resource', 'my-event', PRI_HIGH)
        self.manager.subscribe(callback_3, 'my-resource', 'my-event', PRI_LOW)
        self.assertEqual(
            3, len(self.manager._callbacks['my-resource']['my-event']))
        self.manager.unsubscribe(callback_3, 'my-resource', 'my-event')
        self.manager.publish('my-resource', 'my-event', mock.ANY,
                             payload=self.event_payload)
        # callback_3 should be deleted and not executed
        self.assertEqual(
            2, len(self.manager._callbacks['my-resource']['my-event']))
        self.assertEqual(0, callback_3.counter)
        # executed callbacks should have counter incremented
        self.assertEqual(1, callback_2.counter)
        self.assertEqual(1, callback_1.counter)
        callback_ids = _logger.debug.mock_calls[4][1][1]
        # callback_2 should be first in exceution as it has higher priority
        self.assertEqual(callback_id_2, callback_ids[0])
        self.assertEqual(callback_id_1, callback_ids[1])

    @mock.patch("neutron_lib.callbacks.manager.LOG")
    def test__notify_loop_skip_log_errors(self, _logger):
        self.manager.subscribe(
            callback_raise, resources.PORT, events.BEFORE_CREATE)
        self.manager.subscribe(
            callback_raise, resources.PORT, events.PRECOMMIT_CREATE)
        self.manager._notify_loop(
            resources.PORT, events.BEFORE_CREATE, mock.ANY, payload=mock.ANY)
        self.manager._notify_loop(
            resources.PORT, events.PRECOMMIT_CREATE, mock.ANY,
            payload=mock.ANY)
        self.assertFalse(_logger.exception.call_count)
        self.assertTrue(_logger.debug.call_count)

    def test_object_instances_as_subscribers(self):
        """Ensures that the manager doesn't think these are equivalent."""
        a = GloriousObjectWithCallback()
        b = ObjectWithCallback()
        c = ObjectWithCallback()
        for o in (a, b, c):
            self.manager.subscribe(
                o.callback, resources.PORT, events.BEFORE_CREATE)
            # ensure idempotency remains for a single object
            self.manager.subscribe(
                o.callback, resources.PORT, events.BEFORE_CREATE)
        self.manager.publish(resources.PORT, events.BEFORE_CREATE, mock.ANY,
                             payload=events.EventPayload(object()))
        self.assertEqual(1, a.counter)
        self.assertEqual(1, b.counter)
        self.assertEqual(1, c.counter)

    def test_publish_invalid_payload(self):
        self.assertRaises(exceptions.Invalid, self.manager.publish,
                          resources.PORT, events.AFTER_DELETE, self,
                          payload=object())

    def test_publish_empty_payload(self):
        notify_payload = []

        def _memo(resource, event, trigger, payload=None):
            notify_payload.append(payload)

        self.manager.subscribe(_memo, 'x', 'y')
        self.manager.publish('x', 'y', self)
        self.assertIsNone(notify_payload[0])

    def test_publish_payload(self):
        notify_payload = []

        def _memo(resource, event, trigger, payload=None):
            notify_payload.append(payload)

        self.manager.subscribe(_memo, 'x', 'y')
        self.manager.publish('x', 'y', self, payload=self.event_payload)
        self.assertEqual(self.event_payload, notify_payload[0])
