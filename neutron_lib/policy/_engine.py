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

import sys

from oslo_config import cfg
from oslo_policy import opts
from oslo_policy import policy


_ROLE_ENFORCER = None
_ADMIN_CTX_POLICY = 'context_is_admin'
_GLOBAL_CTX_POLICY = 'context_with_global_access'
_ADVSVC_CTX_POLICY = 'context_is_advsvc'
_SERVICE_ROLE = 'service_api'


opts.set_defaults(cfg.CONF)


_BASE_RULES = [
    policy.RuleDefault(
        _ADMIN_CTX_POLICY,
        'role:admin',
        description='Rule for cloud admin access'),
    policy.RuleDefault(
        # By default, no one has global access to the resources.
        # That is special meaning of the "!" in rule, see
        # https://docs.openstack.org/oslo.policy/latest/admin/policy-yaml-file.html#examples.
        # This policy rule should be overridden by the cloud administrator if
        # there is need to have any custom role with global access to the
        # resources from all projects.
        _GLOBAL_CTX_POLICY,
        '!',
        description='Rule for context with global access to the resources'),
    policy.RuleDefault(
        _ADVSVC_CTX_POLICY,
        'role:advsvc',
        description='Rule for advanced service role access'),
    policy.RuleDefault(
        _SERVICE_ROLE,
        'role:service',
        description='Default rule for the service-to-service APIs.'),
]


def init(conf=cfg.CONF, policy_file=None):
    """Initialize the global enforcer if not already initialized.

    Initialize the global enforcer (and load its rules) if not already
    initialized; otherwise this is a no-op.

    :param conf: The configuration to initialize the global enforcer with.
    Defaults to oslo_config.cfg.CONF.
    :param policy_file: The policy file to initialize the global enforcer
    with.
    :returns: None.
    """

    global _ROLE_ENFORCER
    if not _ROLE_ENFORCER:
        _ROLE_ENFORCER = policy.Enforcer(conf, policy_file=policy_file)
        # Skip the undefined rule check to avoid unnecessary warning messages.
        _ROLE_ENFORCER.skip_undefined_check = True
        _ROLE_ENFORCER.register_defaults(_BASE_RULES)
        _ROLE_ENFORCER.load_rules(True)


def _check_rule(context, rule):
    init()
    # the target is user-self
    credentials = context.to_policy_values()
    try:
        return _ROLE_ENFORCER.authorize(rule, credentials, credentials)
    except policy.PolicyNotRegistered:
        return False


def check_is_admin(context):
    """Verify context has admin rights according to the global policy settings.

    :param context: The context object.
    :returns: True if the context has admin rights (as per the global
    enforcer) and False otherwise.
    """
    return _check_rule(context, _ADMIN_CTX_POLICY)


def check_has_global_access(context):
    """Verify context has rights to fetch resources no matter of the owner

    :param context: The context object.
    :returns: True if the context has global rights (as per the global
    enforcer) and False otherwise.
    """
    return _check_rule(context, _GLOBAL_CTX_POLICY)


def check_is_advsvc(context):
    """Verify context has advsvc rights according to global policy settings.

    :param context: The context object.
    :returns: True if the context has advsvc rights (as per the global
    enforcer) and False otherwise.
    """
    return _check_rule(context, _ADVSVC_CTX_POLICY)


def check_is_service_role(context):
    """Verify context is service role according to global policy settings.

    :param context: The context object.
    :returns: True if the context is service role (as per the global
    enforcer) and False otherwise.
    """
    return _check_rule(context, _SERVICE_ROLE)


def list_rules():
    return _BASE_RULES


def get_enforcer():
    # NOTE(amotoki): This was borrowed from nova/policy.py.
    # This method is for use by oslo.policy CLI scripts. Those scripts need the
    # 'output-file' and 'namespace' options, but having those in sys.argv means
    # loading the neutron config options will fail as those are not expected to
    # be present. So we pass in an arg list with those stripped out.
    conf_args = []
    # Start at 1 because cfg.CONF expects the equivalent of sys.argv[1:]
    i = 1
    while i < len(sys.argv):
        if sys.argv[i].strip('-') in ['namespace', 'output-file']:
            i += 2
            continue
        conf_args.append(sys.argv[i])
        i += 1

    # 'project' must be 'neutron' so that get_enforcer looks at
    # /etc/neutron/policy.yaml by default.
    cfg.CONF(conf_args, project='neutron')
    init()
    return _ROLE_ENFORCER
