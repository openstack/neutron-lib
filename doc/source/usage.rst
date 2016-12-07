========
Usage
========

To use neutron-lib in a project::

    import neutron_lib


Hacking Checks
--------------

The ``neutron_lib.hacking`` package implements a number of public
`hacking checks <https://github.com/openstack-dev/hacking>`_ intended to help
adopters validate their compliance with the latest hacking standards.

To adopt neutron-lib's hacking checks:

#. Update your project's ``tox.ini`` to use
   ``neutron_lib.hacking.checks.factory`` for its ``local-check-factory``.

   For example in your ``tox.ini``::

       [hacking]
       local-check-factory = neutron_lib.hacking.checks.factory

   If your project needs to register additional project specific hacking
   checks, you can define your own factory function that calls neutron-lib's
   ``factory`` function.

   For example in your project's python source::

       def my_factory(register):
           # register neutron-lib checks
           neutron_lib_checks.factory(register)
           # register project specific checks
           register(my_project_check)

   And use your project's own factory in ``tox.ini``::

       [hacking]
       local-check-factory = myproject.mypkg.my_factory

#. Update your project's ``tox.ini`` enable any flake8 extensions neutron-lib's
   ``tox.ini`` does. These are hacking checks otherwise disabled by default
   that neutron-lib expects to run.

   For example in neutron-lib's ``tox.ini``::

    [flake8]
    # H904: Delay string interpolations at logging calls
    enable-extensions=H904

   In the example above, adopters should also add ``H904`` to the
   ``enable-extensions`` in their ``tox.ini``.

#. Actively adopt neutron-lib hacking checks that are incubating and will
   soon become adopter checks by manually running the checks on your project.
   This can be done by modifying your ``tox.ini`` to use the
   ``incubating_factory`` in neutron-lib::

       [hacking]
       local-check-factory = neutron_lib.hacking.checks.incubating_factory

   And then manually running pep8 on your project::

       tox -e pep8

   New adopter hacking checks in neutron-lib will be registered via the
   ``incubating_factory`` while sub-projects are adopting the new check(s)
   and then be moved out of incubating and into ``factory``. Announcements
   regarding neutron-lib adopter hacking checks will be communicated via
   openstack-dev email list and `neutron meetings
   <https://wiki.openstack.org/wiki/Network/Meetings>`_.
