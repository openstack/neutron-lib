==============
Hacking Checks
==============

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

#. Actively adopt neutron-lib hacking checks by running and monitoring
   the neutron-lib `periodic job <http://grafana.openstack.org/dashboard/
   db/neutron-lib-failure-rate?panelId=4&fullscreen>`_ (as per `stadium guidelines
   <https://review.openstack.org/389397/>`_ and
   watching for announcements. Announcements regarding neutron-lib adopter
   hacking checks will be communicated via openstack-dev email list
   and `neutron meetings <https://wiki.openstack.org/wiki/Network/Meetings>`_.

   Under certain circumstances, adopters may need to ignore specific
   neutron-lib hacking checks temporarily. This can be done using the
   ``ignore`` property in the ``[flake8]`` section of your ``tox.ini``.
   For example, to ignore the hacking check ``N536`` your tox.ini might
   have::

      [flake8]
      # temporarily ignore N536 while fixing failing checks
      ignore = N536
