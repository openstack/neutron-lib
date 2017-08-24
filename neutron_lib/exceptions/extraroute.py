# Copyright 2013, Nachi Ueno, NTT MCL, Inc.
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
from neutron_lib import exceptions


class InvalidRoutes(exceptions.InvalidInput):
    message = _("Invalid format for routes: %(routes)s, %(reason)s")


class RouterInterfaceInUseByRoute(exceptions.InUse):
    message = _("Router interface for subnet %(subnet_id)s on router "
                "%(router_id)s cannot be deleted, as it is required "
                "by one or more routes.")


class RoutesExhausted(exceptions.BadRequest):
    message = _("Unable to complete operation for %(router_id)s. "
                "The number of routes exceeds the maximum %(quota)s.")
