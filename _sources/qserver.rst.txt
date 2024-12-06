.. _qserver:

queueserver
===========

The bluesky queueserver [#]_ manages sequencing and execution of Bluesky plans.
It has a host process that manages a RunEngine. Client sessions will interact
with that host process.  See :ref:`qs.host.configure` for more details.

.. important:: The queueserver requires a ``redis`` service [#]_ to be running.
    File ``./qserver/qs-config.yml`` has settings to specify the ``redis`` service.

.. [#] https://blueskyproject.io/bluesky-queueserver/
.. [#] https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/install-redis-on-linux/

.. _qs.host:

QS host -- queueserver host process
-----------------------------------

Use the queueserver host management script.  This option stops the server (if it
is running) and then starts it.  This is the usual way to (re)start the QS host
process.

.. code-block:: bash

    ./qserver/qs_host.sh restart

.. _qs.client:

queueserver client GUI
----------------------

At this time, there is one GUI recommended for use with the bluesky queueserver.
Other GUI clients are in development and show promise of improvements.  For now,
use this one.

.. code-block:: bash

    queue-monitor &

.. _qs.host.configure:

Configure the QS Host
---------------------

File ``qs-config.yml`` [#]_ contains all configuration of the QS host process.
The source code contains lots of comments about the various settings. See the
bluesky-queueserver documentation [#]_ for more details of the configuration.

The QS host process writes files into this directory. This directory can be
relocated. However, it should not be moved into the instrument package since
that might be installed into a read-only directory.

.. [#] download file: :download:`qs-config.yml <../../qserver/qs-config.yml>`
.. [#] https://blueskyproject.io/bluesky-queueserver/manager_config.html

shell script ``qs_host.sh``
---------------------------

A shell script ``qs_host.sh`` [#]_ is used to start the QS host process. Typically,
it is run in the background: ``./qserver/qs_host.sh restart``. This command looks for
a running QS host process.  If found, that process is stopped.  Then, a new QS
host process is started in a *screen* [#]_ session.

.. [#] download file: :download:`qs_host.sh <../../qserver/qs_host.sh>`
.. [#] https://www.gnu.org/software/screen/manual/screen.html

.. code-block:: bash
    :linenos:

    (bstest) $ ./qserver/qs_host.sh help
    Usage: qs_host.sh {start|stop|restart|status|checkup|console|run} [NAME]

        COMMANDS
            console   attach to process console if process is running in screen
            checkup   check that process is running, restart if not
            restart   restart process
            run       run process in console (not screen)
            start     start process
            status    report if process is running
            stop      stop process

        OPTIONAL TERMS
            NAME      name of process (default: bluesky_queueserver-)

Alternatively, run the QS host's startup command directly within the ``./qserver/``
subdirectory.

.. code-block:: bash
    :linenos:

    cd ./qserver
    start-re-manager --config=./qs-config.yml
