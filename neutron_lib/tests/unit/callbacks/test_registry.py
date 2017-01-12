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

import mock

from oslotest import base

from neutron_lib.callbacks import events
from neutron_lib.callbacks import registry
from neutron_lib import fixture


def my_callback():
    pass


class TestCallbackRegistryDispatching(base.BaseTestCase):

    def setUp(self):
        super(TestCallbackRegistryDispatching, self).setUp()
        self.callback_manager = mock.Mock()
        self.registry_fixture = fixture.CallbackRegistryFixture(
            callback_manager=self.callback_manager)
        self.useFixture(self.registry_fixture)

    def test_subscribe(self):
        registry.subscribe(my_callback, 'my-resource', 'my-event')
        self.callback_manager.subscribe.assert_called_with(
            my_callback, 'my-resource', 'my-event')

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

    def test_notify(self):
        registry.notify('my-resource', 'my-event', mock.ANY)
        self.callback_manager.notify.assert_called_with(
            'my-resource', 'my-event', mock.ANY)

    def test_clear(self):
        registry.clear()
        self.callback_manager.clear.assert_called_with()

    def test_publish_payload(self):
        event_payload = events.EventPayload(mock.ANY)
        registry.publish('x', 'y', self, payload=event_payload)
        self.callback_manager.publish.assert_called_with(
            'x', 'y', self, payload=event_payload)
