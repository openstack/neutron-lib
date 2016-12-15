# All rights reserved.
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

from neutron_lib.api import converters
from neutron_lib.api.definitions import flowclassifier as fc_api
from neutron_lib import constants
from neutron_lib.db import constants as db_const

# The alias of the extension.
ALIAS = 'sfc'

# Whether or not this extension is simply signaling behavior to the user
# or it actively modifies the attribute map.
IS_SHIM_EXTENSION = False

# Whether the extension is marking the adoption of standardattr model for
# legacy resources, or introducing new standardattr attributes. False or
# None if the standardattr model is adopted since the introduction of
# resource extension.
# If this is True, the alias for the extension should be prefixed with
# 'standard-attr-'.
IS_STANDARD_ATTR_EXTENSION = False

# The name of the extension.
NAME = 'Service Function Chaining'

# The description of the extension.
DESCRIPTION = "Provides support for Service Function Chaining"

# A timestamp of when the extension was last updated.
UPDATED_TIMESTAMP = "2015-10-05T10:00:00-00:00"

API_PREFIX = '/sfc'

# Service Function Chaining constants
PORT_PAIRS = 'port_pairs'
PORT_PAIR_GROUPS = 'port_pair_groups'
PORT_CHAINS = 'port_chains'
MAX_CHAIN_ID = 65535

MPLS = 'mpls'
NSH = 'nsh'

PPG_N_TUPLE_DICT_SPEC = {
    'source_ip_prefix': {
        'default': None,
        'type:subnet_or_none': None
    },
    'destination_ip_prefix': {
        'default': None,
        'type:subnet_or_none': None
    },
    'source_port_range_min': {
        'default': None,
        'convert_to': converters.convert_to_int_if_not_none,
        'type:range_or_none': [0, constants.PORT_MAX]
    },
    'source_port_range_max': {
        'default': None,
        'convert_to': converters.convert_to_int_if_not_none,
        'type:range_or_none': [0, constants.PORT_MAX]
    },
    'destination_port_range_min': {
        'default': None,
        'convert_to': converters.convert_to_int_if_not_none,
        'type:range_or_none': [0, constants.PORT_MAX]
    },
    'destination_port_range_max': {
        'default': None,
        'convert_to': converters.convert_to_int_if_not_none,
        'type:range_or_none': [0, constants.PORT_MAX]
    }
}

# The resource attribute map for the extension.
RESOURCE_ATTRIBUTE_MAP = {
    PORT_PAIRS: {
        'id': {
            'allow_post': False, 'allow_put': False,
            'is_visible': True,
            'validate': {'type:uuid': None},
            'primary_key': True
        },
        'name': {
            'allow_post': True, 'allow_put': True,
            'is_visible': True, 'default': '',
            'validate': {'type:string': db_const.NAME_FIELD_SIZE},
        },
        'description': {
            'allow_post': True, 'allow_put': True,
            'is_visible': True, 'default': '',
            'validate': {'type:string': db_const.DESCRIPTION_FIELD_SIZE},
        },
        'tenant_id': {
            'allow_post': True, 'allow_put': False,
            'is_visible': True,
            'validate': {'type:string': db_const.PROJECT_ID_FIELD_SIZE},
            'required_by_policy': True
        },
        'ingress': {
            'allow_post': True, 'allow_put': False,
            'is_visible': True,
            'validate': {'type:uuid': None}
        },
        'egress': {
            'allow_post': True, 'allow_put': False,
            'is_visible': True,
            'validate': {'type:uuid': None}
        },
        'service_function_parameters': {
            'allow_post': True, 'allow_put': False,
            'is_visible': True,
            'dict_populate_defaults': True,
            'validate': {
                'type:dict': {
                    'correlation': {
                        'type:values': [None, MPLS, NSH],
                        'default': None
                    },
                    'weight': {
                        'type:non_negative': None,
                        'default': 1,
                        'convert_to': converters.convert_to_int
                    }
                }
            }
        }
    },
    PORT_PAIR_GROUPS: {
        'id': {
            'allow_post': False, 'allow_put': False,
            'is_visible': True,
            'validate': {'type:uuid': None},
            'primary_key': True},
        'group_id': {
            'allow_post': False, 'allow_put': False,
            'is_visible': True
        },
        'name': {
            'allow_post': True, 'allow_put': True,
            'is_visible': True, 'default': '',
            'validate': {'type:string': db_const.NAME_FIELD_SIZE},
        },
        'description': {
            'allow_post': True, 'allow_put': True,
            'is_visible': True, 'default': '',
            'validate': {'type:string': db_const.DESCRIPTION_FIELD_SIZE},
        },
        'tenant_id': {
            'allow_post': True, 'allow_put': False,
            'is_visible': True,
            'validate': {'type:string': db_const.PROJECT_ID_FIELD_SIZE},
            'required_by_policy': True
        },
        'port_pairs': {
            'allow_post': True, 'allow_put': True,
            'is_visible': True, 'default': None,
            'validate': {'type:uuid_list': None},
            'convert_to': converters.convert_none_to_empty_list
        },
        'port_pair_group_parameters': {
            'allow_post': True, 'allow_put': False,
            'is_visible': True,
            'dict_populate_defaults': True,
            'validate': {
                'type:dict': {
                    'lb_fields': {
                        'type:list_of_regex_or_none':
                            'eth|ip|tcp|udp)_(src|dst)',
                        'default': []
                    },
                    'ppg_n_tuple_mapping': {
                        'dict_populate_defaults': True,
                        'type:dict': {
                            'ingress_n_tuple': {
                                'type:dict': PPG_N_TUPLE_DICT_SPEC,
                                'default': {}
                            },
                            'egress_n_tuple': {
                                'type:dict': PPG_N_TUPLE_DICT_SPEC,
                                'default': {}
                            }
                        }
                    }
                }
            }
        }
    },
    PORT_CHAINS: {
        'id': {
            'allow_post': False, 'allow_put': False,
            'is_visible': True,
            'validate': {'type:uuid': None},
            'primary_key': True
        },
        'chain_id': {
            'allow_post': True, 'allow_put': False,
            'is_visible': True, 'default': 0,
            'validate': {'type:range': (0, MAX_CHAIN_ID)},
            'convert_to': converters.convert_to_int
        },
        'name': {
            'allow_post': True, 'allow_put': True,
            'is_visible': True, 'default': '',
            'validate': {'type:string': db_const.NAME_FIELD_SIZE},
        },
        'description': {
            'allow_post': True, 'allow_put': True,
            'is_visible': True, 'default': '',
            'validate': {'type:string': db_const.DESCRIPTION_FIELD_SIZE},
        },
        'tenant_id': {
            'allow_post': True, 'allow_put': False,
            'is_visible': True,
            'validate': {'type:string': db_const.PROJECT_ID_FIELD_SIZE},
            'required_by_policy': True
        },
        'port_pair_groups': {
            'allow_post': True, 'allow_put': True,
            'is_visible': True,
            'validate': {'type:uuid_list_non_empty': None},
            'default': None
        },
        'flow_classifiers': {
            'allow_post': True, 'allow_put': True,
            'is_visible': True, 'default': None,
            'validate': {'type:uuid_list': None},
            'convert_to': converters.convert_to_list
        },
        'chain_parameters': {
            'allow_post': True, 'allow_put': False,
            'is_visible': True,
            'dict_populate_defaults': True,
            'validate': {
                'type:dict': {
                    'correlation': {
                        'type:values': [MPLS, NSH],
                        'default': MPLS
                    },
                    'symmetric': {
                        'type:boolean': None,
                        'default': False,
                        'convert_to': converters.convert_to_boolean
                    }
                }
            },
        }
    }
}

# The subresource attribute map for the extension. It adds child resources
# to main extension's resource. The subresource map must have a parent and
# a parameters entry. If an extension does not need such a map, None can
# be specified (mandatory).
SUB_RESOURCE_ATTRIBUTE_MAP = None

# The action map.
ACTION_MAP = {
}

ACTION_STATUS = {
}
# The list of required extensions.
REQUIRED_EXTENSIONS = [
    fc_api.ALIAS,
]

# The list of optional extensions.
OPTIONAL_EXTENSIONS = [
]
