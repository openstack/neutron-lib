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

from unittest import mock

from oslo_config import cfg
import oslo_messaging as messaging
from oslo_messaging import conffixture as messaging_conffixture
from oslo_messaging import exceptions as oslomsg_exc
import testtools

from neutron_lib import fixture
from neutron_lib import rpc
from neutron_lib.tests import _base as base


CONF = cfg.CONF


class TestRPC(base.BaseTestCase):
    def setUp(self):
        super().setUp()
        self.useFixture(fixture.RPCFixture())

    @mock.patch.object(rpc, 'RequestContextSerializer')
    @mock.patch.object(messaging, 'get_rpc_transport')
    @mock.patch.object(messaging, 'get_notification_transport')
    def test_init(self, mock_noti_trans, mock_trans, mock_ser):
        transport = mock.Mock()
        noti_transport = mock.Mock()
        conf = mock.Mock()

        mock_trans.return_value = transport
        mock_noti_trans.return_value = noti_transport

        rpc.init(conf, rpc_ext_mods=['foo'])

        expected_mods = list(set(['foo'] + rpc._DFT_EXMODS))
        mock_trans.assert_called_once_with(
            conf, allowed_remote_exmods=expected_mods)
        mock_noti_trans.assert_called_once_with(
            conf, allowed_remote_exmods=expected_mods)
        self.assertIsNotNone(rpc.TRANSPORT)
        self.assertIsNotNone(rpc.NOTIFICATION_TRANSPORT)

    def test_cleanup_transport_null(self):
        rpc.NOTIFICATION_TRANSPORT = mock.Mock()
        rpc.TRANSPORT = None
        self.assertRaises(AssertionError, rpc.cleanup)
        rpc.TRANSPORT = mock.Mock()

    def test_cleanup_notification_transport_null(self):
        rpc.TRANSPORT = mock.Mock()
        rpc.NOTIFICATION_TRANSPORT = None
        self.assertRaises(AssertionError, rpc.cleanup)
        rpc.NOTIFICATION_TRANSPORT = mock.Mock()

    def test_cleanup(self):
        rpc.NOTIFICATION_TRANSPORT = mock.Mock()
        rpc.TRANSPORT = mock.Mock()
        trans_cleanup = mock.Mock()
        not_trans_cleanup = mock.Mock()
        rpc.TRANSPORT.cleanup = trans_cleanup
        rpc.NOTIFICATION_TRANSPORT.cleanup = not_trans_cleanup

        rpc.cleanup()

        trans_cleanup.assert_called_once_with()
        not_trans_cleanup.assert_called_once_with()
        self.assertIsNone(rpc.TRANSPORT)
        self.assertIsNone(rpc.NOTIFICATION_TRANSPORT)

        rpc.TRANSPORT = mock.Mock()
        rpc.NOTIFICATION_TRANSPORT = mock.Mock()

    @mock.patch.object(rpc, 'RequestContextSerializer')
    @mock.patch.object(messaging, 'get_rpc_client')
    def test_get_client(self, mock_get, mock_ser):
        rpc.TRANSPORT = mock.Mock()
        tgt = mock.Mock()
        ser = mock.Mock()
        mock_get.return_value = 'client'
        mock_ser.return_value = ser

        client = rpc.get_client(tgt, version_cap='1.0', serializer='foo')

        mock_ser.assert_called_once_with('foo')
        mock_get.assert_called_once_with(rpc.TRANSPORT,
                                         tgt, version_cap='1.0',
                                         serializer=ser,
                                         client_cls=rpc.BackingOffClient)
        self.assertEqual('client', client)

    @mock.patch.object(rpc, 'RequestContextSerializer')
    @mock.patch.object(messaging, 'get_rpc_server')
    def test_get_server(self, mock_get, mock_ser):
        ser = mock.Mock()
        tgt = mock.Mock()
        ends = mock.Mock()
        mock_ser.return_value = ser
        mock_get.return_value = 'server'

        server = rpc.get_server(tgt, ends, serializer='foo')

        mock_ser.assert_called_once_with('foo')
        mock_get.assert_called_once_with(rpc.TRANSPORT, tgt, ends,
                                         serializer=ser)
        self.assertEqual('server', server)

    def test_get_notifier(self):
        mock_notifier = mock.Mock(return_value=None)
        messaging.Notifier.__init__ = mock_notifier
        rpc.get_notifier('service', publisher_id='foo')
        mock_notifier.assert_called_once_with(
            mock.ANY, serializer=mock.ANY, publisher_id='foo')

    def test_get_notifier_null_publisher(self):
        mock_notifier = mock.Mock(return_value=None)
        messaging.Notifier.__init__ = mock_notifier
        rpc.get_notifier('service', host='bar')
        mock_notifier.assert_called_once_with(
            mock.ANY, serializer=mock.ANY, publisher_id='service.bar')


class TestRequestContextSerializer(base.BaseTestCase):
    def setUp(self):
        super().setUp()
        self.mock_base = mock.Mock()
        self.ser = rpc.RequestContextSerializer(self.mock_base)
        self.ser_null = rpc.RequestContextSerializer(None)

    def test_serialize_entity(self):
        self.mock_base.serialize_entity.return_value = 'foo'

        ser_ent = self.ser.serialize_entity('context', 'entity')

        self.mock_base.serialize_entity.assert_called_once_with('context',
                                                                'entity')
        self.assertEqual('foo', ser_ent)

    def test_deserialize_entity(self):
        self.mock_base.deserialize_entity.return_value = 'foo'

        deser_ent = self.ser.deserialize_entity('context', 'entity')

        self.mock_base.deserialize_entity.assert_called_once_with('context',
                                                                  'entity')
        self.assertEqual('foo', deser_ent)

    def test_deserialize_entity_null_base(self):
        deser_ent = self.ser_null.deserialize_entity('context', 'entity')

        self.assertEqual('entity', deser_ent)

    def test_serialize_context(self):
        context = mock.Mock()

        self.ser.serialize_context(context)

        context.to_dict.assert_called_once_with()

    def test_deserialize_context(self):
        context_dict = {'foo': 'bar',
                        'user_id': 1,
                        'tenant_id': 1,
                        'is_admin': True}

        c = self.ser.deserialize_context(context_dict)

        self.assertEqual(1, c.user_id)
        self.assertEqual(1, c.project_id)

    def test_deserialize_context_no_user_id(self):
        context_dict = {'foo': 'bar',
                        'user': 1,
                        'tenant_id': 1,
                        'is_admin': True}

        c = self.ser.deserialize_context(context_dict)

        self.assertEqual(1, c.user_id)
        self.assertEqual(1, c.project_id)

    def test_deserialize_context_no_tenant_id(self):
        context_dict = {'foo': 'bar',
                        'user_id': 1,
                        'project_id': 1,
                        'is_admin': True}

        c = self.ser.deserialize_context(context_dict)

        self.assertEqual(1, c.user_id)
        self.assertEqual(1, c.project_id)

    def test_deserialize_context_no_ids(self):
        context_dict = {'foo': 'bar', 'is_admin': True}

        c = self.ser.deserialize_context(context_dict)

        self.assertIsNone(c.user_id)
        self.assertIsNone(c.project_id)


class ServiceTestCase(base.BaseTestCase):
    # the class cannot be based on BaseTestCase since it mocks rpc.Connection

    def setUp(self):
        super().setUp()
        self.host = 'foo'
        self.topic = 'neutron-agent'

        self.target_mock = mock.patch('oslo_messaging.Target')
        self.target_mock.start()

        self.messaging_conf = messaging_conffixture.ConfFixture(CONF)
        self.messaging_conf.transport_url = 'fake://'
        self.messaging_conf.response_timeout = 0
        self.useFixture(self.messaging_conf)

        self.addCleanup(rpc.cleanup)
        rpc.init(CONF)

    @mock.patch.object(cfg, 'CONF')
    def test_operations(self, mock_conf):
        mock_conf.host = self.host
        with mock.patch('oslo_messaging.get_rpc_server') as get_rpc_server:
            rpc_server = get_rpc_server.return_value

            service = rpc.Service(self.host, self.topic)
            service.start()
            rpc_server.start.assert_called_once_with()

            service.stop()
            rpc_server.stop.assert_called_once_with()
            rpc_server.wait.assert_called_once_with()


class TimeoutTestCase(base.BaseTestCase):
    def setUp(self):
        super().setUp()

        self.messaging_conf = messaging_conffixture.ConfFixture(CONF)
        self.messaging_conf.transport_url = 'fake://'
        self.messaging_conf.response_timeout = 0
        self.useFixture(self.messaging_conf)

        self.addCleanup(rpc.cleanup)
        rpc.init(CONF)
        rpc.TRANSPORT = mock.MagicMock()
        rpc.TRANSPORT._send.side_effect = messaging.MessagingTimeout
        rpc.TRANSPORT.conf.oslo_messaging_metrics.metrics_enabled = False
        target = messaging.Target(version='1.0', topic='testing')
        self.client = rpc.get_client(target)
        self.call_context = mock.Mock()
        self.sleep = mock.patch('time.sleep').start()
        rpc.TRANSPORT.conf.rpc_response_timeout = 10
        rpc.TRANSPORT.conf.rpc_response_max_timeout = 300

    def test_timeout_unaffected_when_explicitly_set(self):
        rpc.TRANSPORT.conf.rpc_response_timeout = 5
        ctx = self.client.prepare(topic='sandwiches', timeout=77)
        with testtools.ExpectedException(messaging.MessagingTimeout):
            ctx.call(self.call_context, 'create_pb_and_j')
        # ensure that the timeout was not increased and the back-off sleep
        # wasn't called
        self.assertEqual(
            5,
            rpc._BackingOffContextWrapper._METHOD_TIMEOUTS['create_pb_and_j'])
        self.assertFalse(self.sleep.called)

    def test_timeout_store_defaults(self):
        # any method should default to the configured timeout
        self.assertEqual(
            rpc.TRANSPORT.conf.rpc_response_timeout,
            rpc._BackingOffContextWrapper._METHOD_TIMEOUTS['method_1'])
        self.assertEqual(
            rpc.TRANSPORT.conf.rpc_response_timeout,
            rpc._BackingOffContextWrapper._METHOD_TIMEOUTS['method_2'])
        # a change to an existing should not affect new or existing ones
        rpc._BackingOffContextWrapper._METHOD_TIMEOUTS['method_2'] = 7000
        self.assertEqual(
            rpc.TRANSPORT.conf.rpc_response_timeout,
            rpc._BackingOffContextWrapper._METHOD_TIMEOUTS['method_1'])
        self.assertEqual(
            rpc.TRANSPORT.conf.rpc_response_timeout,
            rpc._BackingOffContextWrapper._METHOD_TIMEOUTS['method_3'])

    def test_method_timeout_sleep(self):
        rpc.TRANSPORT.conf.rpc_response_timeout = 2
        for i in range(100):
            with testtools.ExpectedException(messaging.MessagingTimeout):
                self.client.call(self.call_context, 'method_1')
            # sleep value should always be between 0 and configured timeout
            self.assertGreaterEqual(self.sleep.call_args_list[0][0][0], 0)
            self.assertLessEqual(self.sleep.call_args_list[0][0][0], 2)
            self.sleep.reset_mock()

    def test_method_timeout_increases_on_timeout_exception(self):
        rpc._BackingOffContextWrapper._METHOD_TIMEOUTS['method_1'] = 1
        for i in range(5):
            with testtools.ExpectedException(messaging.MessagingTimeout):
                self.client.call(self.call_context, 'method_1')

        # we only care to check the timeouts sent to the transport
        timeouts = [call[1]['timeout']
                    for call in rpc.TRANSPORT._send.call_args_list]
        self.assertEqual([1, 2, 4, 8, 16], timeouts)

    def test_method_timeout_config_ceiling(self):
        rpc.TRANSPORT.conf.rpc_response_timeout = 10
        # 5 doublings should max out at the 10xdefault ceiling
        for i in range(5):
            with testtools.ExpectedException(messaging.MessagingTimeout):
                self.client.call(self.call_context, 'method_1')
        self.assertEqual(
            rpc.TRANSPORT.conf.rpc_response_max_timeout,
            rpc._BackingOffContextWrapper._METHOD_TIMEOUTS['method_1'])
        with testtools.ExpectedException(messaging.MessagingTimeout):
            self.client.call(self.call_context, 'method_1')
        self.assertEqual(
            rpc.TRANSPORT.conf.rpc_response_max_timeout,
            rpc._BackingOffContextWrapper._METHOD_TIMEOUTS['method_1'])

    def test_timeout_unchanged_on_other_exception(self):
        rpc._BackingOffContextWrapper._METHOD_TIMEOUTS['method_1'] = 1
        rpc.TRANSPORT._send.side_effect = ValueError
        with testtools.ExpectedException(ValueError):
            self.client.call(self.call_context, 'method_1')
        rpc.TRANSPORT._send.side_effect = messaging.MessagingTimeout
        with testtools.ExpectedException(messaging.MessagingTimeout):
            self.client.call(self.call_context, 'method_1')
        timeouts = [call[1]['timeout']
                    for call in rpc.TRANSPORT._send.call_args_list]
        self.assertEqual([1, 1], timeouts)

    def test_timeouts_for_methods_tracked_independently(self):
        rpc._BackingOffContextWrapper._METHOD_TIMEOUTS['method_1'] = 1
        rpc._BackingOffContextWrapper._METHOD_TIMEOUTS['method_2'] = 1
        for method in ('method_1', 'method_1', 'method_2',
                       'method_1', 'method_2'):
            with testtools.ExpectedException(messaging.MessagingTimeout):
                self.client.call(self.call_context, method)
        timeouts = [call[1]['timeout']
                    for call in rpc.TRANSPORT._send.call_args_list]
        self.assertEqual([1, 2, 1, 4, 2], timeouts)

    def test_timeouts_for_namespaces_tracked_independently(self):
        rpc._BackingOffContextWrapper._METHOD_TIMEOUTS['ns1.method'] = 1
        rpc._BackingOffContextWrapper._METHOD_TIMEOUTS['ns2.method'] = 1
        for ns in ('ns1', 'ns2'):
            self.client.target.namespace = ns
            for i in range(4):
                with testtools.ExpectedException(messaging.MessagingTimeout):
                    self.client.call(self.call_context, 'method')
        timeouts = [call[1]['timeout']
                    for call in rpc.TRANSPORT._send.call_args_list]
        self.assertEqual([1, 2, 4, 8, 1, 2, 4, 8], timeouts)

    def test_method_timeout_increases_with_prepare(self):
        rpc._BackingOffContextWrapper._METHOD_TIMEOUTS['method_1'] = 1
        ctx = self.client.prepare(version='1.4')
        with testtools.ExpectedException(messaging.MessagingTimeout):
            ctx.call(self.call_context, 'method_1')
        with testtools.ExpectedException(messaging.MessagingTimeout):
            ctx.call(self.call_context, 'method_1')

        # we only care to check the timeouts sent to the transport
        timeouts = [call[1]['timeout']
                    for call in rpc.TRANSPORT._send.call_args_list]
        self.assertEqual([1, 2], timeouts)

    def test_set_max_timeout_caps_all_methods(self):
        rpc.TRANSPORT.conf.rpc_response_timeout = 300
        rpc._BackingOffContextWrapper._METHOD_TIMEOUTS['method_1'] = 100
        rpc.BackingOffClient.set_max_timeout(50)
        # both explicitly tracked
        self.assertEqual(
            50, rpc._BackingOffContextWrapper._METHOD_TIMEOUTS['method_1'])
        # as well as new methods
        self.assertEqual(
            50, rpc._BackingOffContextWrapper._METHOD_TIMEOUTS['method_2'])

    def test_set_max_timeout_retains_lower_timeouts(self):
        rpc._BackingOffContextWrapper._METHOD_TIMEOUTS['method_1'] = 10
        rpc.BackingOffClient.set_max_timeout(50)
        self.assertEqual(
            10, rpc._BackingOffContextWrapper._METHOD_TIMEOUTS['method_1'])

    def test_set_max_timeout_overrides_default_timeout(self):
        rpc.TRANSPORT.conf.rpc_response_timeout = 10
        self.assertEqual(
            rpc.TRANSPORT.conf.rpc_response_max_timeout,
            rpc._BackingOffContextWrapper.get_max_timeout())
        rpc._BackingOffContextWrapper.set_max_timeout(10)
        self.assertEqual(10, rpc._BackingOffContextWrapper.get_max_timeout())


class CastExceptionTestCase(base.BaseTestCase):
    def setUp(self):
        super().setUp()

        self.messaging_conf = messaging_conffixture.ConfFixture(CONF)
        self.messaging_conf.transport_url = 'fake://'
        self.messaging_conf.response_timeout = 0
        self.useFixture(self.messaging_conf)

        self.addCleanup(rpc.cleanup)
        rpc.init(CONF)
        rpc.TRANSPORT = mock.MagicMock()
        rpc.TRANSPORT._send.side_effect = oslomsg_exc.MessageDeliveryFailure
        rpc.TRANSPORT.conf.oslo_messaging_metrics.metrics_enabled = False
        target = messaging.Target(version='1.0', topic='testing')
        self.client = rpc.get_client(target)
        self.cast_context = mock.Mock()

    def test_cast_catches_exception(self):
        self.client.cast(self.cast_context, 'method_1')


class TestConnection(base.BaseTestCase):
    def setUp(self):
        super().setUp()
        self.conn = rpc.Connection()

    @mock.patch.object(messaging, 'Target')
    @mock.patch.object(cfg, 'CONF')
    @mock.patch.object(rpc, 'get_server')
    def test_create_consumer(self, mock_get, mock_cfg, mock_tgt):
        mock_cfg.host = 'foo'
        server = mock.Mock()
        target = mock.Mock()
        mock_get.return_value = server
        mock_tgt.return_value = target

        self.conn.create_consumer('topic', 'endpoints', fanout=True)

        mock_tgt.assert_called_once_with(topic='topic', server='foo',
                                         fanout=True)
        mock_get.assert_called_once_with(target, 'endpoints')
        self.assertEqual([server], self.conn.servers)

    def test_consume_in_threads(self):
        self.conn.servers = [mock.Mock(), mock.Mock()]

        servs = self.conn.consume_in_threads()

        for serv in self.conn.servers:
            serv.start.assert_called_once_with()
        self.assertEqual(servs, self.conn.servers)

    def test_close(self):
        self.conn.servers = [mock.Mock(), mock.Mock()]

        self.conn.close()

        for serv in self.conn.servers:
            serv.stop.assert_called_once_with()
            serv.wait.assert_called_once_with()
