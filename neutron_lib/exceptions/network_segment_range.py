# Copyright (c) 2018 Intel Corporation.
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


class NetworkSegmentRangeNetTypeNotSupported(exceptions.BadRequest):
    message = _("Network type %(type)s does not support "
                "network segment ranges.")


class NetworkSegmentRangeNotFound(exceptions.NotFound):
    message = _("Network Segment Range %(range_id)s could not be found.")


class NetworkSegmentRangeReferencedByProject(exceptions.InUse):
    message = _("Network Segment Range %(range_id)s is referenced by "
                "one or more tenant networks.")


class NetworkSegmentRangeDefaultReadOnly(exceptions.BadRequest):
    message = _("Network Segment Range %(range_id)s is a "
                "default segment range which could not be updated or deleted.")


class NetworkSegmentRangeOverlaps(exceptions.Conflict):
    message = _("Network segment range overlaps with range(s) "
                "with id %(range_id)s")
