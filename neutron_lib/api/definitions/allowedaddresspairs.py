# Copyright 2013 VMware, Inc.  All rights reserved.
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
from neutron_lib.api.definitions import port
from neutron_lib.api import validators
from neutron_lib.api.validators import allowedaddresspairs as addr_validation
from neutron_lib import constants

validators.add_validator('allowed_address_pairs',
                         addr_validation._validate_allowed_address_pairs)


ADDRESS_PAIRS = 'allowed_address_pairs'
ALIAS = 'allowed-address-pairs'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Allowed Address Pairs'
API_PREFIX = ''
DESCRIPTION = 'Provides allowed address pairs'
UPDATED_TIMESTAMP = '2013-07-23T10:00:00-00:00'
RESOURCE_NAME = port.RESOURCE_NAME
COLLECTION_NAME = port.COLLECTION_NAME
RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        ADDRESS_PAIRS: {
            'allow_post': True, 'allow_put': True,
            'convert_to': converters.convert_none_to_empty_list,
            'convert_list_to':
            converters.convert_kvp_list_to_dict,
            'validate': {'type:allowed_address_pairs': None},
            'enforce_policy': True,
            'default': constants.ATTR_NOT_SPECIFIED,
            'is_visible': True},
    }
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = []
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
