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

from neutron_lib.api import validators
from neutron_lib.db import constants as db_const


def validate_bfd_mode(data, valid_modes):
    """Validate BFD monitor mode field

    :param data: The data to validate.
    :param valid_modes: The mode values that are accepted
    :returns: None if data is valid, otherwise a human readable message
        indicating why validation failed.
    """
    msg = validators.validate_not_empty_string(data,
                                               db_const.STATUS_FIELD_SIZE)
    if msg:
        return msg
    if data not in valid_modes:
        msg = (_('BFD monitor mode can be only one of %s') %
               (valid_modes,))
        return msg


def validate_bfd_auth_type(data, valid_auth_types):
    """Validate BFD monitor auth_type field

    :param data: The data to validate.
    :param valid_modes: The authenticatio type values that are accepted
    :returns: None if data is valid, otherwise a human readable message
        indicating why validation failed.
    """
    msg = validators.validate_string_or_none(data, db_const.NAME_FIELD_SIZE)
    if msg:
        return msg
    if not data:
        return
    if data not in valid_auth_types:
        msg = (_('BFD monitor aut_type can only one of %s.') %
               (valid_auth_types,))
        return msg
