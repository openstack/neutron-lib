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


class AddressGroupNotFound(exceptions.NotFound):
    message = _("Address group %(address_group_id)s could not be found.")


class AddressGroupInUse(exceptions.InUse):
    message = _("Address group %(address_group_id)s is in use on one or more "
                "security group rules.")


class AddressesNotFound(exceptions.NotFound):
    message = _("Addresses %(addresses)s not found in the address group "
                "%(address_group_id)s.")


class AddressesAlreadyExist(exceptions.BadRequest):
    message = _("Addresses %(addresses)s already exist in the "
                "address group %(address_group_id)s.")
