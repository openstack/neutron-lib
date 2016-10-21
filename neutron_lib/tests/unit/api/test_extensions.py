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
