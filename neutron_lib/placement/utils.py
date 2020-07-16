# Copyright 2018 Ericsson
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import uuid

import os_traits
from oslo_log import log as logging

from neutron_lib._i18n import _
from neutron_lib import constants as const
from neutron_lib.placement import constants as place_const


LOG = logging.getLogger(__name__)


def physnet_trait(physnet):
    """A Placement trait name to represent being connected to a physnet.

    :param physnet: The physnet name.
    :returns: The trait name representing the physnet.
    """
    return os_traits.normalize_name('%s%s' % (
        place_const.TRAIT_PREFIX_PHYSNET, physnet))


def vnic_type_trait(vnic_type):
    """A Placement trait name to represent support for a vnic_type.

    :param physnet: The vnic_type.
    :returns: The trait name representing the vnic_type.
    """
    return os_traits.normalize_name('%s%s' % (
        place_const.TRAIT_PREFIX_VNIC_TYPE, vnic_type))


def six_uuid5(namespace, name):
    """A uuid.uuid5 variant that takes utf-8 'name' both in Python 2 and 3.

    :param namespace: A UUID object used as a namespace in the generation of a
                      v5 UUID.
    :param name: Any string (either bytecode or unicode) used as a name in the
                 generation of a v5 UUID.
    :returns: A v5 UUID object.
    """

    # NOTE(bence romsics):
    # uuid.uuid5() behaves seemingly consistently but still incompatibly
    # different in cPython 2 and 3. Both expects the 'name' parameter to have
    # the type of the default string literal in each language version.
    # That is:
    #     The cPython 2 variant expects a byte string.
    #     The cPython 3 variant expects a unicode string.
    # Which types are called respectively 'str' and 'str' for the sake of
    # confusion. But the sha1() hash inside uuid5() always needs a byte string,
    # so we have to treat the two versions asymmetrically. See also:
    #
    # cPython 2.7:
    # https://github.com/python/cpython/blob
    #        /ea9a0994cd0f4bd37799b045c34097eb21662b3d/Lib/uuid.py#L603
    # cPython 3.6:
    # https://github.com/python/cpython/blob
    #        /e9e2fd75ccbc6e9a5221cf3525e39e9d042d843f/Lib/uuid.py#L628
    return uuid.uuid5(namespace=namespace, name=name)


# NOTE(bence romsics): The spec said: "Agent resource providers shall
# be identified by their already existing Neutron agent UUIDs [...]"
#
# https://review.opendev.org/#/c/508149/14/specs/rocky
#        /minimum-bandwidth-allocation-placement-api.rst@465
#
# However we forgot that agent UUIDs are not stable through a few
# admin operations like after a manual 'openstack network agent
# delete'. Here we make up a stable UUID instead.
def agent_resource_provider_uuid(namespace, host):
    """Generate a stable UUID for an agent.

    :param namespace: A UUID object identifying a mechanism driver (including
                      its agent).
    :param host: The hostname of the agent.
    :returns: A unique and stable UUID identifying an agent.
    """
    return six_uuid5(namespace=namespace, name=host)


def device_resource_provider_uuid(namespace, host, device, separator=':'):
    """Generate a stable UUID for a physical network device.

    :param namespace: A UUID object identifying a mechanism driver (including
                      its agent).
    :param host: The hostname of the agent.
    :param device: A host-unique name of the physical network device.
    :param separator: A string used in assembling a name for uuid5(). Choose
                      one that cannot occur either in 'host' or 'device'.
                      Optional.
    :returns: A unique and stable UUID identifying a physical network device.
    """
    name = separator.join([host, device])
    return six_uuid5(namespace=namespace, name=name)


def _parse_bandwidth_value(bw_str):
    """Parse the config string of a bandwidth value to an integer.

    :param bw_str: A decimal string represantation of an integer, allowing
                   the empty string.
    :raises: ValueError on invalid input.
    :returns: The bandwidth value as an integer or None if not set in config.
    """
    try:
        bw = None
        if bw_str:
            bw = int(bw_str)
            if bw < 0:
                raise ValueError()
    except ValueError as e:
        raise ValueError(_(
            'Cannot parse resource_provider_bandwidths. '
            'Expected: non-negative integer bandwidth value, got: %s') %
            bw_str) from e
    return bw


def parse_rp_bandwidths(bandwidths):
    """Parse and validate config option: resource_provider_bandwidths.

    Input in the config:
        resource_provider_bandwidths = eth0:10000:10000,eth1::10000,eth2::,eth3
    Input here:
        ['eth0:10000:10000', 'eth1::10000', 'eth2::', 'eth3']
    Output:
        {
            'eth0': {'egress': 10000, 'ingress': 10000},
            'eth1': {'egress': None, 'ingress': 10000},
            'eth2': {'egress': None, 'ingress': None},
            'eth3': {'egress': None, 'ingress': None},
        }

    :param bandwidths: The list of 'interface:egress:ingress' bandwidth
                       config options as pre-parsed by oslo_config.
    :raises: ValueError on invalid input.
    :returns: The fully parsed bandwidth config as a dict of dicts.
    """

    rv = {}
    for bandwidth in bandwidths:
        if ':' not in bandwidth:
            bandwidth += '::'
        try:
            device, egress_str, ingress_str = bandwidth.split(':')
        except ValueError as e:
            raise ValueError(_(
                'Cannot parse resource_provider_bandwidths. '
                'Expected: DEVICE:EGRESS:INGRESS, got: %s') % bandwidth) from e
        if device in rv:
            raise ValueError(_(
                'Cannot parse resource_provider_bandwidths. '
                'Same device listed multiple times: %s') % device)
        egress = _parse_bandwidth_value(egress_str)
        ingress = _parse_bandwidth_value(ingress_str)
        rv[device] = {
            const.EGRESS_DIRECTION: egress,
            const.INGRESS_DIRECTION: ingress,
        }
    return rv


def parse_rp_inventory_defaults(inventory_defaults):
    """Parse and validate config option: parse_rp_inventory_defaults.

    Cast the dict values to the proper numerical types.

    Input in the config:
        resource_provider_inventory_defaults = allocation_ratio:1.0,min_unit:1
    Input here:
        {
            'allocation_ratio': '1.0',
            'min_unit': '1',
        }
    Output here:
        {
            'allocation_ratio': 1.0,
            'min_unit': 1,
        }

    :param inventory_defaults: The dict of inventory parameters and values (as
                               strings) as pre-parsed by oslo_config.
    :raises: ValueError on invalid input.
    :returns: The fully parsed inventory parameters and values (as numerical
              values) as a dict.
    """

    unexpected_options = (set(inventory_defaults.keys()) -
                          place_const.INVENTORY_OPTIONS)
    if unexpected_options:
        raise ValueError(_(
            'Cannot parse inventory_defaults. Unexpected options: %s') %
            ','.join(unexpected_options))

    # allocation_ratio is a float
    try:
        if 'allocation_ratio' in inventory_defaults:
            inventory_defaults['allocation_ratio'] = float(
                inventory_defaults['allocation_ratio'])
            if inventory_defaults['allocation_ratio'] < 0:
                raise ValueError()
    except ValueError as e:
        raise ValueError(_(
            'Cannot parse inventory_defaults.allocation_ratio. '
            'Expected: non-negative float, got: %s') %
            inventory_defaults['allocation_ratio']) from e

    # the others are ints
    for key in ('min_unit', 'max_unit', 'reserved', 'step_size'):
        try:
            if key in inventory_defaults:
                inventory_defaults[key] = int(inventory_defaults[key])
                if inventory_defaults[key] < 0:
                    raise ValueError()
        except ValueError as e:
            raise ValueError(_(
                'Cannot parse inventory_defaults.%(key)s. '
                'Expected: non-negative int, got: %(got)s') % {
                    'key': key,
                    'got': inventory_defaults[key],
            }) from e

    return inventory_defaults
