# Copyright 2026 Red Hat, LLC
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from neutron_lib.api.definitions import availability_zone as az
from neutron_lib.api.definitions import l3
from neutron_lib.api.definitions import router_availability_zone as router_az
from neutron_lib.types import (
    ActionMap,
    ResourceAttributeMap,
    SubResourceAttributeMap,
)

ALIAS = 'router-availability-zone-hints-writable'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Router Availability Zone Hints (writable)'
API_PREFIX = ''
DESCRIPTION = (
    "Provides a writable availability_zone_hints attribute for routers.")
UPDATED_TIMESTAMP = '2026-10-16T00:00:00-00:00'
RESOURCE_ATTRIBUTE_MAP: ResourceAttributeMap = {
    l3.ROUTERS: {
        az.AZ_HINTS: {
            'allow_post': True, 'allow_put': True, 'is_visible': True,
            'validate': {'type:availability_zone_hint_list': None},
            'default': [],
        },
    },
}
SUB_RESOURCE_ATTRIBUTE_MAP: SubResourceAttributeMap = {}
ACTION_MAP: ActionMap = {}
ACTION_STATUS = {}
REQUIRED_EXTENSIONS = [router_az.ALIAS]
OPTIONAL_EXTENSIONS = []
