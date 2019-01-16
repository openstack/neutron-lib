=====================
Consuming neutron-lib
=====================

Many OpenStack projects consume neutron-lib by importing and using its code.
As a result, these consumers must define ``neutron-lib`` as a dependency in their
respective ``requirements.txt`` file. While this is likely nothing new to most
OpenStack developers, it may not be obvious to consumers if they need to always
use the latest release of neutron-lib, or if they can lag behind using an
old(er) release of it.

The answer is that it's up to the consuming project if they want to stay
"current" or not in terms of the neutron-lib version they use. While we might
like all consumers to stay current and there are benefits to it, this isn't
always realistic for projects that have less developers/velocity. Therefore,
each project has two options for consuming neutron-lib.

* Opt-in to stay current by adding a comment with ``neutron-lib-current`` in
  their ``requirements.txt``. This string declares the project's intent to use
  the latest version of neutron-lib as well as their agreement to stay current
  with overall OpenStack initiatives. These projects receive updates "for free"
  as part of the ongoing neutron-lib work. For more details see the
  `ML archive <http://lists.openstack.org/pipermail/openstack-dev/2018-September/135063.html>`_

* Do not opt-in and rather manage your own consumption of neutron-lib. In this
  case your project developers must define the version of neutron-lib to use
  and update the project's code to consume it as they bump up the version. In
  this scenario most projects will also be managing a back-leveled version of
  ``neutron`` since neutron is always current with neutron-lib and might otherwise
  break the consuming code.
