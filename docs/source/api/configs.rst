.. _api.configs:

``instrument.configs``
======================

Configuration files related to this Bluesky instrument package. Configuration of
the bluesky queueserver host process (QS host) is described  in the :ref:`qserver`
section.

.. _api.configs.iconfig:

``iconfig.yml``
---------------

Various constants and terms used to configure the instrument package.

.. literalinclude:: ../../../src/instrument/configs/iconfig.yml
    :language: yaml
    :linenos:

.. _api.configs.devices:

``devices.yml``
------------------------------

Declarations of the ophyd (and ophyd-like) devices and signals used by the
instrument package.  Configuration is used by the guarneri package to create the
objects.

.. literalinclude:: ../../../src/instrument/configs/devices.yml
    :language: yaml
    :linenos:

.. _api.configs.devices_aps_only:

``devices_aps_only.yml``
------------------------------

Declarations of the ophyd (and ophyd-like) devices and signals
only available when Bluesky is used at the APS.

.. literalinclude:: ../../../src/instrument/configs/devices_aps_only.yml
    :language: yaml
    :linenos:
