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

from oslo_db.sqlalchemy import models
import sqlalchemy as sa
from sqlalchemy.ext import declarative
from sqlalchemy import orm

from neutron_lib.api import attributes
from neutron_lib.db import utils
from neutron_lib import exceptions as n_exc

from neutron_lib.tests import _base as base


class FakePort(declarative.declarative_base(cls=models.ModelBase)):
    __tablename__ = 'fakeports'
    port_id = sa.Column(sa.String(36), primary_key=True)
    name = sa.Column(sa.String(64))
    status = sa.Column(sa.String(16), nullable=False)


class FakeRouter(declarative.declarative_base(cls=models.ModelBase)):
    __tablename__ = 'fakerouters'
    router_id = sa.Column(sa.String(36), primary_key=True)
    gw_port_id = sa.Column(sa.String(36), sa.ForeignKey(FakePort.port_id))
    gw_port = orm.relationship(FakePort, lazy='joined')


class TestUtils(base.BaseTestCase):

    def test_get_sort_dirs(self):
        sorts = [(1, True), (2, False), (3, True)]
        self.assertEqual(['asc', 'desc', 'asc'],
                         utils.get_sort_dirs(sorts))

    def test_get_sort_dirs_reversed(self):
        sorts = [(1, True), (2, False), (3, True)]
        self.assertEqual(['desc', 'asc', 'desc'],
                         utils.get_sort_dirs(sorts, page_reverse=True))

    def test_get_and_validate_sort_keys(self):
        sorts = [('name', False), ('status', True)]
        self.assertEqual(['name', 'status'],
                         utils.get_and_validate_sort_keys(sorts, FakePort))

    def test_get_and_validate_sort_keys_bad_key_fails(self):
        sorts = [('master', True)]
        self.assertRaises(n_exc.BadRequest,
                          utils.get_and_validate_sort_keys, sorts, FakePort)

    def test_get_and_validate_sort_keys_by_relationship_fails(self):
        sorts = [('gw_port', True)]
        self.assertRaises(n_exc.BadRequest,
                          utils.get_and_validate_sort_keys, sorts, FakeRouter)

    def test_get_marker_obj(self):
        plugin = mock.Mock()
        plugin._get_myr.return_value = 'obj'
        obj = utils.get_marker_obj(plugin, 'ctx', 'myr', 10, mock.ANY)
        self.assertEqual('obj', obj)
        plugin._get_myr.assert_called_once_with('ctx', mock.ANY)

    def test_get_marker_obj_no_limit_and_marker(self):
        self.assertIsNone(utils.get_marker_obj(
            mock.Mock(), 'ctx', 'myr', 0, mock.ANY))
        self.assertIsNone(utils.get_marker_obj(
            mock.Mock(), 'ctx', 'myr', 10, None))

    @mock.patch.object(attributes, 'populate_project_info')
    def test_resource_fields(self, mock_populate):
        r = {
            'name': 'n',
            'id': '1',
            'desc': None
        }
        utils.resource_fields(r, ['name'])
        mock_populate.assert_called_once_with({'name': 'n'})
