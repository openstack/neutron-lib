# Copyright (c) 2012 OpenStack Foundation.
# Copyright (c) 2014 Red Hat, Inc.
# All Rights Reserved.
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

import collections
import random
import time

from oslo_config import cfg
from oslo_log import log as logging
import oslo_messaging
from oslo_messaging import exceptions as oslomsg_exc
from oslo_messaging import serializer as om_serializer
from oslo_service import service as os_service
from oslo_utils import excutils
from osprofiler import profiler

from neutron_lib._i18n import _
from neutron_lib import context
from neutron_lib import exceptions
from neutron_lib.utils import runtime


LOG = logging.getLogger(__name__)
TRANSPORT = None
NOTIFICATION_TRANSPORT = None

_DFT_EXMODS = runtime.list_package_modules(exceptions.__name__)


def init(conf, rpc_ext_mods=None):
    """Initialize the global RPC objects.

    :param conf: The oslo conf to use for initialization.
    :param rpc_ext_mods: Exception modules to expose via RPC.
    :returns: None.
    """
    global TRANSPORT, NOTIFICATION_TRANSPORT

    if rpc_ext_mods is None:
        rpc_ext_mods = _DFT_EXMODS
    else:
        rpc_ext_mods = list(set(rpc_ext_mods + _DFT_EXMODS))

    TRANSPORT = oslo_messaging.get_rpc_transport(
        conf, allowed_remote_exmods=rpc_ext_mods)
    NOTIFICATION_TRANSPORT = oslo_messaging.get_notification_transport(
        conf, allowed_remote_exmods=rpc_ext_mods)


def cleanup():
    """Deactivate and cleanup the global RPC objects.

    :returns: None.
    """
    global TRANSPORT, NOTIFICATION_TRANSPORT
    if TRANSPORT is None:
        raise AssertionError(_("'TRANSPORT' must not be None"))
    if NOTIFICATION_TRANSPORT is None:
        raise AssertionError(
            _("'NOTIFICATION_TRANSPORT' must not be None"))
    TRANSPORT.cleanup()
    NOTIFICATION_TRANSPORT.cleanup()
    _BackingOffContextWrapper.reset_timeouts()
    TRANSPORT = NOTIFICATION_TRANSPORT = None


def _get_default_method_timeout():
    return TRANSPORT.conf.rpc_response_timeout


def _get_default_method_timeouts():
    return collections.defaultdict(_get_default_method_timeout)


def _get_rpc_response_max_timeout():
    return TRANSPORT.conf.rpc_response_max_timeout


class _ContextWrapper:
    def __init__(self, original_context):
        self._original_context = original_context

    def __getattr__(self, name):
        return getattr(self._original_context, name)

    def cast(self, ctxt, method, **kwargs):
        try:
            self._original_context.cast(ctxt, method, **kwargs)
        except oslomsg_exc.MessageDeliveryFailure as e:
            LOG.debug("Ignored exception during cast: %s", str(e))


class _BackingOffContextWrapper(_ContextWrapper):
    """Wraps oslo messaging contexts to set the timeout for calls.

    This intercepts RPC calls and sets the timeout value to the globally
    adapting value for each method. An oslo messaging timeout results in
    a doubling of the timeout value for the method on which it timed out.
    There currently is no logic to reduce the timeout since busy Neutron
    servers are more frequently the cause of timeouts rather than lost
    messages.
    """
    _METHOD_TIMEOUTS = _get_default_method_timeouts()
    _max_timeout = None

    @classmethod
    def reset_timeouts(cls):
        # restore the original default timeout factory
        cls._METHOD_TIMEOUTS = _get_default_method_timeouts()
        cls._max_timeout = None

    @classmethod
    def get_max_timeout(cls):
        return cls._max_timeout or _get_rpc_response_max_timeout()

    @classmethod
    def set_max_timeout(cls, max_timeout):
        if max_timeout < cls.get_max_timeout():
            cls._METHOD_TIMEOUTS.default_factory = lambda: max_timeout
            for k, v in cls._METHOD_TIMEOUTS.items():
                if v > max_timeout:
                    cls._METHOD_TIMEOUTS[k] = max_timeout
            cls._max_timeout = max_timeout

    def call(self, ctxt, method, **kwargs):
        # two methods with the same name in different namespaces should
        # be tracked independently
        if self._original_context.target.namespace:
            scoped_method = '{}.{}'.format(
                self._original_context.target.namespace, method)
        else:
            scoped_method = method
        # set the timeout from the global method timeout tracker for this
        # method
        self._original_context.timeout = self._METHOD_TIMEOUTS[scoped_method]
        try:
            return self._original_context.call(ctxt, method, **kwargs)
        except oslo_messaging.MessagingTimeout:
            with excutils.save_and_reraise_exception():
                wait = random.uniform(
                    0,
                    min(self._METHOD_TIMEOUTS[scoped_method],
                        TRANSPORT.conf.rpc_response_timeout)
                )
                LOG.error("Timeout in RPC method %(method)s. Waiting for "
                          "%(wait)s seconds before next attempt. If the "
                          "server is not down, consider increasing the "
                          "rpc_response_timeout option as Neutron "
                          "server(s) may be overloaded and unable to "
                          "respond quickly enough.",
                          {'wait': int(round(wait)), 'method': scoped_method})
                new_timeout = min(
                    self._original_context.timeout * 2, self.get_max_timeout())
                if new_timeout > self._METHOD_TIMEOUTS[scoped_method]:
                    LOG.warning("Increasing timeout for %(method)s calls "
                                "to %(new)s seconds. Restart the agent to "
                                "restore it to the default value.",
                                {'method': scoped_method, 'new': new_timeout})
                    self._METHOD_TIMEOUTS[scoped_method] = new_timeout
                time.sleep(wait)


class BackingOffClient(oslo_messaging.RPCClient):
    """An oslo messaging RPC Client that implements a timeout backoff.

    This has all of the same interfaces as oslo_messaging.RPCClient but
    if the timeout parameter is not specified, the _BackingOffContextWrapper
    returned will track when call timeout exceptions occur and exponentially
    increase the timeout for the given call method.
    """
    def prepare(self, *args, **kwargs):
        ctx = super().prepare(*args, **kwargs)
        # don't back off contexts that explicitly set a timeout
        if 'timeout' in kwargs:
            return _ContextWrapper(ctx)
        return _BackingOffContextWrapper(ctx)

    @staticmethod
    def set_max_timeout(max_timeout):
        '''Set RPC timeout ceiling for all backing-off RPC clients.'''
        _BackingOffContextWrapper.set_max_timeout(max_timeout)


def get_client(target, version_cap=None, serializer=None):
    """Get an RPC client for the said target.

    The init() function must be called prior to calling this.
    :param target: The RPC target for the client.
    :param version_cap: The optional version cap for the RPC client.
    :param serializer: The optional serializer to use for the RPC client.
    :returns: A new RPC client.
    """
    if TRANSPORT is None:
        raise AssertionError(_("'TRANSPORT' must not be None"))
    serializer = RequestContextSerializer(serializer)
    return oslo_messaging.get_rpc_client(
        TRANSPORT, target, version_cap=version_cap,
        serializer=serializer, client_cls=BackingOffClient)


def get_server(target, endpoints, serializer=None):
    """Get a new RPC server reference.

    :param target: The target for the new RPC server.
    :param endpoints: The endpoints for the RPC server.
    :param serializer: The optional serialize to use for the RPC server.
    :returns: A new RPC server reference.
    """
    if TRANSPORT is None:
        raise AssertionError(_("'TRANSPORT' must not be None"))
    serializer = RequestContextSerializer(serializer)
    return oslo_messaging.get_rpc_server(TRANSPORT, target, endpoints,
                                         serializer=serializer)


def get_notifier(service=None, host=None, publisher_id=None):
    """Get a new notifier reference.

    :param service: The optional service for the notifier. If not given,
        `None` is used as the service name (deprecated since 2025.1).
    :param host: The optional host for the notifier. If not given, the host
        will be taken from the global CONF.
    :param publisher_id: The optional publisher ID for the notifier. Overrides
        `service` and `host` arguments.
    :returns: A new RPC notifier reference.
    """
    if NOTIFICATION_TRANSPORT is None:
        raise AssertionError(_("'NOTIFICATION_TRANSPORT' must not be None"))
    if not publisher_id:
        if service is None:
            LOG.warning("The 'service' argument to get_notifier is set to "
                        "None. This is deprecated since 2025.1 release and "
                        "will be removed in one of the future releases. "
                        "Please always pass the 'service' argument.")
        publisher_id = "{}.{}".format(service, host or cfg.CONF.host)
    serializer = RequestContextSerializer()
    return oslo_messaging.Notifier(NOTIFICATION_TRANSPORT,
                                   serializer=serializer,
                                   publisher_id=publisher_id)


class RequestContextSerializer(om_serializer.Serializer):
    """Convert RPC common context into Neutron Context."""
    def __init__(self, base=None):
        super().__init__()
        self._base = base

    def serialize_entity(self, ctxt, entity):
        if not self._base:
            return entity
        return self._base.serialize_entity(ctxt, entity)

    def deserialize_entity(self, ctxt, entity):
        if not self._base:
            return entity
        return self._base.deserialize_entity(ctxt, entity)

    def serialize_context(self, ctxt):
        _context = ctxt.to_dict()
        prof = profiler.get()
        if prof:
            trace_info = {
                "hmac_key": prof.hmac_key,
                "base_id": prof.get_base_id(),
                "parent_id": prof.get_id()
            }
            _context['trace_info'] = trace_info
        return _context

    def deserialize_context(self, ctxt):
        rpc_ctxt_dict = ctxt.copy()
        trace_info = rpc_ctxt_dict.pop("trace_info", None)
        if trace_info:
            profiler.init(**trace_info)
        return context.Context.from_dict(rpc_ctxt_dict)


@profiler.trace_cls("rpc")
class Service(os_service.Service):
    """Service object for binaries running on hosts.

    A service enables rpc by listening to queues based on topic and host.
    """
    def __init__(self, host, topic, manager=None, serializer=None):
        super().__init__()
        self.host = host
        self.topic = topic
        self.serializer = serializer
        if manager is None:
            self.manager = self
        else:
            self.manager = manager

    def start(self):
        super().start()

        self.conn = Connection()
        LOG.debug("Creating Consumer connection for Service %s",
                  self.topic)

        endpoints = [self.manager]

        self.conn.create_consumer(self.topic, endpoints)

        # Hook to allow the manager to do other initializations after
        # the rpc connection is created.
        if callable(getattr(self.manager, 'initialize_service_hook', None)):
            self.manager.initialize_service_hook(self)

        # Consume from all consumers in threads
        self.conn.consume_in_threads()

    def stop(self):
        # Try to shut the connection down, but if we get any sort of
        # errors, go ahead and ignore them.. as we're shutting down anyway
        try:
            self.conn.close()
        except Exception:  # nosec
            pass
        super().stop()


class Connection:
    """A utility class that manages a collection of RPC servers."""

    def __init__(self):
        super().__init__()
        self.servers = []

    def create_consumer(self, topic, endpoints, fanout=False):
        target = oslo_messaging.Target(
            topic=topic, server=cfg.CONF.host, fanout=fanout)
        server = get_server(target, endpoints)
        self.servers.append(server)

    def consume_in_threads(self):
        for server in self.servers:
            server.start()
        return self.servers

    def close(self):
        for server in self.servers:
            server.stop()
        for server in self.servers:
            server.wait()
