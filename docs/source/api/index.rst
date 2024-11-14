.. _api:

API: The Source Code
====================

The instrument model is described by this directory structure:

.. code-block:: text
    :linenos:

    docs/source         sphinx documentation source
    pyproject.toml      project configuration
    qserver/                 files for running a queueserver host process
    src/                Python source code tree
        instrument/     root of the 'instrument' package
            startup.py  Python code to setup a session for Bluesky data acquisition
            callbacks/  receive and handle info from other code
            configs/    configuration files
            core/       create core components of Bluesky data acquisition
            devices/    your instrument's controls
            plans/      your instrument's measurement procedures
            utils/      other code to setup or use your instrument

A Bluesky data acquisition session :ref:`begins with <api.startup>`:

.. code-block:: py

    from instrument.startup import *

The ``instrument/`` directory is described in the following sections.

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   startup
   callbacks
   configs
   core
   devices
   plans
   utils
