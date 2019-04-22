=================
Review Guidelines
=================

When reviewing neutron-lib changes, please be aware:

* When code is moved from neutron, please evaluate with the following
  criteria:

  - Is all of the code shared? Don't move neutron-only code.
  - Is the interface good, or does it need to be refactored? If refactoring
    is required it must be done before the public interface is released to
    PyPI as once released it must follow our `conventions <./conventions.html>`_.
  - Does it need new tests, specifically around the interface? We want
    a global unit coverage greater than 90%, and a per-module coverage
    greater than 80%. If neutron does not yet have a test, it needs to
    be added. Note that tests on things like constants are uninteresting,
    but any code or interface should have a unit test, if you cannot
    tell for sure that it is not going to be traversed in some alternative
    way (e.g. tempest/functional coverage).
  - Do the public APIs have their parameters and return values documented
    using reStructuredText docstring format (see below)?
  - In certain cases, it may be beneficial to determine how the neutron-lib
    code changes impact neutron `master`. This can be done as follows:

    - Publish a 'Do Not Merge' dummy patch to neutron that uses the code
      changes proposed (or already in) neutron-lib. Make sure to mark this
      neutron change as a 'DNM' (or 'WIP') and use -1 for workflow to indicate.
    - Publish a change to neutron-lib that uses `Depends-On:` for the
      dummy change in neutron; this pulls the neutron dummy change into the
      neutron-lib gate job. For example
      `386846 <https://review.opendev.org/386846/>`_ uses a dummy
      neutron-lib patch to test code that already exists in neutron-lib
      `master` whereas `346554 <https://review.opendev.org/#/c/346554/13>`_
      tests the neutron-lib patch's code itself.
    - View neutron-lib gate job results and repeat as necessary.

* Public APIs should be documented using `reST style docstrings <https://www.python.org/dev/peps/pep-0287/>`_
  that include an overview as well as parameter and return documentation.
  The format of docstrings can be found in the `OpenStack developer hacking docs <https://docs.openstack.org/hacking/latest/user/hacking.html#docstrings>`_.
  Note that public API documentation is a bonus, not a requirement.

* Once public classes and methods are pushed to PyPI as part of a neutron-lib
  release, they must not be destructively changed without following the full
  OpenStack deprecation path.

  For example, do not:

  - Change names of classes or methods
  - Reorder method arguments
  - Change side effects

  Alternatives:

  - Add a second method with the new signature
  - Add keyword arguments

  The above implies that if you add something, we are stuck with that interface
  for a long time, so be careful.

* Removing the code from neutron can be done without a temporary `debtcollector
  <https://docs.openstack.org/debtcollector/latest/>`_ notice by following
  the steps described in the 'Consume' phase of the
  `contributing doc <./contributing.html>`_.

* Any code that imports/uses the following python modules should not be
  moved into neutron-lib:

  - eventlet

* With respect to `Oslo config options <https://docs.openstack.org/oslo.config/latest/>`_:

  - Config options should only be included in neutron-lib when the respective
    functionality that uses the options lives in neutron-lib. In this case the
    options will need to be exposed as entry points for
    `config generation <https://docs.openstack.org/oslo.config/latest/cli/generator.html>`_.
  - Common functionality in neutron-lib that accesses config values should
    assume the caller has registered them and document such in the docstring for
    the respective functionality in neutron-lib.
