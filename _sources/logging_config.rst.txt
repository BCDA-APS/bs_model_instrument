.. _logging.session:
.. index:: !logging

===============
Session logging
===============

Configure logging for this session.

There are many *loggers* that report messages via the Python ``logging``
package. A logger could be created by a Python package, module, class, or
object. The level of detail for each is controlled by the *level* of the logger.
The level indicates the minimum severity of message to be reported.
In order of increasing detail: ``critical``, ``error``, ``warning`` (the default
level), ``info``, ``debug``.

The next table shows some of the many possible loggers. Configure the
``configs/logging.yml`` file in the ``module_logging_levels`` section, assigning
one of the logging to each logger to be configured.

.. tip:: If you see too much detail from a logger, set its level to ``warning``
    or higher severity in the ``configs/logging.yml`` file. See section
    :ref:`logging.named.levels` for a table of the logging levels.

Here is a list of some of the loggers in which you may be interested (there
could be others):

==========================  ====================================================
logger name                 description
==========================  ====================================================
``apstools``                logger for messages from the apstools package
``bluesky``                 logger to which all bluesky log records propagate
``bluesky.emit_document``   when a Document is emitted. The log record does not contain the full content of the Document.
``bluesky.RE``              Records from a RunEngine. INFO-level notes state changes. DEBUG-level notes when each message from a plan is about to be processed and when a status object has completed.
``bluesky.RE.msg``          when each ``Msg`` is about to be processed.
``bluesky.RE.state``        when the RunEngine’s state changes.
``databroker``              logger to which all databroker log records propagate
``ophyd``                   logger to which all ophyd log records propagate
``ophyd.objects``           records from all devices and signals (that is, OphydObject subclasses)
``ophyd.control_layer``     requests issued to the underlying control layer (e.g. pyepics, caproto)
``ophyd.event_dispatcher``  regular summaries of the backlog of updates from the control layer that are being processed on background threads
==========================  ====================================================

.. _logging.named.levels:

Python logging's named levels
-----------------------------

Python has six *named* log levels.  The level specifies the minimum severity of
messages to report. Each named level is assigned a specific integer indicating
the severity of the log.

This package adds `"BSDEV"` to the list.

=========   =========   ==================================================
name        severity    comments
=========   =========   ==================================================
CRITICAL    50          Examine immediately. **Quietest** level.
ERROR       40          Something has failed.  [#includes]_
WARNING     30          Something needs attention.  [#includes]_
INFO        20          A report that may be of interest.  [#includes]_
BSDEV       15          A report of interest to developers.  [#includes]_
DEBUG       10          Diagnostic. **Noisiest** level.  [#includes]_
NOTSET      0           Initial setting, defaults to WARNING.
=========   =========   ==================================================

.. [#includes] Includes all above level(s).

.. tip:: Level names used in the ``configs/logging.yml`` file may be
    upper or lower case.  The code converts them to upper case.

References
----------

* https://blueskyproject.io/bluesky/main/debugging.html#logger-names
* https://blueskyproject.io/ophyd/user_v1/reference/logging.html#logger-names
