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

from neutron_lib.api.definitions import l3


SERVICE_TYPE_ID = 'service_type_id'

ALIAS = 'router-service-type'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Router Service Type'
API_PREFIX = ''
DESCRIPTION = 'Provides router service type'
UPDATED_TIMESTAMP = '2013-01-29T00:00:00-00:00'
RESOURCE_ATTRIBUTE_MAP = {
    l3.ROUTERS: {
        SERVICE_TYPE_ID: {
            'allow_post': True,
            'allow_put': False,
            'validate': {
                'type:uuid_or_none': None
            },
            'default': None,
            'is_visible': True},
    }
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = [l3.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
