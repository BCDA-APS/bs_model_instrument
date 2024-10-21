
"""Loader for creating instances of the devices from a config file."""

import asyncio
import inspect
import logging
import os
import time
from pathlib import Path
from typing import Mapping, Sequence

import tomlkit
from ophyd import Device as ThreadedDevice
from ophyd.sim import make_fake_device
from ophyd_async.core import DEFAULT_TIMEOUT, NotConnected
from ophydregistry import Registry


log = logging.getLogger(__name__)


instrument = None


class Instrument:
    """A beamline instrument built from config files of Ophyd devices.

    *device_classes* should be dictionary that maps configuration
     section names to device classes (or similar items).

    Example:

    ```python
    instrument = Instrument({
      "ion_chamber": IonChamber
      "motors": load_motors,
    })
    ```

    The values in *device_classes* should be one of the following:

    1. A device class
    2. A callable that returns an instantiated device object
    3. A callable that returns a sequence of device objects

    Parameters
    ==========
    device_classes
      Maps config section names to device classes.

    """

    devices: list
    registry: Registry
    beamline_name: str = ""
    hardware_is_present: bool | None = None

    def __init__(self, device_classes: Mapping, registry: Registry | None = None):
        self.devices = []
        if registry is None:
            registry = Registry(auto_register=False, use_typhos=False)
        self.registry = registry
        self.device_classes = device_classes

    def parse_toml_file(self, fd):
        """Parse TOML instrument configuration and create devices.

        An open file descriptor
        """
        config = tomlkit.load(fd)
        # Set global parameters
        beamline = config.get("beamline", {})
        self.beamline_name = beamline.get("name", self.beamline_name)
        self.hardware_is_present = beamline.get(
            "hardware_is_present", self.hardware_is_present
        )
        # Make devices from config file
        return self.parse_config(config)

    def parse_config(self, cfg):
        devices = []
        for key, Klass in self.device_classes.items():
            # Create the devices
            for params in cfg.get(key, []):
                self.validate_params(params, Klass)
                device = self.make_device(params, Klass)
                try:
                    # Maybe its a list of devices?
                    devices.extend(device)
                except TypeError:
                    # No, assume it's just a single device then
                    devices.append(device)
        # Save devices for connecting to later
        self.devices.extend(devices)
        return devices

    def validate_params(self, params, Klass):
        """Check that parameters match a Device class's initializer."""
        sig = inspect.signature(Klass)
        has_kwargs = any(
            [param.kind == param.VAR_KEYWORD for param in sig.parameters.values()]
        )
        # Make sure we're not missing any required parameters
        for key, sig_param in sig.parameters.items():
            # Check for missing parameters
            param_missing = key not in params
            param_required = (
                sig_param.default is sig_param.empty
                and sig_param.kind != sig_param.VAR_KEYWORD
            )

    def make_device(self, params, Klass):
        """Create the devices from their parameters."""
        # Mock threaded ophyd devices if necessary
        try:
            is_threaded_device = issubclass(Klass, ThreadedDevice)
        except TypeError:
            is_threaded_device = False
        if is_threaded_device and not self.hardware_is_present:
            Klass = make_fake_device(Klass)
        # Turn the parameters into pure python objects
        kwargs = {}
        for key, param in params.items():
            if isinstance(param, tomlkit.items.Item):
                kwargs[key] = param.unwrap()
            else:
                kwargs[key] = param
        # Check if we need to injec the registry
        extra_params = {}
        sig = inspect.signature(Klass)
        if "registry" in sig.parameters.keys():
            kwargs["registry"] = self.registry
        # Create the device
        result = Klass(**kwargs)
        return result

    async def connect(
        self,
        mock: bool = False,
        timeout: float = DEFAULT_TIMEOUT,
        force_reconnect: bool = False,
        return_exceptions: bool = False,
    ):
        """Connect all Devices.

        Contains a timeout that gets propagated to device.connect methods.

        Parameters
        ----------
        mock:
          If True then use ``MockSignalBackend`` for all Signals
        timeout:
          Time to wait before failing with a TimeoutError.
        force_reconnect
          Force the signals to establish a new connection.
        """
        t0 = time.monotonic()
        # Sort out which devices are which
        threaded_devices = []
        async_devices = []
        for device in self.devices:
            if hasattr(device, "connect"):
                async_devices.append(device)
            else:
                threaded_devices.append(device)
        # Connect to async devices
        aws = (
            dev.connect(mock=mock, timeout=timeout, force_reconnect=force_reconnect)
            for dev in async_devices
        )
        results = await asyncio.gather(*aws, return_exceptions=True)
        # Filter out the disconnected devices
        new_devices = []
        exceptions = {}
        for device, result in zip(async_devices, results):
            if result is None:
                log.debug(f"Successfully connected device {device.name}")
                new_devices.append(device)
            else:
                # Unexpected exception, raise it so it can be handled
                log.debug(f"Failed connection for device {device.name}")
                exceptions[device.name] = result
        # Connect to threaded devices
        timeout_reached = False
        while not timeout_reached and len(threaded_devices) > 0:
            # Remove any connected devices for the running list
            connected_devices = [
                dev for dev in threaded_devices if getattr(dev, "connected", True)
            ]
            new_devices.extend(connected_devices)
            threaded_devices = [
                dev for dev in threaded_devices if dev not in connected_devices
            ]
            # Tick the clock for the next round through the while loop
            await asyncio.sleep(min((0.05, timeout / 10.0)))
            timeout_reached = (time.monotonic() - t0) > timeout
        # Add disconnected devices to the exception list
        for device in threaded_devices:
            try:
                device.wait_for_connection(timeout=0)
            except TimeoutError as exc:
                exceptions[device.name] = NotConnected(str(exc))
        # Raise exceptions if any were present
        if return_exceptions:
            return new_devices, exceptions
        if len(exceptions) > 0:
            raise NotConnected(exceptions)
        return new_devices

    async def load(
        self,
        connect: bool = True,
        device_classes: Mapping | None = None,
        config_files: Sequence[Path] | None = None,
        return_exceptions: bool = False,
    ):
        """Load instrument specified in config files.

        Unless, explicitly overridden by the *config_files* argument,
        configuration files are read from the environmental variable
        HAVEN_CONFIG_FILES (separated by ':').

        Parameters
        ==========
        connect
          If true, establish connections for the devices now.
        device_classes
          A temporary set of device classes to use for this call
          only. Overrides any device classes given during
          initalization.
        config_files
          I list of file paths that will be loaded. If omitted, those
          files listed in HAVEN_CONFIG_FILES will be used.
        return_exceptions
          If true, exceptions will be returned for further processing,
          otherwise, exceptions will be raised (default).

        """
        self.devices = []
        # Decide which config files to use
        if config_files is None:
            env_key = "HAVEN_CONFIG_FILES"
            if env_key in os.environ.keys():
                config_files = os.environ.get("HAVEN_CONFIG_FILES", "")
                config_files = [Path(fp) for fp in config_files.split(":")]
            else:
                config_files = [
                    Path(__file__).parent.resolve() / "../configs"
                ]
        # Load the instrument from config files
        old_classes = self.device_classes
        try:
            # Temprary override of device classes
            if device_classes is not None:
                self.device_classes = device_classes
            # Parse TOML files
            for fp in config_files:
                with open(fp, mode="tr", encoding="utf-8") as fd:
                    self.parse_toml_file(fd)
        finally:
            self.device_classes = old_classes
        # Connect the devices
        if connect:
            new_devices, exceptions = await self.connect(
                mock=not self.hardware_is_present, return_exceptions=True
            )
        else:
            new_devices = self.devices
            exceptions = []
        # Registry devices
        for device in new_devices:
            self.registry.register(device)
        # Raise exceptions
        if return_exceptions:
            return exceptions
        elif len(exceptions) > 0:
            raise NotConnected(exceptions)


