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

import netaddr
from oslo_policy import policy
import webob.exc

from neutron_lib import exceptions

FAULT_MAP = {
    exceptions.NotFound: webob.exc.HTTPNotFound,
    exceptions.Conflict: webob.exc.HTTPConflict,
    exceptions.InUse: webob.exc.HTTPConflict,
    exceptions.BadRequest: webob.exc.HTTPBadRequest,
    exceptions.ServiceUnavailable: webob.exc.HTTPServiceUnavailable,
    exceptions.NotAuthorized: webob.exc.HTTPForbidden,
    netaddr.AddrFormatError: webob.exc.HTTPBadRequest,
    policy.PolicyNotAuthorized: webob.exc.HTTPForbidden,
    policy.InvalidScope: webob.exc.HTTPForbidden,
}
