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

import collections
import functools
import inspect
import re

import netaddr
from os_ken.lib.packet import ether_types
from oslo_config import cfg
from oslo_log import log as logging
from oslo_utils import netutils
from oslo_utils import strutils
from oslo_utils import uuidutils
from webob import exc

from neutron_lib._i18n import _
from neutron_lib import constants
from neutron_lib import exceptions as n_exc
from neutron_lib.plugins import directory


LOG = logging.getLogger(__name__)

# Used by range check to indicate no limit for a bound.
UNLIMITED = None

# Note: In order to ensure that the MAC address is unicast the first byte
# must be even.
MAC_PATTERN = "^{}[aceACE02468](:{}{{2}}){{5}}$".format(constants.HEX_ELEM,
                                                        constants.HEX_ELEM)


def _verify_dict_keys(expected_keys, target_dict, strict=True):
    """Verify expected keys in a dictionary.

    :param expected_keys: A list of keys expected to be present.
    :param target_dict: The dictionary which should be verified.
    :param strict: Specifies whether additional keys are allowed to be present.
    :returns: None if the expected keys are found. Otherwise a human readable
        message indicating why the validation failed.
    """
    if not isinstance(target_dict, dict):
        msg_data = {'target_dict': target_dict,
                    'expected_keys': expected_keys}
        msg = ("Invalid input. '%(target_dict)s' must be a dictionary "
               "with keys: %(expected_keys)s")
        LOG.debug(msg, msg_data)
        return _(msg) % msg_data

    expected_keys = set(expected_keys)
    provided_keys = set(target_dict.keys())

    predicate = expected_keys.__eq__ if strict else expected_keys.issubset

    if not predicate(provided_keys):
        msg_data = {'expected_keys': expected_keys,
                    'provided_keys': provided_keys}
        msg = ("Validation of dictionary's keys failed. "
               "Expected keys: %(expected_keys)s "
               "Provided keys: %(provided_keys)s")
        LOG.debug(msg, msg_data)
        return _(msg) % msg_data


def _collect_duplicates(data_list):
    """Collects duplicate items from a list and returns them.

    :param data_list: A list of items to check for duplicates. The list may
        include dict items.
    :returns: A list of items that are duplicates in data_list. If no
        duplicates are found, the returned list is empty.
    """
    seen = []
    dups = []
    for datum in data_list:
        if datum in seen and datum not in dups:
            dups.append(datum)
            continue
        seen.append(datum)
    return dups


def is_attr_set(attribute):
    """Determine if an attribute value is set.

    :param attribute: The attribute value to check.
    :returns: False if the attribute value is None or ATTR_NOT_SPECIFIED,
        otherwise True.
    """
    return not (attribute is None or
                attribute is constants.ATTR_NOT_SPECIFIED)


def _validate_list_of_items(item_validator, data, *args, **kwargs):
    if not isinstance(data, list):
        msg = _("'%s' is not a list") % data
        return msg

    dups = _collect_duplicates(data)

    if dups:
        msg = _("Duplicate items in the list: '%s'") % ', '.join(
            [str(d) for d in dups])
        return msg

    for item in data:
        msg = item_validator(item, *args, **kwargs)
        if msg:
            return msg


def _validate_list_of_items_non_empty(item_validator, data, *args, **kwargs):
    res = _validate_list_of_items(item_validator, data, *args, **kwargs)

    if res is not None:
        return res

    if len(data) == 0:
        msg = _("List should not be empty")
        return msg


def validate_values(data, valid_values=None, valid_values_display=None):
    """Validate that the provided 'data' is within 'valid_values'.

    :param data: The data to check within valid_values.
    :param valid_values: A collection of values that 'data' must be in to be
        valid. The collection can be any type that supports the 'in' operation.
    :param valid_values_display: A string to display that describes the valid
        values. This string is only displayed when an invalid value is
        encountered.
        If no string is provided, the string "valid_values" will be used.
    :returns: The message to return if data not in valid_values.
    :raises: TypeError if the values for 'data' or 'valid_values' are not
        compatible for comparison or doesn't have __contains__.
        If TypeError is raised this is considered a programming error and the
        inputs (data) and (valid_values) must be checked so this is never
        raised on validation.
    """

    # If valid_values is not specified we don't check against it.
    if valid_values is None:
        return

    # Check if we can use 'in' to find membership of data in valid_values
    contains = getattr(valid_values, "__contains__", None)
    if callable(contains):
        try:
            if data not in valid_values:
                valid_values_display = valid_values_display or 'valid_values'
                msg_data = {'data': data,
                            'valid_values': valid_values_display}
                msg = "%(data)s is not in %(valid_values)s"
                LOG.debug(msg, msg_data)
                return _(msg) % msg_data
        except TypeError as e:
            # This is a programming error
            msg = (_("'data' of type '%(typedata)s' and 'valid_values' "
                     "of type '%(typevalues)s' are not "
                     "compatible for comparison") %
                   {'typedata': type(data),
                    'typevalues': type(valid_values)})
            raise TypeError(msg) from e
    else:
        # This is a programming error
        msg = (_("'valid_values' does not support membership operations"))
        raise TypeError(msg)


def validate_not_empty_string_or_none(data, max_len=None):
    """Validate data is a non-empty string or None.

    :param data: The data to validate.
    :param max_len: An optional cap on the str length to validate.
    :returns: None if the data string is not None and is not an empty string,
        otherwise a human readable message as to why the string data is
        invalid.
    """
    if data is not None:
        return validate_not_empty_string(data, max_len=max_len)


def validate_not_empty_string(data, max_len=None):
    """Validate data is a non-empty/non-blank string.

    :param data: The data to validate.
    :param max_len: An optional cap on the length of the string data.
    :returns: None if the data is non-empty/non-blank, otherwise a human
        readable string message indicating why validation failed.
    """
    msg = validate_string(data, max_len=max_len)
    if msg:
        return msg
    if not data.strip():
        msg = "'%s' Blank strings are not permitted"
        LOG.debug(msg, data)
        return _(msg) % data


def validate_string_or_none(data, max_len=None):
    """Validate data is a string or None.

    :param data: The data to validate.
    :param max_len: An optional cap on the length of the string data.
    :returns: None if the data is None or a valid string, otherwise a human
        readable message indicating why validation failed.
    """
    if data is not None:
        return validate_string(data, max_len=max_len)


def validate_string(data, max_len=None):
    """Validate data is a string object optionally capping it length.

    :param data: The data to validate.
    :param max_len: An optional cap on the length of the string.
    :returns: None if the data is a valid string type and (optionally) within
        the given max_len. Otherwise a human readable message indicating why
        the data is invalid.
    """
    if not isinstance(data, str):
        msg = "'%s' is not a valid string"
        LOG.debug(msg, data)
        return _(msg) % data

    if max_len is not None and len(data) > max_len:
        msg_data = {'data': data, 'max_len': max_len}
        msg = "'%(data)s' exceeds maximum length of %(max_len)s"
        LOG.debug(msg, msg_data)
        return _(msg) % msg_data


_validate_list_of_unique_strings = functools.partial(_validate_list_of_items,
                                                     validate_string)


# NOTE(boden): stubbed out for docstring comments.
def validate_list_of_unique_strings(data, max_len=None):
    """Validate data is a list of unique strings.

    :param data: The data to validate.
    :param max_len: An optional cap on the length of the string.
    :returns: None if the data is a list of non-empty/non-blank strings,
        otherwise a human readable message indicating why validation failed.
    """
    return _validate_list_of_unique_strings(data, max_len=max_len)


def validate_oneline_not_empty_string(data, max_len=None):
    """Validate data is a non-empty string without newline character.

    :param data: The data to validate.
    :param max_len: An optional cap on the length of the string.
    :returns: None if the data is a string without newline character,
        otherwise a human readable message indicating why validation failed.
    """
    msg = validate_not_empty_string(data, max_len=max_len)
    if msg:
        return msg
    if len(data.splitlines()) > 1:
        msg = "Multi-line string is not allowed: '%s'"
        LOG.debug(msg, data)
        return _(msg) % data


def validate_oneline_not_empty_string_or_none(data, max_len=None):
    """Validate data is a non-empty string without newline character or None.

    :param data: The data to validate.
    :param max_len: An optional cap on the length of the string data.
    :returns: None if the data is None or a valid string without newline
        character, otherwise a human readable message indicating why
        validation failed.
    """
    if data is not None:
        return validate_oneline_not_empty_string(data, max_len=max_len)


def validate_boolean(data, valid_values=None):
    """Validate data is a python bool compatible object.

    :param data: The data to validate.
    :param valid_values: Not used!
    :return: None if the value can be converted to a bool, otherwise a
        human readable message indicating why data is invalid.
    """
    try:
        strutils.bool_from_string(data, strict=True)
    except ValueError:
        msg = "'%s' is not a valid boolean value"
        LOG.debug(msg, data)
        return _(msg) % data


def validate_integer(data, valid_values=None):
    """This function validates if the data is an integer.

    It checks both number or string provided to validate it's an
    integer and returns a message with the error if it's not

    :param data: The string or number to validate as integer.
    :param valid_values: values to limit the 'data' to.
    :returns: None if data is an integer, otherwise a human readable message
        indicating why validation failed..
    """

    if valid_values is not None:
        msg = validate_values(data=data, valid_values=valid_values)
        if msg:
            return msg

    msg = "'%s' is not an integer"
    try:
        fl_n = float(data)
        int_n = int(data)
    except (ValueError, TypeError, OverflowError):
        LOG.debug(msg, data)
        return _(msg) % data

    # Fail test if non equal or boolean
    if fl_n != int_n:
        LOG.debug(msg)
        return _(msg) % data
    elif isinstance(data, bool):
        msg = "'%s' is not an integer:boolean"
        LOG.debug(msg, data)
        return _(msg) % data


def validate_range(data, valid_values=None):
    """Check that integer value is within a range provided.

    Test is inclusive. Allows either limit to be ignored, to allow
    checking ranges where only the lower or upper limit matter.
    It is expected that the limits provided are valid integers or
    the value None.

    :param data: The data to validate.
    :param valid_values: A list of 2 elements where element 0 is the min
        value the int data can have and element 1 is the max.
    :returns: None if the data is a valid int in the given range, otherwise
        a human readable message as to why validation failed.
    """

    min_value = valid_values[0]
    max_value = valid_values[1]
    try:
        data = int(data)
    except (ValueError, TypeError):
        msg = "'%s' is not an integer"
        LOG.debug(msg, data)
        return _(msg) % data
    if min_value is not UNLIMITED and data < min_value:
        msg_data = {'data': data, 'limit': min_value}
        msg = "'%(data)s' is too small - must be at least '%(limit)d'"
        LOG.debug(msg, msg_data)
        return _(msg) % msg_data
    if max_value is not UNLIMITED and data > max_value:
        msg_data = {'data': data, 'limit': max_value}
        msg = "'%(data)s' is too large - must be no larger than '%(limit)d'"
        LOG.debug(msg, msg_data)
        return _(msg) % msg_data


def validate_range_or_none(data, valid_values=None):
    """Check that the provided value is none or a ranged integer"""

    if data is not None:
        return validate_range(data, valid_values)


def validate_no_whitespace(data):
    """Validates that input has no whitespace.

    :param data: The data to validate. Must be a python string type suitable
        for searching via regex.
    :returns: The data itself.
    :raises InvalidInput: If the data contains whitespace.
    """
    if re.search(r'\s', data):
        msg = "'%s' contains whitespace"
        LOG.debug(msg, data)
        raise n_exc.InvalidInput(error_message=_(msg) % data)
    return data


def validate_mac_address(data, valid_values=None):
    """Validate data is a MAC address.

    :param data: The data to validate.
    :param valid_values: Not used!
    :returns: None if the data is a valid MAC address, otherwise a human
        readable message as to why validation failed.
    """
    try:
        valid_mac = netaddr.valid_mac(validate_no_whitespace(data))
    except Exception:
        valid_mac = False

    if valid_mac:
        valid_mac = (netaddr.EUI(data) not in
                     map(netaddr.EUI, constants.INVALID_MAC_ADDRESSES))
    # TODO(arosen): The code in this file should be refactored
    # so it catches the correct exceptions. validate_no_whitespace
    # raises AttributeError if data is None.
    if not valid_mac:
        msg = "'%s' is not a valid MAC address"
        LOG.debug(msg, data)
        return _(msg) % data


def validate_mac_address_or_none(data, valid_values=None):
    """Validate data is a MAC address if the data isn't None.

    :param data: The data to validate.
    :param valid_values: Not used!
    :returns: None if the data is None or a valid MAC address, otherwise
        a human readable message indicating why validation failed.
    """
    if data is not None:
        return validate_mac_address(data, valid_values)


def validate_ip_address(data, valid_values=None):
    """Validate data is an IP address.

    :param data: The data to validate.
    :param valid_values: Not used!
    :returns: None if data is an IP address, otherwise a human readable
        message indicating why data isn't an IP address.
    """
    msg = None
    msg_data = data
    try:
        try:
            # netaddr.core.ZEROFILL is only applicable to IPv4.
            # it will remove leading zeros from IPv4 address octets.
            ip = netaddr.IPAddress(validate_no_whitespace(data),
                                   flags=netaddr.core.ZEROFILL)
        except ValueError:
            # It could be an IPv6 address and netaddr.core.ZEROFILL flag
            # cannot be used in netaddr>=1.0.0
            ip = netaddr.IPAddress(validate_no_whitespace(data))
        # The followings are quick checks for IPv6 (has ':') and
        # IPv4.  (has 3 periods like 'xx.xx.xx.xx')
        # NOTE(yamamoto): netaddr uses libraries provided by the underlying
        # platform to convert addresses.  For example, inet_aton(3).
        # Some platforms, including NetBSD and OS X, have inet_aton
        # implementation which accepts more varying forms of addresses than
        # we want to accept here.  The following check is to reject such
        # addresses.  For Example:
        #   >>> netaddr.IPAddress('1' * 59)
        #   IPAddress('199.28.113.199')
        #   >>> netaddr.IPAddress(str(int('1' * 59) & 0xffffffff))
        #   IPAddress('199.28.113.199')
        #   >>>
        if ':' not in data and data.count('.') != 3:
            msg = "'%s' is not a valid IP address"
        # A leading '0' in IPv4 address may be interpreted as an octal number,
        # e.g. 011 octal is 9 decimal. Since there is no standard saying
        # whether IP address with leading '0's should be interpreted as octal
        # or decimal, hence we reject leading '0's to avoid ambiguity.
        elif ip.version == 4 and str(ip) != data:
            msg_data = {"data": data, "ip": ip}
            msg = ("'%(data)s' is not an accepted IP address, "
                   "'%(ip)s' is recommended")
    except Exception:
        msg = "'%s' is not a valid IP address"
    if msg:
        LOG.debug(msg, msg_data)
        msg = _(msg) % msg_data
    return msg


def _validate_any_key_spec(data, key_specs=None):
    """Validate a dict matches at least 1 key spec.

    :param data: The dict to validate.
    :param key_specs: An iterable collection of key spec dicts used to validate
        data.
    :returns: None if at least 1 of the key_specs matches data, otherwise
        a message is returned indicating data could not be matched with any
        of the key_specs.
    """
    for spec in key_specs:
        if validate_dict(data, spec) is None:
            return None
    msg = "No valid key specs matched for: %s"
    LOG.debug(msg, data)
    return _(msg) % data


def validate_any_key_specs_or_none(data, key_specs=None):
    """Validate each dict in a list matches at least 1 key_spec.

    :param data: The list of dicts to validate.
    :param key_specs: An iterable collection of key spec dicts that is used
        to check each dict in data.
    :returns: None.
    :raises InvalidInput: If any of the dicts in data do not match at least
        1 of the key_specs given.
    """
    if data is None:
        return

    def dict_validator(data_dict):
        msg = _validate_any_key_spec(data_dict, key_specs=key_specs)
        if msg:
            raise n_exc.InvalidInput(error_message=msg)

    msg = _validate_list_of_items(dict_validator, data)
    if msg:
        raise n_exc.InvalidInput(error_message=msg)


def validate_ip_pools(data, valid_values=None):
    """Validate that start and end IP addresses are present.

    In addition to this the IP addresses will also be validated.

    :param data: The data to validate. Must be a list-like structure of
        IP pool dicts that each have a 'start' and 'end' key value.
    :param valid_values: Not used!
    :returns: None if data is a valid list of IP pools, otherwise a message
        indicating why the data is invalid.
    """
    if not isinstance(data, list):
        msg = "Invalid data format for IP pool: '%s'"
        LOG.debug(msg, data)
        return _(msg) % data

    expected_keys = ['start', 'end']
    for ip_pool in data:
        msg = _verify_dict_keys(expected_keys, ip_pool)
        if msg:
            return msg
        for k in expected_keys:
            msg = validate_ip_address(ip_pool[k])
            if msg:
                return msg


def validate_fixed_ips(data, valid_values=None):
    """Validate data is a list of fixed IP dicts.

    In addition this function validates the ip_address and subnet_id
    if present in each fixed IP dict.

    :param data: The data to validate.
    :param valid_values: Not used!
    :returns: None if data is a valid list of fixed IP dicts. Otherwise a
        human readable message is returned indicating why validation failed.
    """
    if not isinstance(data, list):
        msg = "Invalid data format for fixed IP: '%s'"
        LOG.debug(msg, data)
        return _(msg) % data

    ips = []
    for fixed_ip in data:
        if not isinstance(fixed_ip, dict):
            msg = "Invalid data format for fixed IP: '%s'"
            LOG.debug(msg, fixed_ip)
            return _(msg) % fixed_ip
        if 'ip_address' in fixed_ip:
            # Ensure that duplicate entries are not set - just checking IP
            # suffices. Duplicate subnet_id's are legitimate.
            fixed_ip_address = fixed_ip['ip_address']
            if fixed_ip_address in ips:
                msg = "Duplicate IP address '%s'"
                LOG.debug(msg, fixed_ip_address)
                msg = _(msg) % fixed_ip_address
            else:
                msg = validate_ip_address(fixed_ip_address)
            if msg:
                return msg
            ips.append(fixed_ip_address)
        if 'subnet_id' in fixed_ip:
            msg = validate_uuid(fixed_ip['subnet_id'])
            if msg:
                return msg


def validate_nameservers(data, valid_values=None):
    """Validate a list of unique IP addresses.

    :param data: The data to validate.
    :param valid_values: Not used!
    :returns: None if data is a list of valid IP addresses, otherwise
        a human readable message is returned indicating why validation failed.
    """
    if not hasattr(data, '__iter__'):
        msg = "Invalid data format for nameserver: '%s'"
        LOG.debug(msg, data)
        return _(msg) % data

    hosts = []
    for host in data:
        # This must be an IP address only
        msg = validate_ip_address(host)
        if msg:
            msg_data = {'host': host, 'msg': msg}
            msg = "'%(host)s' is not a valid nameserver. %(msg)s"
            LOG.debug(msg, msg_data)
            return _(msg) % msg_data
        if host in hosts:
            msg = "Duplicate nameserver '%s'"
            LOG.debug(msg, host)
            return _(msg) % host
        hosts.append(host)


def validate_hostroutes(data, valid_values=None):
    """Validate a list of unique host route dicts.

    :param data: The data to validate. To be valid it must be a list like
        structure of host route dicts, each containing 'destination' and
        'nexthop' key values.
    :param valid_values: Not used!
    :returns: None if data is a valid list of unique host route dicts,
        otherwise a human readable message indicating why validation failed.
    """
    if not isinstance(data, list):
        msg = "Invalid data format for hostroute: '%s'"
        LOG.debug(msg, data)
        return _(msg) % data

    expected_keys = ['destination', 'nexthop']
    hostroutes = []
    for hostroute in data:
        msg = _verify_dict_keys(expected_keys, hostroute)
        if msg:
            return msg
        msg = validate_route_cidr(hostroute['destination'])
        if msg:
            return msg
        msg = validate_ip_address(hostroute['nexthop'])
        if msg:
            return msg
        if hostroute in hostroutes:
            msg = "Duplicate hostroute '%s'"
            LOG.debug(msg, hostroute)
            return _(msg) % hostroute
        hostroutes.append(hostroute)


def validate_ip_address_or_none(data, valid_values=None):
    """Validate data is an IP address or None.

    :param data: The data to validate.
    :param valid_values: An optional list of values data may take on.
    :return: None if data is None or a valid IP address, otherwise a
        human readable message indicating why the data is invalid.
    """
    if data is not None:
        return validate_ip_address(data, valid_values)


def validate_ip_or_subnet_or_none(data, valid_values=None):
    """Validate data is an IP address, a valid IP subnet string, or None.

    :param data: The data to validate.
    :param valid_values: Not used!
    :return: None if data is None or a valid IP address or a valid IP subnet,
        otherwise a human readable message indicating why the data is neither
        an IP address nor IP subnet.
    """
    msg_ip = validate_ip_address_or_none(data)
    msg_subnet = validate_subnet_or_none(data)
    if msg_ip is not None and msg_subnet is not None:
        return _("'%(data)s' is neither a valid IP address, nor "
                 "is it a valid IP subnet") % {'data': data}


def validate_subnet(data, valid_values=None):
    """Validate data is an IP network subnet string.

    :param data: The data to validate.
    :param valid_values: Not used!
    :returns: None if data is valid IP network address. Otherwise a human
        readable message as to why data is invalid.
    """
    try:
        net = netaddr.IPNetwork(validate_no_whitespace(data))
        # TODO(ihar): remove this explicit check when the minimal version of
        # netaddr is 1.0.0 that enforces the input format more strictly
        if '/' not in data or (net.version == 4 and str(net) != data):
            raise n_exc.InvalidInput
    except Exception:
        msg = "'%s' is not a valid IP subnet"
        LOG.debug(msg, data)
        return _(msg) % data


def validate_route_cidr(data, valid_values=None):
    """Validate data is a proper CIDR string.

    :param data: The data to validate.
    :param valid_values: Not used!
    :returns: None if data is valid CIDR. Otherwise a human
              readable message as to why data is invalid.
    """
    msg = "'%s' is not a valid CIDR"
    try:
        net = netaddr.IPNetwork(validate_no_whitespace(data))
        # TODO(ihar): remove this explicit check when the minimal version of
        # netaddr is 1.0.0 that enforces the input format more strictly
        if '/' not in data or (net.network != net.ip):
            raise n_exc.InvalidInput
        if net.is_loopback():
            msg = "'%s' is not a routable CIDR"
            raise n_exc.InvalidInput
    except Exception:
        LOG.debug(msg, data)
        return _(msg) % data


def validate_subnet_or_none(data, valid_values=None):
    """Validate data is a valid subnet address string or None.

    :param data: The data to validate.
    :param valid_values: The optional list of values data may take on.
    :returns: None if data is None or a valid subnet, otherwise a human
        readable message as to why data is invalid.
    """
    if data is not None:
        return validate_subnet(data, valid_values)


_validate_subnet_list = functools.partial(_validate_list_of_items,
                                          validate_subnet)


# NOTE(boden): subbed out for docstring comments.
def validate_subnet_list(data, valid_values=None):
    """Validate data is a list of subnet dicts.

    :param data: The data to validate.
    :param valid_values: Not used!
    :returns: None if data is a valid list of subnet dicts, otherwise a human
        readable message as to why the data is invalid.
    """
    return _validate_subnet_list(data, valid_values)


def validate_subnet_list_or_none(data, key_specs=None):
    """Validate data is a list of subnet dicts or None.

    :param data: The data to validate.
    :param key_specs: Not used!
    :returns: None if data is None or a valid list of subnet dicts, otherwise
        a human readable message as to why the data is invalid.
    """
    if data is not None:
        return validate_subnet_list(data, key_specs)


def validate_regex(data, valid_values=None):
    """Validate data is matched against a regex.

    :param data: The data to validate.
    :param valid_values: The regular expression to use with re.match on
        the data.
    :returns: None if data contains matches for valid_values, otherwise a
        human readable message as to why data is invalid.
    """
    try:
        if re.match(valid_values, data):
            return
    except TypeError:
        pass

    msg = "'%s' is not a valid input"
    LOG.debug(msg, data)
    return _(msg) % data


def validate_regex_or_none(data, valid_values=None):
    """Validate data is None or matched against a regex.

    :param data: The data to validate.
    :param valid_values: The regular expression to use with re.match on
        the data.
    :returns: None if data is None or contains matches for valid_values,
        otherwise a human readable message as to why data is invalid.
    """
    if data is not None:
        return validate_regex(data, valid_values)


def validate_list_of_regex_or_none(data, valid_values=None):
    """Validate data is None or a list of items matching regex.

    :param data: A list of data to validate.
    :param valid_values: The regular expression to use with re.match on
        each element of the data.
    :returns: None if data is None or contains matches for valid_values,
        otherwise a human readable message as to why data is invalid.
    """
    if data is not None:
        return _validate_list_of_items(validate_regex, data, valid_values)


def validate_subnetpool_id(data, valid_values=None):
    """Validate data is valid subnet pool ID.

    :param data: The data to validate.
    :param valid_values: Not used!
    :returns: None if data is a valid subnet pool ID, otherwise a
        human readable message as to why it's invalid.
    """
    if data != constants.IPV6_PD_POOL_ID:
        return validate_uuid_or_none(data, valid_values)


def validate_subnetpool_id_or_none(data, valid_values=None):
    """Validate data is valid subnet pool ID or None.

    :param data: The data to validate.
    :param valid_values: Not used!
    :returns: None if data is a valid subnet pool ID or None, otherwise a
        human readable message as to why it's invalid.
    """
    if data is not None:
        return validate_subnetpool_id(data, valid_values)


def validate_uuid(data, valid_values=None):
    """Validate data is UUID like.

    :param data: The data to validate.
    :param valid_values: Not used!
    :returns: None if data is UUID like in form, otherwise a human readable
        message indicating why data is invalid.
    """
    if not uuidutils.is_uuid_like(data):
        msg = "'%s' is not a valid UUID"
        LOG.debug(msg, data)
        return _(msg) % data


def validate_uuid_or_none(data, valid_values=None):
    """Validate data is UUID like or None.

    :param data: The data to validate.
    :param valid_values: Not used!
    :returns: None if data is UUID like in form or None, otherwise a human
        readable message indicating why data is invalid.
    """
    if data is not None:
        return validate_uuid(data)


_validate_uuid_list = functools.partial(_validate_list_of_items,
                                        validate_uuid)


# NOTE(boden): subbed out for docstring comments.
def validate_uuid_list(data, valid_values=None):
    """Validate data is a list of UUID like values.

    :param data: The data to validate.
    :param valid_values: Not used!
    :returns: None if data is an iterable that contains valid UUID values,
        otherwise a message is returned indicating why validation failed.
    """
    return _validate_uuid_list(data, valid_values)


def validate_uuid_list_non_empty(data, valid_values=None):
    """Validate data is a non-empty list of UUID like values.

    :param data: The data to validate.
    :param valid_values: Not used!
    :returns: None if data is a non-empty iterable that contains valid UUID
        values, otherwise a message is returned indicating why validation
        failed.
    """
    return _validate_list_of_items_non_empty(validate_uuid, data)


def _extract_validator(key_validator):
    # Find validator function in key validation spec
    #
    # TODO(salv-orlando): Structure of dict attributes should be improved
    # to avoid iterating over items
    for (k, v) in key_validator.items():
        if k.startswith('type:'):
            (validator_name, validator_params) = (k, v)
            try:
                return (validator_name,
                        validators[validator_name],
                        validator_params)
            except KeyError as e:
                raise UndefinedValidator(validator_name) from e
    return None, None, None


def _validate_dict_item(key, key_validator, data):
    # Find conversion function, if any, and apply it
    conv_func = key_validator.get('convert_to')
    if conv_func:
        data[key] = conv_func(data.get(key))
    try:
        dummy_, val_func, val_params = _extract_validator(key_validator)
        if val_func:
            return val_func(data.get(key), val_params)
        # NOTE(tmorin): here we silently omit to validate a key for which
        # no type validator has been defined
    except UndefinedValidator as e:
        # NOTE(tmorin): Should we really return an API error on such
        # an issue. Wouldn't InternalServer error be more natural ?
        LOG.debug(e.message)
        return e.message


def validate_dict(data, key_specs=None):
    """Validate data is a dict optionally containing a specific set of keys.

    :param data: The data to validate.
    :param key_specs: The optional list of keys that must be contained in
        data.
    :returns: None if data is a dict and (optionally) contains only key_specs.
        Otherwise a human readable message is returned indicating why data is
        not valid.
    """
    if not isinstance(data, dict):
        msg = "'%s' is not a dictionary"
        LOG.debug(msg, data)
        return _(msg) % data
    # Do not perform any further validation, if no constraints are supplied
    if not key_specs:
        return

    # Check whether all required keys are present
    required_keys = [key for key, spec in key_specs.items()
                     if spec.get('required')]

    if required_keys:
        msg = _verify_dict_keys(required_keys, data, False)
        if msg:
            return msg

    # Check whether unexpected keys are supplied in data
    unexpected_keys = [key for key in data if key not in key_specs]
    if unexpected_keys:
        msg_data = ', '.join(unexpected_keys)
        msg = "Unexpected keys supplied: %s"
        LOG.debug(msg, msg_data)
        return _(msg) % msg_data

    # Perform validation and conversion of all values
    # according to the specifications.
    for key, key_validator in [(k, v) for k, v in key_specs.items()
                               if k in data]:
        msg = _validate_dict_item(key, key_validator, data)
        if msg:
            return msg


def validate_dict_or_none(data, key_specs=None):
    """Validate data is None or a dict containing a specific set of keys.

    :param data: The data to validate.
    :param key_specs: The optional list of keys that must be contained in
        data.
    :returns: None if data is None or a dict  that (optionally) contains
        all key_specs. Otherwise a human readable message is returned
        indicating why data is not valid.
    """
    if data is not None:
        return validate_dict(data, key_specs)


def validate_dict_or_empty(data, key_specs=None):
    """Validate data is {} or a dict containing a specific set of keys.

    :param data: The data to validate.
    :param key_specs: The optional list of keys that must be contained in
        data.
    :returns: None if data is {} or a dict (optionally) containing
        only key_specs. Otherwise a human readable message is returned
        indicating why data is not valid.
    """
    if data != {}:
        return validate_dict(data, key_specs)


def validate_dict_or_nodata(data, key_specs=None):
    """Validate no data or a dict containing a specific set of keys.

    :param data: The data to validate. May be None.
    :param key_specs: The optional list of keys that must be contained in
        data.
    :returns: None if no data/empty dict or a dict and (optionally) contains
        all key_specs. Otherwise a human readable message is returned
        indicating why data is not valid.
    """
    if data:
        return validate_dict(data, key_specs)


def validate_non_negative(data, valid_values=None):
    """Validate data is a positive int.

    :param data: The data to validate
    :param valid_values: Not used!
    :returns: None if data is an int and is positive, otherwise a human
        readable message as to why data is invalid.
    """
    try:
        data = int(data)
    except (ValueError, TypeError):
        msg = "'%s' is not an integer"
        LOG.debug(msg, data)
        return _(msg) % data

    if data < 0:
        msg = "'%s' should be non-negative"
        LOG.debug(msg, data)
        return _(msg) % data


def validate_port_range_or_none(data, valid_values=None):
    """Validate data is a range of TCP/UDP port numbers

    :param data: The data to validate
    :param valid_values: valid port range, default is [0, 65535]
    :returns: None if data is a valid port between the values defined in the
        valid_values param, or two valid ports between the values defined in
        the valid_values param with a colon between them, otherwise a human
        readable message as to why data is invalid.
    """
    if data is None:
        return

    min_value, max_value = valid_values or [0, 65535]

    data = str(data)
    ports = data.split(':')
    if len(ports) > 2:
        msg = "Port range must be two integers separated by a colon"
        LOG.debug(msg)
        return _(msg)
    for p in ports:
        if len(p) == 0:
            msg = "Port range must be two integers separated by a colon"
            LOG.debug(msg)
            return _(msg)
        if not netutils.is_valid_port(p):
            msg = "Invalid port: %s"
            LOG.debug(msg, p)
            return _(msg) % p
        if max_value < int(p) or int(p) < min_value:
            msg = "Invalid port: %s, the port must be in the range [%s, %s]"
            LOG.debug(msg, p, min_value, max_value)
            return _(msg) % (p, min_value, max_value)
    if len(ports) > 1 and int(ports[0]) > int(ports[1]):
        msg = "First port in a port range must be lower than the second port"
        LOG.debug(msg)
        return _(msg)


def validate_subports(data, valid_values=None):
    """Validate data is a list of subnet port dicts.

    :param data: The data to validate.
    :param valid_values: Not used!
    :returns: None if data is a list of subport dicts each with a unique valid
        port_id, segmentation_id and segmentation_type. Otherwise a human
        readable message is returned indicating why the data is invalid.
    """
    if not isinstance(data, list):
        msg = "Invalid data format for subports: '%s' is not a list"
        LOG.debug(msg, data)
        return _(msg) % data

    subport_ids = set()
    segmentations = collections.defaultdict(set)
    for subport in data:
        if not isinstance(subport, dict):
            msg = "Invalid data format for subport: '%s' is not a dict"
            LOG.debug(msg, subport)
            return _(msg) % subport

        # Expect a non duplicated and valid port_id for the subport
        if 'port_id' not in subport:
            msg = "A valid port UUID must be specified"
            LOG.debug(msg)
            return _(msg)
        elif validate_uuid(subport["port_id"]):
            msg = _("Invalid UUID for subport: '%s'") % subport["port_id"]
            return msg
        elif subport["port_id"] in subport_ids:
            msg = _("Non unique UUID for subport: '%s'") % subport["port_id"]
            return msg
        subport_ids.add(subport["port_id"])

        # Validate that both segmentation ID and segmentation type are
        # specified, and that the client does not duplicate segmentation
        # IDs (unless it is explicitly asked to inherit segmentation
        # details from the underlying subport's network).
        segmentation_type = subport.get("segmentation_type")
        if segmentation_type == 'inherit':
            return
        segmentation_id = subport.get("segmentation_id")
        if ((not segmentation_type or segmentation_id is None) and
                len(subport) > 1):
            msg = ("Invalid subport details '%s': missing segmentation "
                   "information. Must specify both segmentation_id and "
                   "segmentation_type")
            LOG.debug(msg, subport)
            return _(msg) % subport
        if segmentation_id in segmentations.get(segmentation_type, []):
            msg_data = {"seg_id": segmentation_id,
                        "subport": subport["port_id"]}
            msg = ("Segmentation ID '%(seg_id)s' for '%(subport)s' is not "
                   "unique")
            LOG.debug(msg, msg_data)
            return _(msg) % msg_data
        if segmentation_id is not None:
            segmentations[segmentation_type].add(segmentation_id)


def validate_service_plugin_type(data, valid_values=None):
    """Validates data is a valid service plugin.

    :param data: The service plugin type to validate.
    :param valid_values: Not used.
    :returns: None if data is a valid service plugin known to the plugin
        directory.
    :raises: InvalidServiceType if data is not a service known by the
        plugin directory.
    """
    if not directory.get_plugin(data):
        raise n_exc.InvalidServiceType(service_type=data)


def validate_subnet_service_types(service_types, valid_values=None):
    if service_types:
        if not isinstance(service_types, list):
            raise exc.HTTPBadRequest(
                _("Subnet service types must be a list."))

        # Include standard prefixes
        prefixes = list(constants.DEVICE_OWNER_PREFIXES)
        prefixes += constants.DEVICE_OWNER_COMPUTE_PREFIX

        for service_type in service_types:
            if not isinstance(service_type, str):
                raise n_exc.InvalidInputSubnetServiceType(
                    service_type=service_type)
            if not service_type.startswith(tuple(prefixes)):
                raise n_exc.InvalidSubnetServiceType(service_type=service_type)


def validate_ethertype(ethertype, valid_values=None):
    """Validates ethertype is a valid ethertype.

    :param ethertype: Ethertype to validate.
    :returns: None if data is a valid ethertype.  Otherwise a human-readable
        message indicating that the data is not a valid ethertype.
    """

    if cfg.CONF.sg_filter_ethertypes:
        os_ken_ethertypes = ether_types.__dict__
        try:
            # Use the ethertype constants from os_ken with the special
            # exception of 'IPv4', which appears as 'ETH_TYPE_IP' in os_ken.
            # Be case-insensitive.
            ethertype_str = str(ethertype).upper()
            if ethertype_str == "IPV4":
                ethertype_str = "IP"
            ethertype_name = 'ETH_TYPE_' + ethertype_str
            ethertype = os_ken_ethertypes.get(ethertype_name, ethertype)
        except TypeError:
            # Value of ethertype cannot be coerced into a string, like None
            pass
        try:
            if isinstance(ethertype, str):
                ethertype = int(ethertype, 16)
            if (isinstance(ethertype, int) and
                    constants.ETHERTYPE_MIN <= ethertype <=
                    constants.ETHERTYPE_MAX):
                return None
        except ValueError:
            pass
        msg = ("Ethertype %s is not a two octet hexadecimal "
               "number or ethertype name.")
        LOG.debug(msg, ethertype)
        return _(msg) % ethertype
    else:
        if ethertype in constants.VALID_ETHERTYPES:
            return None
        valids = ','.join(map(str, constants.VALID_ETHERTYPES))
        msg_data = {'ethertype': ethertype, 'valid_ethertypes': valids}
        msg = ("Ethertype %(ethertype)s is not a valid ethertype, must be "
               "one of %(valid_ethertypes)s.")
        LOG.debug(msg, msg_data)
        return _(msg) % msg_data


def validate_list_of_dict_or_nodata(data, valid_values=None):
    """Validate a list of dictionaries.

    :param data: The data to validate. The data could be an empty list or None.
    :param valid_values: The optional list of keys that must be contained in
        data.
    :returns: None if valid, error string otherwise.
    """
    if data:
        return _validate_list_of_items(validate_dict_or_nodata, data,
                                       **valid_values)


# Dictionary that maintains a list of validation functions
validators = {'type:dict': validate_dict,
              'type:dict_or_none': validate_dict_or_none,
              'type:dict_or_empty': validate_dict_or_empty,
              'type:dict_or_nodata': validate_dict_or_nodata,
              'type:ethertype': validate_ethertype,
              'type:fixed_ips': validate_fixed_ips,
              'type:hostroutes': validate_hostroutes,
              'type:ip_address': validate_ip_address,
              'type:ip_address_or_none': validate_ip_address_or_none,
              'type:ip_or_subnet_or_none': validate_ip_or_subnet_or_none,
              'type:ip_pools': validate_ip_pools,
              'type:list_of_regex_or_none': validate_list_of_regex_or_none,
              'type:mac_address': validate_mac_address,
              'type:mac_address_or_none': validate_mac_address_or_none,
              'type:nameservers': validate_nameservers,
              'type:non_negative': validate_non_negative,
              'type:port_range': validate_port_range_or_none,
              'type:range': validate_range,
              'type:range_or_none': validate_range_or_none,
              'type:regex': validate_regex,
              'type:regex_or_none': validate_regex_or_none,
              'type:string': validate_string,
              'type:string_or_none': validate_string_or_none,
              'type:not_empty_string': validate_not_empty_string,
              'type:not_empty_string_or_none':
              validate_not_empty_string_or_none,
              'type:oneline_not_empty_string':
              validate_oneline_not_empty_string,
              'type:oneline_not_empty_string_or_none':
              validate_oneline_not_empty_string_or_none,
              'type:subnet': validate_subnet,
              'type:subnet_list': validate_subnet_list,
              'type:subnet_or_none': validate_subnet_or_none,
              'type:subnetpool_id': validate_subnetpool_id,
              'type:subnetpool_id_or_none': validate_subnetpool_id_or_none,
              'type:subports': validate_subports,
              'type:uuid': validate_uuid,
              'type:uuid_or_none': validate_uuid_or_none,
              'type:uuid_list': validate_uuid_list,
              'type:uuid_list_non_empty': validate_uuid_list_non_empty,
              'type:values': validate_values,
              'type:boolean': validate_boolean,
              'type:integer': validate_integer,
              'type:list_of_unique_strings': validate_list_of_unique_strings,
              'type:list_of_any_key_specs_or_none':
                  validate_any_key_specs_or_none,
              'type:service_plugin_type': validate_service_plugin_type,
              'type:list_of_subnets_or_none': validate_subnet_list_or_none,
              'type:list_of_subnet_service_types':
                  validate_subnet_service_types,
              'type:list_of_dict_or_nodata': validate_list_of_dict_or_nodata,
              }


class UndefinedValidator(Exception):

    def __init__(self, validator_name):
        self.validator_name = validator_name
        self.message = _("Validator '%s' does not exist") % self.validator_name


def _to_validation_type(validation_type):
    return (validation_type
            if validation_type.startswith('type:')
            else 'type:' + validation_type)


def get_validator(validation_type, default=None):
    """Get a registered validator by type.

    :param validation_type: The type to retrieve the validator for.
    :param default: A default value to return if the validator is
        not registered.
    :return: The validator if registered, otherwise the default value.
    """
    return validators.get(_to_validation_type(validation_type), default)


def add_validator(validation_type, validator):
    """Dynamically add a validator.

    This can be used by clients to add their own, private validators, rather
    than directly modifying the data structure. The clients can NOT modify
    existing validators.
    """
    key = _to_validation_type(validation_type)
    if key in validators:
        # NOTE(boden): imp.load_source() forces module reinitialization that
        # can lead to validator redefinition from the same call site
        if inspect.getsource(validator) != inspect.getsource(validators[key]):
            msg = _("Validator type %s is already defined") % validation_type
            raise KeyError(msg)
        return
    validators[key] = validator
