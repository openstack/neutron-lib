# Copyright (c) 2013 NEC Corporation
# All Rights Reserved.
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

import os
import platform
import random
import time

from debtcollector import removals
import netaddr

from neutron_lib.utils import helpers
from neutron_lib.utils import net


class UnorderedList(list):
    """A list that is equals to any permutation of itself."""

    def __eq__(self, other):
        if not isinstance(other, list):
            return False
        return (sorted(self, key=helpers.safe_sort_key) ==
                sorted(other, key=helpers.safe_sort_key))

    def __neq__(self, other):
        return not self == other


@removals.remove
def is_bsd():
    """Return True on BSD-based systems."""

    system = platform.system()
    if system == 'Darwin':
        return True
    if 'bsd' in system.lower():
        return True
    return False


def get_random_cidr(version=4):
    if version == 4:
        return '10.%d.%d.0/%d' % (random.randint(3, 254),
                                  random.randint(3, 254),
                                  24)
    return '2001:db8:%x::/%d' % (random.getrandbits(16), 64)


def reset_random_seed():
    # reset random seed to make sure other processes extracting values from RNG
    # don't get the same results (useful especially when you then use the
    # random values to allocate system resources from global pool, like ports
    # to listen). Use both current time and pid to make sure no tests started
    # at the same time get the same values from RNG
    seed = time.time() + os.getpid()
    random.seed(seed)


def get_random_EUI():
    return netaddr.EUI(
        net.get_random_mac(['fe', '16', '3e', '00', '00', '00'])
    )


def get_random_ip_network(version=4):
    return netaddr.IPNetwork(get_random_cidr(version=version))
