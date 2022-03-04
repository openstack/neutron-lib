# Copyright 2016 OpenStack Foundation
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

import itertools
import uuid

import netaddr
from oslo_serialization import jsonutils
from oslo_versionedobjects import fields as obj_fields

from neutron_lib._i18n import _
from neutron_lib import constants as lib_constants
from neutron_lib.db import constants as lib_db_const
from neutron_lib.objects import exceptions as o_exc
from neutron_lib.utils import net as net_utils


class HARouterEnumField(obj_fields.AutoTypedField):
    AUTO_TYPE = obj_fields.Enum(valid_values=lib_constants.VALID_HA_STATES)


class IPV6ModeEnumField(obj_fields.AutoTypedField):
    AUTO_TYPE = obj_fields.Enum(valid_values=lib_constants.IPV6_MODES)


class RangeConstrainedInteger(obj_fields.Integer):
    def __init__(self, start, end, **kwargs):
        try:
            self._start = int(start)
            self._end = int(end)
        except (TypeError, ValueError) as e:
            raise o_exc.NeutronRangeConstrainedIntegerInvalidLimit(
                start=start, end=end) from e
        super().__init__(**kwargs)

    def coerce(self, obj, attr, value):
        if not isinstance(value, int):
            msg = _("Field value %s is not an integer") % value
            raise ValueError(msg)
        if not self._start <= value <= self._end:
            msg = _("Field value %s is invalid") % value
            raise ValueError(msg)
        return super().coerce(obj, attr, value)


class IPNetworkPrefixLen(RangeConstrainedInteger):
    """IP network (CIDR) prefix length custom Enum"""
    def __init__(self, **kwargs):
        super().__init__(start=0, end=lib_constants.IPv6_BITS, **kwargs)


class IPNetworkPrefixLenField(obj_fields.AutoTypedField):
    AUTO_TYPE = IPNetworkPrefixLen()


class PortRanges(obj_fields.FieldType):
    @staticmethod
    def _is_port_acceptable(port):
        start = lib_constants.PORT_RANGE_MIN
        end = lib_constants.PORT_RANGE_MAX
        return start <= port <= end

    def get_schema(self):
        return {'type': ['string', 'integer']}

    def _validate_port(self, attr, value):
        if self._is_port_acceptable(value):
            return
        raise ValueError(
            _('The port %(value)s does not respect the '
              'range (%(min)s, %(max)s) in field %(attr)s')
            % {'attr': attr,
               'value': value,
               'min': lib_constants.PORT_RANGE_MIN,
               'max': lib_constants.PORT_RANGE_MAX})

    def coerce(self, obj, attr, value):
        if isinstance(value, int):
            self._validate_port(attr, value)
            return value
        if isinstance(value, str):
            if value.isnumeric():
                self._validate_port(attr, int(value))
                return value
            values = value.split(':')
            if len(values) == 2:
                start, end = list(map(int, values))
                if start > end:
                    raise ValueError(
                        _('The first port %(start)s must be less or equals '
                          'than the second port %(end)s of the port range '
                          'configuration %(value)s'
                          'in field %(attr)s.') % {
                            'attr': attr,
                            'value': value,
                            'start': start,
                            'end': end})
                self._validate_port(attr, start)
                self._validate_port(attr, end)
                return value
            raise ValueError(
                _('The field %(attr)s must be in the format PORT_RANGE or'
                  'PORT_RANGE:PORT_RANGE (two numeric values separated '
                  'by a colon), and PORT_RANGE must be a numeric '
                  'value and respect the range '
                  '(%(min)s, %(max)s).') % {
                    'attr': attr,
                    'min': lib_constants.PORT_RANGE_MIN,
                    'max': lib_constants.PORT_RANGE_MAX})
        raise ValueError(
            _('An string/int PORT_RANGE or a string with '
              'PORT_RANGE:PORT_RANGE format is '
              'expected in field %(attr)s, not a %(type)s') % {
                'attr': attr, 'type': value})


class PortRangesField(obj_fields.AutoTypedField):
    AUTO_TYPE = PortRanges()


class PortRange(RangeConstrainedInteger):
    def __init__(self, start=lib_constants.PORT_RANGE_MIN, **kwargs):
        super().__init__(start=start,
                         end=lib_constants.PORT_RANGE_MAX,
                         **kwargs)


class PortRangeField(obj_fields.AutoTypedField):
    AUTO_TYPE = PortRange()


class PortRangeWith0Field(obj_fields.AutoTypedField):
    AUTO_TYPE = PortRange(start=0)


class VlanIdRange(RangeConstrainedInteger):
    def __init__(self, **kwargs):
        super().__init__(start=lib_constants.MIN_VLAN_TAG,
                         end=lib_constants.MAX_VLAN_TAG,
                         **kwargs)


class VlanIdRangeField(obj_fields.AutoTypedField):
    AUTO_TYPE = VlanIdRange()


class ListOfIPNetworksField(obj_fields.AutoTypedField):
    AUTO_TYPE = obj_fields.List(obj_fields.IPNetwork())


class SetOfUUIDsField(obj_fields.AutoTypedField):
    AUTO_TYPE = obj_fields.Set(obj_fields.UUID())


class DomainName(obj_fields.String):
    def coerce(self, obj, attr, value):
        if not isinstance(value, str):
            msg = _("Field value %s is not a string") % value
            raise ValueError(msg)
        if len(value) > lib_db_const.FQDN_FIELD_SIZE:
            msg = _("Domain name %s is too long") % value
            raise ValueError(msg)
        return super().coerce(obj, attr, value)


class DomainNameField(obj_fields.AutoTypedField):
    AUTO_TYPE = DomainName()


class IntegerEnum(obj_fields.Integer):
    def __init__(self, valid_values=None, **kwargs):
        if not valid_values:
            msg = _("No possible values specified")
            raise ValueError(msg)
        for value in valid_values:
            if not isinstance(value, int):
                msg = _("Possible value %s is not an integer") % value
                raise ValueError(msg)
        self._valid_values = valid_values
        super().__init__(**kwargs)

    def coerce(self, obj, attr, value):
        if not isinstance(value, int):
            msg = _("Field value %s is not an integer") % value
            raise ValueError(msg)
        if value not in self._valid_values:
            msg = (
                _("Field value %(value)s is not in the list "
                  "of valid values: %(values)s") %
                {'value': value, 'values': self._valid_values}
            )
            raise ValueError(msg)
        return super().coerce(obj, attr, value)


class IPVersionEnum(IntegerEnum):
    """IP version integer Enum"""
    def __init__(self, **kwargs):
        super().__init__(
            valid_values=lib_constants.IP_ALLOWED_VERSIONS, **kwargs)


class IPVersionEnumField(obj_fields.AutoTypedField):
    AUTO_TYPE = IPVersionEnum()


class DscpMark(IntegerEnum):
    def __init__(self, valid_values=None, **kwargs):
        super().__init__(valid_values=lib_constants.VALID_DSCP_MARKS)


class DscpMarkField(obj_fields.AutoTypedField):
    AUTO_TYPE = DscpMark()


class FlowDirectionEnumField(obj_fields.AutoTypedField):
    AUTO_TYPE = obj_fields.Enum(valid_values=lib_constants.VALID_DIRECTIONS)


class FlowDirectionAndAnyEnumField(obj_fields.AutoTypedField):
    AUTO_TYPE = obj_fields.Enum(
        valid_values=lib_constants.VALID_DIRECTIONS_AND_ANY)


class IpamAllocationStatusEnumField(obj_fields.AutoTypedField):
    AUTO_TYPE = obj_fields.Enum(
        valid_values=lib_constants.VALID_IPAM_ALLOCATION_STATUSES)


class EtherTypeEnumField(obj_fields.AutoTypedField):
    AUTO_TYPE = obj_fields.Enum(valid_values=lib_constants.VALID_ETHERTYPES)


class IpProtocolEnum(obj_fields.Enum):
    """IP protocol number Enum"""
    def __init__(self, **kwargs):
        super().__init__(
            valid_values=list(
                itertools.chain(
                    lib_constants.IP_PROTOCOL_MAP.keys(),
                    [str(v) for v in range(256)]
                )
            ),
            **kwargs)


class PortBindingStatusEnumField(obj_fields.AutoTypedField):
    AUTO_TYPE = obj_fields.Enum(
        valid_values=lib_constants.PORT_BINDING_STATUSES)


class IpProtocolEnumField(obj_fields.AutoTypedField):
    AUTO_TYPE = IpProtocolEnum()


class MACAddress(obj_fields.FieldType):
    """MACAddress custom field.

    This custom field is different from the one provided by
    oslo.versionedobjects library: it uses netaddr.EUI type instead of strings.
    """
    def coerce(self, obj, attr, value):
        if not isinstance(value, netaddr.EUI):
            msg = _("Field value %s is not a netaddr.EUI") % value
            raise ValueError(msg)
        return super().coerce(obj, attr, value)

    @staticmethod
    def to_primitive(obj, attr, value):
        return str(value)

    @staticmethod
    def from_primitive(obj, attr, value):
        try:
            return net_utils.AuthenticEUI(value)
        except Exception as e:
            msg = _("Field value %s is not a netaddr.EUI") % value
            raise ValueError(msg) from e


class MACAddressField(obj_fields.AutoTypedField):
    AUTO_TYPE = MACAddress()


class DictOfMiscValues(obj_fields.FieldType):
    """DictOfMiscValues custom field

    This custom field is handling dictionary with miscellaneous value types,
    including integer, float, boolean and list and nested dictionaries.
    """
    @staticmethod
    def coerce(obj, attr, value):
        if isinstance(value, dict):
            return value
        if isinstance(value, str):
            try:
                return jsonutils.loads(value)
            except Exception as e:
                msg = _("Field value %s is not stringified JSON") % value
                raise ValueError(msg) from e
        msg = (_("Field value %s is not type of dict or stringified JSON")
               % value)
        raise ValueError(msg)

    @staticmethod
    def from_primitive(obj, attr, value):
        return DictOfMiscValues.coerce(obj, attr, value)

    @staticmethod
    def to_primitive(obj, attr, value):
        return jsonutils.dumps(value)

    @staticmethod
    def stringify(value):
        return jsonutils.dumps(value)


class DictOfMiscValuesField(obj_fields.AutoTypedField):
    AUTO_TYPE = DictOfMiscValues


class ListOfDictOfMiscValuesField(obj_fields.AutoTypedField):
    AUTO_TYPE = obj_fields.List(DictOfMiscValuesField())


class IPNetwork(obj_fields.FieldType):
    """IPNetwork custom field.

    This custom field is different from the one provided by
    oslo.versionedobjects library: it does not reset string representation for
    the field.
    """
    def coerce(self, obj, attr, value):
        if not isinstance(value, netaddr.IPNetwork):
            msg = _("Field value %s is not a netaddr.IPNetwork") % value
            raise ValueError(msg)
        return super().coerce(obj, attr, value)

    @staticmethod
    def to_primitive(obj, attr, value):
        return str(value)

    @staticmethod
    def from_primitive(obj, attr, value):
        try:
            return net_utils.AuthenticIPNetwork(value)
        except Exception as e:
            msg = _("Field value %s is not a netaddr.IPNetwork") % value
            raise ValueError(msg) from e


class IPNetworkField(obj_fields.AutoTypedField):
    AUTO_TYPE = IPNetwork()


class UUID(obj_fields.UUID):
    def coerce(self, obj, attr, value):
        uuid.UUID(str(value))
        return str(value)


class UUIDField(obj_fields.AutoTypedField):
    AUTO_TYPE = UUID()


class FloatingIPStatusEnumField(obj_fields.AutoTypedField):
    AUTO_TYPE = obj_fields.Enum(
        valid_values=lib_constants.VALID_FLOATINGIP_STATUS)


class RouterStatusEnumField(obj_fields.AutoTypedField):
    AUTO_TYPE = obj_fields.Enum(
        valid_values=lib_constants.VALID_ROUTER_STATUS)


class NetworkSegmentRangeNetworkTypeEnumField(obj_fields.AutoTypedField):
    AUTO_TYPE = obj_fields.Enum(
        valid_values=lib_constants.NETWORK_SEGMENT_RANGE_TYPES)


class NumaAffinityPoliciesEnumField(obj_fields.AutoTypedField):
    AUTO_TYPE = obj_fields.Enum(valid_values=lib_constants.PORT_NUMA_POLICIES)
