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

import mock

from keystoneauth1 import exceptions as ks_exc
from oslo_utils import uuidutils

from neutron_lib._i18n import _
from neutron_lib.clients import placement
from neutron_lib.exceptions import placement as n_exc
from neutron_lib import fixture
from neutron_lib.tests import _base as base


RESOURCE_PROVIDER_UUID = uuidutils.generate_uuid()
RESOURCE_PROVIDER_GENERATION = 1
RESOURCE_CLASS_NAME = 'resource_class_name'
INVENTORY = {
    RESOURCE_CLASS_NAME: {
        'total': 42
    }
}


class TestPlacementAPIClient(base.BaseTestCase):

    def setUp(self):
        super(TestPlacementAPIClient, self).setUp()
        config = mock.Mock()
        config.region_name = 'region_name'
        self.openstack_api_version = (
            placement.PLACEMENT_API_LATEST_SUPPORTED)
        self.placement_api_client = placement.PlacementAPIClient(
            config, self.openstack_api_version)
        self.placement_fixture = self.useFixture(
            fixture.PlacementAPIClientFixture(self.placement_api_client))
        self.headers = {'OpenStack-API-Version': self.openstack_api_version}

    def test_create_resource_provider(self):
        self.placement_api_client.create_resource_provider(
            RESOURCE_PROVIDER_UUID)
        self.placement_fixture.mock_post.assert_called_once_with(
            '/resource_providers',
            RESOURCE_PROVIDER_UUID,
            headers=self.headers)

    def test_delete_resource_provider(self):
        self.placement_api_client.delete_resource_provider(
            RESOURCE_PROVIDER_UUID)
        self.placement_fixture.mock_delete.assert_called_once_with(
            '/resource_providers/%s' % RESOURCE_PROVIDER_UUID)

    def test_get_resource_provider(self):
        self.placement_api_client.get_resource_provider(RESOURCE_PROVIDER_UUID)
        self.placement_fixture.mock_get.assert_called_once_with(
            '/resource_providers/%s' % RESOURCE_PROVIDER_UUID,
            headers=self.headers)

    def test_get_resource_provider_no_resource_provider(self):
        self.placement_fixture.mock_get.side_effect = ks_exc.NotFound()
        self.assertRaises(n_exc.PlacementResourceProviderNotFound,
                          self.placement_api_client.get_resource_provider,
                          RESOURCE_PROVIDER_UUID)

    def test_list_resource_providers(self):
        filter_1 = {'name': 'name1', 'in_tree': 'tree1_uuid'}
        self.placement_api_client.list_resource_providers(**filter_1)
        self.placement_fixture.mock_get.assert_called_once_with(
            '/resource_providers', headers=self.headers, **filter_1)

        filter_2 = {'member_of': ['aggregate_uuid'], 'uuid': 'uuid_1',
                    'resources': {'r_class1': 'value1'}}
        self.placement_fixture.mock_get.reset_mock()
        self.placement_api_client.list_resource_providers(**filter_2)
        self.placement_fixture.mock_get.assert_called_once_with(
            '/resource_providers', headers=self.headers, **filter_2)

        filter_1.update(filter_2)
        self.placement_fixture.mock_get.reset_mock()
        self.placement_api_client.list_resource_providers(**filter_1)
        self.placement_fixture.mock_get.assert_called_once_with(
            '/resource_providers', headers=self.headers, **filter_1)

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

    def test_update_resource_provider_inventories(self):
        expected_body = {
            'resource_provider_generation': RESOURCE_PROVIDER_GENERATION,
            'inventories': INVENTORY
        }
        self.placement_api_client.update_resource_provider_inventories(
            RESOURCE_PROVIDER_UUID, INVENTORY, RESOURCE_PROVIDER_GENERATION)
        self.placement_fixture.mock_put.assert_called_once_with(
            '/resource_providers/%s/inventories' % RESOURCE_PROVIDER_UUID,
            expected_body)

    def test_update_resource_provider_inventories_no_rp(self):
        self.placement_fixture.mock_put.side_effect = ks_exc.NotFound()

        self.assertRaises(
            n_exc.PlacementResourceProviderNotFound,
            self.placement_api_client.update_resource_provider_inventories,
            RESOURCE_PROVIDER_UUID, INVENTORY, RESOURCE_PROVIDER_GENERATION)

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
        self.placement_fixture.mock_get.side_effect = _exception
        self.assertRaises(ks_exc.NotFound,
                          self.placement_api_client.get_inventory,
                          RESOURCE_PROVIDER_UUID, RESOURCE_CLASS_NAME)

    def test_update_resource_provider_inventory(self):
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

    def test_update_resource_inventory_inventory_conflict_exception(self):
        self.placement_fixture.mock_put.side_effect = ks_exc.Conflict()
        self.assertRaises(
            n_exc.PlacementInventoryUpdateConflict,
            self.placement_api_client.update_resource_provider_inventory,
            RESOURCE_PROVIDER_UUID, INVENTORY,
            RESOURCE_CLASS_NAME, resource_provider_generation=1)

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
            mock.ANY, headers=self.headers)

    def test_list_aggregates(self):
        self.placement_api_client.list_aggregates(RESOURCE_PROVIDER_UUID)
        self.placement_fixture.mock_get.assert_called_once_with(
            '/resource_providers/%s/aggregates' % RESOURCE_PROVIDER_UUID,
            headers=self.headers)

    def test_list_aggregates_no_resource_provider(self):
        self.placement_fixture.mock_get.side_effect = ks_exc.NotFound()
        self.assertRaises(n_exc.PlacementAggregateNotFound,
                          self.placement_api_client.list_aggregates,
                          RESOURCE_PROVIDER_UUID)
