"""
Custom folder to store all beamline specific implementations
"""

from apsbits.utils.context_aware import StartupConfig
from pathlib import Path

# Get the instrument path and config path for reference
instrument_path = Path(__file__).parent
iconfig_path = instrument_path / "configs" / "iconfig.yml"

# Initialize the configuration with explicit path
startup_config = StartupConfig(config_path=iconfig_path)

# Access configuration values using the startup_config instance
# Example: startup_config.get('some_key', default_value)
# Or: startup_config['required_key']

print("Starting Instrument with iconfig:", iconfig_path)


