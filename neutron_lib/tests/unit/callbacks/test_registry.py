# Copyright 2015 Cisco Systems Inc
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

from oslotest import base
import testtools

from neutron_lib.callbacks import events
from neutron_lib.callbacks import priority_group
from neutron_lib.callbacks import registry
from neutron_lib.callbacks import resources
from neutron_lib import fixture

PRI_CALLBACK = 20


@registry.has_registry_receivers
class ObjectWithDecoratedCallback:

    def __init__(self):
        self.counter = 0

    @registry.receives(resources.PORT, [events.AFTER_CREATE,
                                        events.AFTER_UPDATE])
    @registry.receives(resources.NETWORK, [events.AFTER_DELETE])
    def callback(self, *args, **kwargs):
        self.counter += 1


class MixinWithNew:
    def __new__(cls):
        i = super().__new__(cls)
        i.new_called = True
        return i


@registry.has_registry_receivers
class AnotherObjectWithDecoratedCallback(ObjectWithDecoratedCallback,
                                         MixinWithNew):

    def __init__(self):
        super().__init__()
        self.counter2 = 0

    @registry.receives(resources.NETWORK, [events.AFTER_DELETE], PRI_CALLBACK)
    def callback2(self, *args, **kwargs):
        self.counter2 += 1


@registry.has_registry_receivers
class CallbackClassWithParameters:

    def __init__(self, dummy):
        pass


def my_callback():
    pass


class CallBacksManagerTestCase(base.BaseTestCase):

    def test_decorated_inst_method_receives(self):
        i1 = ObjectWithDecoratedCallback()
        event_payload = events.EventPayload(mock.ANY)
        registry.publish(resources.PORT, events.BEFORE_CREATE, self,
                         payload=event_payload)
        self.assertEqual(0, i1.counter)
        registry.publish(resources.PORT, events.AFTER_CREATE, self,
                         payload=event_payload)
        self.assertEqual(1, i1.counter)
        registry.publish(resources.PORT, events.AFTER_UPDATE, self,
                         payload=event_payload)
        self.assertEqual(2, i1.counter)
        registry.publish(resources.NETWORK, events.AFTER_UPDATE, self,
                         payload=event_payload)
        self.assertEqual(2, i1.counter)
        registry.publish(resources.NETWORK, events.AFTER_DELETE, self,
                         payload=event_payload)
        self.assertEqual(3, i1.counter)
        i2 = ObjectWithDecoratedCallback()
        self.assertEqual(0, i2.counter)
        registry.publish(resources.NETWORK, events.AFTER_DELETE, self,
                         payload=event_payload)
        self.assertEqual(4, i1.counter)
        self.assertEqual(1, i2.counter)

    def test_object_inheriting_others_no_double_subscribe(self):
        with mock.patch.object(registry, 'subscribe') as sub:
            callback = AnotherObjectWithDecoratedCallback()
            # there are 3 methods (2 in parent and one in child) and 1
            # subscribes to 2 events, so we expect 4 subscribes
            priority_call = [mock.call(
                callback.callback2,
                resources.NETWORK, events.AFTER_DELETE, PRI_CALLBACK)]
            self.assertEqual(4, len(sub.mock_calls))
            sub.assert_has_calls(priority_call)

    def test_new_inheritance_not_broken(self):
        self.assertTrue(AnotherObjectWithDecoratedCallback().new_called)

    def test_object_new_not_broken(self):
        CallbackClassWithParameters('dummy')

    def test_no_strings_in_events_arg(self):
        with testtools.ExpectedException(AssertionError):
            registry.receives(resources.PORT, events.AFTER_CREATE)


class TestCallbackRegistryDispatching(base.BaseTestCase):

    def setUp(self):
        super().setUp()
        self.callback_manager = mock.Mock()
        self.registry_fixture = fixture.CallbackRegistryFixture(
            callback_manager=self.callback_manager)
        self.useFixture(self.registry_fixture)

    def test_subscribe(self):
        registry.subscribe(my_callback, 'my-resource', 'my-event')
        self.callback_manager.subscribe.assert_called_with(
            my_callback, 'my-resource', 'my-event',
            priority_group.PRIORITY_DEFAULT, False)

    def test_subscribe_explicit_priority(self):
        registry.subscribe(my_callback, 'my-resource', 'my-event',
                           PRI_CALLBACK)
        self.callback_manager.subscribe.assert_called_with(
            my_callback, 'my-resource', 'my-event', PRI_CALLBACK, False)

    def test_unsubscribe(self):
        registry.unsubscribe(my_callback, 'my-resource', 'my-event')
        self.callback_manager.unsubscribe.assert_called_with(
            my_callback, 'my-resource', 'my-event')

    def test_unsubscribe_by_resource(self):
        registry.unsubscribe_by_resource(my_callback, 'my-resource')
        self.callback_manager.unsubscribe_by_resource.assert_called_with(
            my_callback, 'my-resource')

    def test_unsubscribe_all(self):
        registry.unsubscribe_all(my_callback)
        self.callback_manager.unsubscribe_all.assert_called_with(
            my_callback)

    def test_clear(self):
        registry.clear()
        self.callback_manager.clear.assert_called_with()

    def test_publish_payload(self):
        event_payload = events.EventPayload(mock.ANY)
        registry.publish('x', 'y', self, payload=event_payload)
        self.callback_manager.publish.assert_called_with(
            'x', 'y', self, payload=event_payload)
