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


def policy_and(*args):
    return ' and '.join(args)


def policy_or(*args):
    return ' or '.join(args)


RULE_ADMIN_OR_OWNER = 'rule:admin_or_owner'
RULE_ADMIN_ONLY = 'rule:admin_only'
RULE_ANY = 'rule:regular_user'
RULE_ADVSVC = 'rule:context_is_advsvc'
RULE_SERVICE_ROLE = 'rule:service_api'
RULE_ADMIN_OR_NET_OWNER = 'rule:admin_or_network_owner'
RULE_ADMIN_OR_PARENT_OWNER = 'rule:admin_or_ext_parent_owner'
