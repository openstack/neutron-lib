# Copyright (c) 2015 IBM Corp.
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

import hashlib
from unittest import mock

from oslo_utils import encodeutils
from oslo_utils import excutils
from oslo_utils import uuidutils

from neutron_lib.api.definitions import portbindings_extended as pb_ext
from neutron_lib import constants
from neutron_lib import exceptions
from neutron_lib.plugins import utils
from neutron_lib.tests import _base as base


LONG_NAME1 = "A_REALLY_LONG_INTERFACE_NAME1"
LONG_NAME2 = "A_REALLY_LONG_INTERFACE_NAME2"
SHORT_NAME = "SHORT"


class TestUtils(base.BaseTestCase):

    def test_is_valid_vlan_tag(self):
        for v in [constants.MIN_VLAN_TAG, constants.MIN_VLAN_TAG + 2,
                  constants.MAX_VLAN_TAG, constants.MAX_VLAN_TAG - 2]:
            self.assertTrue(utils.is_valid_vlan_tag(v))

    def test_is_valid_vlan_tag_invalid_data(self):
        for v in [constants.MIN_VLAN_TAG - 1, constants.MIN_VLAN_TAG - 2,
                  constants.MAX_VLAN_TAG + 1, constants.MAX_VLAN_TAG + 2]:
            self.assertFalse(utils.is_valid_vlan_tag(v))

    def test_verify_vlan_range(self):
        for v in [(constants.MIN_VLAN_TAG, constants.MIN_VLAN_TAG + 2),
                  (constants.MIN_VLAN_TAG + 2, constants.MAX_VLAN_TAG - 2)]:
            self.assertIsNone(utils.verify_vlan_range(v))

    def test_verify_vlan_range_invalid_range(self):
        for v in [(constants.MIN_VLAN_TAG, constants.MAX_VLAN_TAG + 2),
                  (constants.MIN_VLAN_TAG + 4, constants.MIN_VLAN_TAG + 1)]:
            self.assertRaises(exceptions.NetworkVlanRangeError,
                              utils.verify_vlan_range, v)

    def test_parse_network_vlan_range(self):
        self.assertEqual(
            ('n1', (1, 3)),
            utils.parse_network_vlan_range('n1:1:3'))
        self.assertEqual(
            ('n1', (1, 1111)),
            utils.parse_network_vlan_range('n1:1:1111'))

    def test_parse_network_vlan_range_invalid_range(self):
        self.assertRaises(exceptions.NetworkVlanRangeError,
                          utils.parse_network_vlan_range,
                          'n1:1,4')

    def test_parse_network_vlan_range_missing_network(self):
        self.assertRaises(exceptions.PhysicalNetworkNameError,
                          utils.parse_network_vlan_range,
                          ':1:4')

    def test_parse_network_vlan_range_invalid_min_type(self):
        self.assertRaises(exceptions.NetworkVlanRangeError,
                          utils.parse_network_vlan_range,
                          'n1:a:4')

    def test_parse_network_vlan_ranges(self):
        ranges = utils.parse_network_vlan_ranges(
            ['n1:1:3', 'n2:2:4', 'n3', 'n4', 'n4:10:12'])
        self.assertEqual(4, len(ranges.keys()))
        self.assertIn('n1', ranges.keys())
        self.assertIn('n2', ranges.keys())
        self.assertEqual(2, len(ranges['n1'][0]))
        self.assertEqual(1, ranges['n1'][0][0])
        self.assertEqual(3, ranges['n1'][0][1])
        self.assertEqual(2, len(ranges['n2'][0]))
        self.assertEqual(2, ranges['n2'][0][0])
        self.assertEqual(4, ranges['n2'][0][1])
        self.assertEqual([constants.VLAN_VALID_RANGE], ranges['n3'])
        self.assertEqual([constants.VLAN_VALID_RANGE], ranges['n4'])

    def test_is_valid_gre_id(self):
        for v in [constants.MIN_GRE_ID, constants.MIN_GRE_ID + 2,
                  constants.MAX_GRE_ID, constants.MAX_GRE_ID - 2]:
            self.assertTrue(utils.is_valid_gre_id(v))

    def test_is_valid_gre_id_invalid_id(self):
        for v in [constants.MIN_GRE_ID - 1, constants.MIN_GRE_ID - 2,
                  True, 'z', 99.999, []]:
            self.assertFalse(utils.is_valid_gre_id(v))

    def test_is_valid_vxlan_vni(self):
        for v in [constants.MIN_VXLAN_VNI, constants.MAX_VXLAN_VNI,
                  constants.MIN_VXLAN_VNI + 1, constants.MAX_VXLAN_VNI - 1]:
            self.assertTrue(utils.is_valid_vxlan_vni(v))

    def test_is_valid_vxlan_vni_invalid_values(self):
        for v in [constants.MIN_VXLAN_VNI - 1, constants.MAX_VXLAN_VNI + 1,
                  True, 'a', False, {}]:
            self.assertFalse(utils.is_valid_vxlan_vni(v))

    def test_is_valid_geneve_vni(self):
        for v in [constants.MIN_GENEVE_VNI, constants.MAX_GENEVE_VNI,
                  constants.MIN_GENEVE_VNI + 1, constants.MAX_GENEVE_VNI - 1]:
            self.assertTrue(utils.is_valid_geneve_vni(v))

    def test_is_valid_geneve_vni_invalid_values(self):
        for v in [constants.MIN_GENEVE_VNI - 1, constants.MAX_GENEVE_VNI + 1,
                  True, False, (), 'True']:
            self.assertFalse(utils.is_valid_geneve_vni(v))

    def test_verify_tunnel_range_known_tunnel_type(self):
        mock_fns = [mock.Mock(return_value=False) for _ in range(3)]
        mock_map = {
            constants.TYPE_GRE: mock_fns[0],
            constants.TYPE_VXLAN: mock_fns[1],
            constants.TYPE_GENEVE: mock_fns[2]
        }

        with mock.patch.dict(utils._TUNNEL_MAPPINGS, mock_map):
            for t in [constants.TYPE_GRE, constants.TYPE_VXLAN,
                      constants.TYPE_GENEVE]:
                self.assertRaises(
                    exceptions.NetworkTunnelRangeError,
                    utils.verify_tunnel_range, [0, 1], t)
            for f in mock_fns:
                f.assert_called_once_with(0)

    def test_verify_tunnel_range_invalid_range(self):
        for r in [[1, 0], [0, -1], [2, 1]]:
            self.assertRaises(
                exceptions.NetworkTunnelRangeError,
                utils.verify_tunnel_range, r, constants.TYPE_FLAT)

    def test_verify_tunnel_range(self):
        for r in [[0, 1], [-1, 0], [1, 2]]:
            self.assertIsNone(
                utils.verify_tunnel_range(r, constants.TYPE_FLAT))

    def test_delete_port_on_error(self):
        core_plugin = mock.Mock()
        with mock.patch.object(excutils, 'save_and_reraise_exception'):
            with mock.patch.object(utils, 'LOG'):
                with utils.delete_port_on_error(core_plugin, 'ctx', '1'):
                    raise Exception()

        core_plugin.delete_port.assert_called_once_with(
            'ctx', '1', l3_port_check=False)

    def test_update_port_on_error(self):
        core_plugin = mock.Mock()
        with mock.patch.object(excutils, 'save_and_reraise_exception'):
            with mock.patch.object(utils, 'LOG'):
                with utils.update_port_on_error(core_plugin, 'ctx', '1', '2'):
                    raise Exception()

        core_plugin.update_port.assert_called_once_with(
            'ctx', '1', {'port': '2'})

    @staticmethod
    def _hash_prefix(name):
        # nosec B324
        hashed_name = hashlib.sha1(encodeutils.to_utf8(name))
        return hashed_name.hexdigest()[0:utils.INTERFACE_HASH_LEN]

    def test_get_interface_name(self):
        prefix = "pre-"
        prefix_long = "long_prefix"
        prefix_exceeds_max_dev_len = "much_too_long_prefix"
        self.assertEqual("A_REALLY_" + self._hash_prefix(LONG_NAME1),
                         utils.get_interface_name(LONG_NAME1))
        self.assertEqual("SHORT",
                         utils.get_interface_name(SHORT_NAME))
        self.assertEqual("pre-A_REA" + self._hash_prefix(LONG_NAME1),
                         utils.get_interface_name(LONG_NAME1, prefix=prefix))
        self.assertEqual("pre-SHORT",
                         utils.get_interface_name(SHORT_NAME, prefix=prefix))
        # len(prefix) > max_device_len - len(hash_used)
        self.assertRaises(ValueError, utils.get_interface_name, SHORT_NAME,
                          prefix_long)
        # len(prefix) > max_device_len
        self.assertRaises(ValueError, utils.get_interface_name, SHORT_NAME,
                          prefix=prefix_exceeds_max_dev_len)

    def test_get_interface_uniqueness(self):
        prefix = "prefix-"
        if_prefix1 = utils.get_interface_name(LONG_NAME1, prefix=prefix)
        if_prefix2 = utils.get_interface_name(LONG_NAME2, prefix=prefix)
        self.assertNotEqual(if_prefix1, if_prefix2)

    def test_get_interface_max_len(self):
        self.assertEqual(constants.DEVICE_NAME_MAX_LEN,
                         len(utils.get_interface_name(LONG_NAME1)))
        self.assertEqual(10, len(utils.get_interface_name(LONG_NAME1,
                                                          max_len=10)))
        self.assertEqual(12, len(utils.get_interface_name(LONG_NAME1,
                                                          prefix="pre-",
                                                          max_len=12)))

    def test_create_network(self):
        mock_plugin = mock.Mock()
        mock_plugin.create_network = lambda c, n: n
        mock_ctx = mock.Mock()
        mock_ctx.project_id = 'p1'
        net = utils.create_network(
            mock_plugin, mock_ctx, {'network': {'name': 'n1'}})
        self.assertDictEqual(
            {'project_id': 'p1', 'admin_state_up': True, 'shared': False,
             'tenant_id': 'p1', 'name': 'n1'},
            net['network'])

    def test_create_subnet(self):
        mock_plugin = mock.Mock()
        mock_plugin.create_subnet = lambda c, s: s
        mock_ctx = mock.Mock()
        mock_ctx.project_id = 'p1'
        net_id = uuidutils.generate_uuid()
        snet = utils.create_subnet(
            mock_plugin, mock_ctx,
            {'subnet': {'network_id': net_id, 'ip_version': 4}})
        self.assertEqual('p1', snet['subnet']['tenant_id'])
        self.assertEqual('p1', snet['subnet']['project_id'])
        self.assertEqual(4, snet['subnet']['ip_version'])
        self.assertEqual(net_id, snet['subnet']['network_id'])

    def test_create_port(self):
        mock_plugin = mock.Mock()
        mock_plugin.create_port = lambda c, p: p
        mock_ctx = mock.Mock()
        mock_ctx.project_id = 'p1'
        net_id = uuidutils.generate_uuid()
        port = utils.create_port(
            mock_plugin, mock_ctx,
            {'port': {'network_id': net_id, 'name': 'aport'}})
        self.assertEqual('p1', port['port']['tenant_id'])
        self.assertEqual('p1', port['port']['project_id'])
        self.assertEqual('aport', port['port']['name'])
        self.assertEqual(net_id, port['port']['network_id'])

    def test_get_port_binding_by_status_and_host(self):
        bindings = []
        self.assertIsNone(utils.get_port_binding_by_status_and_host(
                          bindings, constants.INACTIVE))
        bindings.extend([{pb_ext.STATUS: constants.INACTIVE,
                          pb_ext.HOST: 'host-1'},
                         {pb_ext.STATUS: constants.INACTIVE,
                          pb_ext.HOST: 'host-2'}])
        self.assertEqual(
            'host-1', utils.get_port_binding_by_status_and_host(
                bindings,
                constants.INACTIVE)[pb_ext.HOST])
        self.assertEqual(
            'host-2', utils.get_port_binding_by_status_and_host(
                bindings,
                constants.INACTIVE,
                host='host-2')[pb_ext.HOST])
        self.assertIsNone(utils.get_port_binding_by_status_and_host(
                          bindings, constants.ACTIVE))
        self.assertRaises(exceptions.PortBindingNotFound,
                          utils.get_port_binding_by_status_and_host, bindings,
                          constants.ACTIVE, 'host', True, 'port_id')
