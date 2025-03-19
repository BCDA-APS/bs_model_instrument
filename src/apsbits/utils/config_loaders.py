"""
Load configuration files
========================

Load supported configuration files, such as ``iconfig.yml``.

.. autosummary::
    ~load_config_yaml
    ~IConfigFileVersionError
"""

import logging
import pathlib
from typing import Dict, Any

from apsbits.core.config import get_config

logger = logging.getLogger(__name__)
logger.bsdev(__file__)

# Minimum required version for iconfig.yml files
ICONFIG_MINIMUM_VERSION = "2.0.0"


def load_config_yaml(iconfig_yml: str = None) -> Dict[str, Any]:
    """
    Load iconfig.yml (and other YAML) configuration files.

    Args:
        iconfig_yml: Path to the configuration file.

    Returns:
        Dict containing the configuration.

    Raises:
        IConfigFileVersionError: If the configuration version is too old.
    """
    if iconfig_yml is None:
        raise ValueError(
            "No configuration file provided. Please specify a valid 'iconfig.yml' file."
        )

    path = pathlib.Path(iconfig_yml)
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {iconfig_yml}")

    # Get the current configuration
    iconfig = get_config()
    
    # Validate the iconfig file has the minimum version
    _version = iconfig.get("ICONFIG_VERSION")
    if _version is None or _version < ICONFIG_MINIMUM_VERSION:
        raise ValueError(
            f"Configuration file '{iconfig_yml}' has version {_version!r}."
            f" Expected minimum {ICONFIG_MINIMUM_VERSION!r}."
        )

    return iconfig


# class IConfigFileVersionError(ValueError):
#     """Configuration file version too old."""


# # Validate the iconfig file has the minimum version.
# _version = iconfig.get("ICONFIG_VERSION")
# print(f"\n\n\niconfig version: {_version}\n\n\n")
# if _version is None or _version < ICONFIG_MINIMUM_VERSION:
#     raise IConfigFileVersionError(
#         "Configuration file version too old."
#         f" Found {_version!r}."
#         f" Expected minimum {ICONFIG_MINIMUM_VERSION!r}."
#         f" Configuration file '{DEFAULT_ICONFIG_YML_FILE}'."
#     )
