# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import gettext

import pbr.version

from neutron_lib.db import api  # noqa


gettext.install('neutron_lib')


# NOTE(boden): neutron_lib.db.api is imported to ensure the ORM event listeners
# are registered upon importing any neutron-lib module. For more details see
# defect https://bugs.launchpad.net/networking-ovn/+bug/1802369

__version__ = pbr.version.VersionInfo(
    'neutron_lib').version_string()
