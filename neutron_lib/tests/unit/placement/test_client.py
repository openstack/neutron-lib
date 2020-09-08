# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from unittest import mock

from keystoneauth1 import exceptions as ks_exc
from keystoneauth1 import loading as keystone
from oslo_serialization import jsonutils
from oslo_utils import uuidutils

from neutron_lib._i18n import _
from neutron_lib.exceptions import placement as n_exc
from neutron_lib import fixture
from neutron_lib.placement import client as place_client
from neutron_lib.tests import _base as base


RESOURCE_PROVIDER_UUID = uuidutils.generate_uuid()
CONSUMER_UUID = uuidutils.generate_uuid()
RESOURCE_PROVIDER_NAME = 'resource_provider_name'
RESOURCE_PROVIDER = {
    'uuid': RESOURCE_PROVIDER_UUID,
    'name': RESOURCE_PROVIDER_NAME,
}
RESOURCE_PROVIDER_GENERATION = 1
RESOURCE_CLASS_NAME = 'resource_class_name'
TRAIT_NAME = 'trait_name'
INVENTORY = {
    RESOURCE_CLASS_NAME: {
        'total': 42
    }
}


class TestNoAuthClient(base.BaseTestCase):

    def setUp(self):
        super(TestNoAuthClient, self).setUp()
        self.noauth_client = place_client.NoAuthClient('placement/')
        self.body_json = jsonutils.dumps({'name': 'foo'})
        self.uuid = '42'

    @mock.patch.object(place_client.NoAuthClient, 'request')
    def test_get(self, mock_request):
        self.noauth_client.get('resource_providers', '')
        mock_request.assert_called_with('placement/resource_providers', 'GET')

    @mock.patch.object(place_client.NoAuthClient, 'request')
    def test_post(self, mock_request):
        self.noauth_client.post('resource_providers', self.body_json, '')
        mock_request.assert_called_with('placement/resource_providers', 'POST',
                                        body=self.body_json)

    @mock.patch.object(place_client.NoAuthClient, 'request')
    def test_put(self, mock_request):
        self.noauth_client.put('resource_providers/%s' % self.uuid,
                               self.body_json, '')
        mock_request.assert_called_with(
            'placement/resource_providers/%s' % self.uuid, 'PUT',
            body=self.body_json)

    @mock.patch.object(place_client.NoAuthClient, 'request')
    def test_delete(self, mock_request):
        self.noauth_client.delete('resource_providers/%s' % self.uuid, '')
        mock_request.assert_called_with(
            'placement/resource_providers/%s' % self.uuid, 'DELETE')


class TestPlacementAPIClientNoAuth(base.BaseTestCase):
    def setUp(self):
        super(TestPlacementAPIClientNoAuth, self).setUp()
        self.config = mock.Mock()

    @mock.patch('neutron_lib.placement.client.NoAuthClient', autospec=True)
    def test__create_client_noauth(self, mock_auth_client):
        self.config.placement.auth_type = 'noauth'
        self.config.placement.auth_section = 'placement/'
        self.placement_api_client = place_client.PlacementAPIClient(
            self.config)
        self.placement_api_client._create_client()
        mock_auth_client.assert_called_once_with('placement/')

    @mock.patch.object(keystone, 'load_auth_from_conf_options')
    @mock.patch.object(keystone, 'load_session_from_conf_options')
    def test__create_client(self, mock_session_from_conf, mock_auth_from_conf):
        self.config.placement.auth_type = 'password'
        self.placement_api_client = place_client.PlacementAPIClient(
            self.config)
        self.placement_api_client._create_client()
        mock_auth_from_conf.assert_called_once_with(self.config, 'placement')
        mock_session_from_conf.assert_called_once()


class TestPlacementAPIClient(base.BaseTestCase):

    def setUp(self):
        super(TestPlacementAPIClient, self).setUp()
        config = mock.Mock()
        config.region_name = 'region_name'
        self.openstack_api_version = (
            place_client.PLACEMENT_API_LATEST_SUPPORTED)
        self.placement_api_client = place_client.PlacementAPIClient(
            config, self.openstack_api_version)
        self.placement_fixture = self.useFixture(
            fixture.PlacementAPIClientFixture(self.placement_api_client))

    def test_create_resource_provider(self):
        self.placement_api_client.create_resource_provider(
            RESOURCE_PROVIDER)
        self.placement_fixture.mock_post.assert_called_once_with(
            '/resource_providers',
            RESOURCE_PROVIDER
        )

    def test_update_resource_provider(self):
        self.placement_api_client.update_resource_provider(
            RESOURCE_PROVIDER)
        self.placement_fixture.mock_put.assert_called_once_with(
            '/resource_providers/%s' % RESOURCE_PROVIDER_UUID,
            {'name': RESOURCE_PROVIDER_NAME}
        )

    def test_ensure_update_resource_provider(self):
        self.placement_api_client.ensure_resource_provider(
            RESOURCE_PROVIDER)
        self.placement_fixture.mock_put.assert_called_once_with(
            '/resource_providers/%s' % RESOURCE_PROVIDER_UUID,
            {'name': RESOURCE_PROVIDER_NAME}
        )
        self.placement_fixture.mock_post.assert_not_called()

    def test_ensure_create_resource_provider(self):
        self.placement_fixture.mock_put.side_effect = \
            n_exc.PlacementResourceProviderNotFound(
                resource_provider=RESOURCE_PROVIDER_UUID)
        self.placement_api_client.ensure_resource_provider(
            RESOURCE_PROVIDER)
        self.placement_fixture.mock_post.assert_called_once_with(
            '/resource_providers',
            RESOURCE_PROVIDER
        )

    def test_delete_resource_provider(self):
        self.placement_api_client.delete_resource_provider(
            RESOURCE_PROVIDER_UUID)
        self.placement_fixture.mock_delete.assert_called_once_with(
            '/resource_providers/%s' % RESOURCE_PROVIDER_UUID)

    def test_get_resource_provider(self):
        self.placement_api_client.get_resource_provider(RESOURCE_PROVIDER_UUID)
        self.placement_fixture.mock_get.assert_called_once_with(
            '/resource_providers/%s' % RESOURCE_PROVIDER_UUID)

    def test_get_resource_provider_no_resource_provider(self):
        self.placement_fixture.mock_get.side_effect = ks_exc.NotFound()
        self.assertRaises(n_exc.PlacementResourceProviderNotFound,
                          self.placement_api_client.get_resource_provider,
                          RESOURCE_PROVIDER_UUID)

    def test_list_resource_providers(self):
        filter_1 = {'name': 'name1', 'in_tree': 'tree1_uuid'}
        self.placement_api_client.list_resource_providers(**filter_1)
        args = str(self.placement_fixture.mock_get.call_args)
        self.placement_fixture.mock_get.assert_called_once()
        self.assertIn('name=name1', args)
        self.assertIn('in_tree=tree1_uuid', args)

        filter_2 = {'member_of': ['aggregate_uuid'], 'uuid': 'uuid_1',
                    'resources': {'r_class1': 'value1'}}
        self.placement_fixture.mock_get.reset_mock()
        self.placement_api_client.list_resource_providers(**filter_2)
        args = str(self.placement_fixture.mock_get.call_args)
        self.placement_fixture.mock_get.assert_called_once()
        self.assertIn('member_of', args)
        self.assertIn('uuid', args)
        self.assertIn('resources', args)

        filter_1.update(filter_2)
        self.placement_fixture.mock_get.reset_mock()
        self.placement_api_client.list_resource_providers(**filter_1)
        args = str(self.placement_fixture.mock_get.call_args)
        self.placement_fixture.mock_get.assert_called_once()
        for key in filter_1:
            self.assertIn(key, args)

    def test_list_resource_providers_placement_api_version_too_low(self):
        self.placement_api_client._target_version = (1, 1)
        self.assertRaises(
            n_exc.PlacementAPIVersionIncorrect,
            self.placement_api_client.list_resource_providers,
            member_of=['aggregate_uuid'])
        self.assertRaises(
            n_exc.PlacementAPIVersionIncorrect,
            self.placement_api_client.list_resource_providers,
            in_tree='tree1_uuid')

    def test_update_resource_provider_inventories_generation(self):
        expected_body = {
            'resource_provider_generation': RESOURCE_PROVIDER_GENERATION,
            'inventories': INVENTORY
        }
        self.placement_api_client.update_resource_provider_inventories(
            RESOURCE_PROVIDER_UUID, INVENTORY, RESOURCE_PROVIDER_GENERATION)
        self.placement_fixture.mock_put.assert_called_once_with(
            '/resource_providers/%s/inventories' % RESOURCE_PROVIDER_UUID,
            expected_body)

    def test_update_resource_provider_inventories_no_generation(self):
        expected_body = {
            'resource_provider_generation': RESOURCE_PROVIDER_GENERATION,
            'inventories': INVENTORY
        }
        with mock.patch.object(
                self.placement_api_client, 'get_resource_provider',
                return_value={'generation': RESOURCE_PROVIDER_GENERATION}):
            self.placement_api_client.update_resource_provider_inventories(
                RESOURCE_PROVIDER_UUID, INVENTORY)
        self.placement_fixture.mock_put.assert_called_once_with(
            '/resource_providers/%s/inventories' % RESOURCE_PROVIDER_UUID,
            expected_body)

    def test_update_resource_provider_inventories_no_rp(self):
        self.placement_fixture.mock_put.side_effect = ks_exc.NotFound()

        self.assertRaises(
            n_exc.PlacementResourceProviderNotFound,
            self.placement_api_client.update_resource_provider_inventories,
            RESOURCE_PROVIDER_UUID, INVENTORY, RESOURCE_PROVIDER_GENERATION)

    def test_delete_resource_provider_inventory(self):
        self.placement_api_client.delete_resource_provider_inventory(
            RESOURCE_PROVIDER_UUID, RESOURCE_CLASS_NAME
        )
        self.placement_fixture.mock_delete.assert_called_once_with(
            '/resource_providers/%(rp_uuid)s/inventories/%(rc_name)s' %
            {'rp_uuid': RESOURCE_PROVIDER_UUID,
             'rc_name': RESOURCE_CLASS_NAME}
        )

    def test_delete_resource_provider_inventory_no_rp(self):
        self.placement_fixture.mock_delete.side_effect = ks_exc.NotFound(
            details='No resource provider with uuid'
        )
        self.assertRaises(
            n_exc.PlacementResourceProviderNotFound,
            self.placement_api_client.delete_resource_provider_inventory,
            RESOURCE_PROVIDER_UUID,
            RESOURCE_CLASS_NAME
        )

    def test_get_inventory(self):
        self.placement_api_client.get_inventory(RESOURCE_PROVIDER_UUID,
                                                RESOURCE_CLASS_NAME)
        self.placement_fixture.mock_get.assert_called_once_with(
            '/resource_providers/%(rp_uuid)s/inventories/%(rc_name)s' %
            {'rp_uuid': RESOURCE_PROVIDER_UUID,
             'rc_name': RESOURCE_CLASS_NAME})

    def test_get_inventory_no_resource_provider(self):
        _exception = ks_exc.NotFound()
        _exception.details = "No resource provider with uuid"
        self.placement_fixture.mock_get.side_effect = _exception
        self.assertRaises(n_exc.PlacementResourceProviderNotFound,
                          self.placement_api_client.get_inventory,
                          RESOURCE_PROVIDER_UUID, RESOURCE_CLASS_NAME)

    def test_get_inventory_no_inventory(self):
        _exception = ks_exc.NotFound()
        _exception.details = _("No inventory of class")
        self.placement_fixture.mock_get.side_effect = _exception
        self.assertRaises(n_exc.PlacementInventoryNotFound,
                          self.placement_api_client.get_inventory,
                          RESOURCE_PROVIDER_UUID, RESOURCE_CLASS_NAME)

    def test_get_inventory_not_found(self):
        _exception = ks_exc.NotFound()
        _exception.details = "Any other exception explanation"
        _exception.response = mock.Mock(text="Some error response body")
        self.placement_fixture.mock_get.side_effect = _exception
        self.assertRaises(n_exc.PlacementClientError,
                          self.placement_api_client.get_inventory,
                          RESOURCE_PROVIDER_UUID, RESOURCE_CLASS_NAME)

    def test_update_resource_provider_inventory_generation(self):
        expected_body = {
            'resource_provider_generation': RESOURCE_PROVIDER_GENERATION,
        }
        expected_body.update(INVENTORY)
        self.placement_api_client.update_resource_provider_inventory(
            RESOURCE_PROVIDER_UUID, INVENTORY, RESOURCE_CLASS_NAME,
            resource_provider_generation=1)
        self.placement_fixture.mock_put.assert_called_once_with(
            '/resource_providers/%(rp_uuid)s/inventories/%(rc_name)s' %
            {'rp_uuid': RESOURCE_PROVIDER_UUID,
             'rc_name': RESOURCE_CLASS_NAME},
            expected_body)

    def test_update_resource_provider_inventory_no_generation(self):
        expected_body = {
            'resource_provider_generation': RESOURCE_PROVIDER_GENERATION,
        }
        expected_body.update(INVENTORY)
        with mock.patch.object(
                self.placement_api_client, 'get_resource_provider',
                return_value={'generation': RESOURCE_PROVIDER_GENERATION}):
            self.placement_api_client.update_resource_provider_inventory(
                RESOURCE_PROVIDER_UUID, INVENTORY, RESOURCE_CLASS_NAME)
        self.placement_fixture.mock_put.assert_called_once_with(
            '/resource_providers/%(rp_uuid)s/inventories/%(rc_name)s' %
            {'rp_uuid': RESOURCE_PROVIDER_UUID,
             'rc_name': RESOURCE_CLASS_NAME},
            expected_body)

    def test_update_resource_provider_inventory_not_found(self):
        # Test the resource provider not found case
        self.placement_fixture.mock_put.side_effect = ks_exc.NotFound(
            details="No resource provider with uuid")
        self.assertRaises(
            n_exc.PlacementResourceNotFound,
            self.placement_api_client.update_resource_provider_inventory,
            RESOURCE_PROVIDER_UUID, INVENTORY,
            RESOURCE_CLASS_NAME, RESOURCE_PROVIDER_GENERATION)

    def test_associate_aggregates(self):
        self.placement_api_client.associate_aggregates(RESOURCE_PROVIDER_UUID,
                                                       mock.ANY)
        self.placement_fixture.mock_put.assert_called_once_with(
            '/resource_providers/%s/aggregates' % RESOURCE_PROVIDER_UUID,
            mock.ANY)

    def test_list_aggregates(self):
        self.placement_api_client.list_aggregates(RESOURCE_PROVIDER_UUID)
        self.placement_fixture.mock_get.assert_called_once_with(
            '/resource_providers/%s/aggregates' % RESOURCE_PROVIDER_UUID)

    def test_list_aggregates_no_resource_provider(self):
        self.placement_fixture.mock_get.side_effect = ks_exc.NotFound()
        self.assertRaises(n_exc.PlacementAggregateNotFound,
                          self.placement_api_client.list_aggregates,
                          RESOURCE_PROVIDER_UUID)

    def test_list_traits(self):
        self.placement_api_client.list_traits()
        self.placement_fixture.mock_get.assert_called_once_with(
            '/traits')

    def test_get_trait(self):
        self.placement_api_client.get_trait(TRAIT_NAME)
        self.placement_fixture.mock_get.assert_called_once_with(
            '/traits/%s' % TRAIT_NAME)

    def test_get_trait_no_trait(self):
        self.placement_fixture.mock_get.side_effect = ks_exc.NotFound()
        self.assertRaises(
            n_exc.PlacementTraitNotFound,
            self.placement_api_client.get_trait,
            TRAIT_NAME)

    def test_create_trait(self):
        self.placement_api_client.update_trait(TRAIT_NAME)
        self.placement_fixture.mock_put.assert_called_once_with(
            '/traits/%s' % TRAIT_NAME, None)

    def test_update_resource_provider_traits_generation(self):
        traits = [TRAIT_NAME]
        self.placement_api_client.update_resource_provider_traits(
            RESOURCE_PROVIDER_UUID, traits,
            resource_provider_generation=RESOURCE_PROVIDER_GENERATION)
        self.placement_fixture.mock_put.assert_called_once_with(
            '/resource_providers/%(rp_uuid)s/traits' %
            {'rp_uuid': RESOURCE_PROVIDER_UUID},
            {'resource_provider_generation': RESOURCE_PROVIDER_GENERATION,
             'traits': traits})

    def test_update_resource_provider_traits_no_generation(self):
        traits = [TRAIT_NAME]
        with mock.patch.object(
                self.placement_api_client, 'get_resource_provider',
                return_value={'generation': RESOURCE_PROVIDER_GENERATION}):
            self.placement_api_client.update_resource_provider_traits(
                RESOURCE_PROVIDER_UUID, traits)
        self.placement_fixture.mock_put.assert_called_once_with(
            '/resource_providers/%(rp_uuid)s/traits' %
            {'rp_uuid': RESOURCE_PROVIDER_UUID},
            {'resource_provider_generation': RESOURCE_PROVIDER_GENERATION,
             'traits': traits})

    def test_update_resource_provider_traits_no_rp(self):
        traits = [TRAIT_NAME]
        self.placement_fixture.mock_put.side_effect = ks_exc.NotFound()
        self.assertRaises(
            n_exc.PlacementResourceProviderNotFound,
            self.placement_api_client.update_resource_provider_traits,
            RESOURCE_PROVIDER_UUID, traits, resource_provider_generation=0)

    def test_update_resource_provider_traits_trait_not_found(self):
        traits = [TRAIT_NAME]
        self.placement_fixture.mock_put.side_effect = ks_exc.BadRequest()
        self.assertRaises(
            n_exc.PlacementTraitNotFound,
            self.placement_api_client.update_resource_provider_traits,
            RESOURCE_PROVIDER_UUID, traits, resource_provider_generation=0)

    def test_list_resource_provider_traits(self):
        self.placement_api_client.list_resource_provider_traits(
            RESOURCE_PROVIDER_UUID)
        self.placement_fixture.mock_get.assert_called_once_with(
            '/resource_providers/%s/traits' % RESOURCE_PROVIDER_UUID)

    def test_list_resource_provider_traits_no_rp(self):
        self.placement_fixture.mock_get.side_effect = ks_exc.NotFound()
        self.assertRaises(
            n_exc.PlacementResourceProviderNotFound,
            self.placement_api_client.list_resource_provider_traits,
            RESOURCE_PROVIDER_UUID)

    def test_delete_trait(self):
        self.placement_api_client.delete_trait(TRAIT_NAME)
        self.placement_fixture.mock_delete.assert_called_once_with(
            '/traits/%s' % TRAIT_NAME)

    def test_delete_trait_no_trait(self):
        self.placement_fixture.mock_delete.side_effect = ks_exc.NotFound()
        self.assertRaises(
            n_exc.PlacementTraitNotFound,
            self.placement_api_client.delete_trait,
            TRAIT_NAME)

    def test_delete_resource_provider_traits(self):
        self.placement_api_client.delete_resource_provider_traits(
            RESOURCE_PROVIDER_UUID)
        self.placement_fixture.mock_delete.assert_called_once_with(
            '/resource_providers/%s/traits' % RESOURCE_PROVIDER_UUID)

    def test_delete_resource_provider_traits_no_rp(self):
        self.placement_fixture.mock_delete.side_effect = ks_exc.NotFound()
        self.assertRaises(
            n_exc.PlacementResourceProviderNotFound,
            self.placement_api_client.delete_resource_provider_traits,
            RESOURCE_PROVIDER_UUID)

    def test_list_resource_classes(self):
        self.placement_api_client.list_resource_classes()
        self.placement_fixture.mock_get.assert_called_once_with(
            '/resource_classes'
        )

    def test_get_resource_class(self):
        self.placement_api_client.get_resource_class(RESOURCE_CLASS_NAME)
        self.placement_fixture.mock_get.assert_called_once_with(
            '/resource_classes/%s' % RESOURCE_CLASS_NAME
        )

    def test_get_resource_class_no_resource_class(self):
        self.placement_fixture.mock_get.side_effect = ks_exc.NotFound()
        self.assertRaises(
            n_exc.PlacementResourceClassNotFound,
            self.placement_api_client.get_resource_class,
            RESOURCE_CLASS_NAME
        )

    def test_create_resource_class(self):
        self.placement_api_client.create_resource_class(RESOURCE_CLASS_NAME)
        self.placement_fixture.mock_post.assert_called_once_with(
            '/resource_classes',
            {'name': RESOURCE_CLASS_NAME},
        )

    def test_update_resource_class(self):
        self.placement_api_client.update_resource_class(RESOURCE_CLASS_NAME)
        self.placement_fixture.mock_put.assert_called_once_with(
            '/resource_classes/%s' % RESOURCE_CLASS_NAME, None)

    def test_delete_resource_class(self):
        self.placement_api_client.delete_resource_class(RESOURCE_CLASS_NAME)
        self.placement_fixture.mock_delete.assert_called_once_with(
            '/resource_classes/%s' % RESOURCE_CLASS_NAME
        )

    def test_delete_resource_class_no_resource_class(self):
        self.placement_fixture.mock_delete.side_effect = ks_exc.NotFound()
        self.assertRaises(
            n_exc.PlacementResourceClassNotFound,
            self.placement_api_client.delete_resource_class,
            RESOURCE_CLASS_NAME
        )

    def test_update_rp_traits_caller_handles_generation_conflict(self):
        mock_resp = mock.Mock()
        mock_resp.text = ''
        mock_resp.json = lambda: {
            'errors': [{'code': 'placement.concurrent_update'}]}
        self.placement_fixture.mock_put.side_effect = ks_exc.Conflict(
            response=mock_resp)
        self.assertRaises(
            n_exc.PlacementResourceProviderGenerationConflict,
            self.placement_api_client.update_resource_provider_traits,
            resource_provider_uuid='resource provider uuid',
            traits=['trait a', 'trait b'],
            resource_provider_generation=3,
        )
        self.placement_fixture.mock_put.assert_called_once()

    def test_update_rp_traits_callee_handles_generation_conflict(self):
        mock_resp = mock.Mock()
        mock_resp.text = ''
        mock_resp.json = lambda: {
            'errors': [{'code': 'placement.concurrent_update'}]}
        self.placement_fixture.mock_put.side_effect = [
            ks_exc.Conflict(response=mock_resp),
            mock.Mock(),
        ]
        self.placement_api_client.update_resource_provider_traits(
            resource_provider_uuid='resource provider uuid',
            traits=['trait a', 'trait b'],
            resource_provider_generation=None,
        )
        self.assertEqual(2, self.placement_fixture.mock_put.call_count)

    def test_update_rp_traits_reached_max_tries(self):
        mock_resp = mock.Mock()
        mock_resp.text = ''
        mock_resp.json = lambda: {
            'errors': [{'code': 'placement.concurrent_update'}]}
        self.placement_fixture.mock_put.side_effect = 10 * [
            ks_exc.Conflict(response=mock_resp),
        ]
        self.assertRaises(
            n_exc.PlacementResourceProviderGenerationConflict,
            self.placement_api_client.update_resource_provider_traits,
            resource_provider_uuid='resource provider uuid',
            traits=['trait a', 'trait b'],
            resource_provider_generation=None,
        )
        self.assertEqual(10, self.placement_fixture.mock_put.call_count)

    def test_update_rp_traits_raise_other_conflict(self):
        mock_resp = mock.Mock()
        mock_resp.text = ''
        mock_resp.json = lambda: {
            'errors': [{'code': 'some_other_code'}]}
        self.placement_fixture.mock_put.side_effect = [
            ks_exc.Conflict(response=mock_resp),
            mock.Mock(),
        ]
        self.assertRaises(
            n_exc.PlacementClientError,
            self.placement_api_client.update_resource_provider_traits,
            resource_provider_uuid='resource provider uuid',
            traits=[],
            resource_provider_generation=None,
        )
        self.assertEqual(1, self.placement_fixture.mock_put.call_count)

    def test_update_rp_inventory_caller_handles_generation_conflict(self):
        mock_resp = mock.Mock()
        mock_resp.text = ''
        mock_resp.json = lambda: {
            'errors': [{'code': 'placement.concurrent_update'}]}
        self.placement_fixture.mock_put.side_effect = ks_exc.Conflict(
            response=mock_resp)
        self.assertRaises(
            n_exc.PlacementResourceProviderGenerationConflict,
            self.placement_api_client.update_resource_provider_inventory,
            resource_provider_uuid='resource provider uuid',
            inventory={},
            resource_class='a resource class',
            resource_provider_generation=3,
        )
        self.placement_fixture.mock_put.assert_called_once()

    def test_update_rp_inventory_callee_handles_generation_conflict(self):
        mock_resp = mock.Mock()
        mock_resp.text = ''
        mock_resp.json = lambda: {
            'errors': [{'code': 'placement.concurrent_update'}]}
        self.placement_fixture.mock_put.side_effect = [
            ks_exc.Conflict(response=mock_resp),
            mock.Mock(),
        ]
        self.placement_api_client.update_resource_provider_inventory(
            resource_provider_uuid='resource provider uuid',
            inventory={},
            resource_class='a resource class',
            resource_provider_generation=None,
        )
        self.assertEqual(2, self.placement_fixture.mock_put.call_count)

    def test_update_rp_inventory_reached_max_tries(self):
        mock_resp = mock.Mock()
        mock_resp.text = ''
        mock_resp.json = lambda: {
            'errors': [{'code': 'placement.concurrent_update'}]}
        self.placement_fixture.mock_put.side_effect = 10 * [
            ks_exc.Conflict(response=mock_resp),
        ]
        self.assertRaises(
            n_exc.PlacementResourceProviderGenerationConflict,
            self.placement_api_client.update_resource_provider_inventory,
            resource_provider_uuid='resource provider uuid',
            inventory={},
            resource_class='a resource class',
            resource_provider_generation=None,
        )
        self.assertEqual(10, self.placement_fixture.mock_put.call_count)

    def test_update_rp_inventory_raise_other_conflict(self):
        mock_resp = mock.Mock()
        mock_resp.text = ''
        mock_resp.json = lambda: {
            'errors': [{'code': 'some_other_code'}]}
        self.placement_fixture.mock_put.side_effect = [
            ks_exc.Conflict(response=mock_resp),
            mock.Mock(),
        ]
        self.assertRaises(
            n_exc.PlacementClientError,
            self.placement_api_client.update_resource_provider_inventory,
            resource_provider_uuid='resource provider uuid',
            inventory={},
            resource_class='a resource class',
            resource_provider_generation=None,
        )
        self.assertEqual(1, self.placement_fixture.mock_put.call_count)

    def test_update_rp_inventories_caller_handles_generation_conflict(self):
        mock_resp = mock.Mock()
        mock_resp.text = ''
        mock_resp.json = lambda: {
            'errors': [{'code': 'placement.concurrent_update'}]}
        self.placement_fixture.mock_put.side_effect = ks_exc.Conflict(
            response=mock_resp)
        self.assertRaises(
            n_exc.PlacementResourceProviderGenerationConflict,
            self.placement_api_client.update_resource_provider_inventories,
            resource_provider_uuid='resource provider uuid',
            inventories={},
            resource_provider_generation=3,
        )
        self.placement_fixture.mock_put.assert_called_once()

    def test_update_rp_inventories_callee_handles_generation_conflict(self):
        mock_resp = mock.Mock()
        mock_resp.text = ''
        mock_resp.json = lambda: {
            'errors': [{'code': 'placement.concurrent_update'}]}
        self.placement_fixture.mock_put.side_effect = [
            ks_exc.Conflict(response=mock_resp),
            mock.Mock(),
        ]
        self.placement_api_client.update_resource_provider_inventories(
            resource_provider_uuid='resource provider uuid',
            inventories={},
            resource_provider_generation=None,
        )
        self.assertEqual(2, self.placement_fixture.mock_put.call_count)

    def test_update_rp_inventories_reached_max_tries(self):
        mock_resp = mock.Mock()
        mock_resp.text = ''
        mock_resp.json = lambda: {
            'errors': [{'code': 'placement.concurrent_update'}]}
        self.placement_fixture.mock_put.side_effect = 10 * [
            ks_exc.Conflict(response=mock_resp),
        ]
        self.assertRaises(
            n_exc.PlacementResourceProviderGenerationConflict,
            self.placement_api_client.update_resource_provider_inventories,
            resource_provider_uuid='resource provider uuid',
            inventories={},
            resource_provider_generation=None,
        )
        self.assertEqual(10, self.placement_fixture.mock_put.call_count)

    def test_update_rp_inventories_raise_other_conflict(self):
        mock_resp = mock.Mock()
        mock_resp.text = ''
        mock_resp.json = lambda: {
            'errors': [{'code': 'some_other_code'}]}
        self.placement_fixture.mock_put.side_effect = [
            ks_exc.Conflict(response=mock_resp),
            mock.Mock(),
        ]
        self.assertRaises(
            n_exc.PlacementClientError,
            self.placement_api_client.update_resource_provider_inventories,
            resource_provider_uuid='resource provider uuid',
            inventories={},
            resource_provider_generation=None,
        )
        self.assertEqual(1, self.placement_fixture.mock_put.call_count)

    def test_list_allocations(self):
        self.placement_api_client.list_allocations(CONSUMER_UUID)
        self.placement_fixture.mock_get.assert_called_once_with(
            '/allocations/%s' % CONSUMER_UUID)

    def test_update_allocation(self):
        mock_rsp = mock.Mock()
        mock_rsp.json = lambda: {
            'allocations': {
                RESOURCE_PROVIDER_UUID: {'resources': {'a': 10}}
            }
        }
        self.placement_fixture.mock_get.side_effect = [mock_rsp]
        self.placement_api_client.update_allocation(
            CONSUMER_UUID,
            {'allocations': {
                RESOURCE_PROVIDER_UUID: {
                    'resources': {'a': 20}}
            }})
        self.placement_fixture.mock_put.assert_called_once_with(
            '/allocations/%s' % CONSUMER_UUID,
            {'allocations': {
                RESOURCE_PROVIDER_UUID: {
                    'resources': {'a': 20}}
            }}
        )

    def _get_allocation_response(self, resources):
        mock_rsp_get = mock.Mock()
        mock_rsp_get.json = lambda: {
            'allocations': {
                RESOURCE_PROVIDER_UUID: resources
            }
        }
        return mock_rsp_get

    def test_update_qos_minbw_allocation(self):
        mock_rsp_get = self._get_allocation_response(
            {'resources': {'a': 3, 'b': 2}})
        self.placement_fixture.mock_get.side_effect = [mock_rsp_get]
        self.placement_api_client.update_qos_minbw_allocation(
            consumer_uuid=CONSUMER_UUID,
            minbw_alloc_diff={'a': 2, 'b': 2},
            rp_uuid=RESOURCE_PROVIDER_UUID
        )
        self.placement_fixture.mock_put.assert_called_once_with(
            '/allocations/%s' % CONSUMER_UUID,
            {'allocations': {
                RESOURCE_PROVIDER_UUID: {
                    'resources': {'a': 5, 'b': 4}}
            }}
        )

    def test_update_qos_minbw_allocation_removed(self):
        mock_rsp = mock.Mock()
        mock_rsp.json = lambda: {'allocations': {}}
        self.placement_fixture.mock_get.side_effect = [mock_rsp]
        self.assertRaises(
            n_exc.PlacementAllocationRemoved,
            self.placement_api_client.update_qos_minbw_allocation,
            consumer_uuid=CONSUMER_UUID,
            minbw_alloc_diff={'a': 1, 'b': 1},
            rp_uuid=RESOURCE_PROVIDER_UUID
        )

    def test_update_qos_minbw_allocation_rp_not_exists(self):
        mock_rsp = mock.Mock()
        mock_rsp.json = lambda: {'allocations': {'other:rp:uuid': {'c': 3}}}
        self.placement_fixture.mock_get.side_effect = [mock_rsp]
        self.assertRaises(
            n_exc.PlacementAllocationRpNotExists,
            self.placement_api_client.update_qos_minbw_allocation,
            consumer_uuid=CONSUMER_UUID,
            minbw_alloc_diff={'a': 1, 'b': 1},
            rp_uuid=RESOURCE_PROVIDER_UUID
        )

    def test_update_qos_minbw_allocation_max_retries(self):
        mock_rsp_get = self._get_allocation_response({'c': 3})
        self.placement_fixture.mock_get.side_effect = 10 * [mock_rsp_get]
        mock_rsp_put = mock.Mock()
        mock_rsp_put.json = lambda: {
            'errors': [{'code': 'placement.concurrent_update'}]}
        self.placement_fixture.mock_put.side_effect = ks_exc.Conflict(
            response=mock_rsp_put)
        self.assertRaises(
            n_exc.PlacementAllocationGenerationConflict,
            self.placement_api_client.update_qos_minbw_allocation,
            consumer_uuid=CONSUMER_UUID,
            minbw_alloc_diff={},
            rp_uuid=RESOURCE_PROVIDER_UUID,
        )
        self.assertEqual(10, self.placement_fixture.mock_put.call_count)

    def test_update_qos_minbwallocation_generation_conflict_solved(self):
        mock_rsp_get = self._get_allocation_response({'c': 3})
        self.placement_fixture.mock_get.side_effect = 2 * [mock_rsp_get]
        mock_rsp_put = mock.Mock()
        mock_rsp_put.json = lambda: {
            'errors': [{'code': 'placement.concurrent_update'}]}
        self.placement_fixture.mock_put.side_effect = [
            ks_exc.Conflict(response=mock_rsp_put),
            mock.Mock()
        ]
        self.placement_api_client.update_qos_minbw_allocation(
            consumer_uuid=CONSUMER_UUID,
            minbw_alloc_diff={},
            rp_uuid=RESOURCE_PROVIDER_UUID
        )
        self.assertEqual(2, self.placement_fixture.mock_put.call_count)

    def test_update_qos_minbw_allocation_other_conflict(self):
        mock_rsp_get = self._get_allocation_response({'c': 3})
        self.placement_fixture.mock_get.side_effect = 10*[mock_rsp_get]
        mock_rsp_put = mock.Mock()
        mock_rsp_put.text = ''
        mock_rsp_put.json = lambda: {
            'errors': [{'code': 'some other error code'}]}
        self.placement_fixture.mock_put.side_effect = ks_exc.Conflict(
            response=mock_rsp_put)
        self.assertRaises(
            ks_exc.Conflict,
            self.placement_api_client.update_qos_minbw_allocation,
            consumer_uuid=CONSUMER_UUID,
            minbw_alloc_diff={},
            rp_uuid=RESOURCE_PROVIDER_UUID,
        )
        self.placement_fixture.mock_put.assert_called_once()

    def test_update_qos_minbw_allocation_to_zero(self):
        mock_rsp_get = self._get_allocation_response(
            {'resources': {'a': 3, 'b': 2}})
        self.placement_fixture.mock_get.side_effect = [mock_rsp_get]
        self.placement_api_client.update_qos_minbw_allocation(
            consumer_uuid=CONSUMER_UUID,
            minbw_alloc_diff={'a': -3, 'b': -2},
            rp_uuid=RESOURCE_PROVIDER_UUID
        )
        self.placement_fixture.mock_put.assert_called_once_with(
            '/allocations/%s' % CONSUMER_UUID,
            {'allocations': {}})

    def test_update_qos_minbw_allocation_one_class_to_zero(self):
        mock_rsp_get = self._get_allocation_response(
            {'resources': {'a': 3, 'b': 2}})
        self.placement_fixture.mock_get.side_effect = [mock_rsp_get]
        self.placement_api_client.update_qos_minbw_allocation(
            consumer_uuid=CONSUMER_UUID,
            minbw_alloc_diff={'a': -3, 'b': 1},
            rp_uuid=RESOURCE_PROVIDER_UUID
        )
        self.placement_fixture.mock_put.assert_called_once_with(
            '/allocations/%s' % CONSUMER_UUID,
            {'allocations': {
                RESOURCE_PROVIDER_UUID: {
                    'resources': {'b': 3}}
            }})
