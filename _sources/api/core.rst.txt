.. _api.core:

``instrument.core``
===================

Create the core components of Bluesky data acquisition, in the order required by
their function. (e.g., timeout defaults must be set before any ophyd objects are
created)

.. autosummary::
    :nosignatures:

    ~instrument.core.best_effort_init
    ~instrument.core.catalog_init
    ~instrument.core.run_engine_init

.. automodule:: instrument.core.best_effort_init
.. automodule:: instrument.core.catalog_init
.. automodule:: instrument.core.run_engine_init
