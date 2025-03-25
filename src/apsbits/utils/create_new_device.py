<<<<<<< HEAD
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

=======
from typing import Dict, Optional, Type, Any
from dataclasses import dataclass
import logging
from pathlib import Path
import yaml
import importlib
import inspect

logger = logging.getLogger(__name__)

@dataclass
class DeviceConfig:
    """Configuration data structure for device creation.
    
>>>>>>> d4841a2b133ec2f8de5bd85c87c97e12c58a69a1
    Attributes:
        name: The name of the device
        device_type: The type of device being created
        class_name: The name of the device class to use/create
        parameters: Additional parameters for the device
        location: Optional location identifier for the device
    """
<<<<<<< HEAD

=======
>>>>>>> d4841a2b133ec2f8de5bd85c87c97e12c58a69a1
    name: str
    device_type: str
    class_name: str
    parameters: Dict[str, Any]
    location: Optional[str] = None

<<<<<<< HEAD

def load_or_create_yaml(file_path: Path) -> Dict[str, Any]:
    """Load existing YAML file or create new one if it doesn't exist.

    Args:
        file_path: Path to the YAML file

=======
def load_or_create_yaml(file_path: Path) -> Dict[str, Any]:
    """Load existing YAML file or create new one if it doesn't exist.
    
    Args:
        file_path: Path to the YAML file
        
>>>>>>> d4841a2b133ec2f8de5bd85c87c97e12c58a69a1
    Returns:
        Dict containing the YAML content
    """
    if file_path.exists():
<<<<<<< HEAD
        with open(file_path, "r") as f:
            return yaml.safe_load(f) or {}
    return {"devices": {}}


def create_device_class(class_name: str, device_type: str) -> None:
    """Create a new device class file if it doesn't exist.

=======
        with open(file_path, 'r') as f:
            return yaml.safe_load(f) or {}
    return {"devices": {}}

def create_device_class(class_name: str, device_type: str) -> None:
    """Create a new device class file if it doesn't exist.
    
>>>>>>> d4841a2b133ec2f8de5bd85c87c97e12c58a69a1
    Args:
        class_name: Name of the class to create
        device_type: Type of device for documentation
    """
    devices_dir = Path("instrument/devices")
    devices_dir.mkdir(parents=True, exist_ok=True)
<<<<<<< HEAD

=======
    
>>>>>>> d4841a2b133ec2f8de5bd85c87c97e12c58a69a1
    file_path = devices_dir / f"{class_name.lower()}.py"
    if not file_path.exists():
        class_content = f'''from typing import Dict, Any

class {class_name}:
    """Device class for {device_type}.
<<<<<<< HEAD

    Attributes:
        config: Configuration dictionary for the device
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize the {device_type} device.

=======
    
    Attributes:
        config: Configuration dictionary for the device
    """
    
    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize the {device_type} device.
        
>>>>>>> d4841a2b133ec2f8de5bd85c87c97e12c58a69a1
        Args:
            config: Configuration dictionary for the device
        """
        self.config = config
<<<<<<< HEAD

    def initialize(self) -> None:
        """Initialize the device hardware."""
        pass

=======
        
    def initialize(self) -> None:
        """Initialize the device hardware."""
        pass
        
>>>>>>> d4841a2b133ec2f8de5bd85c87c97e12c58a69a1
    def close(self) -> None:
        """Close the device connection."""
        pass
'''
<<<<<<< HEAD
        with open(file_path, "w") as f:
            f.write(class_content)

=======
        with open(file_path, 'w') as f:
            f.write(class_content)
        
>>>>>>> d4841a2b133ec2f8de5bd85c87c97e12c58a69a1
        # Create __init__.py if it doesn't exist
        init_file = devices_dir / "__init__.py"
        if not init_file.exists():
            init_file.touch()

<<<<<<< HEAD

def get_device_class(class_name: str) -> Type[Any]:
    """Get the device class by name, importing it from the devices directory.

    Args:
        class_name: Name of the class to import

    Returns:
        The device class

=======
def get_device_class(class_name: str) -> Type[Any]:
    """Get the device class by name, importing it from the devices directory.
    
    Args:
        class_name: Name of the class to import
        
    Returns:
        The device class
        
>>>>>>> d4841a2b133ec2f8de5bd85c87c97e12c58a69a1
    Raises:
        ImportError: If the class cannot be imported
    """
    try:
        module = importlib.import_module(f"instrument.devices.{class_name.lower()}")
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        raise ImportError(f"Could not import device class {class_name}: {str(e)}")

<<<<<<< HEAD

def create_new_device(
    config: DeviceConfig, config_file: Optional[Path] = None
) -> Dict[str, Any]:
    """Create a new device with the specified configuration.

    Args:
        config: DeviceConfig object containing device specifications
        config_file: Optional path to the devices configuration file

    Returns:
        Dict containing the created device information

=======
def create_new_device(
    config: DeviceConfig,
    config_file: Optional[Path] = None
) -> Dict[str, Any]:
    """Create a new device with the specified configuration.
    
    Args:
        config: DeviceConfig object containing device specifications
        config_file: Optional path to the devices configuration file
        
    Returns:
        Dict containing the created device information
        
>>>>>>> d4841a2b133ec2f8de5bd85c87c97e12c58a69a1
    Raises:
        ValueError: If the device name is empty or invalid
        ImportError: If the device class cannot be loaded
    """
    if not config.name or not config.name.strip():
        raise ValueError("Device name cannot be empty")
<<<<<<< HEAD

    logger.info(f"Creating new device: {config.name} of type {config.device_type}")

=======
    
    logger.info(f"Creating new device: {config.name} of type {config.device_type}")
    
>>>>>>> d4841a2b133ec2f8de5bd85c87c97e12c58a69a1
    # Create or load device class
    try:
        device_class = get_device_class(config.class_name)
    except ImportError:
        logger.info(f"Creating new device class: {config.class_name}")
        create_device_class(config.class_name, config.device_type)
        device_class = get_device_class(config.class_name)
<<<<<<< HEAD

    # Create device instance to validate configuration
    device = device_class(config.parameters)

=======
    
    # Create device instance to validate configuration
    device = device_class(config.parameters)
    
>>>>>>> d4841a2b133ec2f8de5bd85c87c97e12c58a69a1
    device_info = {
        "name": config.name,
        "type": config.device_type,
        "class": config.class_name,
        "location": config.location or "unknown",
        "parameters": config.parameters,
<<<<<<< HEAD
        "status": "initialized",
    }

=======
        "status": "initialized"
    }
    
>>>>>>> d4841a2b133ec2f8de5bd85c87c97e12c58a69a1
    # Update YAML configuration if provided
    if config_file:
        config_file = Path(config_file)
        yaml_data = load_or_create_yaml(config_file)
        yaml_data["devices"][config.name] = device_info
<<<<<<< HEAD

        config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(config_file, "w") as f:
            yaml.safe_dump(yaml_data, f, default_flow_style=False)

        logger.info(f"Updated device configuration in {config_file}")

    logger.debug(f"Device created successfully: {device_info}")
    return device_info


def main() -> None:
    """Entry point for the device creation script."""
    logging.basicConfig(level=logging.INFO)

=======
        
        config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(config_file, 'w') as f:
            yaml.safe_dump(yaml_data, f, default_flow_style=False)
        
        logger.info(f"Updated device configuration in {config_file}")
    
    logger.debug(f"Device created successfully: {device_info}")
    return device_info

def main() -> None:
    """Entry point for the device creation script."""
    logging.basicConfig(level=logging.INFO)
    
>>>>>>> d4841a2b133ec2f8de5bd85c87c97e12c58a69a1
    try:
        # Example usage
        config = DeviceConfig(
            name="test_sensor_1",
            device_type="temperature_sensor",
            class_name="TemperatureSensor",
<<<<<<< HEAD
            parameters={"port": "/dev/ttyUSB0", "baud_rate": 9600},
            location="lab_room_1",
        )

=======
            parameters={
                "port": "/dev/ttyUSB0",
                "baud_rate": 9600
            },
            location="lab_room_1"
        )
        
>>>>>>> d4841a2b133ec2f8de5bd85c87c97e12c58a69a1
        config_file = Path("instrument/configs/devices.yml")
        result = create_new_device(config, config_file)
        print(f"Device created successfully: {result}")
    except Exception as e:
        logger.error(f"Failed to create device: {str(e)}")
        raise

<<<<<<< HEAD

if __name__ == "__main__":
    main()
=======
if __name__ == "__main__":
    main() 
>>>>>>> d4841a2b133ec2f8de5bd85c87c97e12c58a69a1
