# Copyright (c) 2016 IBM
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

import functools
import re

from keystoneauth1 import exceptions as ks_exc
from keystoneauth1 import loading as keystone
from oslo_log import log as logging
from oslo_utils import versionutils
from six.moves.urllib.parse import urlencode

from neutron_lib._i18n import _
from neutron_lib.exceptions import placement as n_exc


LOG = logging.getLogger(__name__)

API_VERSION_REQUEST_HEADER = 'OpenStack-API-Version'
PLACEMENT_API_WITH_MEMBER_OF = 'placement 1.3'
PLACEMENT_API_WITH_NESTED_RESOURCES = 'placement 1.14'
PLACEMENT_API_LATEST_SUPPORTED = PLACEMENT_API_WITH_NESTED_RESOURCES


def _check_placement_api_available(f):
    """Check if the placement API is available.

    :param f: Function to execute.
    :returns: The returned value of the function f.
    :raises PlacementEndpointNotFound: If the placement API endpoint configured
                                       is not found.
    """
    @functools.wraps(f)
    def wrapper(self, *a, **k):
        try:
            if not self._client:
                self._client = self._create_client()
            return f(self, *a, **k)
        except ks_exc.EndpointNotFound:
            LOG.warning('Please enable the placement service.')
        except ks_exc.MissingAuthPlugin:
            LOG.warning('No authentication information found for placement '
                        'API. Please enable the placement service.')
        except ks_exc.Unauthorized:
            LOG.warning('Placement service credentials do not work. '
                        'Please enable the placement service.')
        except ks_exc.DiscoveryFailure:
            LOG.warning('Discovering suitable URL for placement API failed.')
        except ks_exc.ConnectFailure:
            LOG.warning('Placement API service is not responding.')
    return wrapper


def _get_version(openstack_api_version):
    match = re.search(r"placement (?P<api_version>\d+\.\d+)",
                      openstack_api_version)
    return versionutils.convert_version_to_tuple(match.group('api_version'))


class PlacementAPIClient(object):
    """Client class for placement ReST API."""

    def __init__(self, conf,
                 openstack_api_version=PLACEMENT_API_LATEST_SUPPORTED):
        self._openstack_api_version = openstack_api_version
        self._target_version = _get_version(openstack_api_version)
        self._conf = conf
        self._ks_filter = {'service_type': 'placement',
                           'region_name': self._conf.placement.region_name}
        self._api_version_header = {API_VERSION_REQUEST_HEADER:
                                    self._openstack_api_version}
        self._client = None

    def _create_client(self):
        """Create the HTTP session accessing the placement service."""
        # Flush _resource_providers and aggregates so we start from a
        # clean slate.
        self._resource_providers = {}
        self._provider_aggregate_map = {}
        auth_plugin = keystone.load_auth_from_conf_options(
            self._conf, 'placement')
        return keystone.load_session_from_conf_options(
            self._conf, 'placement', auth=auth_plugin,
            additional_headers={'accept': 'application/json'})

    def _extend_header_with_api_version(self, **kwargs):
        headers = kwargs.get('headers', {})
        if API_VERSION_REQUEST_HEADER not in headers:
            if 'headers' not in kwargs:
                kwargs['headers'] = self._api_version_header
            else:
                kwargs['headers'].update(self._api_version_header)
        return kwargs

    def _get(self, url, **kwargs):
        kwargs = self._extend_header_with_api_version(**kwargs)
        return self._client.get(url, endpoint_filter=self._ks_filter,
                                **kwargs)

    def _post(self, url, data, **kwargs):
        kwargs = self._extend_header_with_api_version(**kwargs)
        return self._client.post(url, json=data,
                                 endpoint_filter=self._ks_filter, **kwargs)

    def _put(self, url, data, **kwargs):
        kwargs = self._extend_header_with_api_version(**kwargs)
        return self._client.put(url, json=data,
                                endpoint_filter=self._ks_filter, **kwargs)

    def _delete(self, url, **kwargs):
        kwargs = self._extend_header_with_api_version(**kwargs)
        return self._client.delete(url, endpoint_filter=self._ks_filter,
                                   **kwargs)

    @_check_placement_api_available
    def create_resource_provider(self, resource_provider):
        """Create a resource provider.

        :param resource_provider: The resource provider. A dict with the name
                                  (required) and the uuid (required).
        """
        url = '/resource_providers'
        self._post(url, resource_provider)

    @_check_placement_api_available
    def delete_resource_provider(self, resource_provider_uuid):
        """Delete a resource provider.

        :param resource_provider_uuid: UUID of the resource provider.
        """
        url = '/resource_providers/%s' % resource_provider_uuid
        self._delete(url)

    @_check_placement_api_available
    def get_resource_provider(self, resource_provider_uuid):
        """Get resource provider by UUID.

        :param resource_provider_uuid: UUID of the resource provider.
        :raises PlacementResourceProviderNotFound: If the resource provider is
                                                   not present.
        :returns: The Resource Provider matching the UUID.
        :raises PlacementResourceProviderNotFound: For failure to find resource
        """
        url = '/resource_providers/%s' % resource_provider_uuid
        try:
            return self._get(url).json()
        except ks_exc.NotFound:
            raise n_exc.PlacementResourceProviderNotFound(
                resource_provider=resource_provider_uuid)

    @_check_placement_api_available
    def list_resource_providers(self, name=None, member_of=None,
                                resources=None, in_tree=None, uuid=None):
        """Get a list of resource providers.

        :param name: Name of the resource providers.
        :param member_of: List of aggregate UUID to get those resource
                          providers that are associated with.
                          NOTE: placement 1.3 needed.
        :param resources: Dictionary of resource classes and requested values.
        :param in_tree: UUID of a resource provider that the caller wants to
                        limit the returned providers to those within its
                        'provider tree'. The returned list will contain only
                        resource providers with the root_provider_id of the
                        resource provider with UUID == tree_uuid.
                        NOTE: placement 1.14 needed.
        :param uuid: UUID of the resource provider.
        :returns: A list of Resource Provider matching the filters.
        :raises PlacementAPIVersionIncorrect: If placement API target version
                                              is too low
        """
        url = '/resource_providers'
        filters = {}
        if name:
            filters['name'] = name
        if member_of:
            needed_version = _get_version(PLACEMENT_API_WITH_MEMBER_OF)
            if self._target_version < needed_version:
                raise n_exc.PlacementAPIVersionIncorrect(
                    current_version=self._target_version,
                    needed_version=needed_version)
            filters['member_of'] = member_of
        if resources:
            filters['resources'] = resources
        if in_tree:
            needed_version = _get_version(
                PLACEMENT_API_WITH_NESTED_RESOURCES)
            if self._target_version < needed_version:
                raise n_exc.PlacementAPIVersionIncorrect(
                    current_version=self._target_version,
                    needed_version=needed_version)
            filters['in_tree'] = in_tree
        if uuid:
            filters['uuid'] = uuid
        url = '%s?%s' % (url, urlencode(filters))
        return self._get(url).json()

    @_check_placement_api_available
    def update_resource_provider_inventories(
            self, resource_provider_uuid, inventories,
            resource_provider_generation):
        """Update resource provider inventories.

        :param resource_provider_uuid: UUID of the resource provider.
        :param inventories: The inventories. A dict in the format (see:
                            Placement API ref: https://goo.gl/F22mtk)
                            {resource_class(required):
                            {allocation_ratio(required):
                            total(required):
                            max_unit(required):
                            min_unit(required):
                            reserved(required):
                            step_size(required):
                            }}
        :param resource_provider_generation: The generation of the resource
                                             provider.
        :raises PlacementResourceProviderNotFound: if the resource provider
                                                   is not found.
        :raises PlacementResourceProviderGenerationConflict: if the generation
                                                             of the resource
                                                             provider does not
                                                             match with the
                                                             server side.
        """
        url = '/resource_providers/%s/inventories' % resource_provider_uuid
        body = {
            'resource_provider_generation': resource_provider_generation,
            'inventories': inventories
        }
        try:
            return self._put(url, body).json()
        except ks_exc.NotFound:
            raise n_exc.PlacementResourceProviderNotFound(
                resource_provider=resource_provider_uuid)
        except ks_exc.Conflict:
            raise n_exc.PlacementResourceProviderGenerationConflict(
                resource_provider=resource_provider_uuid,
                generation=resource_provider_generation)

    @_check_placement_api_available
    def delete_resource_provider_inventories(self, resource_provider_uuid):
        """Delete all inventory records for the resource provider.

        :param resource_provider_uuid: UUID of the resource provider.
        :raises PlacementResourceProviderNotFound: If the resource provider
                                                   is not found.
        """
        url = '/resource_providers/%s/inventories' % (
            resource_provider_uuid)
        try:
            self._delete(url)
        except ks_exc.NotFound as e:
            if "No resource provider with uuid" in e.details:
                raise n_exc.PlacementResourceProviderNotFound(
                    resource_provider=resource_provider_uuid)
            else:
                raise

    @_check_placement_api_available
    def delete_resource_provider_inventory(self, resource_provider_uuid,
                                           resource_class):
        """Delete inventory of the resource class for a resource provider.

        :param resource_provider_uuid: UUID of the resource provider.
        :param resource_class: The name of the resource class
        """
        url = '/resource_providers/%s/inventories/%s' % (
            resource_provider_uuid, resource_class)
        try:
            self._delete(url)
        except ks_exc.NotFound as e:
            if "No resource provider with uuid" in e.details:
                raise n_exc.PlacementResourceProviderNotFound(
                    resource_provider=resource_provider_uuid)
            elif "No inventory of class" in e.details:
                raise n_exc.PlacementInventoryNotFound(
                    resource_provider=resource_provider_uuid,
                    resource_class=resource_class)
            else:
                raise

    @_check_placement_api_available
    def get_inventory(self, resource_provider_uuid, resource_class):
        """Get resource provider inventory.

        :param resource_provider_uuid: UUID of the resource provider.
        :param resource_class: Resource class name of the inventory to be
                               returned.
        :raises PlacementInventoryNotFound: For failure to find inventory
                                            for a resource provider.
        """
        url = '/resource_providers/%s/inventories/%s' % (
            resource_provider_uuid, resource_class)
        try:
            return self._get(url).json()
        except ks_exc.NotFound as e:
            if "No resource provider with uuid" in e.details:
                raise n_exc.PlacementResourceProviderNotFound(
                    resource_provider=resource_provider_uuid)
            elif _("No inventory of class") in e.details:
                raise n_exc.PlacementInventoryNotFound(
                    resource_provider=resource_provider_uuid,
                    resource_class=resource_class)
            else:
                raise

    @_check_placement_api_available
    def update_resource_provider_inventory(
            self, resource_provider_uuid, inventory, resource_class,
            resource_provider_generation):
        """Update resource provider inventory.

        :param resource_provider_uuid: UUID of the resource provider.
        :param inventory: The inventory to be updated for the resource class.
        :param resource_class: The name of the resource class.
        :param resource_provider_generation: The generation of the resource
                                             provider.
        :raises PlacementResourceNotFound: If the resource provider or the
                                           resource class is not found.
        :raises PlacementInventoryUpdateConflict: If the resource provider
                                                  generation does not match
                                                  with the server side.
        """
        url = '/resource_providers/%s/inventories/%s' % (
            resource_provider_uuid, resource_class)
        inventory['resource_provider_generation'] = \
            resource_provider_generation
        try:
            return self._put(url, inventory).json()
        except ks_exc.NotFound as e:
            raise n_exc.PlacementResourceNotFound(url=e.url)
        except ks_exc.Conflict:
            raise n_exc.PlacementInventoryUpdateConflict(
                resource_provider=resource_provider_uuid,
                resource_class=resource_class)

    @_check_placement_api_available
    def associate_aggregates(self, resource_provider_uuid, aggregates):
        """Associate a list of aggregates with a resource provider.

        :param resource_provider_uuid: UUID of the resource provider.
        :param aggregates: aggregates to be associated to the resource
                           provider.
        """
        url = '/resource_providers/%s/aggregates' % resource_provider_uuid
        self._put(url, aggregates)

    @_check_placement_api_available
    def list_aggregates(self, resource_provider_uuid):
        """List resource provider aggregates.

        :param resource_provider_uuid: UUID of the resource provider.
        :raises PlacementAggregateNotFound: For failure to the aggregates of
                                            a resource provider.
        """
        url = '/resource_providers/%s/aggregates' % resource_provider_uuid
        try:
            return self._get(url).json()
        except ks_exc.NotFound:
            raise n_exc.PlacementAggregateNotFound(
                resource_provider=resource_provider_uuid)

    @_check_placement_api_available
    def list_traits(self):
        """List all traits."""
        url = '/traits'
        return self._get(url).json()

    @_check_placement_api_available
    def get_trait(self, name):
        """Check if a given trait exists

        :param name: name of the trait to check.
        :raises PlacementTraitNotFound: If the trait name not found.
        """
        url = '/traits/%s' % name
        try:
            return self._get(url)
        except ks_exc.NotFound:
            raise n_exc.PlacementTraitNotFound(trait=name)

    @_check_placement_api_available
    def update_trait(self, name):
        """Insert a single custom trait.

        :param name: name of the trait to create.
        """
        url = '/traits/%s' % (name)
        return self._put(url, None)

    @_check_placement_api_available
    def delete_trait(self, name):
        """Delete the specified trait.

        :param name: the name of the trait to be deleted.
        """
        url = '/traits/%s' % (name)
        try:
            self._delete(url)
        except ks_exc.NotFound:
            raise n_exc.PlacementTraitNotFound(trait=name)

    @_check_placement_api_available
    def update_resource_provider_traits(
            self, resource_provider_uuid, traits,
            resource_provider_generation):
        """Update resource provider traits

        :param resource_provider_uuid: UUID of the resource provider for which
                                       to set the traits
        :param traits: a list of traits.
        :param resource_provider_generation: The generation of the resource
                                             provider.
        :raises PlacementResourceProviderNotFound: If the resource provider
                                                   is not found.
        :raises PlacementTraitNotFound: If any of the specified traits are not
                                        valid.
        """
        url = '/resource_providers/%s/traits' % (resource_provider_uuid)
        body = {
            'resource_provider_generation': resource_provider_generation,
            'traits': traits
        }
        try:
            return self._put(url, body).json()
        except ks_exc.NotFound:
            raise n_exc.PlacementResourceProviderNotFound(
                resource_provider=resource_provider_uuid)
        except ks_exc.BadRequest:
            raise n_exc.PlacementTraitNotFound(trait=traits)

    @_check_placement_api_available
    def list_resource_provider_traits(self, resource_provider_uuid):
        """List all traits associated with a resource provider

        :param resource_provider_uuid: UUID of the resource provider for which
                                       the traits will be listed
        :raises PlacementResourceProviderNotFound: If the resource provider
                                                   is not found.
        """
        url = '/resource_providers/%s/traits' % (resource_provider_uuid)
        try:
            return self._get(url).json()
        except ks_exc.NotFound:
            raise n_exc.PlacementResourceProviderNotFound(
                resource_provider=resource_provider_uuid)

    @_check_placement_api_available
    def delete_resource_provider_traits(self, resource_provider_uuid):
        """Delete resource provider traits.

        :param resource_provider_uuid: The UUID of the resource provider for
                                       which to delete all the traits.
        """
        url = '/resource_providers/%s/traits' % (resource_provider_uuid)
        try:
            self._delete(url)
        except ks_exc.NotFound:
            raise n_exc.PlacementResourceProviderNotFound(
                resource_provider=resource_provider_uuid)

    @_check_placement_api_available
    def list_resource_classes(self):
        """List resource classes"""
        url = '/resource_classes'
        return self._get(url).json()

    @_check_placement_api_available
    def get_resource_class(self, name):
        """Show resource class.

        :param name: The name of the resource class to show
        """
        url = '/resource_classes/%s' % (name)
        try:
            return self._get(url).json()
        except ks_exc.NotFound:
            raise n_exc.PlacementResourceClassNotFound(resource_class=name)

    @_check_placement_api_available
    def create_resource_class(self, name):
        """Create a custom resource class

        :param name: the name of the resource class
        """
        url = '/resource_classes'
        body = {'name': name}
        self._post(url, body)

    @_check_placement_api_available
    def update_resource_class(self, name):
        """Create or validate the existence of the resource custom class.

        :param name: the name of the resource class to be updated or validated
        """
        url = '/resource_classes/%s' % name
        self._put(url)

    @_check_placement_api_available
    def delete_resource_class(self, name):
        """Delete a custom resource class.

        :param name: The name of the resource class to be deleted.
        """
        url = '/resource_classes/%s' % (name)
        try:
            self._delete(url)
        except ks_exc.NotFound:
            raise n_exc.PlacementResourceClassNotFound(resource_class=name)
