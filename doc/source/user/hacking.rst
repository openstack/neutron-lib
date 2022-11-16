==============
Hacking Checks
==============

The ``neutron_lib.hacking`` package implements a number of public
`flake8 checks <https://github.com/pycqa/flake8>`__ intended to help
adopters validate their compliance with the latest hacking standards.

To adopt neutron-lib's hacking checks:

#. Update your project's ``tox.ini`` to include hacking checks from
   neutron-lib. More specifically, copy hacking checks under
   "Checks for neutron and related projects" in
   ``[flake8.local-plugin] extension`` in neutron-lib ``tox.ini``
   to ``[flake8.local-plugin] extension`` in your project's ``tox.ini``.

   For example in your ``tox.ini``::

     [flake8:local-plugins]
     extension =
       # Checks from neutron-lib
       N521 = neutron_lib.hacking.checks:use_jsonutils
       N524 = neutron_lib.hacking.checks:check_no_contextlib_nested
       N529 = neutron_lib.hacking.checks:no_mutable_default_args
       N530 = neutron_lib.hacking.checks:check_neutron_namespace_imports
       N532 = neutron_lib.hacking.translation_checks:check_log_warn_deprecated
       N534 = neutron_lib.hacking.translation_checks:check_raised_localized_exceptions
       N536 = neutron_lib.hacking.checks:assert_equal_none
       N537 = neutron_lib.hacking.translation_checks:no_translate_logs

   Under certain circumstances, adopters may need to ignore specific
   neutron-lib hacking checks temporarily. You can ignore such checks
   just by commenting out them (hopefully with a proper reason).

   If your project has its own hacking checks, you can add more rules
   to ``[flake8.local-plugin] extension`` along with hacking checks
   from neutron-lib.

   .. note::

      The above configuration assumes hacking 2.x.
      If your project uses hacking 1.x, see :ref:`hacking1_support` below.

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
   <https://review.opendev.org/389397/>`_ and
   watching for announcements. Announcements regarding neutron-lib adopter
   hacking checks will be communicated via openstack-discuss email list
   and `neutron meetings <https://wiki.openstack.org/wiki/Network/Meetings>`_.

.. _hacking1_support:

Hacking 1.x support
-------------------

If your project uses hacking 1.x, you need a different way to consume hacking
checks from neutron-lib.

.. warning::

   hacking 1.x support is deprecated and will be dropped once all neutron
   related projects migrate to hacking 2.x.

Update your project's ``tox.ini`` to use
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
