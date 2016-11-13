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

from webob import exc

from neutron_lib._i18n import _


def populate_project_info(attributes):
    """Ensure that both project_id and tenant_id attributes are present.

    If either project_id or tenant_id is present in attributes then ensure
    that both are present.

    If neither are present then attributes is not updated.

    :param attributes: a dictionary of resource/API attributes
    :type attributes: dict

    :return: the updated attributes dictionary
    :rtype: dict

    """
    if 'tenant_id' in attributes and 'project_id' not in attributes:
        attributes['project_id'] = attributes['tenant_id']
    elif 'project_id' in attributes and 'tenant_id' not in attributes:
        # Backward compatibility for code still using tenant_id
        attributes['tenant_id'] = attributes['project_id']

    if attributes.get('project_id') != attributes.get('tenant_id'):
        msg = _("'project_id' and 'tenant_id' do not match")
        raise exc.HTTPBadRequest(msg)

    return attributes
