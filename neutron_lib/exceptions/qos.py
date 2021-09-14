# Copyright 2011 VMware, Inc
# All Rights Reserved.
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
from neutron_lib import exceptions as e


class QosPolicyNotFound(e.NotFound):
    message = _("QoS policy %(policy_id)s could not be found.")


class QosRuleNotFound(e.NotFound):
    message = _("QoS rule %(rule_id)s for policy %(policy_id)s "
                "could not be found.")


class QoSPolicyDefaultAlreadyExists(e.Conflict):
    message = _("A default QoS policy exists for project %(project_id)s.")


class PortQosBindingNotFound(e.NotFound):
    message = _("QoS binding for port %(port_id)s and policy %(policy_id)s "
                "could not be found.")


class PortQosBindingError(e.NeutronException):
    message = _("QoS binding for port %(port_id)s and policy %(policy_id)s "
                "could not be created: %(db_error)s.")


class NetworkQosBindingNotFound(e.NotFound):
    message = _("QoS binding for network %(net_id)s and policy %(policy_id)s "
                "could not be found.")


class FloatingIPQosBindingNotFound(e.NotFound):
    message = _("QoS binding for floating IP %(fip_id)s and policy "
                "%(policy_id)s could not be found.")


class QosPolicyInUse(e.InUse):
    message = _("QoS Policy %(policy_id)s is used by "
                "%(object_type)s %(object_id)s.")


class FloatingIPQosBindingError(e.NeutronException):
    message = _("QoS binding for floating IP %(fip_id)s and policy "
                "%(policy_id)s could not be created: %(db_error)s.")


class NetworkQosBindingError(e.NeutronException):
    message = _("QoS binding for network %(net_id)s and policy %(policy_id)s "
                "could not be created: %(db_error)s.")


class QosRuleNotSupported(e.Conflict):
    message = _("Rule %(rule_type)s is not supported by port %(port_id)s")


class QosRuleNotSupportedByNetwork(e.Conflict):
    message = _("Rule %(rule_type)s is not supported "
                "by network %(network_id)s")


class QoSRuleParameterConflict(e.Conflict):
    message = _("Unable to add the rule with value %(rule_value)s to the "
                "policy %(policy_id)s as the existing rule of type "
                "%(existing_rule)s has value %(existing_value)s.")


class QoSRulesConflict(e.Conflict):
    message = _("Rule %(new_rule_type)s conflicts with "
                "rule %(rule_id)s which already exists in "
                "QoS Policy %(policy_id)s.")


class PolicyRemoveAuthorizationError(e.NotAuthorized):
    message = _("Failed to remove provided policy %(policy_id)s "
                "because you are not authorized.")


class TcLibQdiscTypeError(e.NeutronException):
    message = _("TC Qdisc type %(qdisc_type)s is not supported; supported "
                "types: %(supported_qdisc_types)s.")


class TcLibQdiscNeededArguments(e.NeutronException):
    message = _("TC Qdisc type %(qdisc_type)s needs following arguments: "
                "%(needed_arguments)s.")


class RouterQosBindingNotFound(e.NotFound):
    message = _("QoS binding for router %(router_id)s gateway and policy "
                "%(policy_id)s could not be found.")


class RouterQosBindingError(e.NeutronException):
    message = _("QoS binding for router %(router_id)s gateway and policy "
                "%(policy_id)s could not be created: %(db_error)s.")


class QosPlacementAllocationConflict(e.Conflict):
    message = _("Allocation for consumer %(consumer)s is not possible on "
                "resource provider %(rp)s, the requested amount of bandwidth "
                "would exceed the capacity available.")


class QosPlacementAllocationUpdateConflict(e.Conflict):
    message = _("Updating placement allocation with %(alloc_diff)s for "
                "consumer %(consumer)s failed. The requested resources would "
                "exceed the capacity available.")
