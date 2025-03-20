"""
Demo instrument package.

This package provides a demo instrument implementation for testing and development.
"""

import logging
from pathlib import Path

from apsbits.utils.config_loaders import load_config

logger = logging.getLogger(__name__)
logger.bsdev(__file__)

# Get the path to the instrument package
instrument_path = Path(__file__).parent

# Load configuration
iconfig_path = instrument_path / "configs" / "iconfig.yml"
load_config(iconfig_path)

logger.info("Starting Instrument with iconfig: %s", iconfig_path)
