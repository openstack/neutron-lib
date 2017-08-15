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


class FlavorNotFound(exceptions.NotFound):
    message = _("Flavor %(flavor_id)s could not be found.")


class FlavorInUse(exceptions.InUse):
    message = _("Flavor %(flavor_id)s is used by some service instance.")


class ServiceProfileNotFound(exceptions.NotFound):
    message = _("Service Profile %(sp_id)s could not be found.")


class ServiceProfileInUse(exceptions.InUse):
    message = _("Service Profile %(sp_id)s is used by some service instance.")


class FlavorServiceProfileBindingExists(exceptions.Conflict):
    message = _("Service Profile %(sp_id)s is already associated "
                "with flavor %(fl_id)s.")


class FlavorServiceProfileBindingNotFound(exceptions.NotFound):
    message = _("Service Profile %(sp_id)s is not associated "
                "with flavor %(fl_id)s.")


class ServiceProfileDriverNotFound(exceptions.NotFound):
    message = _("Service Profile driver %(driver)s could not be found.")


class ServiceProfileEmpty(exceptions.InvalidInput):
    message = _("Service Profile needs either a driver or metainfo.")


class FlavorDisabled(exceptions.ServiceUnavailable):
    message = _("Flavor is not enabled.")


class ServiceProfileDisabled(exceptions.ServiceUnavailable):
    message = _("Service Profile is not enabled.")
