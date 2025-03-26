APSBITS (|release|)
======================

A Python package providing tools and utilities to build Bluesky Data Acquisition Instruments that can run in console, notebook, & queueserver environments.

Start your data collection session using the demo instrument as an example:

.. code-block:: py
      :linenos:

      from apsbits.demo_instrument.startup import *
      from apsbits.demo_instrument.plans import *

      RE(sim_print_plan())
      RE(sim_count_plan())
      RE(sim_rel_scan_plan())


.. for icon suggestions, see:
      https://fonts.google.com/icons

.. grid:: 2

    .. grid-item-card:: :material-regular:`install_desktop;3em` :doc:`install`

      How to install the *apsbits* package.

    .. grid-item-card:: :material-regular:`preview;3em` :doc:`demo`

      Demo: Using the demo instrument.

    .. grid-item-card:: :material-regular:`school;3em` :ref:`guides`

      Guides, How-Tos, and examples for creating your own instrument.

    .. grid-item-card:: :material-regular:`play_arrow;3em` :doc:`sessions`

      Run instruments in IPython, Jupyter notebook, Python scripts, and
      Bluesky Queueserver sessions.

    .. grid-item-card:: :material-regular:`subscriptions;3em` :ref:`api`

      Explore the Python code and core functionality.

    .. grid-item-card:: :material-regular:`description;3em` :doc:`logging_config`

      Configure the session logging capabilities.

.. toctree::
   :maxdepth: 1
   :hidden:

   install
   guides/template_creation
   sessions
   guides/index
   guides/qserver_service
   logging_config
   demo
   api/index
   license
   history


About ...
---------

:home: https://BCDA-APS.github.io/BITS/
:bug tracker: https://github.com/BCDA-APS/BITS/issues
:source: https://github.com/BCDA-APS/BITS
:license: :ref:`license`
:full version: |version|
:published: |today|
:reference: :ref:`genindex`, :ref:`modindex`, :ref:`search`
:release notes: :doc:`History of Changes with each Release <history>`
