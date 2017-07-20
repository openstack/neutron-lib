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
     `meeting topic <https://wiki.openstack.org/wiki/Network/Meetings#Neutron-lib_and_planned_neutron_refactoring>`_.
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

- `319769 <https://review.openstack.org/319769/>`_ brought over a number of common
  utility functions as-is from neutron into a new package structure within neutron-lib.
- `253661 <https://review.openstack.org/253661/>`_ rehomed neutron callbacks into a
  private package that's enhanced via `346554 <https://review.openstack.org/346554/>`_.
- `319386 <https://review.openstack.org/319386/>`_ rehomes a validator from neutron
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

- `346554 <https://review.openstack.org/346554/>`_ enhances the rehomed private callback
  API in neutron-lib.

Phase 3: Release
~~~~~~~~~~~~~~~~

A new neutron-lib release can be cut at any time. You can also request a release by following
the README instructions in the `openstack/releases <https://github.com/openstack/releases>`_
project.

Once a release is cut, an openstack infra proposal bot will submit patches to the master branch
of all projects that consume neutron-lib to set the new release as the minimum requirement.
Someone from the neutron release team can bump `global requirements` (g-r); for example
`review 393600 <https://review.openstack.org/393600/>`_.

When the bot-proposed requirement patches have merged, your rehomed code can be consumed.

Phase 4: Consume
~~~~~~~~~~~~~~~~

It's critical that before you submit your patch to remove the rehomed code from its source that
you perform a diff between it and the rehomed version in neutron-lib to ensure nothing has
changed in the source. If something has changed in the source, you need to push and shepherd a
patch to neutron-lib with the difference(s) before proceeding with this consumption phase.

The following guidelines are intended to provide a smooth transition to the rehomed code
in neutron-lib and minimize impacts to subprojects consuming the rehomed code from its
source.

- If the change to consume the code from neutron-lib is widespread and/or "important",
  introduce your intentions for the change via the Neutron team
  `meeting slot <https://wiki.openstack.org/wiki/Network/Meetings#Neutron-lib_and_planned_neutron_refactoring>`_
  for neutron-lib. Subsequently follow-up with an email to openstack-dev list using a
  subject with ``[neutron] neutron-lib impact`` providing additional details as necessary.
  Ideally we can identify the main impacted subprojects by
  `grepping the OpenStack code <http://codesearch.openstack.org/>`_.
- Prepare a neutron core patch to remove and update the rehomed code from its source.
  This can be done without a `debtcollector <https://docs.openstack.org/debtcollector/latest/>`_
  notice by following the steps here. In the patch's commit message include the ``NeutronLibImpact``
  so that we can easily `query <https://review.openstack.org/#/q/status:open+message:%22NeutronLibImpact%22>`_
  for such changes. Mark the patch as a work in progress with a -1 workflow vote.
- If the change is significant enough, it may warrant a "reference implementation" in an
  impacted subproject to ensure the impacts are fully understood. Testing this
  change can be done using the ``Depends-On:`` approach described in the
  `review guidelines <./review-guidelines.html>`_.
- If you are a core reviewer and about to approve a NeutronLibImpact change, please consider
  checking the state of all Stadium subprojects by looking at the
  `grafana periodic dashboard <http://grafana.openstack.org/dashboard/db/neutron-lib-failure-rate?panelId=4&fullscreen>`_.
  This dashboard shows the status of subprojects' unit tests against neutron and neutron-lib
  master branches, and even though it is not exactly validating unit tests against a released
  version of neutron-lib it may be enough of an alarm bell to indicate that something might
  be wrong because of a patch that recently landed in neutron (assuming that the subprojects
  still has direct neutron imports). The check happens daily therefore consider waiting to
  approve if you are either aware of another impactful change recently merged that has not
  been yet processed or you see failure rates spiking.

Examples:

- `348472 <https://review.openstack.org/348472/>`_ removes a validator in neutron that
  was rehomed to neutron-lib.
