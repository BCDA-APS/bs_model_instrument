"""
Configuration management for the instrument.

This module serves as the single source of truth for instrument configuration.
It loads and validates the configuration from the iconfig.yml file and provides
access to the configuration throughout the application.
"""

import logging
from pathlib import Path
from typing import Dict, Any

import yaml

logger = logging.getLogger(__name__)
logger.bsdev(__file__)

# Default configuration values
DEFAULT_CONFIG = {
    "ICONFIG_VERSION": "2.0.0",
    "DATABROKER_CATALOG": "temp",
    "RUN_ENGINE": {
        "DEFAULT_METADATA": {
            "beamline_id": "instrument",
            "instrument_name": "Most Glorious Scientific Instrument",
            "proposal_id": "commissioning",
            "databroker_catalog": "temp",
        }
    },
    "XMODE_DEBUG_LEVEL": "Plain",
}

# Global configuration instance
_iconfig: Dict[str, Any] = DEFAULT_CONFIG.copy()
_test_config: Dict[str, Any] = {}


def load_config(config_path: Path) -> None:
    """
    Load configuration from a YAML file.

    Args:
        config_path: Path to the configuration file.
    """
    global _iconfig
    
    if not config_path.exists():
        logger.warning(f"Configuration file not found at {config_path}. Using defaults.")
        return

    try:
        with open(config_path) as f:
            config = yaml.safe_load(f)
            if config is None:
                config = {}
            _iconfig.update(config)
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")


def get_config() -> Dict[str, Any]:
    """
    Get the current configuration.

    Returns:
        The current configuration dictionary.
    """
    return _test_config if _test_config else _iconfig


def update_config(updates: Dict[str, Any]) -> None:
    """
    Update the current configuration.

    Args:
        updates: Dictionary of configuration updates.
    """
    _iconfig.update(updates)


def set_test_config(config: Dict[str, Any]) -> None:
    """
    Set a test configuration.

    Args:
        config: Dictionary of test configuration.
    """
    global _test_config
    _test_config = config


def reset_test_config() -> None:
    """Reset the test configuration."""
    global _test_config
    _test_config = {}


# Initialize with default configuration
_iconfig = DEFAULT_CONFIG.copy() 