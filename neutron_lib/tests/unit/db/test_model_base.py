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

import sqlalchemy as sa

from neutron_lib import context
from neutron_lib.db import model_base

from neutron_lib.tests.unit.db import _base as db_base


class TestTable(model_base.BASEV2, model_base.HasProject,
                model_base.HasId, model_base.HasStatusDescription):

    name = sa.Column(sa.String(8), primary_key=True)


class TestModelBase(db_base.SqlTestCase):

    def setUp(self):
        super().setUp()
        self.ctx = context.Context('user', 'project')
        self.session = self.ctx.session

    def test_model_base(self):
        table = TestTable(name='meh')
        self.assertEqual('meh', table.name)
        self.assertIn('meh', str(table))  # test table.__repr__
        cols = [k for k, _v in table]  # test table.__iter__ and table.next
        self.assertIn('name', cols)

    def test_get_set_tenant_id_tenant(self):
        table = TestTable(tenant_id='tenant')
        self.assertEqual('tenant', table.get_tenant_id())
        table.set_tenant_id('project')
        self.assertEqual('project', table.get_tenant_id())

    def test_get_set_tenant_id_project(self):
        table = TestTable(project_id='project')
        self.assertEqual('project', table.get_tenant_id())
        table.set_tenant_id('tenant')
        self.assertEqual('tenant', table.get_tenant_id())

    def test_project_id_attribute(self):
        table = TestTable(project_id='project')
        self.assertEqual('project', table.project_id)
        self.assertEqual('project', table.tenant_id)

    def test_tenant_id_attribute(self):
        table = TestTable(tenant_id='tenant')
        self.assertEqual('tenant', table.project_id)
        self.assertEqual('tenant', table.tenant_id)
