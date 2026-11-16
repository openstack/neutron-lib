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

from neutron_lib.api.definitions import tap_mirror
from neutron_lib.api.definitions import tap_mirror_both_direction
from neutron_lib.api.definitions import tap_mirror_lport
from neutron_lib.api import validators
from neutron_lib.tests.unit.api.definitions import base


class TapMirrorLportDefinitionTestCase(base.DefinitionBaseTestCase):
    extension_module = tap_mirror_lport
    extension_resources = (tap_mirror.COLLECTION_NAME,)
    extension_attributes = ('remote_ip', 'mirror_type', 'directions',
                            tap_mirror_lport.REMOTE_PORT_ID)

    def test_lport_mirror_type_is_added(self):
        mirror_type = self.resource_map[tap_mirror.COLLECTION_NAME][
            'mirror_type']
        self.assertIn(tap_mirror_lport.MIRROR_TYPE_LPORT,
                      mirror_type['validate']['type:values'])
        for legacy_type in tap_mirror.mirror_types_list:
            self.assertIn(legacy_type, mirror_type['validate']['type:values'])

    def test_directions_values_are_optional(self):
        spec = self.resource_map[tap_mirror.COLLECTION_NAME][
            'directions']['validate']['type:dict']
        self.assertEqual({'IN', 'OUT', 'BOTH'}, set(spec))
        for key_spec in spec.values():
            self.assertIn('type:integer_or_none', key_spec)
            self.assertFalse(key_spec['required'])

    def test_directions_values_accept_none_or_integer(self):
        # Same integer validation as ``tap-mirror-both-direction``, plus
        # ``null`` for lport mirrors; no range check is added here.
        spec = self.resource_map[tap_mirror.COLLECTION_NAME][
            'directions']['validate']['type:dict']
        both_spec = tap_mirror_both_direction.RESOURCE_ATTRIBUTE_MAP[
            tap_mirror.COLLECTION_NAME]['directions']['validate'][
            'type:dict']
        for direction in ('IN', 'OUT', 'BOTH'):
            self.assertIsNone(validators.validate_dict(
                {direction: None}, spec))
            for value in (-1, 0, 2 ** 32 - 1, 2 ** 32, '123', 1.0):
                self.assertIsNone(validators.validate_dict(
                    {direction: value}, spec), value)
                self.assertIsNone(validators.validate_dict(
                    {direction: value}, both_spec), value)
            for value in (True, False, 1.5, '1.5', 'x'):
                self.assertIsNotNone(validators.validate_dict(
                    {direction: value}, spec), value)
                self.assertIsNotNone(validators.validate_dict(
                    {direction: value}, both_spec), value)

    def test_remote_ip_and_remote_port_id_are_optional(self):
        attrs = self.resource_map[tap_mirror.COLLECTION_NAME]
        for name in ('remote_ip', tap_mirror_lport.REMOTE_PORT_ID):
            self.assertTrue(attrs[name]['allow_post'])
            self.assertFalse(attrs[name]['allow_put'])
            self.assertIsNone(attrs[name]['default'])
