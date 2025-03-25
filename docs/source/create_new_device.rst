Create New Device
==================

The Queue Server provides a way to run Bluesky plans remotely.

Overview
--------

The ``create_new_device`` module allows you to:

* Create new device configurations
* Generate device class files automatically
* Manage device configurations in YAML format
* Load existing device classes

Example Configuration Files
---------------------------

The demo instrument includes example configuration files:

* Main device configuration: ``src/apsbits/demo_instrument/configs/devices.yml``
* Instrument configuration: ``src/apsbits/demo_instrument/configs/iconfig.yml``
* Logging configuration: ``src/apsbits/demo_instrument/configs/logging.yml``

Example Device Definitions
--------------------------

The demo instrument includes example device definitions in ``src/apsbits/demo_instrument/devices/__init__.py``:

.. literalinclude:: ../../src/apsbits/demo_instrument/devices/__init__.py
   :language: python

Device Configuration Examples
-----------------------------

Here's an example of various device configurations that can be defined in your ``devices.yml`` file:

.. code-block:: yaml

    # Simulated Devices
    apsbits.utils.sim_creator.predefined_device:
    - {creator: ophyd.sim.motor, name: sim_motor}
    - {creator: ophyd.sim.noisy_det, name: sim_det}

    # Simulated Shutter
    apstools.devices.SimulatedApsPssShutterWithStatus:
    - name: shutter
      labels: ["shutters"]

    # Example Signal Device
    ophyd.Signal:
    - name: test
      value: 50.7
    - name: t2
      value: 2

    # Example 2D Slit Device
    apstools.synApps.Optics2Slit2D_HV:
    - name: slit1
      prefix: ioc:Slit1
      labels: ["slits"]

    # Example Scaler Channel Device
    ophyd.scaler.ScalerCH:
    - name: scaler1
      prefix: vme:scaler1
      labels: ["scalers", "detectors"]

    # Example EPICS Motors
    ophyd.EpicsMotor:
    - {name: m1, prefix: gp:m1, labels: ["motor"]}
    - {name: m2, prefix: gp:m2, labels: ["motor"]}
    - {name: m3, prefix: gp:m3, labels: ["motor"]}
    - {name: m4, prefix: gp:m4, labels: ["motor"]}

Each device configuration specifies:

* Device class path (e.g., ``ophyd.Signal``, ``ophyd.EpicsMotor``)
* Device name and prefix (if applicable)
* Labels for device categorization
* Additional parameters specific to each device type

Usage
-----

Basic Usage
~~~~~~~~~~~

.. code-block:: python

    from pathlib import Path
    from apsbits.utils.create_new_device import DeviceConfig, create_new_device

    # Create a device configuration
    config = DeviceConfig(
        name="my_sensor",
        device_type="temperature_sensor",
        class_name="TemperatureSensor",
        parameters={
            "port": "/dev/ttyUSB0",
            "baud_rate": 9600
        },
        location="lab_1"
    )

    # Create the device
    result = create_new_device(
        config,
        config_file=Path("src/apsbits/demo_instrument/configs/devices.yml")
    )

Configuration Structure
~~~~~~~~~~~~~~~~~~~~~~~

The ``DeviceConfig`` dataclass accepts the following parameters:

* ``name`` (str): Unique identifier for the device
* ``device_type`` (str): Type of device (e.g., "temperature_sensor", "power_supply")
* ``class_name`` (str): Name of the Python class to use/create
* ``parameters`` (Dict[str, Any]): Device-specific configuration parameters
* ``location`` (Optional[str]): Physical location of the device

YAML Configuration
~~~~~~~~~~~~~~~~~~

Devices are stored in ``instrument/configs/devices.yml`` with the following structure:

.. code-block:: yaml

    devices:
      my_sensor:
        name: my_sensor
        type: temperature_sensor
        class: TemperatureSensor
        location: lab_1
        parameters:
          port: /dev/ttyUSB0
          baud_rate: 9600
        status: initialized

Generated Device Classes
~~~~~~~~~~~~~~~~~~~~~~~~

When a new device class is created, it will be placed in ``instrument/devices/`` with the following structure:

.. code-block:: python

    from typing import Dict, Any

    class DeviceName:
        """Device class for device_type.

        Attributes:
            config: Configuration dictionary for the device
        """

        def __init__(self, config: Dict[str, Any]) -> None:
            self.config = config

        def initialize(self) -> None:
            """Initialize the device hardware."""
            pass

        def close(self) -> None:
            """Close the device connection."""
            pass

API Reference
-------------

DeviceConfig
~~~~~~~~~~~~

.. code-block:: python

    @dataclass
    class DeviceConfig:
        name: str
        device_type: str
        class_name: str
        parameters: Dict[str, Any]
        location: Optional[str] = None

create_new_device
~~~~~~~~~~~~~~~~~

.. code-block:: python

    def create_new_device(
        config: DeviceConfig,
        config_file: Optional[Path] = None
    ) -> Dict[str, Any]
    """

Creates a new device with the specified configuration and optionally saves it to a YAML file.

**Parameters:**
* ``config``: DeviceConfig object containing device specifications
* ``config_file``: Optional path to the devices configuration file

**Returns:**
* Dictionary containing the created device information

**Raises:**
* ``ValueError``: If the device name is empty or invalid
* ``ImportError``: If the device class cannot be loaded

Helper Functions
~~~~~~~~~~~~~~~~~

load_or_create_yaml
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    def load_or_create_yaml(file_path: Path) -> Dict[str, Any]
    """

Loads an existing YAML file or creates a new one if it doesn't exist.

create_device_class
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    def create_device_class(class_name: str, device_type: str) -> None
    """

Creates a new device class file if it doesn't exist.

get_device_class
^^^^^^^^^^^^^^^^

.. code-block:: python

    def get_device_class(class_name: str) -> Type[Any]
    """

Gets a device class by name, importing it from the devices directory.

**Parameters:**
* ``class_name``: Name of the class to import

**Returns:**
* The device class

**Raises:**
* ``ImportError``: If the class cannot be imported

validate_device_config
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    def validate_device_config(config: DeviceConfig) -> None
    """

Validates a device configuration.

**Parameters:**
* ``config``: Device configuration to validate

**Raises:**
* ``ValueError``: If configuration is invalid

update_device_config
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    def update_device_config(
        device_name: str,
        updates: Dict[str, Any],
        config_file: Path
    ) -> Dict[str, Any]
    """

Updates an existing device configuration.

**Parameters:**
* ``device_name``: Name of the device to update
* ``updates``: Dictionary of updates to apply
* ``config_file``: Path to configuration file

**Returns:**
* Updated device configuration

**Raises:**
* ``ValueError``: If device does not exist

delete_device
^^^^^^^^^^^^

.. code-block:: python

    def delete_device(device_name: str, config_file: Path) -> None
    """

Deletes a device from the configuration.

**Parameters:**
* ``device_name``: Name of the device to delete
* ``config_file``: Path to configuration file

**Raises:**
* ``ValueError``: If device does not exist

list_devices
^^^^^^^^^^^

.. code-block:: python

    def list_devices(config_file: Path) -> Dict[str, Dict[str, Any]]
    """

Lists all devices in the configuration.

**Parameters:**
* ``config_file``: Path to configuration file

**Returns:**
* Dictionary of device configurations

File Structure
--------------

::

    instrument/
    ├── configs/
    │   └── devices.yml
    ├── devices/
    │   ├── __init__.py
    │   └── <device_classes>.py
    └── src/
        └── create_new_device.py

Error Handling
--------------

The module includes comprehensive error handling for common scenarios:

* Invalid device names
* Missing configuration files
* Import errors for device classes
* File system access issues

All errors are logged using Python's logging module, with appropriate debug and info messages for successful operations.

Testing
-------

Tests are provided in ``tests/test_create_new_device.py`` and can be run using pytest:

.. code-block:: bash

    pytest tests/test_create_new_device.py

The tests cover:

* Device creation with and without configuration files
* Device class file generation
* Error handling
* YAML file management
* Logging functionality
