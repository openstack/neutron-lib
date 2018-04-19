# Copyright 2018 Orange
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

from neutron_lib.api.definitions import bgpvpn_routes_control

ALIAS = 'standard-attr-bgpvpn-port-association'
IS_SHIM_EXTENSION = True
IS_STANDARD_ATTR_EXTENSION = True
NAME = 'BGPVPN Port Association Standard Attributes'
DESCRIPTION = 'Add standard attributes to BGPVPN Port Association resources'
UPDATED_TIMESTAMP = '2018-04-19T10:00:00-00:00'
RESOURCE_ATTRIBUTE_MAP = {}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = [bgpvpn_routes_control.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
