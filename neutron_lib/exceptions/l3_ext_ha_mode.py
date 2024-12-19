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

from oslo_log import log as logging

from neutron_lib._i18n import _
from neutron_lib import exceptions

LOG = logging.getLogger(__name__)


class MaxVRIDAllocationTriesReached(exceptions.NeutronException):
    message = _("Failed to allocate a VRID in the network %(network_id)s "
                "for the router %(router_id)s after %(max_tries)s tries.")


class NoVRIDAvailable(exceptions.Conflict):
    message = _("No more Virtual Router Identifier (VRID) available when "
                "creating router %(router_id)s. The limit of number "
                "of HA Routers per tenant is 254.")


class HANetworkConcurrentDeletion(exceptions.Conflict):
    message = _("Network for project %(project_id)s concurrently deleted.")

    # NOTE(haleyb): remove fall-back and warning in E+2 release, or when
    # all callers have been changed to use project_id.
    def __init__(self, **kwargs):
        project_id = kwargs.get('project_id')
        tenant_id = kwargs.get('tenant_id')
        project_id = project_id or tenant_id
        if tenant_id:
            LOG.warning('Keyword tenant_id has been deprecated, use '
                        'project_id instead')
        kwargs.setdefault('project_id', project_id)
        super().__init__(**kwargs)


class HANetworkCIDRNotValid(exceptions.NeutronException):
    message = _("The HA Network CIDR specified in the configuration file "
                "isn't valid; %(cidr)s.")


class HAMaximumAgentsNumberNotValid(exceptions.NeutronException):
    message = _("max_l3_agents_per_router %(max_agents)s config parameter "
                "is not valid as it cannot be negative. It must be 1 or "
                "greater. Alternatively, it can be 0 to mean unlimited.")


class DuplicatedHANetwork(exceptions.Conflict):
    message = _('Project %(project_id)s already has a HA network.')
