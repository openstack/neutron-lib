=================
Review Guidelines
=================

When reviewing neutron-lib changes, please be aware:

* When code is moved from neutron, please evaluate with the following
  criteria:

  - Is all of the code shared? Don't move neutron-only code.
  - Is the interface good, or does it need to be refactored?
  - Does it need new tests, specifically around the interface? We want
    100% unit coverage on this library, so if neutron does not yet have
    a test, it needs to be added. Note that tests on things like constants
    are uninteresting, but any code or interface should have a unit test.
  - Is there a corresponding Depends-On review in neutron removing
    this code, and adding backwards compatibility shims for Mitaka?

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

