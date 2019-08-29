# Copyright 2019 Ericsson Software Technology
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

from neutron_lib.api.definitions import extraroute
from neutron_lib.api.definitions import l3


ALIAS = 'extraroute-atomic'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Atomically add/remove extra routes'
DESCRIPTION = ('Edit extra routes of a router on server side by atomically '
               'adding/removing extra routes')
UPDATED_TIMESTAMP = '2019-07-10T00:00:00+00:00'
RESOURCE_ATTRIBUTE_MAP = {
    l3.ROUTERS: {}
}
SUB_RESOURCE_ATTRIBUTE_MAP = None
ACTION_MAP = l3.ACTION_MAP
ACTION_MAP[l3.ROUTER].update({
    'add_extraroutes': 'PUT',
    'remove_extraroutes': 'PUT',
})
REQUIRED_EXTENSIONS = [l3.ALIAS, extraroute.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
