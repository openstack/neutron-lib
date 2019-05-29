=========
Releasing
=========

Before you intend to release a new version of neutron-lib consider posting
a `sentinel patch <https://review.opendev.org/#q,I261ec7ea9a5443fd23b806df8c1a109049264fcb,n,z>`_
that will allow to validate that the neutron-lib hash chosen for tagging is
not breaking gate or check jobs affecting a project you care about, first
and foremost Neutron.

As the patch shows, upper-constraints must be bypassed and that may itself
lead to failures due to upstream package changes. The patch also shows (expected)
Grenade failures in that Grenade pulls its own upper-constraints
file during the upgrade phase. In general a newer version of neutron-lib is
validated through the Tempest -full job (and Grenade runs a subset of it), so
Grenade failures can be safely ignored.

In any other case consider (for failures caused by unpinned global requirements)
hard-coding a dummy upper-constraints file that itself uses the specific
neutron-lib hash you want to test. Furthermore, consider using a commit header
that starts with DNM (Do Not Merge) to indicate that the change is just a test,
or -2, if you have the right access permissions.

It is also worth noting that every Stadium project will have a periodic job
running unit tests and pep8 against the master version of neutron-lib
Checking Grafana's `periodic <http://grafana.openstack.org/dashboard/db/neutron-lib-failure-rate?panelId=6&fullscreen>`_
dashboard can give you a glimpse into the sanity of the integration between
neutron-lib and the Stadium projects, and can be considered the quick check
before going ahead with a full blown sentinel patch. Periodic failures can be
debugged by viewing the `periodic logs <http://logs.openstack.org/periodic/opendev.org/>`_

In addition, both the API reference as well as the project docs should be
validated to ensure there are no dead links. To do so run
``tox -e linkcheck`` and address the errors.
