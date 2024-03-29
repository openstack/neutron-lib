# Copyright (c) 2022 Inspur, Inc.
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
from neutron_lib.api.definitions import dvr
from neutron_lib.api.definitions import l3
from neutron_lib import constants


ALIAS = 'floating-ip-distributed'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Floating IP Distributed Extension'
DESCRIPTION = 'Add distributed attribute to Floating IP resource'
UPDATED_TIMESTAMP = '2022-08-30T10:00:00-00:00'
DISTRIBUTED = 'distributed'
RESOURCE_ATTRIBUTE_MAP = {
    l3.FLOATINGIPS: {
        DISTRIBUTED: {
            'allow_post': True,
            'allow_put': True,
            'convert_to': converters.convert_to_boolean_if_not_none,
            'default': constants.ATTR_NOT_SPECIFIED,
            'is_visible': True,
            'is_filter': True
        }
    }
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = [l3.ALIAS, dvr.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
