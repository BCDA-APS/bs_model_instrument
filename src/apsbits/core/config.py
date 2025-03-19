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
        with open(config_path, 'r') as f:
            loaded_config = yaml.safe_load(f)
            
        # Validate version
        version = loaded_config.get("ICONFIG_VERSION")
        if not version or version < DEFAULT_CONFIG["ICONFIG_VERSION"]:
            logger.warning(
                f"Configuration version {version} is older than minimum required "
                f"version {DEFAULT_CONFIG['ICONFIG_VERSION']}. Using defaults."
            )
            return

        # Update the global configuration
        _iconfig.update(loaded_config)
        logger.info(f"Successfully loaded configuration from: {config_path}")
        
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        logger.warning("Using default configuration.")


def get_config() -> Dict[str, Any]:
    """
    Get the current configuration.

    Returns:
        The current configuration dictionary.
    """
    return _iconfig.copy()


def update_config(updates: Dict[str, Any]) -> None:
    """
    Update the configuration with new values.

    Args:
        updates: Dictionary of configuration updates.
    """
    global _iconfig
    _iconfig.update(updates)
    logger.info("Configuration updated")


# Initialize with default configuration
_iconfig = DEFAULT_CONFIG.copy() 