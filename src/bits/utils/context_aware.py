"""
Minimalist configuration system following the 'configs convention'.

Core principle: Configuration always lives in the 'configs' subdirectory
of wherever startup.py is located.
"""

import inspect
import pathlib
from functools import lru_cache
from typing import Any
from typing import Dict
from typing import Optional

import yaml


class ConfigError(Exception):
    """Base exception for configuration errors."""

    pass


class StartupConfig:
    """Configuration provider following the configs-subdirectory convention."""

    CONFIG_FILENAMES = [
        "iconfig.yml",
        "config.yml",
        "iconfig.yaml",
        "config.yaml",
        "config.toml",
        "ifconfig.toml",
    ]

    def __init__(self):
        """Initialize the configuration."""
        self._config = None

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value with an optional default."""
        return self.config.get(key, default)

    def __getitem__(self, key: str) -> Any:
        """Dictionary-style access to configuration."""
        try:
            return self.config[key]
        except KeyError:
            raise KeyError(f"Missing required config key: '{key}'") from None

    def __contains__(self, key: str) -> bool:
        """Support for 'in' operator."""
        return key in self.config

    def __repr__(self) -> str:
        """Create a helpful string representation."""
        startup_name = self.startup_path.parent.name if self.startup_path else "unknown"
        config_file = self.config_file.name if self.config_file else "none"
        return f"<Config: {startup_name}/configs/{config_file}>"

    @property
    def config(self) -> Dict:
        """Get the configuration dictionary, loading it if necessary."""
        if self._config is None:
            self._config = self._load_config()
        return self._config

    def to_dict(self) -> Dict:
        """Convert config to a regular dictionary for serialization."""
        return dict(self.config)

    @property
    @lru_cache(maxsize=1)  # noqa B019
    def startup_path(self) -> Optional[pathlib.Path]:
        """Find the startup.py that's being executed."""
        # First check main module
        startup = self._find_startup_in_main()
        if startup:
            return startup

        # Then check call stack
        return self._find_startup_in_stack()

    @property
    def configs_dir(self) -> Optional[pathlib.Path]:
        """Get the configs directory path."""
        if not self.startup_path:
            return None
        return self.startup_path.parent / "configs"

    @property
    @lru_cache(maxsize=1)  # noqa B019
    def config_file(self) -> Optional[pathlib.Path]:
        """Find the active config file."""
        if not self.configs_dir or not self.configs_dir.exists():
            return None

        # Try each filename in order
        for filename in self.CONFIG_FILENAMES:
            path = self.configs_dir / filename
            if path.exists():
                return path

        return None

    def resolve_path(self, filename: str) -> Optional[pathlib.Path]:
        """Resolve a filename relative to the configs directory."""
        if not self.configs_dir:
            return None
        return self.configs_dir / filename

    def _find_startup_in_main(self) -> Optional[pathlib.Path]:
        """Check if the main module is startup.py."""
        import sys

        main_module = sys.modules.get("__main__")
        if main_module and hasattr(main_module, "__file__"):
            path = pathlib.Path(main_module.__file__).resolve()
            if path.name == "startup.py":
                return path
        return None

    def _find_startup_in_stack(self) -> Optional[pathlib.Path]:
        """Search the call stack for a startup.py file."""
        for frame_info in inspect.stack():
            module = inspect.getmodule(frame_info.frame)
            if not module or not hasattr(module, "__file__"):
                continue

            path = pathlib.Path(module.__file__).resolve()

            # Direct match if this is startup.py
            if path.name == "startup.py":
                return path

            # Check if there's a startup.py in the same directory
            startup_path = path.parent / "startup.py"
            if startup_path.exists():
                return startup_path

        return None

    def _load_config(self) -> Dict:
        """Load the configuration file."""
        if not self.config_file:
            return {}

        try:
            with open(self.config_file) as f:
                return yaml.safe_load(f) or {}
        except Exception:
            return {}


# Create a single instance
_config = StartupConfig()

# Public API - Simple and clean


def get(key: str, default: Any = None) -> Any:
    """Get a configuration value with an optional default."""
    return _config.get(key, default)


def get_dict() -> Dict:
    """Get the entire configuration as a dictionary (for serialization)."""
    return _config.to_dict()


def resolve_path(filename: str) -> pathlib.Path:
    """Resolve a filename relative to the configs directory."""
    path = _config.resolve_path(filename)
    if not path:
        raise ConfigError(f"Cannot resolve '{filename}': No startup.py found")
    return path


def get_configs_dir() -> pathlib.Path:
    """Get the path to the configs directory."""
    if not _config.configs_dir:
        raise ConfigError("No configs directory found (No startup.py detected)")
    return _config.configs_dir


# For backward compatibility
iconfig = _config
