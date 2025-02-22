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

# Database field sizes
NAME_FIELD_SIZE = 255
LONG_DESCRIPTION_FIELD_SIZE = 1024
DESCRIPTION_FIELD_SIZE = 255
PROJECT_ID_FIELD_SIZE = 255
DEVICE_ID_FIELD_SIZE = 255
DEVICE_OWNER_FIELD_SIZE = 255
UUID_FIELD_SIZE = 36
STATUS_FIELD_SIZE = 16
IP_ADDR_FIELD_SIZE = 64  # large enough to hold a v4 or v6 address
MAC_ADDR_FIELD_SIZE = 32
RESOURCE_TYPE_FIELD_SIZE = 255
FQDN_FIELD_SIZE = 255
AZ_HINTS_DB_LEN = 255

# Alembic branches
EXPAND_BRANCH = 'expand'
CONTRACT_BRANCH = 'contract'

# Maximum value integer can take in MySQL.
# In SQLite integer can be stored in 1, 2, 3, 4, 6, or 8 bytes,
# but here it will be limited by this value for consistency.
DB_INTEGER_MAX_VALUE = 2 ** 31 - 1
