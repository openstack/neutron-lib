# Copyright 2013 OpenStack Foundation.
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

SERVICE_ATTR = 'service_type'
PLUGIN_ATTR = 'plugin'
DRIVER_ATTR = 'driver'

ALIAS = 'service-type'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Neutron Service Type Management'
API_PREFIX = ''
DESCRIPTION = ("API for retrieving service providers for "
               "Neutron advanced services")
UPDATED_TIMESTAMP = '2013-01-20T00:00:00-00:00'
RESOURCE_NAME = 'service_provider'
COLLECTION_NAME = RESOURCE_NAME + 's'
RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        SERVICE_ATTR: {
            'allow_post': False,
            'allow_put': False,
            'is_visible': True
        },
        'name': {
            'allow_post': False,
            'allow_put': False,
            'is_visible': True
        },
        'default': {
            'allow_post': False,
            'allow_put': False,
            'is_visible': True
        }
    }
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = []
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
