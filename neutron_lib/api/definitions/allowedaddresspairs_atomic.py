# Copyright 2023 EasyStack Limited. All rights reserved.
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

from neutron_lib.api.definitions import allowedaddresspairs
from neutron_lib.api.definitions import port


ALIAS = 'allowed-address-pairs-atomic'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Atomically add/remove allowed address pairs'
DESCRIPTION = ('Edit allowed address pairs of a port on server side by '
               'atomically adding/removing allowed address pairs')
UPDATED_TIMESTAMP = '2023-04-17T00:00:00+00:00'
RESOURCE_ATTRIBUTE_MAP = {
    port.COLLECTION_NAME: {}
}
SUB_RESOURCE_ATTRIBUTE_MAP = None
ACTION_MAP = {
    port.RESOURCE_NAME: {
        'add_allowed_address_pairs': 'PUT',
        'remove_allowed_address_pairs': 'PUT',
    }
}
REQUIRED_EXTENSIONS = [allowedaddresspairs.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
