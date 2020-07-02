============
Contributing
============

.. include:: ../../../CONTRIBUTING.rst

As your code is subject to the `review guidelines <./review-guidelines.html>`_,
please take the time to familiarize yourself with those guidelines.


Rehoming Existing Code
----------------------

The checklist below aims to provide guidance for developers rehoming (moving) code into
neutron-lib. Rehoming approaches that fall outside the scope herein will need to be
considered on a case by case basis.

Please note that the effort to rehome existing code from neutron to neutron-lib
so that no stadium projects would import directly from neutron has been suspended.

The rehoming workflow procedure has four main phases:

#. `Phase 1: Rehome`_ the code from neutron into neutron-lib.
#. `Phase 2: Enhance`_ the code in neutron-lib if necessary.
#. `Phase 3: Release`_ neutron-lib with the code so consumers can use it.
#. `Phase 4: Consume`_ by removing the rehomed code from its source and changing references
   to use neutron-lib.

Phase 1: Rehome
~~~~~~~~~~~~~~~

#. Identify the chunk of code for rehoming. Applicable code includes common
   classes/functions/modules/etc. that are consumed by networking project(s) outside of
   neutron. Optimal consumption patterns of the code at hand must also be considered to
   ensure the rehomed code addresses any technical debt. Finally, leave low-hanging
   fruit for last and tackle the most commonly used code first. If you have any doubt
   about the applicability of code for rehoming, reach out to one of the neutron core
   developers before digging in.

#. Find and identify any unit tests for the code being rehomed. These unit tests
   can often be moved into neutron-lib with minimal effort. After inspecting the
   applicable unit tests, rewrite any that are non-optimal.

#. Search and understand the consumers of the code being rehomed. This must include other
   networking projects in addition to neutron itself. At this point it may be determined
   that the code should be refactored before it is consumed. There are a few common
   strategies for refactoring, and the one chosen will depend on the nature of the code
   at hand:

   - Refactor/enhance the code as part of the initial neutron-lib patch. If this change
     will be disruptive to consumers, clearly communicate the change via email list or
     `meeting topic <https://wiki.openstack.org/wiki/Network/Meetings>`_.
   - Leave the refactoring to the next (Enhance) phase. In this rehome phase, copy the code
     as-is into a private module according to our `conventions <./conventions.html>`_. This
     approach is slower, but may be necessary in some cases.

#. Understand existing work underway which may impact the rehomed code, for example,
   in-flight patch sets that update the code being rehomed. In some cases it may make
   sense to let the in-flight patch merge and solidify a bit before rehoming.

#. Prepare the code for neutron-lib. This may require replacing existing imports
   with those provided by neutron-lib and/or rewriting/rearchitecting non-optimal
   code (see above). The interfaces in the rehomed code are subject to our
   `conventions <./conventions.html>`_.

#. Prepare the unit test code for neutron-lib. As indicated in the `review guidelines
   <./review-guidelines.html>`_ we are looking for a high code coverage by tests. This may
   require adding additional tests if neutron was lacking in coverage.

#. Submit and shepherd your patch through its neutron-lib review. Include a
   `release note <https://docs.openstack.org/reno/latest/>`_ that describes the code's
   old neutron location and new neutron-lib location. Also note that in some cases it makes
   sense to prototype a change in a consumer project to better understand the impacts of
   the change, which can be done using the ``Depends-On:`` approach described in the
   `review guidelines <./review-guidelines.html>`_

Examples:

- `319769 <https://review.opendev.org/319769/>`_ brought over a number of common
  utility functions as-is from neutron into a new package structure within neutron-lib.
- `253661 <https://review.opendev.org/253661/>`_ rehomed neutron callbacks into a
  private package that's enhanced via `346554 <https://review.opendev.org/346554/>`_.
- `319386 <https://review.opendev.org/319386/>`_ rehomes a validator from neutron
  into neutron-lib.

Phase 2: Enhance
~~~~~~~~~~~~~~~~

If the rehomed code is not applicable for enhancements and wasn't made private in Phase 1,
you can skip this step.

Develop and shepherd the enhancements to the private rehomed code applicable at this time.
Private APIs made public as part of this phase will also need
`release notes <https://docs.openstack.org/reno/latest/>`_ indicating the new public
functionality.

Examples:

- `346554 <https://review.opendev.org/346554/>`_ enhances the rehomed private callback
  API in neutron-lib.

Phase 3: Release
~~~~~~~~~~~~~~~~

A new neutron-lib release can be cut at any time. You can also request a release by following
the README instructions in the `openstack/releases <https://github.com/openstack/releases>`_
project.

Once a release is cut, an openstack infra proposal bot will submit patches to the master branch
of all projects that consume neutron-lib to set the new release as the minimum requirement.
Someone from the neutron release team can bump `global requirements` (g-r); for example
`review 393600 <https://review.opendev.org/393600/>`_.

When the bot-proposed requirement patches have merged, your rehomed code can be consumed.

Phase 4: Consume
~~~~~~~~~~~~~~~~

When code is rehomed from neutron-lib then the original location of the code
should be flagged with a `debtcollector removal
<https://docs.openstack.org/debtcollector/latest/user/usage.html#removing-a-class-classmethod-method-function>`_.
This will indicate to any consuming projects that the given code is deprecated.
Be sure that this change is accompanied by a release note that notes the
deprecation.
