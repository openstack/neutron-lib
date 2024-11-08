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


def _replace_register(flow_params, register_number, register_value):
    """Replace value from flows to given register number

    'register_value' key in dictionary will be replaced by register number
    given by 'register_number'

    :param flow_params: Dictionary containing defined flows
    :param register_number: The number of register where value will be stored
    :param register_value: Key to be replaced by register number

    """
    try:
        reg_port = flow_params[register_value]
        del flow_params[register_value]
        flow_params[f'reg{register_number:d}'] = reg_port
    except KeyError:
        pass


def create_reg_numbers(flow_params):
    """Replace reg_(port|net) values with defined register numbers"""
    _replace_register(flow_params, constants.REG_PORT, constants.PORT_REG_NAME)
    _replace_register(flow_params, constants.REG_NET, constants.NET_REG_NAME)
    _replace_register(flow_params,
                      constants.REG_REMOTE_GROUP,
                      constants.REMOTE_GROUP_REG_NAME)
    _replace_register(flow_params,
                      constants.REG_MIN_BW,
                      constants.MIN_BW_REG_NAME)
    _replace_register(flow_params,
                      constants.REG_INGRESS_BW_LIMIT,
                      constants.INGRESS_BW_LIMIT_REG_NAME)
