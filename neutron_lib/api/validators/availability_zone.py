# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from oslo_serialization import jsonutils

from neutron_lib._i18n import _
from neutron_lib.api import validators
from neutron_lib.db import constants as db_const
from neutron_lib import exceptions


def convert_az_list_to_string(az_list):
    """Convert a list of availability zones into a string.

    :param az_list: A list of AZs.
    :returns: The az_list in string format.
    """
    return jsonutils.dumps(az_list)


def convert_az_string_to_list(az_string):
    """Convert an AZ list in string format into a python list.

    :param az_string: The AZ list in string format.
    :returns: The python list of AZs build from az_string.
    """
    return jsonutils.loads(az_string) if az_string else []


def _validate_availability_zone_hints(data, valid_value=None):
    msg = validators.validate_list_of_unique_strings(data)
    if msg:
        return msg
    az_string = convert_az_list_to_string(data)
    if len(az_string) > db_const.AZ_HINTS_DB_LEN:
        msg = _("Too many availability_zone_hints specified")
        raise exceptions.InvalidInput(error_message=msg)
