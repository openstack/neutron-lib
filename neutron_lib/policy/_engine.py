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
_ADVSVC_CTX_POLICY = 'context_is_advsvc'


# TODO(gmann): Remove setting the default value of config policy_file
# once oslo_policy change the default value to 'policy.yaml'.
# https://github.com/openstack/oslo.policy/blob/a626ad12fe5a3abd49d70e3e5b95589d279ab578/oslo_policy/opts.py#L49
DEFAULT_POLICY_FILE = 'policy.yaml'
opts.set_defaults(cfg.CONF, DEFAULT_POLICY_FILE)


_BASE_RULES = [
    policy.RuleDefault(
        _ADMIN_CTX_POLICY,
        'role:admin',
        description='Rule for cloud admin access'),
    policy.RuleDefault(
        _ADVSVC_CTX_POLICY,
        'role:advsvc',
        description='Rule for advanced service role access'),
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


def check_is_advsvc(context):
    """Verify context has advsvc rights according to global policy settings.

    :param context: The context object.
    :returns: True if the context has advsvc rights (as per the global
    enforcer) and False otherwise.
    """
    return _check_rule(context, _ADVSVC_CTX_POLICY)


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
