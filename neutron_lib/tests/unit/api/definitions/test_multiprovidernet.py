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

from neutron_lib.api.definitions import multiprovidernet
from neutron_lib.api.definitions import provider_net
from neutron_lib.exceptions import multiprovidernet as mp_exc
from neutron_lib.tests.unit.api.definitions import base
from neutron_lib.tests.unit.api.validators import test_multiprovidernet \
    as test_mpnet


class MultiProviderNetworkDefinitionTestCase(base.DefinitionBaseTestCase):
    extension_module = multiprovidernet
    extension_attributes = (multiprovidernet.SEGMENTS,)

    def test_check_duplicate_segments_with_dups(self):
        self.assertRaises(mp_exc.SegmentsContainDuplicateEntry,
                          multiprovidernet.check_duplicate_segments,
                          [test_mpnet._build_segment('nt0', 'pn0', 2),
                           test_mpnet._build_segment('nt0', 'pn0', 2)])

    def test_check_duplicate_segments_with_dups_and_partial(self):

        def _seg_partial(seg):
            return seg[provider_net.PHYSICAL_NETWORK] == 'pn0'

        self.assertIsNone(
            multiprovidernet.check_duplicate_segments(
                [test_mpnet._build_segment('nt0', 'pn0', 2),
                 test_mpnet._build_segment('nt1', 'pn1', 2)],
                is_partial_func=_seg_partial))

    def test_check_duplicate_segments_no_dups(self):
        self.assertIsNone(
            multiprovidernet.check_duplicate_segments(
                [test_mpnet._build_segment('nt0', 'pn0', 2),
                 test_mpnet._build_segment('nt0', 'pn0', 3)]))
