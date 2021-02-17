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

from neutron_lib.api.definitions import bfd_monitor
from neutron_lib.api.definitions import extraroute
from neutron_lib.api.definitions import l3


ALIAS = 'bfd-for-extraroutes'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'BFD monitors for extraroutes'
DESCRIPTION = ('Provides the possibility to associate a bfd_monitor to'
               'extra_routes')
UPDATED_TIMESTAMP = '2021-02-17T00:00:00+00:00'
RESOURCE_NAME = l3.ROUTER
COLLECTION_NAME = l3.ROUTERS
RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {}
}
SUB_RESOURCE_ATTRIBUTE_MAP = None
ACTION_MAP = {}
REQUIRED_EXTENSIONS = [l3.ALIAS, extraroute.ALIAS, bfd_monitor.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
