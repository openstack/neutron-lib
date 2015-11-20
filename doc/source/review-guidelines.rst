=================
Review Guidelines
=================

When reviewing neutron-lib changes, please be aware:

* When code is moved from neutron, please evaluate with the following
  criteria:

  - Is all of the code shared? Don't move neutron-only code.
  - Is the interface good, or does it need to be refactored?
  - Does it need new tests, specifically around the interface?
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
  for the sake of subprojects.  Refer to neutron/i18n.py and
  neutron/common/exceptions.py for examples. Use of oslo's <insert name
  that I forget of deprecation tracker here>, example: <insert example
  here.>

The above implies that if you add something, we are stuck with that interface
for a long time, so be careful.

