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
import time
from urllib import parse
import uuid as uuid_lib

import requests

from keystoneauth1 import exceptions as ks_exc
from keystoneauth1 import loading as keystone
from oslo_log import log as logging
from oslo_serialization import jsonutils
from oslo_utils import versionutils

from neutron_lib._i18n import _
from neutron_lib.exceptions import placement as n_exc


LOG = logging.getLogger(__name__)

API_VERSION_REQUEST_HEADER = 'OpenStack-API-Version'
PLACEMENT_API_WITH_MEMBER_OF = 'placement 1.3'
PLACEMENT_API_WITH_NESTED_RESOURCES = 'placement 1.14'
PLACEMENT_API_RETURN_PROVIDER_BODY = 'placement 1.20'
PLACEMENT_API_ERROR_CODE = 'placement 1.23'
PLACEMENT_API_CONSUMER_GENERATION = 'placement 1.28'
PLACEMENT_API_UPDATE_REPARENT = 'placement 1.37'
PLACEMENT_API_LATEST_SUPPORTED = PLACEMENT_API_UPDATE_REPARENT
GENERATION_CONFLICT_RETRIES = 10


def _check_placement_api_available(f):
    """Check if the placement API is available.

    :param f: Function to execute.
    :returns: The returned value of the function f.
    """
    @functools.wraps(f)
    def wrapper(self, *a, **k):
        try:
            if not self._client:
                self._client = self._create_client()
            return f(self, *a, **k)
        except ks_exc.http.HttpError as exc:
            if 400 <= exc.http_status <= 499:
                # NOTE(bence romsics): Placement has inconsistently formatted
                # error messages. Some error response bodies are JSON
                # formatted, seemingly machine readible objects. While others
                # are free format text. We have to keep the whole thing
                # to avoid losing information.
                raise n_exc.PlacementClientError(
                    msg=exc.response.text.replace('\n', ' '))
            raise
    return wrapper


def _get_version(openstack_api_version):
    match = re.search(r"placement (?P<api_version>\d+\.\d+)",
                      openstack_api_version)
    return versionutils.convert_version_to_tuple(match.group('api_version'))


class UUIDEncoder(jsonutils.JSONEncoder):
    def default(self, o):
        if isinstance(o, uuid_lib.UUID):
            return str(o)
        return super().default(o)


class NoAuthClient:
    """Placement NoAuthClient for fullstack testing"""

    def __init__(self, url):
        self.url = url
        # TODO(lajoskatona): use perhaps http_connect_timeout from
        # keystone_authtoken group
        self.timeout = 5
        self.retries = 2

    def request(self, url, method, body=None, headers=None, **kwargs):
        headers = headers or {}
        headers.setdefault('Accept', 'application/json')

        # Note(lajoskatona): placement report plugin fills uuid fields with
        # UUID objects, and that is good for keystone, but requests goes mad
        # with that if we use json=body as it can't serialize UUID.
        # To make things worse if we give a serialized json, it will do the
        # jsonification again, so better to create the json here and give it
        # to requests with the data parameter.
        body = jsonutils.dumps(body, cls=UUIDEncoder)
        for i in range(self.retries):
            try:
                resp = requests.request(
                    method,
                    url,
                    data=body,
                    headers=headers,
                    verify=False,
                    timeout=self.timeout,
                    **kwargs)
                return resp
            except requests.Timeout:
                LOG.exception('requests Timeout, let\'s retry it...')
            except requests.ConnectionError:
                LOG.exception('Connection Error appeared')
            except requests.RequestException:
                LOG.exception('Some really weird thing happened, let\'s '
                              'retry it')
            time.sleep(self.timeout)
        # Note(lajoskatona): requests raise ConnectionError, but
        # PlacementReportPlugin expects keystonauth1 HttpError.
        raise ks_exc.HttpError

    def get(self, url, endpoint_filter, **kwargs):
        return self.request('{}{}'.format(self.url, url), 'GET', **kwargs)

    def post(self, url, json, endpoint_filter, **kwargs):
        return self.request('{}{}'.format(self.url, url), 'POST', body=json,
                            **kwargs)

    def put(self, url, json, endpoint_filter, **kwargs):
        resp = self.request('{}{}'.format(self.url, url), 'PUT', body=json,
                            **kwargs)
        return resp

    def delete(self, url, endpoint_filter, **kwargs):
        return self.request('{}{}'.format(self.url, url), 'DELETE', **kwargs)


class PlacementAPIClient:
    """Client class for placement ReST API."""

    def __init__(self, conf,
                 openstack_api_version=PLACEMENT_API_LATEST_SUPPORTED):
        self._openstack_api_version = openstack_api_version
        self._target_version = _get_version(openstack_api_version)
        self._conf = conf
        self._ks_filter = {'service_type': 'placement',
                           'region_name': self._conf.placement.region_name,
                           'interface': self._conf.placement.endpoint_type}
        self._api_version_header = {API_VERSION_REQUEST_HEADER:
                                    self._openstack_api_version}
        self._client = None

    def _create_client(self):
        """Create the HTTP session accessing the placement service."""
        # Flush _resource_providers and aggregates so we start from a
        # clean slate.
        self._resource_providers = {}
        self._provider_aggregate_map = {}
        # TODO(lajoskatona): perhaps not the best to override config options,
        # actually the abused keystoneauth1 options are:
        # auth_type (used for deciding for NoAuthClient) and auth_section
        # (used for communicating the url for the NoAuthClient)
        if self._conf.placement.auth_type == 'noauth':
            return NoAuthClient(self._conf.placement.auth_section)
        else:
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

    def _put_with_retry_for_generation_conflict(
            self, url, body,
            resource_provider_uuid,
            resource_provider_generation=None):

        if resource_provider_generation is None:
            # If the client's user did not supply a generation to us we dare to
            # retry without handing the control back to our caller.
            max_tries = GENERATION_CONFLICT_RETRIES
        else:
            # If the client's user supplied a generation to us we don't dare to
            # retry on her behalf since we don't know her intention.
            max_tries = 1

        body['resource_provider_generation'] = resource_provider_generation

        for i in range(max_tries):
            if resource_provider_generation is None:
                # In the bodies of
                # PUT /resource_providers/{uuid}/traits
                # PUT /resource_providers/{uuid}/inventories
                # PUT /resource_providers/{uuid}/inventories/{resource_class}
                # resource_provider_generation happens to be at the same place.
                body['resource_provider_generation'] = \
                    self.get_resource_provider(
                        resource_provider_uuid=resource_provider_uuid)[
                            'generation']
            try:
                return self._put(url, body).json()
            except ks_exc.Conflict as e:
                if e.response.json()[
                        'errors'][0]['code'] == 'placement.concurrent_update':
                    continue
                raise

        raise n_exc.PlacementResourceProviderGenerationConflict(
            resource_provider=resource_provider_uuid,
            generation=body['resource_provider_generation'])

    def _delete(self, url, **kwargs):
        kwargs = self._extend_header_with_api_version(**kwargs)
        return self._client.delete(url, endpoint_filter=self._ks_filter,
                                   **kwargs)

    @_check_placement_api_available
    def create_resource_provider(self, resource_provider):
        """Create a resource provider.

        :param resource_provider: The resource provider. A dict with
                                  the uuid (required),
                                  the name (required) and
                                  the parent_provider_uuid (optional).
        :returns: The resource provider created.
        """
        url = '/resource_providers'
        rsp = self._post(url, resource_provider)
        if (self._target_version <
                _get_version(PLACEMENT_API_RETURN_PROVIDER_BODY)):
            return
        else:
            return rsp.json()

    @_check_placement_api_available
    def update_resource_provider(self, resource_provider):
        """Update the resource provider identified by uuid.

        :param resource_provider: The resource provider. A dict with
                                  the uuid (required),
                                  the name (required) and
                                  the parent_provider_uuid (optional).
        :raises PlacementResourceProviderNotFound: No such resource provider.
        :raises PlacementResourceProviderNameNotUnique: Conflict with another
                                                        resource provider with
                                                        the same name.
        :returns: The updated resource provider.
        """
        # pylint: disable=raise-missing-from
        url = '/resource_providers/%s' % resource_provider['uuid']
        # update does not tolerate if the uuid is repeated in the body
        update_body = resource_provider.copy()
        update_body.pop('uuid')
        try:
            return self._put(url, update_body).json()
        except ks_exc.NotFound:
            raise n_exc.PlacementResourceProviderNotFound(
                resource_provider=resource_provider['uuid'])
        except ks_exc.Conflict:
            raise n_exc.PlacementResourceProviderNameNotUnique(
                name=resource_provider['name'])

    @_check_placement_api_available
    def ensure_resource_provider(self, resource_provider):
        """Ensure a resource provider exists by updating or creating it.

        :param resource_provider: The resource provider. A dict with
                                  the uuid (required),
                                  the name (required) and
                                  the parent_provider_uuid (optional).
        :returns: The Resource Provider updated or created.

        Beware, this is not an atomic operation of the API.
        """
        try:
            return self.update_resource_provider(
                resource_provider=resource_provider)
        except n_exc.PlacementResourceProviderNotFound:
            return self.create_resource_provider(resource_provider)

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
        :raises PlacementResourceProviderNotFound: For failure to find resource
        :returns: The Resource Provider matching the UUID.
        """
        # pylint: disable=raise-missing-from
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
        :raises PlacementAPIVersionIncorrect: If placement API target version
                                              is too low
        :returns: A list of Resource Provider matching the filters.
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
        url = '{}?{}'.format(url, parse.urlencode(filters))
        return self._get(url).json()

    @_check_placement_api_available
    def update_resource_provider_inventories(
            self, resource_provider_uuid, inventories,
            resource_provider_generation=None):
        """Replaces the set of inventory records for a resource provider.

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
                                             provider. Optional.
        :raises PlacementResourceProviderNotFound: if the resource provider
                                                   is not found.
        :raises PlacementResourceProviderGenerationConflict: if the generation
                                                             of the resource
                                                             provider does not
                                                             match with the
                                                             server side.
        :returns: The updated set of inventory records.
        """
        # pylint: disable=raise-missing-from
        url = '/resource_providers/%s/inventories' % resource_provider_uuid
        body = {
            'resource_provider_generation': resource_provider_generation,
            'inventories': inventories
        }

        try:
            return self._put_with_retry_for_generation_conflict(
                url, body, resource_provider_uuid,
                resource_provider_generation)
        except ks_exc.NotFound:
            raise n_exc.PlacementResourceProviderNotFound(
                resource_provider=resource_provider_uuid)

    @_check_placement_api_available
    def delete_resource_provider_inventories(self, resource_provider_uuid):
        """Delete all inventory records for the resource provider.

        :param resource_provider_uuid: UUID of the resource provider.
        :raises PlacementResourceProviderNotFound: If the resource provider
                                                   is not found.
        :returns: None.
        """
        url = '/resource_providers/%s/inventories' % (
            resource_provider_uuid)
        try:
            self._delete(url)
        except ks_exc.NotFound as e:
            if "No resource provider with uuid" in e.details:
                raise n_exc.PlacementResourceProviderNotFound(
                    resource_provider=resource_provider_uuid)
            raise

    @_check_placement_api_available
    def delete_resource_provider_inventory(self, resource_provider_uuid,
                                           resource_class):
        """Delete inventory of the resource class for a resource provider.

        :param resource_provider_uuid: UUID of the resource provider.
        :param resource_class: The name of the resource class
        :raises PlacementResourceProviderNotFound: If the resource provider
                                                   is not found.
        :raises PlacementInventoryNotFound: No inventory of class.
        :returns: None.
        """
        url = '/resource_providers/{}/inventories/{}'.format(
            resource_provider_uuid, resource_class)
        try:
            self._delete(url)
        except ks_exc.NotFound as e:
            if "No resource provider with uuid" in e.details:
                raise n_exc.PlacementResourceProviderNotFound(
                    resource_provider=resource_provider_uuid)
            if "No inventory of class" in e.details:
                raise n_exc.PlacementInventoryNotFound(
                    resource_provider=resource_provider_uuid,
                    resource_class=resource_class)
            raise

    @_check_placement_api_available
    def get_inventory(self, resource_provider_uuid, resource_class):
        """Get resource provider inventory.

        :param resource_provider_uuid: UUID of the resource provider.
        :param resource_class: Resource class name of the inventory to be
                               returned.
        :raises PlacementResourceProviderNotFound: If the resource provider is
                                                   not found.
        :raises PlacementInventoryNotFound: For failure to find inventory
                                            for a resource provider.
        :returns: The inventory of the resource class as a dict.
        """
        url = '/resource_providers/{}/inventories/{}'.format(
            resource_provider_uuid, resource_class)
        try:
            return self._get(url).json()
        except ks_exc.NotFound as e:
            if "No resource provider with uuid" in e.details:
                raise n_exc.PlacementResourceProviderNotFound(
                    resource_provider=resource_provider_uuid)
            if _("No inventory of class") in e.details:
                raise n_exc.PlacementInventoryNotFound(
                    resource_provider=resource_provider_uuid,
                    resource_class=resource_class)
            raise

    @_check_placement_api_available
    def update_resource_provider_inventory(
            self, resource_provider_uuid, inventory, resource_class,
            resource_provider_generation=None):
        """Update resource provider inventory.

        :param resource_provider_uuid: UUID of the resource provider.
        :param inventory: The inventory to be updated for the resource class.
        :param resource_class: The name of the resource class.
        :param resource_provider_generation: The generation of the resource
                                             provider. Optional.
        :raises PlacementResourceNotFound: If the resource provider or the
                                           resource class is not found.
        :raises PlacementResourceProviderGenerationConflict: If the resource
                                                             provider
                                                             generation does
                                                             not match with the
                                                             server side.
        :returns: The updated inventory of the resource class as a dict.
        """
        url = '/resource_providers/{}/inventories/{}'.format(
            resource_provider_uuid, resource_class)
        body = inventory

        try:
            return self._put_with_retry_for_generation_conflict(
                url, body, resource_provider_uuid,
                resource_provider_generation)
        except ks_exc.NotFound as e:
            raise n_exc.PlacementResourceNotFound(url=e.url)

    @_check_placement_api_available
    def associate_aggregates(self, resource_provider_uuid, aggregates):
        """Associate a list of aggregates with a resource provider.

        :param resource_provider_uuid: UUID of the resource provider.
        :param aggregates: aggregates to be associated to the resource
                           provider.
        :returns: All aggregates associated with the resource provider.
        """
        url = '/resource_providers/%s/aggregates' % resource_provider_uuid
        return self._put(url, aggregates).json()

    @_check_placement_api_available
    def list_aggregates(self, resource_provider_uuid):
        """List resource provider aggregates.

        :param resource_provider_uuid: UUID of the resource provider.
        :raises PlacementAggregateNotFound: For failure to the aggregates of
                                            a resource provider.
        :returns: The list of aggregates together with the resource provider
                  generation.
        """
        # pylint: disable=raise-missing-from
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
        :returns: Evaluates to True if the trait exists.
        """
        # pylint: disable=raise-missing-from
        url = '/traits/%s' % name
        try:
            return self._get(url)
        except ks_exc.NotFound:
            raise n_exc.PlacementTraitNotFound(trait=name)

    @_check_placement_api_available
    def update_trait(self, name):
        """Insert a single custom trait.

        :param name: name of the trait to create.
        :returns: The Response object so you may access response headers.
        """
        url = '/traits/%s' % (name)
        return self._put(url, None)

    @_check_placement_api_available
    def delete_trait(self, name):
        """Delete the specified trait.

        :param name: the name of the trait to be deleted.
        :raises PlacementTraitNotFound: If the trait did not exist.
        :returns: None.
        """
        # pylint: disable=raise-missing-from
        url = '/traits/%s' % (name)
        try:
            self._delete(url)
        except ks_exc.NotFound:
            raise n_exc.PlacementTraitNotFound(trait=name)

    @_check_placement_api_available
    def update_resource_provider_traits(
            self, resource_provider_uuid, traits,
            resource_provider_generation=None):
        """Replace all associated traits of a resource provider.

        :param resource_provider_uuid: UUID of the resource provider for which
                                       to set the traits
        :param traits: a list of traits.
        :param resource_provider_generation: The generation of the resource
                                             provider. Optional. If not
                                             supplied by the caller, handle
                                             potential generation conflict
                                             by retrying the call. If supplied
                                             we assume the caller handles
                                             generation conflict.
        :raises PlacementResourceProviderNotFound: If the resource provider
                                                   is not found.
        :raises PlacementTraitNotFound: If any of the specified traits are not
                                        valid.
        :raises PlacementResourceProviderGenerationConflict: For concurrent
                                                             conflicting
                                                             updates detected.
        :returns: The new traits of the resource provider together with the
                  resource provider generation.
        """
        # pylint: disable=raise-missing-from
        url = '/resource_providers/%s/traits' % (resource_provider_uuid)
        body = {
            'resource_provider_generation': resource_provider_generation,
            'traits': traits
        }

        try:
            return self._put_with_retry_for_generation_conflict(
                url, body, resource_provider_uuid,
                resource_provider_generation)
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
        :returns: The associated traits of the resource provider together
                  with the resource provider generation.
        """
        # pylint: disable=raise-missing-from
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
        :raises PlacementResourceProviderNotFound: If the resource provider
                                                   is not found.
        :returns: None.
        """
        # pylint: disable=raise-missing-from
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
        :raises PlacementResourceClassNotFound: If the resource class
                                                is not found.
        :returns: The name of resource class and its set of links.
        """
        # pylint: disable=raise-missing-from
        url = '/resource_classes/%s' % (name)
        try:
            return self._get(url).json()
        except ks_exc.NotFound:
            raise n_exc.PlacementResourceClassNotFound(resource_class=name)

    @_check_placement_api_available
    def create_resource_class(self, name):
        """Create a custom resource class

        :param name: the name of the resource class
        :returns: None.
        """
        url = '/resource_classes'
        body = {'name': name}
        self._post(url, body)

    @_check_placement_api_available
    def update_resource_class(self, name):
        """Create or validate the existence of the resource custom class.

        :param name: the name of the resource class to be updated or validated
        :returns: None.
        """
        url = '/resource_classes/%s' % name
        self._put(url, None)

    @_check_placement_api_available
    def delete_resource_class(self, name):
        """Delete a custom resource class.

        :param name: The name of the resource class to be deleted.
        :raises PlacementResourceClassNotFound: If the resource class
                                                is not found.
        :returns: None.
        """
        # pylint: disable=raise-missing-from
        url = '/resource_classes/%s' % (name)
        try:
            self._delete(url)
        except ks_exc.NotFound:
            raise n_exc.PlacementResourceClassNotFound(resource_class=name)

    @_check_placement_api_available
    def list_allocations(self, consumer_uuid):
        """List allocations for the consumer

        :param consumer_uuid: The uuid of the consumer, in case of bound port
                              owned by a VM, the VM uuid.
        :returns: All allocation records for the consumer.
        """
        url = '/allocations/%s' % consumer_uuid
        return self._get(url).json()

    def update_qos_allocation(self, consumer_uuid, alloc_diff):
        """Update allocation for QoS minimum bandwidth consumer

        :param consumer_uuid: The uuid of the consumer, in case of bound port
                              owned by a VM, the VM uuid.
        :param alloc_diff: A dict which contains RP UUIDs as keys and
                           corresponding fields to update for the allocation
                           under the given resource provider.
        """
        for i in range(GENERATION_CONFLICT_RETRIES):
            body = self.list_allocations(consumer_uuid)
            if not body['allocations']:
                raise n_exc.PlacementAllocationRemoved(consumer=consumer_uuid)
            # Count new values based on the diff in alloc_diff
            for rp_uuid, diff in alloc_diff.items():
                if rp_uuid not in body['allocations']:
                    raise n_exc.PlacementAllocationRpNotExists(
                        resource_provider=rp_uuid, consumer=consumer_uuid)
                for drctn, value in diff.items():
                    orig_value = body['allocations'][rp_uuid][
                        'resources'].get(drctn, 0)
                    new_value = orig_value + value
                    if new_value > 0:
                        body['allocations'][rp_uuid]['resources'][
                            drctn] = new_value
                    else:
                        # Remove the resource class if the new value is 0
                        resources = body['allocations'][rp_uuid]['resources']
                        resources.pop(drctn, None)

            # Remove RPs without any resources
            body['allocations'] = {
                rp: alloc for rp, alloc in body['allocations'].items()
                if alloc.get('resources')}
            try:
                # Update allocations has no return body, but leave the loop
                return self.update_allocation(consumer_uuid, body)
            except ks_exc.Conflict as e:
                resp = e.response.json()
                if resp['errors'][0]['code'] == 'placement.concurrent_update':
                    continue
                raise
        raise n_exc.PlacementAllocationGenerationConflict(
            consumer=consumer_uuid)

    def update_allocation(self, consumer_uuid, allocations):
        """Update allocation record for given consumer and rp

        :param consumer_uuid: The uuid of the consumer
        :param allocations: Dict in the form described in placement API ref:
                            https://tinyurl.com/yxeuzn6l
        """
        url = '/allocations/%s' % consumer_uuid
        self._put(url, allocations)
