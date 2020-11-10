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
import datetime
import warnings

from oslo_context import context as oslo_context
from oslo_db.sqlalchemy import enginefacade

from neutron_lib.db import api as db_api
from neutron_lib.policy import _engine as policy_engine


class ContextBase(oslo_context.RequestContext):
    """Security context and request information.

    Represents the user taking a given action within the system.

    """

    def __init__(self, user_id=None, tenant_id=None, is_admin=None,
                 timestamp=None, tenant_name=None, user_name=None,
                 is_advsvc=None, **kwargs):
        # NOTE(jamielennox): We maintain this argument in order for tests that
        # pass arguments positionally.
        kwargs.setdefault('project_id', tenant_id)
        # prefer project_name, as that's what's going to be set by
        # keystone. Fall back to tenant_name if for some reason it's blank.
        kwargs.setdefault('project_name', tenant_name)
        super().__init__(
            is_admin=is_admin, user_id=user_id, **kwargs)

        self.user_name = user_name

        if not timestamp:
            timestamp = datetime.datetime.utcnow()
        self.timestamp = timestamp
        self.is_advsvc = is_advsvc
        if self.is_advsvc is None:
            self.is_advsvc = (self.is_admin or
                              policy_engine.check_is_advsvc(self))
        if self.is_admin is None:
            self.is_admin = policy_engine.check_is_admin(self)

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
        })
        return context

    def to_policy_values(self):
        values = super().to_policy_values()
        values['tenant_id'] = self.project_id
        values['is_admin'] = self.is_admin

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
        return cls(user_id=values.get('user_id', values.get('user')),
                   tenant_id=values.get('tenant_id', values.get('project_id')),
                   is_admin=values.get('is_admin'),
                   roles=values.get('roles'),
                   timestamp=values.get('timestamp'),
                   request_id=values.get('request_id'),
                   tenant_name=values.get('tenant_name'),
                   user_name=values.get('user_name'),
                   auth_token=values.get('auth_token'))

    def elevated(self):
        """Return a version of this context with admin flag set."""
        context = copy.copy(self)
        context.is_admin = True

        if 'admin' not in [x.lower() for x in context.roles]:
            context.roles = context.roles + ["admin"]

        return context


@enginefacade.transaction_context_provider
class ContextBaseWithSession(ContextBase):
    pass


_TransactionConstraint = collections.namedtuple(
    'TransactionConstraint', ['if_revision_match', 'resource', 'resource_id'])


class Context(ContextBaseWithSession):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._session = None
        self._txn_constraint = None

    @property
    def session(self):
        # TODO(akamyshnikova): checking for session attribute won't be needed
        # when reader and writer will be used
        if hasattr(super(), 'session'):
            if self._session:
                warnings.warn('context.session is used with and without '
                              'new enginefacade. Please update the code to '
                              'use new enginefacede consistently.',
                              DeprecationWarning)
            return super().session
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
    return Context(user_id=None,
                   tenant_id=None,
                   is_admin=True,
                   overwrite=False)


def get_admin_context_without_session():
    return ContextBase(user_id=None,
                       tenant_id=None,
                       is_admin=True)
