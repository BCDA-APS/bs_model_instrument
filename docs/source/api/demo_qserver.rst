.. _api.demo_qserver:

Demo Queue Server
================

The demo queue server provides an example implementation of a Bluesky Queue Server using APSBITS.

Configuration
============

The Queue Server configuration is stored in ``src/apsbits/demo_qserver/qs-config.yml``:

.. literalinclude:: ../../../src/apsbits/demo_qserver/qs-config.yml
   :language: yaml

Starting the Server
=================

The Queue Server can be started using the script at ``src/apsbits/demo_qserver/qs_host.sh``:

.. literalinclude:: ../../../src/apsbits/demo_qserver/qs_host.sh
   :language: bash

Example Usage
============

Here's how to use the queue server:

.. code-block:: python

    from bluesky.plans import count
    from ophyd.sim import det

    # Connect to the Queue Server
    from bluesky_queueserver_api import BPlan
    from bluesky_queueserver_api.zmq import REManagerAPI

    # Create a plan
    plan = BPlan("count", [det], num=5)

    # Add the plan to the queue
    api = REManagerAPI()
    api.item_add(plan)

    # Start the queue
    api.queue_start()

    # Monitor progress
    status = api.status()
    print(f"Queue status: {status['manager_state']}")

<<<<<<< HEAD
For more details on using the Queue Server, see :doc:`../qserver_service`.
=======
For more details on using the Queue Server, see :doc:`../qserver_service`.
>>>>>>> d4841a2b133ec2f8de5bd85c87c97e12c58a69a1
