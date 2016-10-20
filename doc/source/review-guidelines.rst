=================
Review Guidelines
=================

When reviewing neutron-lib changes, please be aware:

* When code is moved from neutron, please evaluate with the following
  criteria:

  - Is all of the code shared? Don't move neutron-only code.
  - Is the interface good, or does it need to be refactored?
  - Does it need new tests, specifically around the interface? We want
    a global unit coverage greater than 90%, and a per-module coverage
    greater than 80%. If neutron does not yet have a test, it needs to
    be added. Note that tests on things like constants are uninteresting,
    but any code or interface should have a unit test, if you cannot
    tell for sure that it is not going to be traversed in some alternative
    way (e.g. tempest/functional coverage).
  - Is there a corresponding Depends-On review in neutron removing
    this code, and adding backwards compatibility shims for Mitaka?
  - Do the public APIs have their parameters and return values documented
    using reStructuredText docstring format (see below)?

* Public APIs should be documented using `reST style docstrings <https://www.python.org/dev/peps/pep-0287/>`_
  that include an overview as well as parameter and return documentation.
  The format of docstrings can be found in the `OpenStack developer hacking docs <http://docs.openstack.org/developer/hacking/#docstrings>`_.
  Note that public API documentation is a bonus, not a requirement.

* Public classes and methods must not be destructively changed without
  following the full OpenStack deprecation path.

  For example, do not:

  - Change names of classes or methods
  - Reorder method arguments
  - Change side effects

  Alternatives:

  - Add a second method with the new signature
  - Add keyword arguments

* Removing the code from neutron should include a shim in neutron
  for the sake of subprojects.  Refer to neutron/common/exceptions.py
  for an example. Please Use oslo's debtcollector library,
  example: http://docs.openstack.org/developer/debtcollector/

  The above implies that if you add something, we are stuck with that interface
  for a long time, so be careful.

* Any code that imports/uses the following python modules should not be
  moved into neutron-lib:

  - eventlet
