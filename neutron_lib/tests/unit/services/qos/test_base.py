# All rights reserved.
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

from unittest import mock

from neutron_lib.api.definitions import portbindings
from neutron_lib import constants
from neutron_lib.services.qos import base as qos_base
from neutron_lib.services.qos import constants as qos_consts
from neutron_lib.tests import _base


SUPPORTED_RULES = {
    qos_consts.RULE_TYPE_MINIMUM_BANDWIDTH: {
        qos_consts.MIN_KBPS: {'type:values': None},
        qos_consts.DIRECTION: {'type:values': ['egress']}
    }
}


def _make_rule(rule_type='fake-rule-type', params=None):
    mock_rule = mock.MagicMock()
    mock_rule.rule_type = rule_type
    params = params or {}
    mock_rule.get = params.get
    return mock_rule


def _make_driver(name='fake-driver',
                 vif_types=[portbindings.VIF_TYPE_OVS],
                 vnic_types=[portbindings.VNIC_NORMAL],
                 supported_rules=SUPPORTED_RULES,
                 requires_rpc_notifications=False):
    return qos_base.DriverBase(
        name, vif_types, vnic_types, supported_rules,
        requires_rpc_notifications=requires_rpc_notifications)


class TestDriverBase(_base.BaseTestCase):

    def test_is_loaded(self):
        self.assertTrue(_make_driver().is_loaded())

    def test_is_vif_type_compatible(self):
        self.assertTrue(
            _make_driver().is_vif_type_compatible(
                portbindings.VIF_TYPE_OVS))
        self.assertFalse(
            _make_driver().is_vif_type_compatible(
                portbindings.VIF_TYPE_BRIDGE))

    def test_is_vnic_compatible(self):
        self.assertTrue(
            _make_driver().is_vnic_compatible(portbindings.VNIC_NORMAL))
        self.assertFalse(
            _make_driver().is_vnic_compatible(portbindings.VNIC_BAREMETAL))

    def test_is_rule_supported_with_unsupported_rule(self):
        self.assertFalse(_make_driver().is_rule_supported(_make_rule()))

    def test_is_rule_supported(self):
        self.assertTrue(
            _make_driver().is_rule_supported(
                _make_rule(
                    rule_type=qos_consts.RULE_TYPE_MINIMUM_BANDWIDTH,
                    params={qos_consts.MIN_KBPS: None,
                            qos_consts.DIRECTION:
                                constants.EGRESS_DIRECTION})))
        self.assertFalse(
            _make_driver().is_rule_supported(
                _make_rule(
                    rule_type=qos_consts.RULE_TYPE_MINIMUM_BANDWIDTH,
                    params={qos_consts.MIN_KBPS: None,
                            qos_consts.DIRECTION:
                                constants.INGRESS_DIRECTION})))
