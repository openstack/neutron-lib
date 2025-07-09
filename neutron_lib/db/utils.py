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

import functools

from oslo_db import exception as db_exc
from oslo_utils import excutils
import sqlalchemy
from sqlalchemy.ext import associationproxy
from sqlalchemy.orm import exc
from sqlalchemy.orm import properties

from neutron_lib._i18n import _
from neutron_lib.api import attributes
from neutron_lib import exceptions as n_exc


def get_and_validate_sort_keys(sorts, model):
    """Extract sort keys from sorts and ensure they are valid for the model.

    :param sorts: A list of (key, direction) tuples.
    :param model: A sqlalchemy ORM model class.
    :returns: A list of the extracted sort keys.
    :raises BadRequest: If a sort key attribute references another resource
        and cannot be used in the sort.
    """

    sort_keys = [s[0] for s in sorts]
    for sort_key in sort_keys:
        try:
            sort_key_attr = getattr(model, sort_key)
        except AttributeError as e:
            # Extension attributes don't support sorting. Because it
            # existed in attr_info, it will be caught here.
            msg = _("'%s' is an invalid attribute for sort key") % sort_key
            raise n_exc.BadRequest(
                resource=model.__tablename__, msg=msg) from e
        if isinstance(sort_key_attr.property,
                      properties.RelationshipProperty):
            msg = _("Attribute '%(attr)s' references another resource and "
                    "cannot be used to sort '%(resource)s' resources"
                    ) % {'attr': sort_key, 'resource': model.__tablename__}
            raise n_exc.BadRequest(resource=model.__tablename__, msg=msg)

    return sort_keys


def get_sort_dirs(sorts, page_reverse=False):
    """Extract sort directions from sorts, possibly reversed.

    :param sorts: A list of (key, direction) tuples.
    :param page_reverse: True if sort direction is reversed.
    :returns: The list of extracted sort directions optionally reversed.
    """
    if page_reverse:
        return ['desc' if s[1] else 'asc' for s in sorts]
    return ['asc' if s[1] else 'desc' for s in sorts]


def _is_nested_instance(exception, etypes):
    """Check if exception or its inner excepts are an instance of etypes."""
    return (isinstance(exception, etypes) or
            isinstance(exception, n_exc.MultipleExceptions) and
            any(_is_nested_instance(i, etypes)
                for i in exception.inner_exceptions))


def is_retriable(exception):
    """Determine if the said exception is retriable.

    :param exception: The exception to check.
    :returns: True if 'exception' is retriable, otherwise False.
    """
    if _is_nested_instance(exception,
                           (db_exc.DBDeadlock, exc.StaleDataError,
                            db_exc.DBConnectionError,
                            db_exc.DBDuplicateEntry, db_exc.RetryRequest)):
        return True
    # Look for savepoints mangled by deadlocks. See bug/1590298 for details.
    return (_is_nested_instance(exception, db_exc.DBError) and
            '1305' in str(exception))


def reraise_as_retryrequest(function):
    """Wrap the said function with a RetryRequest upon error.

    :param function: The function to wrap/decorate.
    :returns: The 'function' wrapped in a try block that will reraise any
        Exception's as a RetryRequest.
    :raises RetryRequest: If the wrapped function raises retriable exception.
    """
    @functools.wraps(function)
    def _wrapped(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            with excutils.save_and_reraise_exception() as ctx:
                if is_retriable(e):
                    ctx.reraise = False
                    raise db_exc.RetryRequest(e)
    return _wrapped


def get_marker_obj(plugin, context, resource, limit, marker):
    """Retrieve a resource marker object.

    This function is used to invoke
    plugin._get_<resource>(context, marker) and is used for pagination.

    :param plugin: The plugin processing the request.
    :param context: The request context.
    :param resource: The resource name.
    :param limit: Indicates if pagination is in effect.
    :param marker: The id of the marker object.
    :returns: The marker object associated with the plugin if limit and marker
        are given.
    """
    if limit and marker:
        return getattr(plugin, '_get_%s' % resource)(context, marker)


def resource_fields(resource, fields):
    """Return only the resource items that are in fields.

    :param resource: A resource dict.
    :param fields: A list of fields to select from the resource.
    :returns: A new dict that contains only fields from resource as well
        as its attribute project info.
    """
    if fields:
        resource = {key: item for key, item in resource.items()
                    if key in fields}
    return attributes.populate_project_info(resource)


def filter_non_model_columns(data, model):
    """Return the attributes from data which are model columns.

    :param data: The dict containing the data to filter.
    :param model: The model who's column names are used when filtering data.
    :returns: A new dict who's keys are columns in model or are association
        proxies of the model.
    """
    mapper = sqlalchemy.inspect(model)
    columns = {c.name for c in mapper.columns}
    try:
        _association_proxy = associationproxy.ASSOCIATION_PROXY
    except AttributeError:
        # SQLAlchemy 2.0
        _association_proxy = (
            associationproxy.AssociationProxyExtensionType.ASSOCIATION_PROXY)
    columns.update(d.value_attr for d in mapper.all_orm_descriptors
                   if d.extension_type is _association_proxy)
    return {k: v for (k, v)
            in data.items() if k in columns}


def model_query_scope_is_project(context, model):
    """Determine if a model should be scoped to a project.

    :param context: The context to check for admin and advsvc rights.
    :param model: The model to check the project_id of.
    :returns: True if the context has no global access and is not advsvc
        and the model has a project_id. False otherwise.
    """
    if not hasattr(model, 'project_id'):
        # If model doesn't have project_id, there is no need to scope query to
        # just one project
        return False
    if context.is_service_role:
        # For context which has 'advanced-service' rights the
        # query will not be scoped to a single project_id
        return False
    # Unless context has 'global' access the
    # resources from the database query will be scoped to a single project_id
    # context with 'admin' rights is treated as it has global access always.
    return not context.has_global_access


def model_query(context, model):
    """Query the context for the said model.

    :param context: The context to use for the query.
    :param model: The model to query for.
    :returns: A query from the said context for the said model.
    """
    query = context.session.query(model)
    # define basic filter condition for model query
    query_filter = None
    if model_query_scope_is_project(context, model):
        query_filter = (model.tenant_id == context.project_id)

    if query_filter is not None:
        query = query.filter(query_filter)
    return query
