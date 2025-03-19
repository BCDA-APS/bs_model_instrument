"""
Load device definitions from YAML files.

This module provides functionality to load device definitions from YAML files
and register them with the ophyd registry.
"""

import logging
from pathlib import Path
from typing import Dict, Any, Optional, Generator

from bluesky.utils import Msg
from apsbits.core.config import get_config
from apsbits.utils.controls_setup import oregistry

logger = logging.getLogger(__name__)
logger.bsdev(__file__)



def make_devices() -> Generator[Msg, None, None]:
    """
    Load device definitions from YAML files and register them with the ophyd registry.

    This is a Bluesky plan that loads device definitions. Since this is just loading
    device definitions and not collecting data, it doesn't create a run.

    Returns:
        A generator that yields Bluesky messages.
    """
    iconfig = get_config()
    
    # Load local control devices
    local_control_devices_file = Path(iconfig.get("DEVICES_FILE", "")).resolve()
    if local_control_devices_file.exists():
        logger.info("Loading local control devices from: %s", local_control_devices_file)
        _load_devices(local_control_devices_file)

    # Load APS control devices
    aps_control_devices_file = Path(iconfig.get("APS_DEVICES_FILE", "")).resolve()
    if aps_control_devices_file.exists():
        logger.info("Loading APS control devices from: %s", aps_control_devices_file)
        _load_devices(aps_control_devices_file)

    # Yield a null message to make this a valid plan
    yield Msg('null')


def _load_devices(devices_file: Path) -> None:
    """
    Load device definitions from a YAML file.

    Args:
        devices_file: Path to the devices YAML file.
    """
    import yaml

    try:
        with open(devices_file, "r") as f:
            devices = yaml.safe_load(f)

        for name, device_config in devices.items():
            if name not in oregistry:
                logger.info("Registering device: %s", name)
                oregistry[name] = device_config
            else:
                logger.warning("Device already registered: %s", name)

    except Exception as e:
        logger.error("Error loading devices from %s: %s", devices_file, e)
        raise
