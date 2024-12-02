# Copyright (c) 2024 Red Hat, Inc.
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
from neutron_lib import constants

ALIAS = 'qinq'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = "QinQ networks"
DESCRIPTION = (
    "Expose network 'qinq' attribute in the API. "
    "This allows to configure network to allow vlan in vlan "
    "configuration using 0x8a88 ethertype (QinQ)."
)
UPDATED_TIMESTAMP = "2024-12-02T10:00:00-00:00"
RESOURCE_NAME = network.RESOURCE_NAME
COLLECTION_NAME = network.COLLECTION_NAME
QINQ_FIELD = 'qinq'
RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        QINQ_FIELD: {
            'allow_post': True,
            'allow_put': False,
            'convert_to': converters.convert_to_boolean,
            'default': constants.ATTR_NOT_SPECIFIED,
            'is_visible': True,
            'is_filter': True,
            'validate': {'type:boolean': None}
            }
    },
}
SUB_RESOURCE_ATTRIBUTE_MAP = None
ACTION_MAP = {}
ACTION_STATUS = {}
REQUIRED_EXTENSIONS = []
OPTIONAL_EXTENSIONS = []
