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


class PlacementEndpointNotFound(exceptions.NotFound):
    message = _("Placement API endpoint not found.")


class PlacementResourceNotFound(exceptions.NotFound):
    message = _("Placement resource not found on url: %(url)s.")


class PlacementResourceProviderNotFound(exceptions.NotFound):
    message = _("Placement resource provider not found %(resource_provider)s.")


class PlacementResourceProviderGenerationConflict(exceptions.Conflict):
    message = _("Placement resource provider generation does not match with "
                "the server side for resource provider: "
                "%(resource_provider)s with generation %(generation)s.")


class PlacementInventoryNotFound(exceptions.NotFound):
    message = _("Placement inventory not found for resource provider "
                "%(resource_provider)s, resource class %(resource_class)s.")


class PlacementInventoryUpdateConflict(exceptions.Conflict):
    message = _("Placement inventory update conflict for resource provider "
                "%(resource_provider)s, resource class %(resource_class)s.")


class PlacementAggregateNotFound(exceptions.NotFound):
    message = _("Aggregate not found for resource provider "
                "%(resource_provider)s.")


class PlacementTraitNotFound(exceptions.NotFound):
    message = _("Placement trait not found %(trait)s.")


class PlacementResourceClassNotFound(exceptions.NotFound):
    message = _("Placement resource class not found %(resource_class)s")


class PlacementAPIVersionIncorrect(exceptions.NotFound):
    message = _("Placement API version %(current_version)s, do not meet the "
                "needed version %(needed_version)s.")


class PlacementResourceProviderNameNotUnique(exceptions.Conflict):
    message = _("Another resource provider exists with the provided name: "
                "%(name)s.")


class PlacementClientError(exceptions.NeutronException):
    message = _("Placement Client Error (4xx): %(msg)s")


class UnknownResourceProvider(exceptions.BadRequest):
    """Resource provider not known by neutron backends."""
    message = _("No such resource provider known by Neutron: %(rsc_provider)s")


class AmbiguousResponsibilityForResourceProvider(exceptions.NeutronException):
    """Not clear who's responsible for resource provider."""
    message = _("Expected one driver to be responsible for resource provider "
                "%(rsc_provider)s, but got many: %(drivers)s")


class PlacementAllocationGenerationConflict(exceptions.Conflict):
    message = _("Resource allocation has been changed for consumer "
                "%(consumer)s in Placement while Neutron tried to update it.")


class PlacementAllocationRemoved(exceptions.BadRequest):
    message = _("Resource allocation is deleted for consumer %(consumer)s")


class PlacementAllocationRpNotExists(exceptions.BadRequest):
    message = _("Resource provider %(resource_provider)s for %(consumer)s "
                "does not exist")
