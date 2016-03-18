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

from neutron_lib import exceptions as n_exc
from sqlalchemy.orm import properties

from neutron_lib._i18n import _


def get_and_validate_sort_keys(sorts, model):
    """Extract sort keys from sorts and ensure they are valid for the model.

    :param sorts: list of (key, direction) tuples
    :param model: sqlalchemy ORM model class
    """

    sort_keys = [s[0] for s in sorts]
    for sort_key in sort_keys:
        try:
            sort_key_attr = getattr(model, sort_key)
        except AttributeError:
            # Extension attributes don't support sorting. Because it
            # existed in attr_info, it will be caught here.
            msg = _("'%s' is an invalid attribute for sort key") % sort_key
            raise n_exc.BadRequest(resource=model.__tablename__, msg=msg)
        if isinstance(sort_key_attr.property,
                      properties.RelationshipProperty):
            msg = _("Attribute '%(attr)s' references another resource and "
                    "cannot be used to sort '%(resource)s' resources"
                    ) % {'attr': sort_key, 'resource': model.__tablename__}
            raise n_exc.BadRequest(resource=model.__tablename__, msg=msg)

    return sort_keys


def get_sort_dirs(sorts, page_reverse=False):
    """Extract sort directions from sorts, possibly reversed.

    :param sorts: list of (key, direction) tuples
    :param page_reverse: True if sort direction is reversed
    """
    if page_reverse:
        return ['desc' if s[1] else 'asc' for s in sorts]
    return ['asc' if s[1] else 'desc' for s in sorts]
