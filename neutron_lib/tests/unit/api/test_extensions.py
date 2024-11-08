# Copyright 2016 OpenStack Foundation
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

from neutron_lib.api import extensions
from neutron_lib import fixture
from neutron_lib.services import base as service_base
from neutron_lib.tests import _base as base


class InheritFromExtensionDescriptor(extensions.ExtensionDescriptor):
    """Class to inherit from ExtensionDescriptor to test its methods

    Because ExtensionDescriptor is an abstract class, in order to test methods
    we need to create something to inherit from it so we have something
    instantiatable.  The only things defined here are those that are required
    because in ExtensionDescriptor they are marked as @abc.abstractmethod.
    """

    def get_name(self):
        pass

    def get_alias(self):
        pass

    def get_description(self):
        pass

    def get_updated(self):
        pass

    def update_attributes_map_save(self, extended_attributes,
                                   extension_attrs_map=None):
        """Update attributes map for this extension.

        This is default method for extending an extension's attributes map.
        An extension can use this method and supplying its own resource
        attribute map in extension_attrs_map argument to extend all its
        attributes that needs to be extended.

        If an extension does not implement update_attributes_map, the method
        does nothing and just return.
        """
        if not extension_attrs_map:
            return

        for resource, attrs in extension_attrs_map.items():
            extended_attrs = extended_attributes.get(resource)
            if extended_attrs:
                attrs.update(extended_attrs)


class TestExtensionDescriptor(base.BaseTestCase):

    def _setup_attribute_maps(self):
        self.extended_attributes = {'resource_one': {'one': 'first'},
                                    'resource_two': {'two': 'second'}}
        self.extension_attrs_map = {'resource_one': {'three': 'third'}}

    def test_update_attributes_map_works(self):
        self._setup_attribute_maps()
        extension_description = InheritFromExtensionDescriptor()
        extension_description.update_attributes_map(self.extended_attributes,
                                                    self.extension_attrs_map)
        self.assertEqual(self.extension_attrs_map,
                         {'resource_one': {'one': 'first',
                                           'three': 'third'}})

    def test_update_attributes_map_short_circuit_exit(self):
        self._setup_attribute_maps()
        extension_description = InheritFromExtensionDescriptor()
        extension_description.update_attributes_map(self.extended_attributes)
        self.assertEqual(self.extension_attrs_map,
                         {'resource_one': {'three': 'third'}})


class DummyPlugin(service_base.ServicePluginBase):

    supported_extension_aliases = ['flash']

    def get_plugin_type(self):
        return 'Flash Gordon'

    def get_plugin_description(self):
        return 'Legend!'


class TestExtensionIsSupported(base.BaseTestCase):

    def setUp(self):
        super().setUp()
        self._plugin = DummyPlugin()

    def test_extension_exists(self):
        self.assertTrue(extensions.is_extension_supported(self._plugin,
                                                          "flash"))

    def test_extension_does_not_exist(self):
        self.assertFalse(extensions.is_extension_supported(self._plugin,
                                                           "gordon"))


class TestAPIExtensionDescriptor(base.BaseTestCase):

    # API definition attributes; acts as an API definition module
    NAME = 'Test API'
    ALIAS = 'test-api'
    DESCRIPTION = 'A test API definition'
    UPDATED_TIMESTAMP = '2017-02-01T10:00:00-00:00'
    RESOURCE_ATTRIBUTE_MAP = {'ports': {}}
    SUB_RESOURCE_ATTRIBUTE_MAP = {'ports': {'debug': {}}}
    REQUIRED_EXTENSIONS = ['l3']
    OPTIONAL_EXTENSIONS = ['fw']

    def setUp(self):
        super().setUp()
        self.extn = _APIDefinition()
        self.empty_extn = _EmptyAPIDefinition()
        self.useFixture(fixture.APIDefinitionFixture(self))

    def test__assert_api_definition_no_defn(self):
        self.assertRaises(NotImplementedError,
                          _NoAPIDefinition._assert_api_definition)

    def test__assert_api_definition_no_attr(self):
        self.assertRaises(
            NotImplementedError, self.extn._assert_api_definition, attr='NOPE')

    def test_get_name(self):
        self.assertEqual(self.NAME, self.extn.get_name())

    def test_get_name_unset(self):
        self.assertRaises(NotImplementedError, _EmptyAPIDefinition.get_name)

    def test_get_alias(self):
        self.assertEqual(self.ALIAS, self.extn.get_alias())

    def test_get_alias_unset(self):
        self.assertRaises(NotImplementedError, _EmptyAPIDefinition.get_alias)

    def test_get_description(self):
        self.assertEqual(self.DESCRIPTION, self.extn.get_description())

    def test_get_description_unset(self):
        self.assertRaises(NotImplementedError,
                          _EmptyAPIDefinition.get_description)

    def test_get_updated(self):
        self.assertEqual(self.UPDATED_TIMESTAMP, self.extn.get_updated())

    def test_get_updated_unset(self):
        self.assertRaises(NotImplementedError, _EmptyAPIDefinition.get_updated)

    def test_get_extended_resources_v2(self):
        self.assertEqual(
            dict(list(self.RESOURCE_ATTRIBUTE_MAP.items()) +
                 list(self.SUB_RESOURCE_ATTRIBUTE_MAP.items())),
            self.extn.get_extended_resources('2.0'))

    def test_get_extended_resources_v2_unset(self):
        self.assertRaises(NotImplementedError,
                          self.empty_extn.get_extended_resources, '2.0')

    def test_get_extended_resources_v1(self):
        self.assertEqual({}, self.extn.get_extended_resources('1.0'))

    def test_get_extended_resources_v1_unset(self):
        self.assertEqual({}, self.empty_extn.get_extended_resources('1.0'))

    def test_get_required_extensions(self):
        self.assertEqual(self.REQUIRED_EXTENSIONS,
                         self.extn.get_required_extensions())

    def test_get_required_extensions_unset(self):
        self.assertRaises(NotImplementedError,
                          self.empty_extn.get_required_extensions)

    def test_get_optional_extensions(self):
        self.assertEqual(self.OPTIONAL_EXTENSIONS,
                         self.extn.get_optional_extensions())

    def test_get_optional_extensions_unset(self):
        self.assertRaises(NotImplementedError,
                          self.empty_extn.get_optional_extensions)

    def test_update_attributes_map_extensions_unset(self):
        self.assertRaises(NotImplementedError,
                          self.empty_extn.update_attributes_map, {})

    def test_update_attributes_map_with_ext_attrs(self):
        base_attrs = {'ports': {'a': 'A'}}
        ext_attrs = {'ports': {'b': 'B'}}
        self.extn.update_attributes_map(base_attrs, ext_attrs)
        self.assertEqual({'ports': {'a': 'A', 'b': 'B'}}, ext_attrs)

    def test_update_attributes_map_without_ext_attrs(self):
        base_attrs = {'ports': {'a': 'A'}}
        self.extn.update_attributes_map(base_attrs)
        self.assertIn('a', self.extn.get_extended_resources('2.0')['ports'])


class _APIDefinition(extensions.APIExtensionDescriptor):
    api_definition = TestAPIExtensionDescriptor


class _NoAPIDefinition(extensions.APIExtensionDescriptor):
    pass


class _EmptyAPIDefinition(extensions.APIExtensionDescriptor):
    api_definition = {}
