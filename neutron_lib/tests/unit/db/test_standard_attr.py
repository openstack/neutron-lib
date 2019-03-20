#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import gc

from sqlalchemy.ext import declarative
import testtools

from neutron_lib.db import standard_attr
from neutron_lib.tests import _base as base


class StandardAttrTestCase(base.BaseTestCase):
    def setUp(self):
        super(StandardAttrTestCase, self).setUp()
        self.addCleanup(gc.collect)

    def _make_decl_base(self):
        # construct a new base so we don't interfere with the main
        # base used in the sql test fixtures
        return declarative.declarative_base(
            cls=standard_attr.model_base.NeutronBaseV2)

    def test_standard_attr_resource_model_map(self):
        rs_map = standard_attr.get_standard_attr_resource_model_map()
        base = self._make_decl_base()

        class MyModel(standard_attr.HasStandardAttributes,
                      standard_attr.model_base.HasId,
                      base):
            api_collections = ['my_resource', 'my_resource2']
            api_sub_resources = ['my_subresource']

        rs_map = standard_attr.get_standard_attr_resource_model_map()
        self.assertEqual(MyModel, rs_map['my_resource'])
        self.assertEqual(MyModel, rs_map['my_resource2'])
        self.assertEqual(MyModel, rs_map['my_subresource'])

        sub_rs_map = standard_attr.get_standard_attr_resource_model_map(
            include_resources=False,
            include_sub_resources=True)
        self.assertNotIn('my_resource', sub_rs_map)
        self.assertNotIn('my_resource2', sub_rs_map)
        self.assertEqual(MyModel, sub_rs_map['my_subresource'])

        nosub_rs_map = standard_attr.get_standard_attr_resource_model_map(
            include_resources=True,
            include_sub_resources=False)
        self.assertEqual(MyModel, nosub_rs_map['my_resource'])
        self.assertEqual(MyModel, nosub_rs_map['my_resource2'])
        self.assertNotIn('my_subresource', nosub_rs_map)

        class Dup(standard_attr.HasStandardAttributes,
                  standard_attr.model_base.HasId,
                  base):
            api_collections = ['my_resource']

        with testtools.ExpectedException(RuntimeError):
            standard_attr.get_standard_attr_resource_model_map()

    def test_standard_attr_resource_parent_map(self):
        base = self._make_decl_base()

        class TagSupportModel(standard_attr.HasStandardAttributes,
                              standard_attr.model_base.HasId,
                              base):
            collection_resource_map = {'collection_name': 'member_name'}
            tag_support = True

        class TagUnsupportModel(standard_attr.HasStandardAttributes,
                                standard_attr.model_base.HasId,
                                base):
            collection_resource_map = {'collection_name2': 'member_name2'}
            tag_support = False

        class TagUnsupportModel2(standard_attr.HasStandardAttributes,
                                 standard_attr.model_base.HasId,
                                 base):
            collection_resource_map = {'collection_name3': 'member_name3'}

        parent_map = standard_attr.get_tag_resource_parent_map()
        self.assertEqual('member_name', parent_map['collection_name'])
        self.assertNotIn('collection_name2', parent_map)
        self.assertNotIn('collection_name3', parent_map)

        class DupTagSupportModel(standard_attr.HasStandardAttributes,
                                 standard_attr.model_base.HasId,
                                 base):
            collection_resource_map = {'collection_name': 'member_name'}
            tag_support = True

        with testtools.ExpectedException(RuntimeError):
            standard_attr.get_tag_resource_parent_map()
