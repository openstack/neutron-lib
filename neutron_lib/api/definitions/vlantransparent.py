# Copyright (c) 2015 Cisco Systems, Inc.  All rights reserved.
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

from neutron_lib.api import converters
from neutron_lib.api.definitions import network
from neutron_lib.api import validators
from neutron_lib import constants


VLANTRANSPARENT = 'vlan_transparent'


def get_vlan_transparent(network):
    """Get the value of vlan_transparent from a network if set.

    :param network: The network dict to retrieve the value of vlan_transparent
        from.
    :returns: The value of vlan_transparent from the network dict if set in
        the dict, otherwise False is returned.
    """
    return (network[VLANTRANSPARENT]
            if (VLANTRANSPARENT in network and
                validators.is_attr_set(network[VLANTRANSPARENT]))
            else False)


ALIAS = 'vlan-transparent'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Vlantransparent'
API_PREFIX = ''
DESCRIPTION = 'Provides Vlan Transparent Networks'
UPDATED_TIMESTAMP = '2015-03-23T09:00:00-00:00'
RESOURCE_ATTRIBUTE_MAP = {
    network.COLLECTION_NAME: {
        VLANTRANSPARENT: {
            'allow_post': True,
            'allow_put': False,
            'convert_to': converters.convert_to_boolean,
            'default': constants.ATTR_NOT_SPECIFIED,
            'is_visible': True,
            'is_filter': True
        }
    }
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = []
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
