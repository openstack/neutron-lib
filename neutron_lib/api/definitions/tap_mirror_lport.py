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

from neutron_lib.api.definitions import taas
from neutron_lib.api.definitions import tap_mirror
from neutron_lib.api.definitions import tap_mirror_both_direction
from neutron_lib.types import (
    ActionMap,
    AttributeValidator,
    ResourceAttributeMap,
    SubResourceAttributeMap,
)

ALIAS = 'tap-mirror-lport'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = "Tap as a Service mirror to a logical port"
DESCRIPTION = ("Neutron Tap as a Service extension to mirror the traffic of a "
               "port to another Neutron port inside the overlay.")
UPDATED_TIMESTAMP = "2026-09-22T10:00:00-00:00"

# New mirror type: the sink of the mirror is a Neutron port (an OVN logical
# switch port) instead of a remote IP address. The mirrored frames are
# delivered inside the overlay without any tunnel encapsulation.
MIRROR_TYPE_LPORT = 'lport'
mirror_types_list = tap_mirror.mirror_types_list + [MIRROR_TYPE_LPORT]

REMOTE_PORT_ID = 'remote_port_id'

# Redefines ``directions`` of the ``tap-mirror-both-direction`` extension
# (``IN``, ``OUT`` and ``BOTH`` keys) with optional tunnel ID values: the
# values keep the integer validation of that extension and may also be
# ``null``. The tunnel IDs are meaningless for an ``lport`` mirror, so
# ``{"IN": null, "OUT": null}`` or ``{"BOTH": null}`` only selects the
# mirrored directions. The service plugin checks the values per mirror type:
# ``gre``/``erspanv1`` mirrors still need a tunnel ID per direction,
# ``lport`` mirrors must not carry one.
DIRECTION_SPEC: AttributeValidator = {
    'type:dict': {
        taas.DIRECTION_IN: {'type:integer_or_none': None,
                            'default': None, 'required': False},
        taas.DIRECTION_OUT: {'type:integer_or_none': None,
                             'default': None, 'required': False},
        taas.DIRECTION_BOTH: {'type:integer_or_none': None,
                              'default': None, 'required': False},
    }
}

RESOURCE_ATTRIBUTE_MAP: ResourceAttributeMap = {
    tap_mirror.COLLECTION_NAME: {
        'mirror_type': {
            'allow_post': True,
            'allow_put': False,
            'validate': {'type:values': mirror_types_list},
            'is_visible': True,
            'is_filter': True
        },
        'directions': {
            'allow_post': True,
            'allow_put': False,
            'validate': DIRECTION_SPEC,
            'is_visible': True
        },
        # Still mandatory for ``gre``/``erspanv1`` mirrors, must be unset
        # for the ``lport`` mirror type (checked by the service plugin).
        'remote_ip': {
            'allow_post': True,
            'allow_put': False,
            'validate': {'type:ip_address_or_none': None},
            'default': None,
            'is_visible': True,
            'is_filter': True
        },
        # The Neutron port that receives the mirrored traffic. Mandatory for
        # the ``lport`` mirror type, must be unset for the other types.
        REMOTE_PORT_ID: {
            'allow_post': True,
            'allow_put': False,
            'validate': {'type:uuid_or_none': None},
            'default': None,
            'is_visible': True,
            'is_filter': True
        },
    }
}

SUB_RESOURCE_ATTRIBUTE_MAP: SubResourceAttributeMap = {}

ACTION_MAP: ActionMap = {}
ACTION_STATUS = {}
REQUIRED_EXTENSIONS = [tap_mirror.ALIAS, tap_mirror_both_direction.ALIAS]
OPTIONAL_EXTENSIONS = []
