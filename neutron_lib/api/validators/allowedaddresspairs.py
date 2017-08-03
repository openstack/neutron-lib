# Copyright 2013 VMware, Inc.  All rights reserved.
#
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
from webob import exc

from neutron_lib._i18n import _
from neutron_lib.api import validators
from neutron_lib.exceptions import allowedaddresspairs as exceptions


def _validate_allowed_address_pairs(address_pairs, valid_values=None):
    """Validates a list of allowed address pair dicts.

    Validation herein requires the caller to have registered the
    max_allowed_address_pair oslo config option in the global CONF prior
    to having this validator used.

    :param address_pairs: A list of address pair dicts to validate.
    :param valid_values: Not used.
    :returns: None
    :raises: AllowedAddressPairExhausted if the address pairs requested
    exceeds cfg.CONF.max_allowed_address_pair. AllowedAddressPairsMissingIP
    if any address pair dicts are missing and IP address.
    DuplicateAddressPairInRequest if duplicated IPs are in the list of
    address pair dicts. Otherwise a HTTPBadRequest is raised if any of
    the address pairs are invalid.
    """
    unique_check = {}
    if not isinstance(address_pairs, list):
        raise exc.HTTPBadRequest(
            _("Allowed address pairs must be a list."))
    if len(address_pairs) > cfg.CONF.max_allowed_address_pair:
        raise exceptions.AllowedAddressPairExhausted(
            quota=cfg.CONF.max_allowed_address_pair)

    for address_pair in address_pairs:
        msg = validators.validate_dict(address_pair)
        if msg:
            return msg
        # mac_address is optional, if not set we use the mac on the port
        if 'mac_address' in address_pair:
            msg = validators.validate_mac_address(address_pair['mac_address'])
            if msg:
                raise exc.HTTPBadRequest(msg)
        if 'ip_address' not in address_pair:
            raise exceptions.AllowedAddressPairsMissingIP()

        mac = address_pair.get('mac_address')
        ip_address = address_pair['ip_address']
        if (mac, ip_address) not in unique_check:
            unique_check[(mac, ip_address)] = None
        else:
            raise exceptions.DuplicateAddressPairInRequest(
                mac_address=mac, ip_address=ip_address)

        invalid_attrs = set(address_pair.keys()) - set(['mac_address',
                                                        'ip_address'])
        if invalid_attrs:
            msg = (_("Unrecognized attribute(s) '%s'") %
                   ', '.join(set(address_pair.keys()) -
                             set(['mac_address', 'ip_address'])))
            raise exc.HTTPBadRequest(msg)

        if '/' in ip_address:
            msg = validators.validate_subnet(ip_address)
        else:
            msg = validators.validate_ip_address(ip_address)
        if msg:
            raise exc.HTTPBadRequest(msg)
