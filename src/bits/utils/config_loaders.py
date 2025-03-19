"""
Load configuration files
========================

Load supported configuration files, such as ``iconfig.yml``.

.. autosummary::
    ~load_config_yaml
    ~IConfigFileVersionError
"""

import gc
import inspect
import logging
import pathlib
from typing import Any

import yaml


from bits.utils.context_aware import iconfig

logger = logging.getLogger(__name__)
logger.bsdev(__file__)
ICONFIG_MINIMUM_VERSION = "2.0.0"


# def load_i_config_yaml(iconfig_yml=None) -> dict:
#     """
#     Load iconfig.yml (and other YAML) configuration files.

#     Parameters
#     ----------
#     iconfig_yml: str
#         Name of the YAML file to be loaded.  The name can be
#         absolute or relative to the current working directory.
#         Default: ``INSTRUMENT/demo_instrument/configs/iconfig.yml``
#     """

#     if iconfig_yml is None:
#         raise ValueError(
#             "No configuration file provided. Please specify a valid 'iconfig.yml' file."
#         )

#     path = pathlib.Path(iconfig_yml)
#     if not path.exists():
#         raise FileExistsError(f"Configuration file '{path}' does not exist.")

#     iconfig = yaml.load(open(path, "r").read(), yaml.Loader)

#     ## appends local execution variables at runtime.
#     iconfig["ICONFIG_PATH"] = str(path)
#     iconfig["INSTRUMENT_PATH"] = str(path.parent)
#     iconfig["INSTRUMENT_FOLDER"] = str(path.parent.name)
#     return iconfig

def load_config_yaml(config_yml=None) -> dict:
    """
    Load iconfig.yml (and other YAML) configuration files.

    Parameters
    ----------
    iconfig_yml: str
        Name of the YAML file to be loaded.  The name can be
        absolute or relative to the current working directory.
    """

    path = pathlib.Path(config_yml)

    if not path.exists():
        raise FileExistsError(f"Configuration file '{path}' does not exist.")
    config = yaml.load(open(path, "r").read(), yaml.Loader)

    return config


class IConfigFileVersionError(ValueError):
    """Configuration file version too old."""


def check_iconfig_version(config: dict, config_file: str) -> None:
    """
    Validate the iconfig file has the minimum version.

    Parameters
    ----------
    iconfig : dict
        The loaded configuration dictionary.
    config_file : str
        The path to the configuration file being validated.

    Raises
    ------
    IConfigFileVersionError
        If the configuration file version is too old or missing.
    """
    _version = config.get("ICONFIG_VERSION")
    if _version is None or _version < ICONFIG_MINIMUM_VERSION:
        raise IConfigFileVersionError(
            "Configuration file version too old."
            f" Found {_version!r}."
            f" Expected minimum {ICONFIG_MINIMUM_VERSION!r}."
            f" Configuration file '{config_file}'."
        )

