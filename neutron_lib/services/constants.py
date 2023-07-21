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

from neutron_lib.api.definitions import l3
from neutron_lib.api.definitions import local_ip
from neutron_lib.api.definitions import qos
from neutron_lib.plugins import constants as plugin_const


# Registered extension parent resource check mapping
# If we want to register some service plugin resources into policy and check
# the owner when operating their subresources. We can write here to use
# existing policy engine for parent resource owner check.
# Each entry here should be PARENT_RESOURCE_NAME: SERVICE_PLUGIN_NAME,
# PARENT_RESOURCE_NAME is usually from api definition.
# SERVICE_PLUGIN_NAME is the service plugin which introduced the resource and
# registered the service plugin name in neutron-lib.
EXT_PARENT_RESOURCE_MAPPING = {
    l3.FLOATINGIP: plugin_const.L3,
    l3.ROUTER: plugin_const.CONNTRACKHELPER,
    local_ip.RESOURCE_NAME: plugin_const.LOCAL_IP,
    qos.POLICY: plugin_const.QOS,
}
