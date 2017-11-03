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

from webob import exc

from neutron_lib.api.definitions import provider_net
from neutron_lib.api.validators import multiprovidernet as mp_validator
from neutron_lib import constants
from neutron_lib.tests import _base as base


def _build_segment(net_type=constants.ATTR_NOT_SPECIFIED,
                   phy_net=constants.ATTR_NOT_SPECIFIED,
                   seg_id=constants.ATTR_NOT_SPECIFIED):
    return {
        provider_net.NETWORK_TYPE: net_type,
        provider_net.PHYSICAL_NETWORK: phy_net,
        provider_net.SEGMENTATION_ID: seg_id
    }


class TestMultiprovidernetValidators(base.BaseTestCase):

    def test_convert_and_validate_segments_default_values(self):
        segs = [{}]
        mp_validator.convert_and_validate_segments(segs)
        self.assertEqual(
            [_build_segment()], segs)

    def test_convert_and_validate_segments_seg_id_to_int(self):
        segs = [_build_segment(seg_id="9")]
        mp_validator.convert_and_validate_segments(segs)
        self.assertEqual(_build_segment(seg_id=9), segs[0])

    def test_convert_and_validate_segments_invalid_key(self):
        segs = [_build_segment(seg_id=2)]
        segs[0]['some_key'] = 'some_value'
        self.assertRaises(exc.HTTPBadRequest,
                          mp_validator.convert_and_validate_segments,
                          segs)
