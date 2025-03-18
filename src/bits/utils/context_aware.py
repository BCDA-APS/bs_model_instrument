"""
Smart configuration system that detects which instrument's startup.py initiated the import.
Updated for the actual directory structure.
"""

import inspect
import logging
import os
import sys
import yaml
from functools import lru_cache
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class ContextConfig:
    """Configuration provider that's aware of which instrument is being used."""

    def __init__(self):
        self._cache = {}  # Cache configs by instrument
        self._active_instrument = None
        self._detect_active_instrument()

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value for the active instrument."""
        config = self._get_instrument_config()
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
        """Make object safely representable as a string."""
        instrument = "unknown"
        if self._active_instrument:
            instrument = os.path.basename(self._active_instrument)
        return f"<ContextConfig: {instrument}>"

    def to_dict(self):
        """Convert config to a regular dictionary for serialization."""
        return dict(self._get_instrument_config())

    def _detect_active_instrument(self):
        """Determine which instrument's startup.py initiated this process."""
        # Look at the main script that was run
        main_module = self._get_main_module()
        if main_module and hasattr(main_module, "__file__"):
            main_path = os.path.abspath(main_module.__file__)

            # Check if this is a startup.py file
            if os.path.basename(main_path) == "startup.py":
                instrument_dir = os.path.dirname(main_path)
                instrument_name = os.path.basename(instrument_dir)

                logger.debug(
                    f"Detected potential instrument from startup.py: {instrument_name}"
                )
                if self._is_instrument_dir(instrument_dir):
                    self._active_instrument = instrument_dir
                    return

        # Fallback: look at the call stack for instrument imports
        self._active_instrument = self._find_instrument_in_stack()

        # If we still don't have an instrument, try the current working directory
        if not self._active_instrument:
            cwd = os.getcwd()
            if self._is_instrument_dir(cwd):
                logger.debug(f"Using current directory as instrument: {cwd}")
                self._active_instrument = cwd

    def _is_instrument_dir(self, directory):
        """Check if a directory is an instrument directory."""
        # Check for presence of configs/iconfig.yml
        config_path = os.path.join(directory, "configs", "iconfig.yml")
        return os.path.exists(config_path)

    def _get_main_module(self):
        """Get the main module that was executed."""
        return sys.modules.get("__main__")

    def _find_instrument_in_stack(self):
        """Search the call stack for references to instrument modules."""
        stack = inspect.stack()
        project_root = self._find_project_root(os.getcwd())

        if not project_root:
            return None

        src_dir = os.path.join(project_root, "src")

        for frame_info in stack:
            module = inspect.getmodule(frame_info.frame)
            if module and hasattr(module, "__file__") and hasattr(module, "__name__"):
                module_path = os.path.abspath(module.__file__)

                # Check if this module is in an instrument directory
                if src_dir in module_path:
                    # Extract the part after src/
                    relative_path = os.path.relpath(module_path, src_dir)
                    parts = relative_path.split(os.sep)

                    if len(parts) >= 1:
                        potential_instrument = parts[0]
                        instrument_dir = os.path.join(src_dir, potential_instrument)

                        if self._is_instrument_dir(instrument_dir):
                            logger.debug(
                                f"Found instrument in stack: {potential_instrument}"
                            )
                            return instrument_dir

        return None

    def _get_instrument_config(self) -> Dict:
        """Get configuration for the active instrument."""
        if not self._active_instrument:
            self._detect_active_instrument()

        # Return cached config if available
        if self._active_instrument in self._cache:
            return self._cache[self._active_instrument]

        # Load config for the active instrument
        config = self._load_config_for_instrument(self._active_instrument)
        self._cache[self._active_instrument] = config
        return config

    def _load_config_for_instrument(self, instrument_path: str) -> Dict:
        """Load configuration file for the given instrument."""
        if not instrument_path:
            logger.warning("No instrument detected, using empty config")
            return {}

        # Try common config locations within the instrument directory
        config_paths = [
            os.path.join(instrument_path, "configs", "iconfig.yml"),
            os.path.join(instrument_path, "configs", "config.yml"),
            os.path.join(instrument_path, "configs", "iconfig.yaml"),
            os.path.join(instrument_path, "configs", "config.yaml"),
            os.path.join(instrument_path, "iconfig.yml"),
            os.path.join(instrument_path, "config.yml"),
        ]

        # Try each path
        for path in config_paths:
            if os.path.exists(path):
                logger.debug(f"Loading instrument config from: {path}")
                try:
                    with open(path) as f:
                        return yaml.safe_load(f) or {}
                except Exception as e:
                    logger.warning(f"Error loading config from {path}: {e}")

        # No config found for this instrument
        logger.warning(f"No config found for instrument at {instrument_path}")
        return {}

    def set_instrument(self, instrument_name: str) -> None:
        """Manually set which instrument configuration to use."""
        # Find the instrument path
        project_root = self._find_project_root(os.getcwd())
        if not project_root:
            logger.warning(
                f"Cannot set instrument {instrument_name}: project root not found"
            )
            return

        src_dir = os.path.join(project_root, "src")
        instrument_path = os.path.join(src_dir, instrument_name)

        if not os.path.exists(instrument_path):
            logger.warning(f"Instrument directory not found: {instrument_path}")
            return

        # Set active instrument and clear cache
        self._active_instrument = instrument_path
        if instrument_path in self._cache:
            del self._cache[instrument_path]

    def _find_project_root(self, start_path: str) -> Optional[str]:
        """Find the project root directory from a starting path."""
        current = start_path

        # Project root indicators
        indicators = ["pyproject.toml", "setup.py", ".git"]

        # Walk up directory tree
        while True:
            for indicator in indicators:
                if os.path.exists(os.path.join(current, indicator)):
                    return current

            parent = os.path.dirname(current)
            if parent == current:  # Reached root
                return None

            current = parent


# Create a function to get config that will be safe to use in metadata
def get_iconfig():
    """Get the config instance in a way that's safe for JSON serialization.
    Use this instead of directly importing iconfig if you're storing in metadata.
    """
    # Returns a regular dict that can be serialized
    return _iconfig.to_dict()


# Internal instance that shouldn't be directly exposed if serialization is needed
_iconfig = ContextConfig()

# For normal usage that doesn't involve JSON serialization
iconfig = _iconfig


# For debugging purposes
def which_instrument():
    """Return the name of the active instrument."""
    if _iconfig._active_instrument:
        return os.path.basename(_iconfig._active_instrument)
    return "No instrument detected"
