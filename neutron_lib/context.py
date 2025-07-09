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

"""Context: context for security/db session."""

import collections
import copy

from oslo_context import context as oslo_context
from oslo_db.sqlalchemy import enginefacade
from oslo_log import log as logging
from oslo_utils import timeutils

from neutron_lib.db import api as db_api
from neutron_lib.policy import _engine as policy_engine

LOG = logging.getLogger(__name__)


class ContextBase(oslo_context.RequestContext):
    """Security context and request information.

    Represents the user taking a given action within the system.

    """

    def __init__(self, user_id=None, project_id=None, is_admin=None,
                 timestamp=None, project_name=None, user_name=None,
                 is_advsvc=None, tenant_id=None, tenant_name=None,
                 has_global_access=False, **kwargs):
        # NOTE(jamielennox): We maintain this argument order for tests that
        # pass arguments positionally.

        # Prefer project_id and project_name, as that's what's going to be
        # set by keystone.
        # NOTE(haleyb): remove fall-back and warning in E+2 release, or when
        # all callers have been changed to use project_*.
        project_id = project_id or tenant_id
        project_name = project_name or tenant_name
        if tenant_id:
            LOG.warning('Keyword tenant_id has been deprecated, use '
                        'project_id instead')
        if tenant_name:
            LOG.warning('Keyword tenant_name has been deprecated, use '
                        'project_name instead')
        kwargs.setdefault('project_id', project_id)
        kwargs.setdefault('project_name', project_name)
        self._has_global_access = has_global_access
        super().__init__(
            is_admin=is_admin, user_id=user_id, **kwargs)

        self.user_name = user_name
        self.timestamp = timestamp or timeutils.utcnow()
        self._is_advsvc = is_advsvc
        if self._is_advsvc is None:
            self._is_advsvc = (self.is_admin or
                               policy_engine.check_is_advsvc(self))
        self._is_service_role = policy_engine.check_is_service_role(self)
        if self.is_admin is None:
            self.is_admin = policy_engine.check_is_admin(self)
        if not self._has_global_access:
            self._has_global_access = policy_engine.check_has_global_access(
                self)

    @property
    def tenant_id(self):
        return self.project_id

    @tenant_id.setter
    def tenant_id(self, tenant_id):
        self.project_id = tenant_id

    @property
    def tenant_name(self):
        return self.project_name

    @tenant_name.setter
    def tenant_name(self, tenant_name):
        self.project_name = tenant_name

    @property
    def is_service_role(self):
        # TODO(slaweq): we will not need to check ContextBase._is_advsvc once
        # we will get rid of the old API policies
        return self._is_service_role or self._is_advsvc

    @property
    def is_advsvc(self):
        # TODO(slaweq): this property should be removed once we will get rid
        # of old policy rules and only new, S-RBAC rules will be available as
        # then we will use ContextBase.is_service_role instead
        LOG.warning("Method 'is_advsvc' is deprecated since 2023.2 release "
                    "(neutron-lib 3.8.0) and will be removed once support for "
                    "the old RBAC API policies will be removed from Neutron. "
                    "Please use method 'is_service_role' instead.")
        return self.is_service_role

    @property
    def has_global_access(self):
        return self.is_admin or self._has_global_access

    def to_dict(self):
        context = super().to_dict()
        context.update({
            'user_id': self.user_id,
            'tenant_id': self.project_id,
            'project_id': self.project_id,
            'timestamp': str(self.timestamp),
            'tenant_name': self.project_name,
            'project_name': self.project_name,
            'user_name': self.user_name,
            'has_global_access': self.has_global_access,
        })
        return context

    def to_policy_values(self):
        values = super().to_policy_values()
        values['tenant_id'] = self.project_id
        values['is_admin'] = self.is_admin
        values['has_global_access'] = self.has_global_access

        # NOTE(jamielennox): These are almost certainly unused and non-standard
        # but kept for backwards compatibility. Remove them in Pike
        # (oslo.context from Ocata release already issues deprecation warnings
        # for non-standard keys).
        values['user'] = self.user_id
        values['tenant'] = self.project_id
        values['domain'] = self.domain_id
        values['user_domain'] = self.user_domain_id
        values['project_domain'] = self.project_domain_id
        values['tenant_name'] = self.project_name
        values['project_name'] = self.project_name
        values['user_name'] = self.user_name

        return values

    @classmethod
    def from_dict(cls, values):
        cls_obj = super().from_dict(values)
        if values.get('timestamp'):
            cls_obj.timestamp = values['timestamp']
        cls_obj.user_id = values.get('user_id', values.get('user'))
        cls_obj.tenant_id = values.get('tenant_id', values.get('project_id'))
        cls_obj.tenant_name = values.get('tenant_name')
        return cls_obj

    def elevated(self):
        """Return a version of this context with admin flag set."""
        context = copy.copy(self)
        context.is_admin = True

        context.roles = list(
            set(context.roles) | {'admin', 'member', 'reader'}
        )

        return context


@enginefacade.transaction_context_provider
class ContextBaseWithSession(ContextBase):
    pass


_TransactionConstraint = collections.namedtuple(
    '_TransactionConstraint', ['if_revision_match', 'resource', 'resource_id'])


class Context(ContextBaseWithSession):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._session = None
        self._txn_constraint = None

    @property
    def session(self):
        # TODO(ralonsoh): "Context.session" is provided by
        # "enginefacade.transaction_context_provider" when a new transaction,
        # READER or WRITER, is created. This property is just a temporary fix
        # for those transactions that are not executed inside a transaction.
        # By manually selecting the type of transaction we can speed up the
        # code because by default a writer session is always created, even
        # within read only operations.
        if hasattr(super(), 'session'):
            self._session = super().session
        if self._session is None:
            self._session = db_api.get_writer_session()
        return self._session

    def set_transaction_constraint(self, resource, resource_id, rev_number):
        """Set a revision constraint to enforce before resource_id is changed.

        :param resource: Collection name of resource (e.g. ports or networks)
        :param resource_id: The primary key ID of the individual resource that
                            should have its revision number matched before
                            allowing the transaction to proceed.
        :param rev_number: The revision_number that the resource should be at.
        """

        self._txn_constraint = _TransactionConstraint(
            if_revision_match=rev_number, resource=resource,
            resource_id=resource_id)

    def clear_transaction_constraint(self):
        self._txn_constraint = None

    def get_transaction_constraint(self):
        return self._txn_constraint


def get_admin_context():
    # NOTE(slaweq): elevated() method will set is_admin=True but setting it
    # explicity here will avoid checking in policy rules if is_admin should be
    # set to True or not
    return Context(user_id=None,
                   project_id=None,
                   is_admin=True,
                   overwrite=False).elevated()


def get_admin_context_without_session():
    # NOTE(slaweq): elevated() method will set is_admin=True but setting it
    # explicity here will avoid checking in policy rules if is_admin should be
    # set to True or not
    return ContextBase(user_id=None, project_id=None, is_admin=True).elevated()
