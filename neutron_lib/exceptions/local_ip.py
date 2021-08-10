# Copyright 2021 Huawei, Inc.
# All rights reserved.
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
from neutron_lib import exceptions


class LocalIPNotFound(exceptions.NotFound):
    message = _("Local IP %(id)s could not be found.")


class LocalIPInUse(exceptions.InUse):
    message = _("Local IP %(id)s is still associated with one or more ports.")


class LocalIPNoIP(exceptions.InvalidInput):
    message = _("Specified Port %(port_id)s has no fixed IPs configured.")


class LocalIPRequestedIPNotFound(exceptions.InvalidInput):
    message = _("Specified Port %(port_id)s does not have "
                "requested IP address: %(ip)s.")


class LocalIPNoRequestedIP(exceptions.InvalidInput):
    message = _("Specified Port %(port_id)s has several IPs, "
                "should specify exact IP address to use for Local IP.")


class LocalIPPortOrNetworkRequired(exceptions.InvalidInput):
    message = _("Either Port ID or Network ID must be specified "
                "for Local IP create.")


class LocalIPAssociationNotFound(exceptions.NotFound):
    message = _("Local IP %(local_ip_id)s association with port %(port_id)s "
                "could not be found.")
