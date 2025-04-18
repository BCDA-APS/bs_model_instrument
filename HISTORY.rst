..
  This file describes user-visible changes between the versions.
  At this time, there is no automation to update this file.
  Try to describe in human terms what is relevant for each release.

  Revise this file before tagging a new release.

  Subsections could include these headings (in this order), omit if no content.

    Notice
    Breaking Changes
    New Features
    Enhancements
    Fixes
    Maintenance
    Deprecations
    New Contributors

.. _release_notes:

========
Releases
========

Brief notes describing each release and what's new.

Project `milestones <https://github.com/prjemian/hklpy2/milestones>`_
describe future plans.

.. Coming release content can be gathered here.
    Some people object to publishing unreleased changes.

    1.0.2
    #####

    release expected 2025-Q2

1.0.1
#####

released 2025-03-24

Fixes
-----

* Calling RE(make_devices()) twice raises a lot of errors.
* startup sequence needs revision
* make_devices() needs a 'clear 'option
* make_devices() is noisy
* Why does make_devices() add all ophyd.sim simulator objects to ophyd registry?
* First argument to logger.LEVEL() should not be an f-string
* Adjust the order of steps when creating RE
* bp.scan (& others) missing in queueserver
* QS restart does not restart when QS was running

1.0.0
#####

released 2025-03-21

Initial public release.
