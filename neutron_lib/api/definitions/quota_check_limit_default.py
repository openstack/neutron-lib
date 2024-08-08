# Copyright 2024 Red Hat, Inc.
#
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

from neutron_lib.api.definitions import quota_check_limit

ALIAS = 'quota-check-limit-default'
IS_SHIM_EXTENSION = True
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Quota engine limit check by default'
DESCRIPTION = ('By default, the Neutron quota engine checks the resource '
               'usage before applying a new quota limit')
UPDATED_TIMESTAMP = '2024-08-21T16:00:00-00:00'
RESOURCE_ATTRIBUTE_MAP = {}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = [quota_check_limit.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
