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

from neutron_lib.api.definitions import port
from neutron_lib.api.definitions import portbindings
from neutron_lib import constants
from neutron_lib.db import constants as db_const

# Plural of the resource
COLLECTION_NAME = 'bindings'

# Name of the resource
RESOURCE_NAME = 'binding'

# Parent
PARENT_RESOURCE_NAME = port.RESOURCE_NAME
PARENT_COLLECTION_NAME = port.COLLECTION_NAME

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

# Name of the extension
NAME = "Port Bindings Extended"

# Extension alias
ALIAS = 'binding-extended'

# Extension description
DESCRIPTION = "Expose port bindings of a virtual port to external application"

# Action name for activating a port binding
ACTIVATE_BINDING = 'activate'

# Timestamp of last update of this extension
UPDATED_TIMESTAMP = "2017-07-17T10:00:00-00:00"

# Extension attributes
HOST = 'host'
VIF_TYPE = 'vif_type'
VIF_DETAILS = 'vif_details'
VNIC_TYPE = 'vnic_type'
PROFILE = 'profile'
STATUS = 'status'
PROJECT_ID = 'project_id'

# No attribute map, this extension defines only sub resource
RESOURCE_ATTRIBUTE_MAP = {}

# Attribute map of bindings
SUB_RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        'parent': {
            'collection_name': PARENT_COLLECTION_NAME,
            'member_name': PARENT_RESOURCE_NAME},
        'parameters': {
            HOST: {'allow_post': True, 'allow_put': True,
                   'is_visible': True, 'primary_key': True,
                   'is_filter': True},
            VIF_TYPE: {'allow_post': False, 'allow_put': False,
                       'default': constants.ATTR_NOT_SPECIFIED,
                       'enforce_policy': True,
                       'is_visible': True, 'is_filter': True},
            VIF_DETAILS: {'allow_post': False, 'allow_put': False,
                          'default': constants.ATTR_NOT_SPECIFIED,
                          'enforce_policy': True,
                          'is_visible': True},
            VNIC_TYPE: {'allow_post': True, 'allow_put': True,
                        'default': portbindings.VNIC_NORMAL,
                        'is_visible': True,
                        'is_filter': True,
                        'validate': {'type:values': portbindings.VNIC_TYPES},
                        'enforce_policy': True},
            PROFILE: {'allow_post': True, 'allow_put': True,
                      'default': constants.ATTR_NOT_SPECIFIED,
                      'enforce_policy': True,
                      'validate': {'type:dict_or_none': None},
                      'is_visible': True},
            STATUS: {'allow_post': False, 'allow_put': False,
                     'is_visible': True, 'is_filter': True},
            PROJECT_ID: {'allow_post': True, 'allow_put': False,
                         'required_by_policy': True,
                         'validate': {
                             'type:string': db_const.PROJECT_ID_FIELD_SIZE},
                         'is_visible': True},
        }
    }
}

# activate is an action
ACTION_MAP = {
    RESOURCE_NAME: {
        ACTIVATE_BINDING: 'PUT',
    },
}

# No action statuses are required
ACTION_STATUS = {
}

# The list of required extensions
REQUIRED_EXTENSIONS = [
    portbindings.ALIAS,
]

# The list of optional extensions
OPTIONAL_EXTENSIONS = []
