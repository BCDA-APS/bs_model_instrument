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
        with open(file_path, 'r') as f:
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
        with open(file_path, 'w') as f:
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
        raise ImportError(f"Could not import device class {class_name}: {str(e)}")

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
        
    Raises:
        ValueError: If the device name is empty or invalid
        ImportError: If the device class cannot be loaded
    """
    if not config.name or not config.name.strip():
        raise ValueError("Device name cannot be empty")
    
    logger.info(f"Creating new device: {config.name} of type {config.device_type}")
    
    # Create or load device class
    try:
        device_class = get_device_class(config.class_name)
    except ImportError:
        logger.info(f"Creating new device class: {config.class_name}")
        create_device_class(config.class_name, config.device_type)
        device_class = get_device_class(config.class_name)
    
    # Create device instance to validate configuration
    device = device_class(config.parameters)
    
    device_info = {
        "name": config.name,
        "type": config.device_type,
        "class": config.class_name,
        "location": config.location or "unknown",
        "parameters": config.parameters,
        "status": "initialized"
    }
    
    # Update YAML configuration if provided
    if config_file:
        config_file = Path(config_file)
        yaml_data = load_or_create_yaml(config_file)
        yaml_data["devices"][config.name] = device_info
        
        config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(config_file, 'w') as f:
            yaml.safe_dump(yaml_data, f, default_flow_style=False)
        
        logger.info(f"Updated device configuration in {config_file}")
    
    logger.debug(f"Device created successfully: {device_info}")
    return device_info

def main() -> None:
    """Entry point for the device creation script."""
    logging.basicConfig(level=logging.INFO)
    
    try:
        # Example usage
        config = DeviceConfig(
            name="test_sensor_1",
            device_type="temperature_sensor",
            class_name="TemperatureSensor",
            parameters={
                "port": "/dev/ttyUSB0",
                "baud_rate": 9600
            },
            location="lab_room_1"
        )
        
        config_file = Path("instrument/configs/devices.yml")
        result = create_new_device(config, config_file)
        print(f"Device created successfully: {result}")
    except Exception as e:
        logger.error(f"Failed to create device: {str(e)}")
        raise

if __name__ == "__main__":
    main() 