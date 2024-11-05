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

import copy
import uuid

import netaddr

from oslo_config import cfg
from oslo_utils import strutils

from neutron_lib._i18n import _
from neutron_lib.api import validators
from neutron_lib import constants
from neutron_lib import exceptions as n_exc
from neutron_lib.placement import utils as pl_utils
from neutron_lib.utils import net as net_utils


def convert_to_boolean(data):
    """Convert a data value into a python bool.

    :param data: The data value to convert to a python bool. This function
        supports string types, bools, and ints for conversion of representation
        to python bool.
    :returns: The bool value of 'data' if it can be coerced.
    :raises InvalidInput: If the value can't be coerced to a python bool.
    """
    try:
        return strutils.bool_from_string(data, strict=True)
    except ValueError as e:
        msg = _("'%s' cannot be converted to boolean") % data
        raise n_exc.InvalidInput(error_message=msg) from e


def convert_to_boolean_if_not_none(data):
    """Uses convert_to_boolean() on the data if the data is not None.

    :param data: The data value to convert.
    :returns: The 'data' returned from convert_to_boolean() if 'data' is not
        None. None is returned if data is None.
    """
    if data is not None:
        return convert_to_boolean(data)


def convert_to_int(data):
    """Convert a data value to a python int.

    :param data: The data value to convert to a python int via python's
        built-in int() constructor.
    :returns: The int value of the data.
    :raises InvalidInput: If the value can't be converted to an int.
    """
    try:
        return int(data)
    except (ValueError, TypeError) as e:
        msg = _("'%s' is not an integer") % data
        raise n_exc.InvalidInput(error_message=msg) from e


def convert_to_int_if_not_none(data):
    """Uses convert_to_int() on the data if the data is not None.

    :param data: The data value to convert.
    :returns: The 'data' returned from convert_to_int() if 'data' is not None.
        None is returned if data is None.
    """
    if data is not None:
        return convert_to_int(data)
    return data


def convert_to_positive_float_or_none(val):
    """Converts a value to a python float if the value is positive.

    :param val: The value to convert to a positive python float.
    :returns: The value as a python float. If the val is None, None is
        returned.
    :raises ValueError, InvalidInput: A ValueError is raised if the 'val'
        is a float, but is negative. InvalidInput is raised if 'val' can't be
        converted to a python float.
    """
    # NOTE(salv-orlando): This conversion function is currently used by
    # a vendor specific extension only at the moment  It is used for
    # port's RXTX factor in neutron.plugins.vmware.extensions.qos.
    # It is deemed however generic enough to be in this module as it
    # might be used in future for other API attributes.
    if val is None:
        return
    try:
        val = float(val)
        if val < 0:
            raise ValueError()
    except (ValueError, TypeError) as e:
        msg = _("'%s' must be a non negative decimal") % val
        raise n_exc.InvalidInput(error_message=msg) from e
    return val


def convert_kvp_str_to_list(data):
    """Convert a value of the form 'key=value' to ['key', 'value'].

    :param data: The string to parse for a key value pair.
    :returns: A list where element 0 is the key and element 1 is the value.
    :raises InvalidInput: If 'data' is not a key value string.
    """
    kvp = [x.strip() for x in data.split('=', 1)]
    if len(kvp) == 2 and kvp[0]:
        return kvp
    msg = _("'%s' is not of the form <key>=[value]") % data
    raise n_exc.InvalidInput(error_message=msg)


def convert_kvp_list_to_dict(kvp_list):
    """Convert a list of 'key=value' strings to a dict.

    :param kvp_list: A list of key value pair strings. For more info on the
        format see; convert_kvp_str_to_list().
    :returns: A dict who's key value pairs are populated by parsing 'kvp_list'.
    :raises InvalidInput: If any of the key value strings are malformed.
    """
    if kvp_list == ['True']:
        # No values were provided (i.e. '--flag-name')
        return {}
    kvp_map = {}
    for kvp_str in kvp_list:
        key, value = convert_kvp_str_to_list(kvp_str)
        kvp_map.setdefault(key, set())
        kvp_map[key].add(value)
    return {x: list(y) for x, y in kvp_map.items()}


def convert_none_to_empty_list(value):
    """Convert value to an empty list if it's None.

    :param value: The value to convert.
    :returns: An empty list of 'value' is None, otherwise 'value'.
    """
    return [] if value is None else value


def convert_none_to_empty_dict(value):
    """Convert the value to an empty dict if it's None.

    :param value: The value to convert.
    :returns: An empty dict if 'value' is None, otherwise 'value'.
    """
    return {} if value is None else value


def convert_none_to_empty_string(value):
    """Convert the value to an empty string if it's None.

    :param value: The value to convert.
    :returns: An empty string if 'value' is None, otherwise 'value'.
    """
    return '' if value is None else value


def convert_to_list(data):
    """Convert a value into a list.

    :param data: The value to convert.
    :return: A new list wrapped around 'data' whereupon the list is empty
        if 'data' is None.
    """
    if data is None:
        return []
    elif hasattr(data, '__iter__') and not isinstance(data, str):
        return list(data)
    else:
        return [data]


def convert_allocation_pools_to_canonical_format(value):
    """Convert allocation pools to canonical format.

    :param value: The allocation pools which need to be checked.
    :returns: Allocation pools with addresses in canonical format.
    :raises InvalidInput: If the value is not a list of allocation pools.
    """
    if value is None:
        return []
    try:
        return [
            {
                k: convert_ip_to_canonical_format(v)
                for k, v in pool.items()
            }
            for pool in value
        ]
    except Exception as e:
        raise n_exc.InvalidInput(
            error_message=_("Invalid data format for allocation pools")) from e


def convert_ip_to_canonical_format(value):
    """IP Address is validated and then converted to canonical format.

    :param value: The IP Address which needs to be checked.
    :returns: - None if 'value' is None,
              - 'value' if 'value' is IPv4 address,
              - 'value' if 'value' is not an IP Address
              - canonical IPv6 address if 'value' is IPv6 address.

    """
    try:
        ip = netaddr.IPAddress(value)
        if ip.version == constants.IP_VERSION_6:
            return str(ip.format(dialect=netaddr.ipv6_compact))
    except Exception:  # nosec B110
        # netaddr may raise all kinds of exceptions (ValueError,
        # AttributeError...) if the input is not a valid IP address. Instead of
        # catching them one by one, just catch all exceptions at once.
        # Obviously, it would be better if netaddr raised a particular
        # exception specific to the library. But we don't control it.
        pass
    return value


def convert_cidr_to_canonical_format(value):
    """CIDR is validated and converted to canonical format.

    :param value: The CIDR which needs to be checked.
    :returns: - 'value' if 'value' is CIDR with IPv4 address,
              - CIDR with canonical IPv6 address if 'value' is IPv6 CIDR.
    :raises: InvalidInput if 'value' is None, not a valid CIDR or
        invalid IP Format.
    """
    error_message = _("%s is not in a CIDR format") % value
    try:
        cidr = netaddr.IPNetwork(value)
        return str(convert_ip_to_canonical_format(
            cidr.ip)) + "/" + str(cidr.prefixlen)
    except netaddr.core.AddrFormatError as e:
        raise n_exc.InvalidInput(error_message=error_message) from e


def convert_string_to_case_insensitive(data):
    """Convert a string value into a lower case string.

    This effectively makes the string case-insensitive.

    :param data: The value to convert.
    :return: The lower-cased string representation of the value, or None is
        'data' is None.
    :raises InvalidInput: If the value is not a string.
    """
    try:
        return data.lower()
    except AttributeError as e:
        error_message = _("Input value %s must be string type") % data
        raise n_exc.InvalidInput(error_message=error_message) from e


def convert_to_protocol(data):
    """Validate that a specified IP protocol is valid.

    For the authoritative list mapping protocol names to numbers, see the IANA:
    http://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml

    :param data: The value to verify is an IP protocol.
    :returns: If data is an int between 0 and 255 or None, return that; if
        data is a string then return it lower-cased if it matches one of the
        allowed protocol names.
    :raises exceptions.InvalidInput: If data is an int < 0, an
        int > 255, or a string that does not match one of the allowed protocol
        names.
    """

    if data is None:
        return
    val = convert_string_to_case_insensitive(data)
    if val in constants.IPTABLES_PROTOCOL_MAP:
        return data

    error_message = _("IP protocol '%s' is not supported. Only protocol "
                      "names and their integer representation (0 to "
                      "255) are supported") % data
    try:
        if validators.validate_range(convert_to_int(data), [0, 255]) is None:
            return data
        else:
            raise n_exc.InvalidInput(error_message=error_message)
    except n_exc.InvalidInput as e:
        raise n_exc.InvalidInput(error_message=error_message) from e


def convert_to_string(data):
    """Convert a data value into a string.

    :param data: The data value to convert to a string.
    :returns: The string value of 'data' if data is not None
    """

    if data is not None:
        return str(data)


def convert_prefix_forced_case(data, prefix):
    """If <prefix> is a prefix of data, case insensitive, then force its case

    This converter forces the case of a given prefix of a string.

    Example, with prefix="Foo":
    * 'foobar' converted into 'Foobar'
    * 'fOozar' converted into 'Foozar'
    * 'FOObaz' converted into 'Foobaz'

    :param data: The data to convert
    :returns: if data is a string starting with <prefix> in a case insensitive
              comparison, then the return value is data with this prefix
              replaced by <prefix>
    """
    plen = len(prefix)
    if (isinstance(data, str) and len(data) >= plen and
            data[0:plen].lower() == prefix.lower()):
        return prefix + data[plen:]
    return data


def convert_uppercase_ip(data):
    """Uppercase "ip" if present at start of data case-insensitive

    Can be used for instance to accept both "ipv4" and "IPv4".

    :param data: The data to convert
    :returns: if data is a string starting with "ip" case insensitive, then
              the return value is data with the first two letter uppercased
    """
    return convert_prefix_forced_case(data, "IP")


def convert_to_mac_if_none(data):
    """Convert to a random mac address if data is None

    :param data: The data value
    :return: Random mac address if data is None, else return data.
    """
    if data is None:
        return net_utils.get_random_mac(cfg.CONF.base_mac.split(':'))

    return data


def convert_to_sanitized_mac_address(mac_address):
    """Return a MAC address with format xx:xx:xx:xx:xx:xx

    :param mac_address: (string, netaddr.EUI) The MAC address value
    :return: A string with the MAC address formatted. If the MAC address
             provided is invalid, the same input value is returned; the goal
             of this method is not to validate it.
    """
    try:
        if isinstance(mac_address, netaddr.EUI):
            _mac_address = copy.deepcopy(mac_address)
            _mac_address.dialect = netaddr.mac_unix_expanded
            return str(_mac_address)
        return str(netaddr.EUI(mac_address, dialect=netaddr.mac_unix_expanded))
    except netaddr.core.AddrFormatError:
        return mac_address


def convert_to_sanitized_binding_profile_allocation(allocation, port_id,
                                                    min_bw_rules):
    """Return binding-profile.allocation in the new format

    :param allocation: binding-profile.allocation attribute containting a
                       string with RP UUID
    :param port_id: ID of the port that is being sanitized
    :param min_bw_rules: A list of minimum bandwidth rules associated with the
                         port.
    :return: A dict with allocation in {'<group_uuid>': '<rp_uuid>'} format.
    """
    if isinstance(allocation, dict):
        return allocation

    group_id = str(
        pl_utils.resource_request_group_uuid(uuid.UUID(port_id), min_bw_rules))
    return {group_id: allocation}
