Setting up your instrument
===============

The iconfig file is a YAML file that contains the configuration for your instrument.
It is used to set up the instrument preferences and settings. The iconfig file is
located in the ``configs`` directory of your instrument package.

RUN_ENGINE
-----------------------------
The ``RUN_ENGINE`` section contains the configuration for the run engine. The run engine is responsible for executing the data acquisition plans.

.. code-block:: yaml

    RUN_ENGINE:
        DEFAULT_METADATA:
            beamline_id: demo_instrument
            instrument_name: Most Glorious Scientific Instrument
            proposal_id: commissioning
            databroker_catalog: *databroker_catalog

        ### EPICS PV to use for the `scan_id`.
        ### Default: `RE.md["scan_id"]` (not using an EPICS PV)
        # SCAN_ID_PV: "IOC:bluesky_scan_id"

        ### Where to "autosave" the RE.md dictionary.
        ### Defaults:
        MD_STORAGE_HANDLER: StoredDict
        MD_PATH: .re_md_dict.yml

        ### The progress bar is nice to see,
        ### except when it clutters the output in Jupyter notebooks.
        ### Default: False
        USE_PROGRESS_BAR: false

.. _iconfig:

BEC
-----------------------------

.. code-block:: yaml

    BEC:
        BASELINE: true
        HEADING: true
        PLOTS: false
        TABLE: true

Callbacks
-----------------------------
.. code-block:: yaml

    NEXUS_DATA_FILES:
    ENABLE: false
    FILE_EXTENSION: hdf

    SPEC_DATA_FILES:
        ENABLE: true
        FILE_EXTENSION: dat

Devices
-----------------------------
.. code-block:: yaml

    ### Local OPHYD Device Control Yaml
    DEVICES_FILES:
    - devices.yml
    APS_DEVICES_FILES:
    - devices_aps_only.yml

    # Log when devices are added to console (__main__ namespace)
    MAKE_DEVICES:
        LOG_LEVEL: info


OPHYD SETTINGS
----------------------------------
.. code-block:: yaml

    OPHYD:
        ### Control layer for ophyd to communicate with EPICS.
        ### Default: PyEpics
        ### Choices: "PyEpics" or "caproto" # caproto is not yet supported
        CONTROL_LAYER: PyEpics

        ### default timeouts (seconds)
        TIMEOUTS:
            PV_READ: &TIMEOUT 5
            PV_WRITE: *TIMEOUT
            PV_CONNECTION: *TIMEOUT


Logging levels
-----------------------------

XMODE_DEBUG_LEVEL: Plain

['Plain', 'Context', 'Verbose', 'Minimal', 'Docs']

Full Iconfig file
-----------------------------

Below we go through the settings available in the iconfig file.

.. literalinclude:: ../../../src/apsbits/demo_instrument/configs/iconfig.yml
   :language: yaml
