# Copyright (c) 2016 Mirantis, Inc.
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


class FirewallGroupNotFound(exceptions.NotFound):
    message = _("Firewall group %(firewall_id)s could not be found.")


class FirewallGroupInUse(exceptions.InUse):
    message = _("Firewall group %(firewall_id)s is still active.")


class FirewallGroupInPendingState(exceptions.Conflict):
    message = _("Operation cannot be performed since associated firewall "
                "group %(firewall_id)s is in %(pending_state)s.")


class FirewallGroupPortInvalid(exceptions.Conflict):
    message = _("Port %(port_id)s of firewall group is invalid.")


class FirewallGroupPortInvalidProject(exceptions.Conflict):
    message = _("Operation cannot be performed as port %(port_id)s "
                "is in an invalid project %(project_id)s.")


class FirewallGroupPortInUse(exceptions.InUse):
    message = _("Port(s) %(port_ids)s provided already associated with "
                "other firewall group(s).")


class FirewallPolicyNotFound(exceptions.NotFound):
    message = _("Firewall policy %(firewall_policy_id)s could not be found.")


class FirewallPolicyInUse(exceptions.InUse):
    message = _("Firewall policy %(firewall_policy_id)s is being used.")


class FirewallPolicyConflict(exceptions.NotFound):
    """FWaaS exception raised for firewall policy conflict

    Raised when user tries to use another project's unshared policy.
    """
    message = _("Operation cannot be performed since firewall policy "
                "%(firewall_policy_id)s for your project could not be found. "
                "Please confirm if the firewall policy exists and is shared.")


class FirewallRuleSharingConflict(exceptions.NotFound):
    """FWaaS exception for sharing policies

    Raised when shared policy uses unshared rules.
    """
    message = _("Operation cannot be performed since firewall policy "
                "%(firewall_policy_id)s could not find the firewall rule "
                "%(firewall_rule_id)s. Please confirm if the firewall rule "
                "exists and is shared.")


class FirewallPolicySharingConflict(exceptions.Conflict):
    """FWaaS exception raised for sharing policies

    Raised if policy is 'shared' but its associated rules are not.
    """
    message = _("Operation cannot be performed. Before sharing firewall "
                "policy %(firewall_policy_id)s, share associated firewall "
                "rule %(firewall_rule_id)s.")


class FirewallRuleNotFound(exceptions.NotFound):
    message = _("Firewall rule %(firewall_rule_id)s could not be found.")


class FirewallRuleInUse(exceptions.InUse):
    message = _("Firewall rule %(firewall_rule_id)s is being used.")


class FirewallRuleNotAssociatedWithPolicy(exceptions.InvalidInput):
    message = _("Firewall rule %(firewall_rule_id)s is not associated "
                "with firewall policy %(firewall_policy_id)s.")


class FirewallRuleInvalidProtocol(exceptions.InvalidInput):
    message = _("Protocol %(protocol)s is not supported. "
                "Only protocol values %(values)s and their integer "
                "representation (0 to 255) are supported.")


class FirewallRuleInvalidAction(exceptions.InvalidInput):
    message = _("Action %(action)s is not supported. "
                "Only action values %(values)s are supported.")


class FirewallRuleInvalidICMPParameter(exceptions.InvalidInput):
    message = _("%(param)s are not allowed when protocol "
                "is set to ICMP.")


class FirewallRuleWithPortWithoutProtocolInvalid(exceptions.InvalidInput):
    message = _("Source/destination port requires a protocol.")


class FirewallRuleInvalidPortValue(exceptions.InvalidInput):
    message = _("Invalid value for port %(port)s.")


class FirewallRuleInfoMissing(exceptions.InvalidInput):
    message = _("Missing rule info argument for insert/remove "
                "rule operation.")


class FirewallIpAddressConflict(exceptions.InvalidInput):
    message = _("Invalid input - IP addresses do not agree with IP Version.")


class FirewallInternalDriverError(exceptions.NeutronException):
    """FWaaS exception for all driver errors

    On any failure or exception in the driver, driver should log it and
    raise this exception to the agent
    """

    message = _("%(driver)s: Internal driver error.")


class FirewallRuleConflict(exceptions.Conflict):
    """FWaaS rule conflict exception

    Occurs when admin policy tries to use another project's rule that is
    not shared.
    """
    message = _("Operation cannot be performed since firewall rule "
                "%(firewall_rule_id)s is not shared and belongs to "
                "another project %(project_id)s.")


class FirewallRuleAlreadyAssociated(exceptions.Conflict):
    """FWaaS exception for an already associated rule

    Occurs when there is an attempt to assign a rule to a policy that
    the rule is already associated with.
    """
    message = _("Operation cannot be performed since firewall rule "
                "%(firewall_rule_id)s is already associated with firewall "
                "policy %(firewall_policy_id)s.")


class FirewallGroupCannotRemoveDefault(exceptions.InUse):
    message = _("Deleting default firewall group not allowed.")


class FirewallGroupCannotUpdateDefault(exceptions.InUse):
    message = _("Updating default firewall group not allowed.")


class FirewallGroupDefaultAlreadyExists(exceptions.InUse):
    """Default firewall group conflict exception

    Occurs when a user creates firewall group named 'default'.
    """
    message = _("Default firewall group already exists. 'default' is the "
                "reserved name for firewall group.")
