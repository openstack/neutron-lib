# Copyright 2022 Red Hat, Inc.
# All rights reserved.
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

from neutron_lib.api.definitions import qos_rule_type_filter
from neutron_lib.tests.unit.api.definitions import base
from neutron_lib.tests.unit.api.definitions import test_qos


class QoSRuleTypeFilterTestCase(base.DefinitionBaseTestCase):
    extension_module = qos_rule_type_filter
    extension_resources = test_qos.QoSDefinitionTestCase.extension_resources
    extension_attributes = (qos_rule_type_filter.QOS_RULE_TYPE_ALL_SUPPORTED,
                            qos_rule_type_filter.QOS_RULE_TYPE_ALL_RULES)
