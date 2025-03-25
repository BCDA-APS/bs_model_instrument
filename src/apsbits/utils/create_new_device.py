"""Device creation and management utilities.

This module provides functionality for creating and managing device configurations,
including:
- Device configuration data structures
- YAML configuration file handling
- Device class generation
- Device instance management
"""

import importlib
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Optional
from typing import Type

import yaml

logger = logging.getLogger(__name__)


@dataclass
class DeviceConfig:
    """Configuration data structure for device creation.

    Attributes:
        name: The name of the device
        device_type: The type of device being created
        class_name: The name of the device class to use/create
        parameters: Additional parameters for the device
        location: Optional location identifier for the device
    """

    name: str
    device_type: str
    class_name: str
    parameters: Dict[str, Any]
    location: Optional[str] = None


def load_or_create_yaml(file_path: Path) -> Dict[str, Any]:
    """Load existing YAML file or create new one if it doesn't exist.

    Args:
        file_path: Path to the YAML file

    Returns:
        Dict containing the YAML content
    """
    if file_path.exists():
        with open(file_path, "r") as f:
            return yaml.safe_load(f) or {}
    return {"devices": {}}


def create_device_class(class_name: str, device_type: str) -> None:
    """Create a new device class file if it doesn't exist.

    Args:
        class_name: Name of the class to create
        device_type: Type of device for documentation
    """
    devices_dir = Path("instrument/devices")
    devices_dir.mkdir(parents=True, exist_ok=True)

    file_path = devices_dir / f"{class_name.lower()}.py"
    if not file_path.exists():
        class_content = f'''from typing import Dict, Any

class {class_name}:
    """Device class for {device_type}.

    Attributes:
        config: Configuration dictionary for the device
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize the {device_type} device.

        Args:
            config: Configuration dictionary for the device
        """
        self.config = config

    def initialize(self) -> None:
        """Initialize the device hardware."""
        pass

    def close(self) -> None:
        """Close the device connection."""
        pass
'''
        with open(file_path, "w") as f:
            f.write(class_content)

        # Create __init__.py if it doesn't exist
        init_file = devices_dir / "__init__.py"
        if not init_file.exists():
            init_file.touch()


def get_device_class(class_name: str) -> Type[Any]:
    """Get the device class by name, importing it from the devices directory.

    Args:
        class_name: Name of the class to import

    Returns:
        The device class

    Raises:
        ImportError: If the class cannot be imported
    """
    try:
        module = importlib.import_module(f"instrument.devices.{class_name.lower()}")
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        raise ImportError(f"Could not import device class {class_name}") from e


def create_new_device(
    config: DeviceConfig,
    config_file: Optional[Path] = None,
) -> Dict[str, Any]:
    """Create a new device with the specified configuration.

    Args:
        config: Configuration for the new device
        config_file: Optional path to configuration file

    Returns:
        Dict containing the device configuration

    Raises:
        ValueError: If device name is empty or invalid
        ImportError: If device class cannot be loaded
    """
    logger.info(f"Creating new device: {config.name}")

    if not config.name:
        raise ValueError("Device name cannot be empty")

    device_data = {
        "name": config.name,
        "type": config.device_type,
        "class": config.class_name,
        "parameters": config.parameters,
    }

    if config.location:
        device_data["location"] = config.location

    if config_file:
        yaml_data = load_or_create_yaml(config_file)
        if config.name in yaml_data.get("devices", {}):
            raise ValueError(f"Device with name {config.name} already exists")
        yaml_data.setdefault("devices", {})[config.name] = device_data
        with open(config_file, "w") as f:
            yaml.dump(yaml_data, f)

    logger.info("Device created successfully")
    return device_data


def validate_device_class(class_name: str) -> None:
    """Validate that a device class name is valid.

    Args:
        class_name: Name of the class to validate

    Raises:
        ValueError: If class name is invalid
    """
    if not class_name.isidentifier():
        raise ValueError("Invalid class name")
    if not class_name[0].isupper():
        raise ValueError("Class name must start with uppercase letter")


def get_device_instance(class_name: str, config: Dict[str, Any]) -> Any:
    """Get an instance of a device class with the given configuration.

    Args:
        class_name: Name of the class to instantiate
        config: Configuration dictionary for the device

    Returns:
        Instance of the device class

    Raises:
        ImportError: If device class cannot be loaded
        TypeError: If device class constructor is invalid
    """
    device_class = get_device_class(class_name)
    try:
        return device_class(config)
    except TypeError as e:
        raise TypeError(f"Failed to instantiate device class {class_name}") from e


def validate_device_config(config: DeviceConfig) -> None:
    """Validate a device configuration.

    Args:
        config: Device configuration to validate

    Raises:
        ValueError: If configuration is invalid
    """
    if not config.name:
        raise ValueError("Device name cannot be empty")
    if not config.device_type:
        raise ValueError("Device type cannot be empty")
    validate_device_class(config.class_name)


def update_device_config(
    device_name: str,
    updates: Dict[str, Any],
    config_file: Path,
) -> Dict[str, Any]:
    """Update an existing device configuration.

    Args:
        device_name: Name of the device to update
        updates: Dictionary of updates to apply
        config_file: Path to configuration file

    Returns:
        Updated device configuration

    Raises:
        ValueError: If device does not exist
    """
    yaml_data = load_or_create_yaml(config_file)
    if device_name not in yaml_data.get("devices", {}):
        raise ValueError(f"Device {device_name} does not exist")

    device_data = yaml_data["devices"][device_name]
    device_data.update(updates)

    with open(config_file, "w") as f:
        yaml.dump(yaml_data, f)

    return device_data


def delete_device(device_name: str, config_file: Path) -> None:
    """Delete a device from the configuration.

    Args:
        device_name: Name of the device to delete
        config_file: Path to configuration file

    Raises:
        ValueError: If device does not exist
    """
    yaml_data = load_or_create_yaml(config_file)
    if device_name not in yaml_data.get("devices", {}):
        raise ValueError(f"Device {device_name} does not exist")

    del yaml_data["devices"][device_name]

    with open(config_file, "w") as f:
        yaml.dump(yaml_data, f)


def list_devices(config_file: Path) -> Dict[str, Dict[str, Any]]:
    """List all devices in the configuration.

    Args:
        config_file: Path to configuration file

    Returns:
        Dictionary of device configurations
    """
    yaml_data = load_or_create_yaml(config_file)
    return yaml_data.get("devices", {})


def main() -> None:
    """Entry point for the device creation script."""
    logging.basicConfig(level=logging.INFO)

    try:
        # Example usage
        config = DeviceConfig(
            name="test_sensor_1",
            device_type="temperature_sensor",
            class_name="TemperatureSensor",
            parameters={"port": "/dev/ttyUSB0", "baud_rate": 9600},
            location="lab_room_1",
        )

        config_file = Path("instrument/configs/devices.yml")
        result = create_new_device(config, config_file)
        print(f"Device created successfully: {result}")
    except Exception as e:
        logger.error(f"Failed to create device: {str(e)}")
        raise


if __name__ == "__main__":
    main()
