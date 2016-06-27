========
Usage
========

To use neutron-lib in a project::

    import neutron_lib


Hacking Checks
--------------

The ``neutron_lib.hacking`` package implements a number of public
`hacking checks <https://github.com/openstack-dev/hacking>`_ that
can be categorized as follows:

Project specific hacking checks
-------------------------------

These hacking checks are intended for validating neutron-lib source
code as part of our pep8 checks. Adopters need not run these checks
and thus a private hacking check factory is used within neutron-lib's
hacking ``tox.ini`` configuration.

General purpose hacking checks
------------------------------

Hacking checks that are shared by two or more consuming projects often
end up in neutron-lib as a general purpose shared hacking check so that
there's a single source for consumption.

All hacking checks in neutron-lib are registered via entry points and are
therefore available via ``flake8`` directly in any environment where
neutron-lib is installed. However, these checks registered via entry points
are disabled by default and therefore must be selectively enabled by
consumers wishing to utilize them.

To selectively enable checks consumers must use ``flake8`` ``select`` to
signify the checks to enable and run.

For example in your ``tox.ini``::

    [flake8]
    select = N530,N531

Via CLI::

    flake8 --select N530,N531 /path/to/src


Adopter hacking checks
----------------------

A subset of checks provided by neutron-lib are intended to validate the
"compliance" of neutron-lib adopter's source code. Consumers can configure
to run the latest set of compliance hacking checks by configuring their
``tox.ini`` as follows::


    [hacking]
    local-check-factory = neutron_lib.hacking.checks.latest_adopter_hacking_checks

The set of hacking checks registered via ``latest_adopter_hacking_checks``
is dynamic and may change from release to release. Consumer's who are not fully
complaint and therefore cannot pass all adopter hacking checks can selectively
enable checks as described in the `General purpose hacking checks`_ section herein.


Hacking Checks Implemented
--------------------------
.. include:: ../../HACKING.rst
