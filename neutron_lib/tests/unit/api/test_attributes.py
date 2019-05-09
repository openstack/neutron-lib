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

from oslo_utils import uuidutils
import testtools
from webob import exc

from neutron_lib.api import attributes
from neutron_lib.api import converters
from neutron_lib.api.definitions import network
from neutron_lib.api.definitions import port
from neutron_lib.api.definitions import subnet
from neutron_lib.api.definitions import subnetpool
from neutron_lib import constants
from neutron_lib import context
from neutron_lib import exceptions

from neutron_lib.tests import _base as base


class TestPopulateProjectInfo(base.BaseTestCase):

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


class TestAttributeInfo(base.BaseTestCase):

    class _MyException(Exception):
        pass

    _EXC_CLS = _MyException
    _RESOURCE_NAME = 'thing'
    _RESOURCE_ATTRS = {'name': {}, 'type': {}}
    _RESOURCE_MAP = {_RESOURCE_NAME: _RESOURCE_ATTRS}
    _ATTRS_INSTANCE = attributes.AttributeInfo(_RESOURCE_MAP)

    def test_create_from_attribute_info_instance(self):
        cloned_attrs = attributes.AttributeInfo(
            TestAttributeInfo._ATTRS_INSTANCE)

        self.assertEqual(TestAttributeInfo._ATTRS_INSTANCE.attributes,
                         cloned_attrs.attributes)

    def test_create_from_api_def(self):
        self.assertEqual(
            port.RESOURCE_ATTRIBUTE_MAP,
            attributes.AttributeInfo(port.RESOURCE_ATTRIBUTE_MAP).attributes)

    def _test_fill_default_value(self, attr_inst, expected, res_dict,
                                 check_allow_post=True):
        attr_inst.fill_post_defaults(
            res_dict, check_allow_post=check_allow_post)
        self.assertEqual(expected, res_dict)

    def test_fill_default_value_ok(self):
        attr_info = {
            'key': {
                'allow_post': True,
                'default': constants.ATTR_NOT_SPECIFIED,
            },
        }
        attr_inst = attributes.AttributeInfo(attr_info)
        self._test_fill_default_value(attr_inst, {'key': 'X'}, {'key': 'X'})
        self._test_fill_default_value(
            attr_inst, {'key': constants.ATTR_NOT_SPECIFIED}, {})

    def test_override_no_allow_post(self):
        attr_info = {
            'key': {
                'allow_post': False,
                'default': constants.ATTR_NOT_SPECIFIED,
            },
        }
        attr_inst = attributes.AttributeInfo(attr_info)
        self._test_fill_default_value(attr_inst, {'key': 'X'}, {'key': 'X'},
                                      check_allow_post=False)

    def test_fill_no_default_value_allow_post(self):
        attr_info = {
            'key': {
                'allow_post': True,
            },
        }
        attr_inst = attributes.AttributeInfo(attr_info)
        self._test_fill_default_value(attr_inst, {'key': 'X'}, {'key': 'X'})
        self.assertRaises(exceptions.InvalidInput,
                          self._test_fill_default_value,
                          attr_inst, {'key': 'X'}, {})
        self.assertRaises(self._EXC_CLS, attr_inst.fill_post_defaults,
                          {}, self._EXC_CLS)

    def test_fill_no_default_value_no_allow_post(self):
        attr_info = {
            'key': {
                'allow_post': False,
            },
        }
        attr_inst = attributes.AttributeInfo(attr_info)
        self.assertRaises(exceptions.InvalidInput,
                          self._test_fill_default_value,
                          attr_inst, {'key': 'X'}, {'key': 'X'})
        self._test_fill_default_value(attr_inst, {}, {})
        self.assertRaises(self._EXC_CLS, attr_inst.fill_post_defaults,
                          {'key': 'X'}, self._EXC_CLS)

    def test_fill_none_overridden_by_default(self):
        attr_info = {
            'key': {
                'allow_post': True,
                'default': 42,
                'default_overrides_none': True,
            },
        }
        attr_inst = attributes.AttributeInfo(attr_info)
        self._test_fill_default_value(attr_inst, {'key': 42}, {'key': None})

    def _test_convert_value(self, attr_inst, expected, res_dict):
        attr_inst.convert_values(res_dict)
        self.assertEqual(expected, res_dict)

    def test_convert_value(self):
        attr_info = {
            'key': {
            },
        }
        attr_inst = attributes.AttributeInfo(attr_info)
        self._test_convert_value(attr_inst,
                                 {'key': constants.ATTR_NOT_SPECIFIED},
                                 {'key': constants.ATTR_NOT_SPECIFIED})
        self._test_convert_value(attr_inst, {'key': 'X'}, {'key': 'X'})
        self._test_convert_value(attr_inst,
                                 {'other_key': 'X'}, {'other_key': 'X'})

        attr_info = {
            'key': {
                'convert_to': converters.convert_to_int,
            },
        }
        attr_inst = attributes.AttributeInfo(attr_info)
        self._test_convert_value(attr_inst,
                                 {'key': constants.ATTR_NOT_SPECIFIED},
                                 {'key': constants.ATTR_NOT_SPECIFIED})
        self._test_convert_value(attr_inst, {'key': 1}, {'key': '1'})
        self._test_convert_value(attr_inst, {'key': 1}, {'key': 1})
        self.assertRaises(exceptions.InvalidInput, self._test_convert_value,
                          attr_inst, {'key': 1}, {'key': 'a'})

        attr_info = {
            'key': {
                'validate': {'type:uuid': None},
            },
        }
        attr_inst = attributes.AttributeInfo(attr_info)
        self._test_convert_value(attr_inst,
                                 {'key': constants.ATTR_NOT_SPECIFIED},
                                 {'key': constants.ATTR_NOT_SPECIFIED})
        uuid_str = '01234567-1234-1234-1234-1234567890ab'
        self._test_convert_value(attr_inst,
                                 {'key': uuid_str}, {'key': uuid_str})
        self.assertRaises(exceptions.InvalidInput, self._test_convert_value,
                          attr_inst, {'key': 1}, {'key': 1})
        self.assertRaises(self._EXC_CLS, attr_inst.convert_values,
                          {'key': 1}, self._EXC_CLS)

    def test_populate_project_id_admin_req(self):
        tenant_id_1 = uuidutils.generate_uuid()
        tenant_id_2 = uuidutils.generate_uuid()
        # non-admin users can't create a res on behalf of another project
        ctx = context.Context(user_id=None, tenant_id=tenant_id_1)
        res_dict = {'tenant_id': tenant_id_2}
        attr_inst = attributes.AttributeInfo({})
        self.assertRaises(exc.HTTPBadRequest,
                          attr_inst.populate_project_id,
                          ctx, res_dict, None)
        # but admin users can
        ctx.is_admin = True
        attr_inst.populate_project_id(ctx, res_dict, is_create=False)

    def test_populate_project_id_from_context(self):
        tenant_id = uuidutils.generate_uuid()
        ctx = context.Context(user_id=None, tenant_id=tenant_id)
        # for each create request, the tenant_id should be added to the
        # req body
        res_dict = {}
        attr_inst = attributes.AttributeInfo({})
        attr_inst.populate_project_id(ctx, res_dict, is_create=True)
        self.assertEqual(
            {'tenant_id': ctx.tenant_id, 'project_id': ctx.tenant_id},
            res_dict)

    def test_populate_project_id_mandatory_not_specified(self):
        tenant_id = uuidutils.generate_uuid()
        ctx = context.Context(user_id=None, tenant_id=tenant_id)
        # if the tenant_id is mandatory for the resource and not specified
        # in the request nor in the context, an exception should be raised
        res_dict = {}
        attr_info = {'tenant_id': {'allow_post': True}}
        ctx.tenant_id = None
        attr_inst = attributes.AttributeInfo(attr_info)
        self.assertRaises(exc.HTTPBadRequest,
                          attr_inst.populate_project_id,
                          ctx, res_dict, True)

    def test_populate_project_id_not_mandatory(self):
        ctx = context.Context(user_id=None)
        # if the tenant_id is not mandatory for the resource it should be
        # OK if it is not in the request.
        res_dict = {'name': 'test_port'}
        attr_inst = attributes.AttributeInfo({})
        ctx.tenant_id = None
        attr_inst.populate_project_id(ctx, res_dict, True)

    def test_verify_attributes_null(self):
        attributes.AttributeInfo({}).verify_attributes({})

    def test_verify_attributes_ok_with_project_id(self):
        attributes.AttributeInfo(
            {'tenant_id': 'foo', 'project_id': 'foo'}).verify_attributes(
            {'tenant_id': 'foo'})

    def test_verify_attributes_ok_subset(self):
        attributes.AttributeInfo(
            {'attr1': 'foo', 'attr2': 'bar'}).verify_attributes(
            {'attr1': 'foo'})

    def test_verify_attributes_unrecognized(self):
        with testtools.ExpectedException(exc.HTTPBadRequest) as bad_req:
            attributes.AttributeInfo(
                {'attr1': 'foo'}).verify_attributes(
                {'attr1': 'foo', 'attr2': 'bar'})
            self.assertEqual(bad_req.message,
                             "Unrecognized attribute(s) 'attr2'")


class TestCoreResources(base.BaseTestCase):

    CORE_DEFS = [network, port, subnet, subnetpool]

    def test_core_resource_names(self):
        self.assertEqual(
            sorted([r.COLLECTION_NAME for r in TestCoreResources.CORE_DEFS]),
            sorted(attributes.RESOURCES.keys()))

    def test_core_resource_attrs(self):
        for r in TestCoreResources.CORE_DEFS:
            self.assertIs(r.RESOURCE_ATTRIBUTE_MAP[r.COLLECTION_NAME],
                          attributes.RESOURCES[r.COLLECTION_NAME])


class TestValidatePriviliges(base.BaseTestCase):

    def test__validate_privileges_same_tenant(self):
        project_id = 'fake_project'
        ctx = context.Context(project_id=project_id)
        res_dict = {'project_id': project_id}
        try:
            attributes._validate_privileges(ctx, res_dict)
        except exc.HTTPBadRequest:
            self.fail("HTTPBadRequest exception should not be raised.")

    def test__validate_privileges_user_other_tenant(self):
        project_id = 'fake_project'
        ctx = context.Context(project_id='fake_project2')
        res_dict = {'project_id': project_id}
        self.assertRaises(
            exc.HTTPBadRequest,
            attributes._validate_privileges,
            ctx, res_dict)

    def test__validate_privileges_admin_other_tenant(self):
        project_id = 'fake_project'
        ctx = context.Context(project_id='fake_project2',
                              is_admin=True)
        res_dict = {'project_id': project_id}
        try:
            attributes._validate_privileges(ctx, res_dict)
        except exc.HTTPBadRequest:
            self.fail("HTTPBadRequest exception should not be raised.")

    def test__validate_privileges_advsvc_other_tenant(self):
        project_id = 'fake_project'
        ctx = context.Context(project_id='fake_project2',
                              is_advsvc=True)
        res_dict = {'project_id': project_id}
        try:
            attributes._validate_privileges(ctx, res_dict)
        except exc.HTTPBadRequest:
            self.fail("HTTPBadRequest exception should not be raised.")


class TestRetrieveValidSortKeys(base.BaseTestCase):

    def test_retrieve_valid_sort_keys(self):
        attr_info = {
            "id": {
                "visible": True,
                "is_sort_key": True
            },
            "name": {
                "is_sort_key": True
            },
            "created_at": {
                "is_sort_key": False
            },
            "tenant_id": {
                "visible": True,
            }
        }
        expect_val = set(["id", "name"])
        actual_val = attributes.retrieve_valid_sort_keys(attr_info)
        self.assertEqual(expect_val, actual_val)
