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

import yaml

logger = logging.getLogger(__name__)
logger.bsdev(__file__)
instrument_path = pathlib.Path(__file__).parent.parent
DEFAULT_ICONFIG_YML_FILE = (
    instrument_path / "demo_instrument" / "configs" / "iconfig.yml"
)
ICONFIG_MINIMUM_VERSION = "2.0.0"


def load_config_yaml(iconfig_yml=None) -> dict:
    """
    Load iconfig.yml (and other YAML) configuration files.

    Parameters
    ----------
    iconfig_yml: str
        Name of the YAML file to be loaded.  The name can be
        absolute or relative to the current working directory.
        Default: ``INSTRUMENT/demo_instrument/configs/iconfig.yml``
    """

    if iconfig_yml is None:
        path = DEFAULT_ICONFIG_YML_FILE
    else:
        path = pathlib.Path(iconfig_yml)
    if not path.exists():
        raise FileExistsError(f"Configuration file '{path}' does not exist.")
    config = yaml.load(open(path, "r").read(), yaml.Loader)
    return config


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
