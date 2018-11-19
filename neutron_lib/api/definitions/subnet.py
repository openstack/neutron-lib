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
from neutron_lib import constants
from neutron_lib.db import constants as db_const


NAME = 'Neutron L3 Subnet'
ALIAS = 'subnet'
DESCRIPTION = "Layer 3 subnet abstraction"

UPDATED_TIMESTAMP = "2012-01-01T10:00:00-00:00"

RESOURCE_NAME = 'subnet'
COLLECTION_NAME = 'subnets'

RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        'id': {'allow_post': False, 'allow_put': False,
               'validate': {'type:uuid': None},
               'is_visible': True,
               'is_filter': True,
               'is_sort_key': True,
               'primary_key': True},
        'name': {'allow_post': True, 'allow_put': True, 'default': '',
                 'validate': {
                     'type:string': db_const.NAME_FIELD_SIZE},
                 'is_filter': True,
                 'is_sort_key': True,
                 'is_visible': True},
        'ip_version': {'allow_post': True, 'allow_put': False,
                       'convert_to': converters.convert_to_int,
                       'validate': {'type:values': [4, 6]},
                       'is_filter': True,
                       'is_sort_key': True,
                       'is_visible': True},
        'network_id': {'allow_post': True, 'allow_put': False,
                       'required_by_policy': True,
                       'validate': {'type:uuid': None},
                       'is_filter': True,
                       'is_sort_key': True,
                       'is_visible': True},
        'subnetpool_id': {'allow_post': True,
                          'allow_put': False,
                          'default': constants.ATTR_NOT_SPECIFIED,
                          'required_by_policy': False,
                          'validate': {'type:subnetpool_id_or_none': None},
                          'is_filter': True,
                          'is_sort_key': True,
                          'is_visible': True},
        'prefixlen': {'allow_post': True,
                      'allow_put': False,
                      'validate': {'type:non_negative': None},
                      'convert_to': converters.convert_to_int,
                      'default': constants.ATTR_NOT_SPECIFIED,
                      'required_by_policy': False,
                      'is_visible': False},
        'cidr': {'allow_post': True,
                 'allow_put': False,
                 'default': constants.ATTR_NOT_SPECIFIED,
                 'convert_to': converters.convert_cidr_to_canonical_format,
                 'validate': {'type:subnet_or_none': None},
                 'required_by_policy': False,
                 'is_filter': True,
                 'is_sort_key': True,
                 'is_visible': True},
        'gateway_ip': {'allow_post': True, 'allow_put': True,
                       'default': constants.ATTR_NOT_SPECIFIED,
                       'convert_to': converters.convert_ip_to_canonical_format,
                       'validate': {'type:ip_address_or_none': None},
                       'is_filter': True,
                       'is_sort_key': True,
                       'is_visible': True},
        'allocation_pools': {
            'allow_post': True, 'allow_put': True,
            'default': constants.ATTR_NOT_SPECIFIED,
            'convert_to': converters.convert_ip_to_canonical_format,
            'validate': {'type:ip_pools': None},
            'is_visible': True},
        'dns_nameservers': {'allow_post': True, 'allow_put': True,
                            'convert_to':
                                converters.convert_none_to_empty_list,
                            'default': constants.ATTR_NOT_SPECIFIED,
                            'validate': {'type:nameservers': None},
                            'is_visible': True},
        'host_routes': {'allow_post': True, 'allow_put': True,
                        'convert_to':
                            converters.convert_none_to_empty_list,
                        'default': constants.ATTR_NOT_SPECIFIED,
                        'validate': {'type:hostroutes': None},
                        'is_visible': True},
        'tenant_id': {'allow_post': True, 'allow_put': False,
                      'validate': {
                          'type:string': db_const.PROJECT_ID_FIELD_SIZE},
                      'required_by_policy': True,
                      'is_filter': True,
                      'is_sort_key': True,
                      'is_visible': True},
        'enable_dhcp': {'allow_post': True, 'allow_put': True,
                        'default': True,
                        'convert_to': converters.convert_to_boolean,
                        'is_filter': True,
                        'is_sort_key': True,
                        'is_visible': True},
        'ipv6_ra_mode': {'allow_post': True, 'allow_put': False,
                         'default': constants.ATTR_NOT_SPECIFIED,
                         'validate': {
                             'type:values': constants.IPV6_MODES},
                         'is_filter': True,
                         'is_sort_key': True,
                         'is_visible': True},
        'ipv6_address_mode': {'allow_post': True, 'allow_put': False,
                              'default': constants.ATTR_NOT_SPECIFIED,
                              'validate': {
                                  'type:values': constants.IPV6_MODES},
                              'is_filter': True,
                              'is_sort_key': True,
                              'is_visible': True},
        constants.SHARED: {
            'allow_post': False,
            'allow_put': False,
            'default': False,
            'convert_to': converters.convert_to_boolean,
            'is_visible': False,
            'is_filter': True,
            'required_by_policy': True,
            'enforce_policy': True
        }
    }
}

# This is a core resource so the following are not applicable.
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = []
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
