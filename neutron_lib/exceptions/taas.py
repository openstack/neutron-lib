# Copyright 2011 VMware, Inc
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


from neutron_lib._i18n import _
from neutron_lib import exceptions as qexception


class TapServiceNotFound(qexception.NotFound):
    message = _("Tap Service  %(tap_id)s does not exist")


class TapFlowNotFound(qexception.NotFound):
    message = _("Tap Flow  %(flow_id)s does not exist")


class InvalidDestinationPort(qexception.NotFound):
    message = _("Destination Port %(port)s does not exist")


class InvalidSourcePort(qexception.NotFound):
    message = _("Source Port  %(port)s does not exist")


class PortDoesNotBelongToTenant(qexception.NotAuthorized):
    message = _("The specified port does not belong to the tenant")


class TapServiceNotBelongToTenant(qexception.NotAuthorized):
    message = _("Specified Tap Service does not belong to the tenant")


class TapServiceLimitReached(qexception.OverQuota):
    message = _("Reached the maximum quota for Tap Services")


class TapMirrorNotFound(qexception.NotFound):
    message = _("Tap Mirror %(mirror_id)s does not exist")


class TapMirrorTunnelConflict(qexception.Conflict):
    message = _("Tap Mirror with tunnel_id %(tunnel_id)s already exists")
