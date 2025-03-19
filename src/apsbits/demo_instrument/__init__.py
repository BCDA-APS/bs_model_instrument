"""
Demo instrument package.

This package provides a demo instrument implementation for testing and development.
"""

import logging
from pathlib import Path

from apsbits.core.config import load_config, get_config

logger = logging.getLogger(__name__)
logger.bsdev(__file__)

# Get the path to the instrument package
instrument_path = Path(__file__).parent

# Load configuration
iconfig_path = instrument_path / "configs" / "iconfig.yml"
load_config(iconfig_path)
iconfig = get_config()

logger.info("Starting Instrument with iconfig: %s", iconfig_path)

# Import the rest of the package
from . import startup
from . import plans
from . import callbacks
from . import configs


