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

import subprocess
import sys

import sqlalchemy as sa

from neutron_lib import context
from neutron_lib.db import model_base

from neutron_lib.tests import _base as base
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


# Imports model_base alone, defines models, then prints any ORM event listener
# from neutron_lib.db.api that is missing.
_LISTENER_CHECK = """
import sys

import sqlalchemy as sa
from sqlalchemy import event
from sqlalchemy import orm

from neutron_lib.db import model_base

api_loaded = 'neutron_lib.db.api' in sys.modules


class Parent(model_base.BASEV2, model_base.HasId):
    children = orm.relationship('Child')


class Child(model_base.BASEV2, model_base.HasId):
    parent_id = sa.Column(sa.String(36), sa.ForeignKey('parents.id'))


orm.configure_mappers()
from neutron_lib.db import api as db_api
session = orm.session.Session
checks = {
    'api loaded with model_base': api_loaded,
    'after_flush': event.contains(
        session, 'after_flush', db_api._add_to_rel_load_list),
    'before_commit': event.contains(
        session, 'before_commit', db_api._load_one_to_manys),
    'pending_to_persistent': event.contains(
        session, 'pending_to_persistent', db_api._pending_callables),
    'persistent_to_deleted': event.contains(
        session, 'persistent_to_deleted', db_api._persistent_to_deleted),
    'attribute_instrument': event.contains(
        model_base.BASEV2, 'attribute_instrument',
        db_api._listen_for_changes),
    # _listen_for_changes adds this backref when Parent.children is mapped.
    'backref': sa.inspect(Child).has_property('_children_backref'),
}
print(','.join(name for name, ok in checks.items() if not ok))
"""


class TestModelBaseListeners(base.BaseTestCase):

    def test_listeners_registered_before_models(self):
        # Run in a fresh interpreter: the test process has already imported
        # neutron_lib.db.api.
        cmd = [sys.executable, '-c', _LISTENER_CHECK]
        out = subprocess.check_output(cmd, text=True)  # noqa: S603
        self.assertEqual('', out.strip())
