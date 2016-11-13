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

from webob import exc

from neutron_lib.api import attributes
from oslo_utils import uuidutils

from neutron_lib.tests import _base as base


class TestApiUtils(base.BaseTestCase):

    def test_populate_project_info_add_project(self):
        attrs_in = {'tenant_id': uuidutils.generate_uuid()}
        attrs_out = attributes.populate_project_info(attrs_in)
        self.assertIn('project_id', attrs_out)
        self.assertEqual(attrs_in['tenant_id'], attrs_out['project_id'])
        self.assertEqual(2, len(attrs_out))

    def test_populate_project_info_add_tenant(self):
        attrs_in = {'project_id': uuidutils.generate_uuid()}
        attrs_out = attributes.populate_project_info(attrs_in)
        self.assertIn('tenant_id', attrs_out)
        self.assertEqual(attrs_in['project_id'], attrs_out['tenant_id'])
        self.assertEqual(2, len(attrs_out))

    def test_populate_project_info_ids_match(self):
        project_id = uuidutils.generate_uuid()
        attrs_in = {'project_id': project_id, 'tenant_id': project_id}
        attrs_out = attributes.populate_project_info(attrs_in)
        self.assertEqual(attrs_in, attrs_out)

    def test_populate_project_info_id_mismatch(self):
        attrs = {
            'project_id': uuidutils.generate_uuid(),
            'tenant_id': uuidutils.generate_uuid()
        }
        self.assertRaises(exc.HTTPBadRequest,
                          attributes.populate_project_info, attrs)
