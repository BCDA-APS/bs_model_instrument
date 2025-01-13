"""
Load control objects
====================

Plans to create the local controls from configuration files.

.. autosummary::
    ~make_controls
    ~_loader

EXAMPLE::

    ipython -i -c "from instrument.startup import *; RE(make_controls())"
"""

import logging
import pathlib
import sys
import time

from apstools.plans import run_blocking_function
from bluesky import plan_stubs as bps

from ..utils.local_controls import Instrument
from ..utils.aps_functions import host_on_aps_subnet
from ..utils.controls_setup import oregistry  # noqa: F401
from ..utils.config_loaders import iconfig 

logger = logging.getLogger(__name__)
logger.bsdev(__file__)


configs_path = pathlib.Path(__file__).parent.parent / "configs"
instr = Instrument({}, registry=oregistry)  # singleton
main_namespace = sys.modules["__main__"]
local_control_devices_file  = iconfig["LOCAL_DEVICES_FILE"]
aps_control_devices_file  = iconfig["APS_DEVICES_FILE"]

def make_controls(*, pause: float = 1):
    """
    (plan) Create the ophyd-style controls for this instrument.

    Feel free to modify this plan to suit the needs of your instrument.

    EXAMPLE::

        RE(make_controls())

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
    instr.load(yaml_device_file)
    logger.debug("Devices loaded in %.3f s.", time.time() - t0)

    if main:
        for label in oregistry.device_names:
            # add to __main__ namespace
            setattr(main_namespace, label, oregistry[label])
