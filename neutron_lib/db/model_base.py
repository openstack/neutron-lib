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

from oslo_db.sqlalchemy import models
from oslo_utils import uuidutils
import sqlalchemy as sa
from sqlalchemy import orm

from neutron_lib.db import constants as db_const


class HasProject:
    """Project mixin, add to subclasses that have a user."""

    # NOTE: project_id is just a free form string
    project_id = sa.Column(sa.String(db_const.PROJECT_ID_FIELD_SIZE),
                           index=True)

    def get_tenant_id(self):
        return self.project_id

    def set_tenant_id(self, value):
        self.project_id = value

    @orm.declared_attr
    def tenant_id(cls):
        return orm.synonym(
            'project_id',
            descriptor=property(cls.get_tenant_id, cls.set_tenant_id))


class HasProjectNoIndex(HasProject):
    """Project mixin, add to subclasses that have a user."""

    # NOTE: project_id is just a free form string
    project_id = sa.Column(sa.String(db_const.PROJECT_ID_FIELD_SIZE))


class HasProjectPrimaryKey(HasProject):
    """Project mixin, add to subclasses that have a user."""

    # NOTE: project_id is just a free form string
    project_id = sa.Column(sa.String(db_const.PROJECT_ID_FIELD_SIZE),
                           nullable=False, primary_key=True)


class HasProjectPrimaryUniqueKey(HasProject):
    """Project mixin, add to subclasses that have a user."""

    # NOTE: project_id is just a free form string
    project_id = sa.Column(sa.String(db_const.PROJECT_ID_FIELD_SIZE),
                           nullable=False, primary_key=True, unique=True)


class HasId:
    """id mixin, add to subclasses that have an id."""

    id = sa.Column(sa.String(db_const.UUID_FIELD_SIZE),
                   primary_key=True,
                   default=uuidutils.generate_uuid)


class HasStatusDescription:
    """Status with description mixin."""

    status = sa.Column(sa.String(db_const.STATUS_FIELD_SIZE),
                       nullable=False)
    status_description = sa.Column(sa.String(db_const.DESCRIPTION_FIELD_SIZE))


class _NeutronBase(models.ModelBase):
    """Base class for Neutron Models."""

    __table_args__ = {'mysql_engine': 'InnoDB'}

    def __iter__(self):
        self._i = iter(orm.object_mapper(self).columns)
        return self

    def next(self):
        n = next(self._i).name
        return n, getattr(self, n)

    __next__ = next

    def __repr__(self):
        """sqlalchemy based automatic __repr__ method."""
        items = ['{}={!r}'.format(col.name, getattr(self, col.name))
                 for col in self.__table__.columns]
        return "<{}.{}[object at {:x}] {{{}}}>".format(
            self.__class__.__module__, self.__class__.__name__,
            id(self), ', '.join(items))


class NeutronBaseV2(_NeutronBase):

    @orm.declared_attr
    def __tablename__(cls):
        # Use the pluralized name of the class as the table name.
        return cls.__name__.lower() + 's'


class BASEV2(orm.DeclarativeBase, NeutronBaseV2):
    pass
