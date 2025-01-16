"""
Make devices from YAML files
=============================

Construct ophyd-style devices from simple specifications in YAML files.

.. autosummary::
    :nosignatures:

    ~make_devices
    ~Instrument
"""

import logging
import pathlib
import sys
import time

import guarneri
from apstools.plans import run_blocking_function
from apstools.utils import dynamic_import
from bluesky import plan_stubs as bps

from .aps_functions import host_on_aps_subnet
from .config_loaders import iconfig
from .config_loaders import load_config_yaml
from .controls_setup import oregistry  # noqa: F401

logger = logging.getLogger(__name__)
logger.bsdev(__file__)


configs_path = pathlib.Path(__file__).parent.parent / "configs"
main_namespace = sys.modules["__main__"]
local_control_devices_file = iconfig["DEVICES_FILE"]
aps_control_devices_file = iconfig["APS_DEVICES_FILE"]


def make_devices(*, pause: float = 1):
    """
    (plan stub) Create the ophyd-style controls for this instrument.

    Feel free to modify this plan to suit the needs of your instrument.

    EXAMPLE::

        RE(make_devices())

    PARAMETERS

    pause : float
        Wait 'pause' seconds (default: 1) for slow objects to connect.

    """
    logger.debug("(Re)Loading local control objects.")
    yield from run_blocking_function(
        _loader, configs_path / local_control_devices_file, main=True
    )

    if host_on_aps_subnet():
        yield from run_blocking_function(
            _loader, configs_path / aps_control_devices_file, main=True
        )

    if pause > 0:
        logger.debug(
            "Waiting %s seconds for slow objects to connect.",
            pause,
        )
        yield from bps.sleep(pause)

    # Configure any of the controls here, or in plan stubs


def _loader(yaml_device_file, main=True):
    """
    Load our ophyd-style controls as described in a YAML file.

    PARAMETERS

    yaml_device_file : str or pathlib.Path
        YAML file describing ophyd-style controls to be created.
    main : bool
        If ``True`` add these devices to the ``__main__`` namespace.

    """
    logger.debug("Devices file %r.", str(yaml_device_file))
    t0 = time.time()
    _instr.load(yaml_device_file)
    logger.debug("Devices loaded in %.3f s.", time.time() - t0)

    if main:
        for label in oregistry.device_names:
            # add to __main__ namespace
            setattr(main_namespace, label, oregistry[label])


class Instrument(guarneri.Instrument):
    """Custom YAML loader for guarneri."""

    def parse_yaml_file(self, config_file: pathlib.Path | str) -> list[dict]:
        """Read device configurations from YAML format file."""
        if isinstance(config_file, str):
            config_file = pathlib.Path(config_file)

        def parser(class_name, specs):
            if class_name not in self.device_classes:
                self.device_classes[class_name] = dynamic_import(class_name)
            entries = [
                {
                    "device_class": class_name,
                    "args": (),  # ALL specs are kwargs!
                    "kwargs": table,
                }
                for table in specs
            ]
            return entries

        devices = [
            device
            # parse the file
            for k, v in load_config_yaml(config_file).items()
            # each support type (class, factory, function, ...)
            for device in parser(k, v)
        ]
        return devices


_instr = Instrument({}, registry=oregistry)  # singleton
