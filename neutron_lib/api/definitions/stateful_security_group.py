# Copyright 2018 NOKIA
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


# The alias of the extension.
ALIAS = 'stateful-security-group'

IS_SHIM_EXTENSION = False

IS_STANDARD_ATTR_EXTENSION = False

# The name of the extension.
NAME = 'Stateful security group'

# The description of the extension.
DESCRIPTION = "Indicates if the security group is stateful or not"

# A timestamp of when the extension was introduced.
UPDATED_TIMESTAMP = "2019-11-26T09:00:00-00:00"

# The resource attribute map for the extension.
RESOURCE_ATTRIBUTE_MAP = {
    'security_groups': {
        'stateful': {'allow_post': True, 'allow_put': True,
                     'is_visible': True, 'default': True,
                     'convert_to': converters.convert_to_boolean}
    }
}

# The subresource attribute map for the extension.
SUB_RESOURCE_ATTRIBUTE_MAP = {
}

# The action map.
ACTION_MAP = {
}

# The action status.
ACTION_STATUS = {
}

# The list of required extensions.
REQUIRED_EXTENSIONS = ['security-group']

# The list of optional extensions.
OPTIONAL_EXTENSIONS = [
]
