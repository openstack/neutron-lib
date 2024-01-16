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

from neutron_lib.callbacks import events
from oslotest import base


class EventPayloadTestCase(base.BaseTestCase):

    def test_context(self):
        e = events.EventPayload(mock.ANY)
        self.assertEqual(mock.ANY, e.context)

    def test_metadata(self):
        meta = {'k1': 'v1', 'k2': mock.ANY}
        e = events.EventPayload(mock.ANY, metadata=meta)
        self.assertEqual(meta, e.metadata)
        event_meta = e.metadata
        event_meta['k3'] = 'v3'
        self.assertIn('k3', e.metadata)

    def test_request_body(self):
        e = events.EventPayload(mock.ANY, request_body={'k', 'v'})
        self.assertEqual({'k', 'v'}, e.request_body)

    def test_states(self):
        e = events.EventPayload(mock.ANY, states=['s1', 's2'])
        self.assertEqual(['s1', 's2'], e.states)
        e.states.append('state')
        self.assertIn('state', e.states)

    def test_resource_id(self):
        e = events.EventPayload(mock.ANY, resource_id='id1')
        self.assertEqual('id1', e.resource_id)

    def test_has_no_states(self):
        e = events.EventPayload(mock.ANY)
        self.assertFalse(e.has_states)

    def test_has_states(self):
        e = events.EventPayload(mock.ANY, states=['s1'])
        self.assertTrue(e.has_states)

    def test_latest_state_with_states(self):
        body = object()
        states = [object(), object()]
        e = events.EventPayload(mock.ANY, request_body=body, states=states)
        self.assertEqual(states[-1], e.latest_state)

    def test_latest_state_without_states(self):
        body = object()
        e = events.EventPayload(mock.ANY, request_body=body)
        self.assertIsNone(e.latest_state)


class DataStoreEventPayloadTestCase(base.BaseTestCase):

    def test_states(self):
        e = events.DBEventPayload(mock.ANY, states=['s1'])
        self.assertEqual(['s1'], e.states)

    def test_desired_state(self):
        desired_state = {'k': object()}
        e = events.DBEventPayload(mock.ANY, desired_state=desired_state)
        self.assertEqual(desired_state, e.desired_state)
        desired_state['a'] = 'A'
        self.assertEqual(desired_state, e.desired_state)

    def test_is_not_persisted(self):
        e = events.DBEventPayload(mock.ANY, states=['s1'])
        self.assertFalse(e.is_persisted)
        e = events.DBEventPayload(mock.ANY, resource_id='1a')
        self.assertFalse(e.is_persisted)

    def test_is_persisted(self):
        e = events.DBEventPayload(mock.ANY, states=['s1'],
                                  resource_id='1a')
        self.assertTrue(e.is_persisted)

    def test_is_not_to_be_committed(self):
        e = events.DBEventPayload(mock.ANY, states=['s1'],
                                  resource_id='1a')
        self.assertFalse(e.is_to_be_committed)

    def test_is_to_be_committed(self):
        e = events.DBEventPayload(mock.ANY, states=[mock.ANY],
                                  resource_id='1a', desired_state=object())
        self.assertTrue(e.is_to_be_committed)

    def test_latest_state_with_desired_state(self):
        desired_state = object()
        e = events.DBEventPayload(mock.ANY, states=[object()],
                                  desired_state=desired_state)
        self.assertEqual(desired_state, e.latest_state)


class APIEventPayloadTestCase(base.BaseTestCase):

    def test_action(self):
        e = events.APIEventPayload(mock.ANY, 'post.end', 'POST')
        self.assertEqual('POST', e.action)

    def test_method_name(self):
        e = events.APIEventPayload(mock.ANY, 'post.end', 'POST')
        self.assertEqual('post.end', e.method_name)
