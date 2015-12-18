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

from neutron_lib._callbacks import registry


def my_callback():
    pass


class TestCallbackRegistryDispatching(base.BaseTestCase):

    def setUp(self):
        super(TestCallbackRegistryDispatching, self).setUp()
        registry.CALLBACK_MANAGER = mock.Mock()

    def test_subscribe(self):
        registry.subscribe(my_callback, 'my-resource', 'my-event')
        registry.CALLBACK_MANAGER.subscribe.assert_called_with(
            my_callback, 'my-resource', 'my-event')

    def test_unsubscribe(self):
        registry.unsubscribe(my_callback, 'my-resource', 'my-event')
        registry.CALLBACK_MANAGER.unsubscribe.assert_called_with(
            my_callback, 'my-resource', 'my-event')

    def test_unsubscribe_by_resource(self):
        registry.unsubscribe_by_resource(my_callback, 'my-resource')
        registry.CALLBACK_MANAGER.unsubscribe_by_resource.assert_called_with(
            my_callback, 'my-resource')

    def test_unsubscribe_all(self):
        registry.unsubscribe_all(my_callback)
        registry.CALLBACK_MANAGER.unsubscribe_all.assert_called_with(
            my_callback)

    def test_notify(self):
        registry.notify('my-resource', 'my-event', mock.ANY)
        registry.CALLBACK_MANAGER.notify.assert_called_with(
            'my-resource', 'my-event', mock.ANY)

    def test_clear(self):
        registry.clear()
        registry.CALLBACK_MANAGER.clear.assert_called_with()
