# Copyright (C) 2014 eNovance SAS <licensing@enovance.com>
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

from neutron_lib._i18n import _
from neutron_lib import exceptions


class MaxVRIDAllocationTriesReached(exceptions.NeutronException):
    message = _("Failed to allocate a VRID in the network %(network_id)s "
                "for the router %(router_id)s after %(max_tries)s tries.")


class NoVRIDAvailable(exceptions.Conflict):
    message = _("No more Virtual Router Identifier (VRID) available when "
                "creating router %(router_id)s. The limit of number "
                "of HA Routers per tenant is 254.")


class HANetworkConcurrentDeletion(exceptions.Conflict):
    message = _("Network for tenant %(tenant_id)s concurrently deleted.")


class HANetworkCIDRNotValid(exceptions.NeutronException):
    message = _("The HA Network CIDR specified in the configuration file "
                "isn't valid; %(cidr)s.")


class HAMaximumAgentsNumberNotValid(exceptions.NeutronException):
    message = _("max_l3_agents_per_router %(max_agents)s config parameter "
                "is not valid as it cannot be negative. It must be 1 or "
                "greater. Alternatively, it can be 0 to mean unlimited.")
