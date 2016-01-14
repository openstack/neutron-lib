# Copyright 2011 VMware, Inc.
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

import socket
import sys

from oslo_config import cfg
from oslo_db import options as db_options
from oslo_log import log as logging

from neutron_lib._i18n import _, _LI
from neutron_lib import version


LOG = logging.getLogger(__name__)

core_opts = [
    cfg.StrOpt('host', default=socket.gethostname(),
               sample_default='example.domain',
               help=_("Hostname to be used by the Neutron server, agents and "
                      "services running on this machine. All the agents and "
                      "services running on this machine must use the same "
                      "host value.")),
]

# Register the configuration options
cfg.CONF.register_opts(core_opts)


def set_db_defaults():
    # Update the default QueuePool parameters. These can be tweaked by the
    # conf variables - max_pool_size, max_overflow and pool_timeout
    db_options.set_defaults(
        cfg.CONF,
        connection='sqlite://',
        sqlite_db='', max_pool_size=10,
        max_overflow=20, pool_timeout=10)


logging.register_options(cfg.CONF)


def setup_logging():
    """Sets up the logging options for a log with supplied name."""
    product_name = "neutron"
    logging.setup(cfg.CONF, product_name)
    LOG.info(_LI("Logging enabled!"))
    LOG.info(_LI("%(prog)s version %(version)s"),
             {'prog': sys.argv[0],
              'version': version.version_info.release_string()})
    LOG.debug("command line: %s", " ".join(sys.argv))
