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

import abc


class WorkerBase:

    @property
    def _workers(self):
        try:
            return self.__workers
        except AttributeError:
            self.__workers = []
        return self.__workers

    def get_workers(self):
        """Returns a collection NeutronWorker instances needed by this service.

        """
        return list(self._workers)

    def add_worker(self, worker):
        """Adds NeutronWorker needed for this service

        If a object needs to define workers thread/processes outside of API/RPC
        workers then it will call this method to register worker. Should be
        called on initialization stage before running services
        """
        self._workers.append(worker)

    def add_workers(self, workers):
        """Adds NeutronWorker list needed for this service

        The same as add_worker but adds a list of workers
        """
        self._workers.extend(workers)


class ServicePluginBase(WorkerBase, metaclass=abc.ABCMeta):
    """Define base interface for any Advanced Service plugin."""
    supported_extension_aliases = []

    @classmethod
    def __subclasshook__(cls, klass):
        """Checking plugin class.

        The __subclasshook__ method is a class method
        that will be called every time a class is tested
        using issubclass(klass, ServicePluginBase).
        In that case, it will check that every method
        marked with the abstractmethod decorator is
        provided by the plugin class.
        """

        if not cls.__abstractmethods__:
            return NotImplemented

        for method in cls.__abstractmethods__:
            if any(method in base.__dict__ for base in klass.__mro__):
                continue
            return NotImplemented
        return True

    @abc.abstractmethod
    def get_plugin_type(self):
        """Return one of predefined service types.

        """
        pass

    @abc.abstractmethod
    def get_plugin_description(self):
        """Return string description of the plugin."""
        pass
