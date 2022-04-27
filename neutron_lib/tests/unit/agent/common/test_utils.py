# Copyright 2022
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

from neutron_lib.agent.common import constants
from neutron_lib.agent.common import utils
from neutron_lib.tests import _base


class TestCreateRegNumbers(_base.BaseTestCase):
    def test_no_registers_defined(self):
        flow = {'foo': 'bar'}
        utils.create_reg_numbers(flow)
        self.assertEqual({'foo': 'bar'}, flow)

    def test_all_registers_defined(self):
        flow = {'foo': 'bar',
                constants.PORT_REG_NAME: 1,
                constants.NET_REG_NAME: 2,
                constants.REMOTE_GROUP_REG_NAME: 3,
                constants.INGRESS_BW_LIMIT_REG_NAME: 4,
                constants.MIN_BW_REG_NAME: 5}
        expected_flow = {'foo': 'bar',
                         'reg{:d}'.format(constants.REG_PORT): 1,
                         'reg{:d}'.format(constants.REG_NET): 2,
                         'reg{:d}'.format(constants.REG_REMOTE_GROUP): 3,
                         'reg{:d}'.format(constants.REG_INGRESS_BW_LIMIT): 4,
                         'reg{:d}'.format(constants.REG_MIN_BW): 5}
        utils.create_reg_numbers(flow)
        self.assertEqual(expected_flow, flow)
