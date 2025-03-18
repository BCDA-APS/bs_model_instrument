"""
Super simple configuration system that always looks in the 'configs' subdirectory
of wherever startup.py is located.
"""

import inspect
import logging
import os
import pathlib
import sys
import yaml
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class StartupConfig:
    """Configuration provider that always uses the configs subdirectory of startup.py location."""

    def __init__(self):
        self._config = None
        self._startup_dir = None
        self._config_path = None

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        config = self._get_config()
        return config.get(key, default)

    def __getitem__(self, key):
        """Dictionary-style access to configuration."""
        value = self.get(key)
        if value is None:
            raise KeyError(key)
        return value

    def __contains__(self, key):
        """Support for 'in' operator."""
        return self.get(key) is not None

    def __repr__(self):
        """String representation."""
        startup_dir = self._get_startup_dir()
        if startup_dir:
            return f"<StartupConfig: {os.path.basename(startup_dir)}>"
        return "<StartupConfig: not initialized>"

    def to_dict(self):
        """Convert config to a regular dictionary for serialization."""
        return dict(self._get_config())

    @property
    def startup_dir(self) -> Optional[str]:
        """Return the directory containing startup.py."""
        return self._get_startup_dir()

    @property
    def configs_path(self) -> Optional[pathlib.Path]:
        """Return the path to the configs directory."""
        startup_dir = self._get_startup_dir()
        if not startup_dir:
            return None

        # Always use the configs subdirectory
        configs_dir = os.path.join(startup_dir, "configs")
        return pathlib.Path(configs_dir)

    def resolve_path(self, filename: str) -> Optional[pathlib.Path]:
        """Resolve a filename relative to the configs directory."""
        if not self.configs_path:
            return None
        return self.configs_path / filename

    def _get_startup_dir(self) -> Optional[str]:
        """Get the directory containing the startup.py that initiated this process."""
        if self._startup_dir:
            return self._startup_dir

        # First check the main module
        main_module = sys.modules.get("__main__")
        if main_module and hasattr(main_module, "__file__"):
            main_file = os.path.abspath(main_module.__file__)
            if os.path.basename(main_file) == "startup.py":
                self._startup_dir = os.path.dirname(main_file)
                logger.debug(f"Found startup.py in main module: {self._startup_dir}")
                return self._startup_dir

        # Then look through the call stack for a startup.py
        stack = inspect.stack()
        for frame_info in stack:
            module = inspect.getmodule(frame_info.frame)
            if module and hasattr(module, "__file__"):
                module_file = os.path.abspath(module.__file__)
                if os.path.basename(module_file) == "startup.py":
                    self._startup_dir = os.path.dirname(module_file)
                    logger.debug(f"Found startup.py in call stack: {self._startup_dir}")
                    return self._startup_dir

                # Check if the module was imported from a startup.py
                module_dir = os.path.dirname(module_file)
                startup_path = os.path.join(module_dir, "startup.py")
                if os.path.exists(startup_path):
                    self._startup_dir = module_dir
                    logger.debug(
                        f"Found directory with startup.py: {self._startup_dir}"
                    )
                    return self._startup_dir

        # If we get here, we couldn't find a startup.py
        logger.warning("Could not find startup.py in call stack or main module")
        return None

    def _get_config(self) -> Dict:
        """Load the configuration file."""
        if self._config is not None:
            return self._config

        # Find the startup directory
        startup_dir = self._get_startup_dir()
        if not startup_dir:
            logger.warning("No startup.py found, using empty config")
            self._config = {}
            return self._config

        # Always look in the configs subdirectory
        configs_dir = os.path.join(startup_dir, "configs")
        if not os.path.isdir(configs_dir):
            logger.warning(f"No configs directory found at {configs_dir}")
            self._config = {}
            return self._config

        # Try various config file names in the configs directory
        config_files = ["iconfig.yml", "config.yml", "iconfig.yaml", "config.yaml"]

        # Try each filename
        for filename in config_files:
            path = os.path.join(configs_dir, filename)
            if os.path.exists(path):
                try:
                    with open(path) as f:
                        self._config = yaml.safe_load(f) or {}
                    self._config_path = path
                    logger.debug(f"Loaded config from {path}")
                    return self._config
                except Exception as e:
                    logger.warning(f"Error loading config from {path}: {e}")

        # If we get here, no config file was found
        logger.warning(f"No config file found in {configs_dir}")
        self._config = {}
        return self._config


# Create a function to get config that will be safe to use in metadata
def get_iconfig():
    """Get the config instance in a way that's safe for JSON serialization."""
    return _iconfig.to_dict()


# Function to get the path to the configs directory
def get_configs_path() -> Optional[pathlib.Path]:
    """Get the path to the configs directory."""
    return _iconfig.configs_path


# Function to resolve a file path relative to the configs directory
def resolve_path(filename: str) -> pathlib.Path:
    """Resolve a filename relative to the configs directory."""
    path = _iconfig.resolve_path(filename)
    if not path:
        raise ValueError(
            f"Could not resolve path for {filename}, no startup.py detected"
        )
    return path


# Internal instance that shouldn't be directly exposed if serialization is needed
_iconfig = StartupConfig()

# For normal usage that doesn't involve JSON serialization
iconfig = _iconfig


# For debugging purposes
def which_startup():
    """Return the directory containing startup.py."""
    if _iconfig.startup_dir:
        return os.path.basename(_iconfig.startup_dir)
    return "No startup.py detected"
