# Copyright (C) 2013 eNovance SAS <licensing@enovance.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from neutron_lib._i18n import _
from neutron_lib import exceptions


class MeteringLabelNotFound(exceptions.NotFound):
    message = _("Metering label '%(label_id)s' does not exist.")


class DuplicateMeteringRuleInPost(exceptions.InUse):
    message = _("Duplicate Metering Rule in POST.")


class MeteringLabelRuleNotFound(exceptions.NotFound):
    message = _("Metering label rule '%(rule_id)s' does not exist.")


class MeteringLabelRuleOverlaps(exceptions.Conflict):
    message = _("Metering label rule with remote_ip_prefix "
                "'%(remote_ip_prefix)s' overlaps another.")
