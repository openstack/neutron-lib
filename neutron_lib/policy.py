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

from oslo_config import cfg
from oslo_policy import policy


_ENFORCER = None
_ADMIN_CTX_POLICY = 'context_is_admin'
_ADVSVC_CTX_POLICY = 'context_is_advsvc'


def reset():
    """Reset the global enforcer.

    Resets the global enforcer thereby deleting any rules and state associated
    with it. Subsequent calls to this modules API will trigger a
    re-initialization of the global enforcer as necessary.

    :returns: None.
    """
    global _ENFORCER
    if _ENFORCER:
        _ENFORCER.clear()
        _ENFORCER = None


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

    global _ENFORCER
    if not _ENFORCER:
        _ENFORCER = policy.Enforcer(conf, policy_file=policy_file)
        _ENFORCER.load_rules(True)


def refresh(policy_file=None):
    """Reset the global enforcer and re-initialize it.

    Reset the global policy and re-initialize it optionally using the said
    policy file.

    :param policy_file: The policy file to initialize the global enforcer with.
    :returns: None.
    """
    reset()
    init(policy_file=policy_file)


def check_is_admin(context):
    """Verify context has admin rights according to the global policy settings.

    :param context: The context object.
    :returns: True if the context has admin rights (as per the global
    enforcer) and False otherwise.
    """
    init()
    # the target is user-self
    credentials = context.to_dict()
    if _ADMIN_CTX_POLICY not in _ENFORCER.rules:
        return False
    return _ENFORCER.enforce(_ADMIN_CTX_POLICY, credentials, credentials)


def check_is_advsvc(context):
    """Verify context has advsvc rights according to global policy settings.

    :param context: The context object.
    :returns: True if the context has advsvc rights (as per the global
    enforcer) and False otherwise.
    """
    init()
    # the target is user-self
    credentials = context.to_dict()
    if _ADVSVC_CTX_POLICY not in _ENFORCER.rules:
        return False
    return _ENFORCER.enforce(_ADVSVC_CTX_POLICY, credentials, credentials)
