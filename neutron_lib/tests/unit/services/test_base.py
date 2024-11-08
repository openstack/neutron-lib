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

from neutron_lib.services import base
from neutron_lib.tests import _base as test_base


class _Worker(base.WorkerBase):
    pass


class Test_WorkerSupportServiceMixin(test_base.BaseTestCase):

    def setUp(self):
        super().setUp()
        self.worker = _Worker()

    def test_allocate_workers(self):
        self.assertEqual([], self.worker.get_workers())

    def test_add_worker(self):
        workers = [object(), object()]
        for w in workers:
            self.worker.add_worker(w)

        self.assertSequenceEqual(workers, self.worker.get_workers())

    def test_add_workers(self):
        workers = [object(), object(), object()]
        self.worker.add_workers(workers)

        self.assertSequenceEqual(workers, self.worker.get_workers())


class TestPluginInterface(test_base.BaseTestCase):

    class ServicePluginStub(base.ServicePluginBase):
        def get_plugin_type(self):
            pass

        def get_plugin_description(self):
            pass

    def test_issubclass_hook(self):
        class A(TestPluginInterface.ServicePluginStub):
            def f(self):
                pass

        class B(base.ServicePluginBase):
            @abc.abstractmethod
            def f(self):
                pass

        self.assertTrue(issubclass(A, B))

    def test_issubclass_hook_class_without_abstract_methods(self):
        class A:
            def f(self):
                pass

        class B(base.ServicePluginBase):
            def f(self):
                pass

        self.assertFalse(issubclass(A, B))

    def test_issubclass_hook_not_all_methods_implemented(self):
        class A(TestPluginInterface.ServicePluginStub):
            def f(self):
                pass

        class B(base.ServicePluginBase):
            @abc.abstractmethod
            def f(self):
                pass

            @abc.abstractmethod
            def g(self):
                pass

        self.assertFalse(issubclass(A, B))
