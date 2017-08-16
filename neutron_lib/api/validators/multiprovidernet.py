# Copyright (c) 2013 OpenStack Foundation.
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

from webob import exc

from neutron_lib._i18n import _
from neutron_lib.api import converters
from neutron_lib.api.definitions import provider_net as pnet
from neutron_lib import constants


def convert_and_validate_segments(segments, valid_values=None):
    for segment in segments:
        segment.setdefault(pnet.NETWORK_TYPE, constants.ATTR_NOT_SPECIFIED)
        segment.setdefault(pnet.PHYSICAL_NETWORK, constants.ATTR_NOT_SPECIFIED)
        segmentation_id = segment.get(pnet.SEGMENTATION_ID)
        if segmentation_id:
            segment[pnet.SEGMENTATION_ID] = converters.convert_to_int(
                segmentation_id)
        else:
            segment[pnet.SEGMENTATION_ID] = constants.ATTR_NOT_SPECIFIED
        if len(segment) != 3:
            msg = (_("Unrecognized attribute(s) '%s'") %
                   ', '.join(set(segment.keys()) -
                             set([pnet.NETWORK_TYPE, pnet.PHYSICAL_NETWORK,
                                  pnet.SEGMENTATION_ID])))
            raise exc.HTTPBadRequest(msg)
