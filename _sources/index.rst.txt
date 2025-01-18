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

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   demo
   sessions
   guides/index
   install
   logging_config
   license
   api/index

About ...
-----------

:home: https://BCDA-APS.github.io/bs_model_instrument/
:bug tracker: https://github.com/BCDA-APS/bs_model_instrument/issues
:source: https://github.com/BCDA-APS/bs_model_instrument
:license: :ref:`license`
:full version: |version|
:published: |today|
:reference: :ref:`genindex`, :ref:`modindex`, :ref:`search`
