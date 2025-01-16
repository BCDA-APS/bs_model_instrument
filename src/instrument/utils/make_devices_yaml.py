"""
Make devices from YAML files
=============================

Construct ophyd-style devices from simple specifications in YAML files.

.. autosummary::

    ~Instrument
    ~make_devices
"""

__all__ = ["Instrument"]

import inspect
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
    (plan) Create the ophyd-style controls for this instrument.

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

    if main and not _sphinx_is_running():
        # CI will stall here when building the docs.
        for label in oregistry.device_names:
            # add to __main__ namespace
            setattr(main_namespace, label, oregistry[label])


def _sphinx_is_running() -> bool:
    """Are we running 'sphinx-build'?"""
    outermost_frame = inspect.getouterframes(inspect.currentframe())[-1]
    return "sphinx-build" in outermost_frame.filename
    #     # When Sphinx is building the documentation,
    #     # CI stalls here.  So, protect this call.


class Instrument(guarneri.Instrument):
    """
    Custom YAML loader for guarneri.

    EXAMPLES:

    .. code-block:: yaml

        apstools.synApps.Optics2Slit2D_HV:
            - name: slit1
                prefix: ioc:Slit1
                labels: ["slits"]

        hkl.SimulatedE4CV:
            - name: sim4c
                prefix: ""
                labels: ["diffractometer"]

        ophyd.scaler.ScalerCH:
            - name: scaler1
                prefix: vme:scaler1
                labels: ["scalers", "detectors"]

        ophyd.EpicsMotor:
            - {name: m1, prefix: gp:m1, labels: ["motor"]}
            - {name: m2, prefix: gp:m2, labels: ["motor"]}
            - {name: m3, prefix: gp:m3, labels: ["motor"]}
            - {name: m4, prefix: gp:m4, labels: ["motor"]}
    """

    def parse_yaml_file(self, config_file: pathlib.Path | str) -> list[dict]:
        """Read device configurations from YAML format file."""
        if isinstance(config_file, str):
            config_file = pathlib.Path(config_file)

        def parse(class_name, specs):
            if class_name not in self.device_classes:
                self.device_classes[class_name] = dynamic_import(class_name)
            entries = []
            for table in specs:
                entry = {
                    "device_class": class_name,
                    "args": (),  # ALL specs are kwargs!
                    "kwargs": table,
                }
                entries.append(entry)
            return entries

        controls = load_config_yaml(config_file)
        devices = []
        for k, v in controls.items():
            devices += parse(k, v)
        return devices


_instr = Instrument({}, registry=oregistry)  # singleton
