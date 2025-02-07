instrument (|release|)
======================

Model of a Bluesky Data Acquisition Instrument in console, notebook, & queueserver.

Start the data collection session with the same command, whether in the IPython
console, a Jupyter notebook, the queueserver, or even a Python script:

.. code-block:: py
      :linenos:

      from instrument.startup import *
      from instrument.tests.sim_plans import *

      RE(sim_print_plan())
      RE(sim_count_plan())
      RE(sim_rel_scan_plan())


.. for icon suggestions, see:
      https://fonts.google.com/icons

.. grid:: 2

    .. grid-item-card:: :material-regular:`install_desktop;3em` :doc:`install`

      How to install the *instrument* package.

    .. grid-item-card:: :material-regular:`preview;3em` :doc:`demo`

      Demo: Notebook Startup.

    .. grid-item-card:: :material-regular:`school;3em` :ref:`guides`

      Guides, How-Tos, ...

    .. grid-item-card:: :material-regular:`play_arrow;3em` :doc:`sessions`

      Start the instrument in IPython, Jupyter notebook, Python scripts, and
      Bluesky Queueserver sessions.

    .. grid-item-card:: :material-regular:`subscriptions;3em` :ref:`api`

      Explore the Python code for your instrument.

    .. grid-item-card:: :material-regular:`description;3em` :doc:`logging_config`

      Configure the session logging capabilities.

.. toctree::
   :maxdepth: 1
   :hidden:

   demo
   sessions
   guides/index
   install
   logging_config
   license
   api/index

About ...
---------

:home: https://BCDA-APS.github.io/bs_model_instrument/
:bug tracker: https://github.com/BCDA-APS/bs_model_instrument/issues
:source: https://github.com/BCDA-APS/bs_model_instrument
:license: :ref:`license`
:full version: |version|
:published: |today|
:reference: :ref:`genindex`, :ref:`modindex`, :ref:`search`
