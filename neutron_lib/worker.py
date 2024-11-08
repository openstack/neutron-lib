# All rights reserved.
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

import os

from oslo_service import service
import setproctitle

from neutron_lib.callbacks import events
from neutron_lib.callbacks import registry
from neutron_lib.callbacks import resources


class BaseWorker(service.ServiceBase):
    """Partial implementation of the ServiceBase ABC.

    Subclasses will still need to add the other abstract methods defined in
    service.ServiceBase. See oslo_service for more details.

    If a plugin needs to handle synchronization with the Neutron database and
    do this only once instead of in every API worker, for instance, it would
    define a BaseWorker class and the plugin would have get_workers return
    an array of BaseWorker instances. For example:

    .. code-block:: python

        class MyPlugin(...):
            def get_workers(self):
                return [MyPluginWorker()]

        class MyPluginWorker(BaseWorker):
            def start(self):
                super(MyPluginWorker, self).start()
                do_sync()
    """

    # default class value for case when super().__init__ is not called
    _default_process_count = 1

    def __init__(self, worker_process_count=_default_process_count,
                 set_proctitle='on', desc=None):
        """Initialize a worker instance.

        :param worker_process_count: Defines how many processes to spawn for
            worker:
                0 - spawn 1 new worker thread,
                1..N - spawn N new worker processes
            set_proctitle:
                'off' - do not change process title
                'on' - set process title to descriptive string and parent
                'brief' - set process title to descriptive string
            desc:
                process descriptive string
        """
        self._worker_process_count = worker_process_count
        self._my_pid = os.getpid()
        self._set_proctitle = set_proctitle
        if set_proctitle == 'on':
            self._parent_proctitle = setproctitle.getproctitle()
        self.desc = desc

    @property
    def worker_process_count(self):
        """The worker's process count.

        :returns: The number of processes to spawn for this worker.
        """
        return self._worker_process_count

    @property
    def set_proctitle(self):
        return self._set_proctitle

    @set_proctitle.setter
    def set_proctitle(self, value):
        self._set_proctitle = value

    def setproctitle(self, name="neutron-server", desc=None):
        if self._set_proctitle == "off" or os.getpid() == self._my_pid:
            return

        if not desc:
            desc = self.__class__.__name__

        proctitle = "{}: {}".format(name, desc)
        if self._set_proctitle == "on":
            proctitle += " (%s)" % self._parent_proctitle

        setproctitle.setproctitle(proctitle)

    def start(self, name="neutron-server", desc=None):
        """Start the worker.

        If worker_process_count is greater than 0, a callback notification
        is sent. Subclasses should call this method before doing their
        own start() work.

        Automatically sets the process title to indicate that this is a
        child worker, customizable via the name and desc arguments.

        :returns: None
        """

        # If we are a child process, set our proctitle to something useful
        desc = desc or self.desc
        self.setproctitle(name, desc)
        if self.worker_process_count > 0:
            registry.publish(resources.PROCESS, events.AFTER_INIT, self.start)
