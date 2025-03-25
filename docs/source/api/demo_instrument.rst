.. _api.demo_instrument:

Demo Instrument
=============

The ``demo_instrument`` module provides a complete example of how to build a Bluesky instrument using APSBITS. It includes:

.. code-block:: text
    :linenos:

    demo_instrument/
        startup.py   setup a demo session for Bluesky data acquisition
        callbacks/   receive and handle info from other code
        configs/    configuration files
        devices/    demo instrument's controls
        plans/      demo instrument's measurement procedures

Example Usage
------------

Start a Bluesky data acquisition session with:

.. code-block:: python

    from apsbits.demo_instrument.startup import *
    from apsbits.demo_instrument.plans import *

    RE(demo_print_plan())
    RE(demo_count_plan())
    RE(demo_rel_scan_plan())

Components
---------

startup
~~~~~~~

.. automodule:: apsbits.demo_instrument.startup
   :members:
   :undoc-members:
   :show-inheritance:

callbacks
~~~~~~~~

.. automodule:: apsbits.demo_instrument.callbacks
   :members:
   :undoc-members:
   :show-inheritance:

devices
~~~~~~~

.. automodule:: apsbits.demo_instrument.devices
   :members:
   :undoc-members:
   :show-inheritance:

plans
~~~~~

.. automodule:: apsbits.demo_instrument.plans
   :members:
   :undoc-members:
<<<<<<< HEAD
   :show-inheritance:
=======
   :show-inheritance:
>>>>>>> d4841a2b133ec2f8de5bd85c87c97e12c58a69a1
