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

import re

from oslo_config import cfg

from neutron_lib._i18n import _
from neutron_lib.api import validators
from neutron_lib import constants
from neutron_lib.db import constants as db_constants


def _validate_dns_format(data, max_len=db_constants.FQDN_FIELD_SIZE):
    # NOTE: An individual name regex instead of an entire FQDN was used
    # because its easier to make correct. The logic should validate that the
    # dns_name matches RFC 1123 (section 2.1) and RFC 952.
    if not data:
        return
    try:
        # A trailing period is allowed to indicate that a name is fully
        # qualified per RFC 1034 (page 7).
        trimmed = data[:-1] if data.endswith('.') else data
        if len(trimmed) > max_len:
            raise TypeError(
                _("'%(trimmed)s' exceeds the %(maxlen)s character FQDN "
                  "limit") % {'trimmed': trimmed, 'maxlen': max_len})
        labels = trimmed.split('.')
        for label in labels:
            if not label:
                raise TypeError(_("Encountered an empty component"))
            if label.endswith('-') or label.startswith('-'):
                raise TypeError(
                    _("Name '%s' must not start or end with a hyphen") % label)
            if not re.match(constants.DNS_LABEL_REGEX, label):
                raise TypeError(
                    _("Name '%s' must be 1-63 characters long, each of "
                      "which can only be alphanumeric or a hyphen") % label)
        # RFC 1123 hints that a TLD can't be all numeric. last is a TLD if
        # it's an FQDN.
        if len(labels) > 1 and re.match("^[0-9]+$", labels[-1]):
            raise TypeError(
                _("TLD '%s' must not be all numeric") % labels[-1])
    except TypeError as e:
        msg = _("'%(data)s' not a valid PQDN or FQDN. Reason: %(reason)s") % {
            'data': data, 'reason': e}
        return msg


def _validate_dns_name_with_dns_domain(request_dns_name, dns_domain):
    # If a PQDN was passed, make sure the FQDN that will be generated is of
    # legal size
    higher_labels = dns_domain
    if dns_domain:
        higher_labels = '.%s' % dns_domain
    higher_labels_len = len(higher_labels)
    dns_name_len = len(request_dns_name)
    if not request_dns_name.endswith('.'):
        if dns_name_len + higher_labels_len > db_constants.FQDN_FIELD_SIZE:
            msg = _("The dns_name passed is a PQDN and its size is "
                    "'%(dns_name_len)s'. The dns_domain option in "
                    "neutron.conf is set to %(dns_domain)s, with a "
                    "length of '%(higher_labels_len)s'. When the two are "
                    "concatenated to form a FQDN (with a '.' at the end), "
                    "the resulting length exceeds the maximum size "
                    "of '%(fqdn_max_len)s'"
                    ) % {'dns_name_len': dns_name_len,
                         'dns_domain': cfg.CONF.dns_domain,
                         'higher_labels_len': higher_labels_len,
                         'fqdn_max_len': db_constants.FQDN_FIELD_SIZE}
            return msg
        return

    # A FQDN was passed
    if (dns_name_len <= higher_labels_len or not
            request_dns_name.endswith(higher_labels)):
        msg = _("The dns_name passed is a FQDN. Its higher level labels "
                "must be equal to the dns_domain option in neutron.conf, "
                "that has been set to '%(dns_domain)s'. It must also "
                "include one or more valid DNS labels to the left "
                "of '%(dns_domain)s'") % {'dns_domain':
                                          cfg.CONF.dns_domain}
        return msg


def _get_dns_domain_config():
    if not cfg.CONF.dns_domain:
        return ''
    if cfg.CONF.dns_domain.endswith('.'):
        return cfg.CONF.dns_domain
    return '%s.' % cfg.CONF.dns_domain


def _get_request_dns_name(dns_name):
    dns_domain = _get_dns_domain_config()
    if (dns_domain and dns_domain != constants.DNS_DOMAIN_DEFAULT):
        # If CONF.dns_domain is the default value 'openstacklocal',
        # neutron don't let the user to assign dns_name to ports
        return dns_name
    return ''


def validate_dns_name(data, max_len=db_constants.FQDN_FIELD_SIZE):
    """Validate DNS name.

    This method validates dns name and also needs to have dns_domain in config
    because this may call a method which uses the config.

    :param data: The data to validate.
    :param max_len: An optional cap on the length of the string.
    :returns: None if data is valid, otherwise a human readable message
        indicating why validation failed.
    """
    msg = _validate_dns_format(data, max_len)
    if msg:
        return msg

    request_dns_name = _get_request_dns_name(data)
    if request_dns_name:
        dns_domain = _get_dns_domain_config()
        msg = _validate_dns_name_with_dns_domain(request_dns_name, dns_domain)
        if msg:
            return msg


def validate_fip_dns_name(data, max_len=db_constants.FQDN_FIELD_SIZE):
    """Validate DNS name for floating IP.

    :param data: The data to validate.
    :param max_len: An optional cap on the length of the string.
    :returns: None if data is valid, otherwise a human readable message
        indicating why validation failed.
    """
    msg = validators.validate_string(data)
    if msg:
        return msg
    if not data:
        return
    if data.endswith('.'):
        msg = _("'%s' is a FQDN. It should be a relative domain name") % data
        return msg
    msg = _validate_dns_format(data, max_len)
    if msg:
        return msg
    length = len(data)
    if length > max_len - 3:
        msg = _("'%(data)s' contains %(length)s characters. Adding a "
                "domain name will cause it to exceed the maximum length "
                "of a FQDN of '%(max_len)s'") % {"data": data,
                                                 "length": length,
                                                 "max_len": max_len}
        return msg


def validate_dns_domain(data, max_len=db_constants.FQDN_FIELD_SIZE):
    """Validate DNS domain.

    :param data: The data to validate.
    :param max_len: An optional cap on the length of the string.
    :returns: None if data is valid, otherwise a human readable message
        indicating why validation failed.
    """
    msg = validators.validate_string(data)
    if msg:
        return msg
    if not data:
        return
    if not data.endswith('.'):
        msg = _("'%s' is not a FQDN") % data
        return msg
    msg = _validate_dns_format(data, max_len)
    if msg:
        return msg
    length = len(data)
    if length > max_len - 2:
        msg = _("'%(data)s' contains %(length)s characters. Adding a "
                "sub-domain will cause it to exceed the maximum length of a "
                "FQDN of '%(max_len)s'") % {"data": data,
                                            "length": length,
                                            "max_len": max_len}
        return msg
