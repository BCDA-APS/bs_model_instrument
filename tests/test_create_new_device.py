from pathlib import Path
from typing import TYPE_CHECKING

import pytest
import yaml

from src.create_new_device import DeviceConfig
from src.create_new_device import create_device_class
from src.create_new_device import create_new_device
from src.create_new_device import get_device_class

if TYPE_CHECKING:
    from _pytest.logging import LogCaptureFixture
    from _pytest.monkeypatch import MonkeyPatch


@pytest.fixture
def temp_config_file(tmp_path: Path) -> Path:
    """Create a temporary config file for testing.

    Args:
        tmp_path: Pytest fixture providing temporary directory

    Returns:
        Path to temporary config file
    """
    return tmp_path / "devices.yml"


@pytest.fixture
def temp_devices_dir(tmp_path: Path, monkeypatch: "MonkeyPatch") -> Path:
    """Create a temporary devices directory for testing.

    Args:
        tmp_path: Pytest fixture providing temporary directory
        monkeypatch: Pytest fixture for modifying Python objects

    Returns:
        Path to temporary devices directory
    """
    devices_dir = tmp_path / "instrument" / "devices"
    devices_dir.mkdir(parents=True)
    monkeypatch.setattr(
        "src.create_new_device.Path",
        lambda x: devices_dir if x == "instrument/devices" else Path(x),
    )
    return devices_dir


def test_create_new_device_with_config_file(temp_config_file: Path) -> None:
    """Test device creation with configuration file.

    Args:
        temp_config_file: Path to temporary config file
    """
    config = DeviceConfig(
        name="test_device",
        device_type="sensor",
        class_name="TestSensor",
        parameters={"port": "COM1"},
        location="room_1",
    )

    result = create_new_device(config, temp_config_file)

    assert result["name"] == "test_device"
    assert result["type"] == "sensor"
    assert result["class"] == "TestSensor"

    # Verify YAML file was created and contains the device
    with open(temp_config_file, "r") as f:
        yaml_data = yaml.safe_load(f)

    assert "devices" in yaml_data
    assert "test_device" in yaml_data["devices"]
    assert yaml_data["devices"]["test_device"] == result


def test_create_device_class(temp_devices_dir: Path) -> None:
    """Test creation of new device class file.

    Args:
        temp_devices_dir: Path to temporary devices directory
    """
    create_device_class("TestDevice", "test_type")

    # Verify class file was created
    class_file = temp_devices_dir / "testdevice.py"
    assert class_file.exists()
    assert (temp_devices_dir / "__init__.py").exists()

    # Verify file content
    content = class_file.read_text()
    assert "class TestDevice:" in content
    assert "def __init__" in content
    assert "def initialize" in content
    assert "def close" in content


def test_create_new_device_empty_name() -> None:
    """Test device creation with empty name raises ValueError."""
    config = DeviceConfig(
        name="", device_type="sensor", class_name="TestSensor", parameters={}
    )

    with pytest.raises(ValueError, match="Device name cannot be empty"):
        create_new_device(config)


def test_create_new_device_logging(caplog: "LogCaptureFixture") -> None:
    """Test that proper logging occurs during device creation.

    Args:
        caplog: Pytest fixture for capturing log messages
    """
    config = DeviceConfig(
        name="test_device", device_type="sensor", class_name="TestSensor", parameters={}
    )

    create_new_device(config)

    assert "Creating new device: test_device" in caplog.text


def test_get_device_class_existing(temp_devices_dir: Path) -> None:
    """Test getting an existing device class.

    Args:
        temp_devices_dir: Path to temporary devices directory
    """
    # Create a test device class
    create_device_class("TestDevice", "test_type")

    # Get the class
    device_class = get_device_class("TestDevice")
    assert device_class.__name__ == "TestDevice"


def test_get_device_class_nonexistent() -> None:
    """Test getting a nonexistent device class raises ImportError."""
    with pytest.raises(ImportError):
        get_device_class("NonexistentDevice")


def test_create_new_device_with_existing_class(
    temp_devices_dir: Path, temp_config_file: Path
) -> None:
    """Test creating a device with an existing class.

    Args:
        temp_devices_dir: Path to temporary devices directory
        temp_config_file: Path to temporary config file
    """
    # Create a test device class first
    create_device_class("TestDevice", "test_type")

    # Create a device using the existing class
    config = DeviceConfig(
        name="test_device",
        device_type="test_type",
        class_name="TestDevice",
        parameters={"param1": "value1"},
    )

    result = create_new_device(config, temp_config_file)

    assert result["name"] == "test_device"
    assert result["class"] == "TestDevice"
    assert result["parameters"] == {"param1": "value1"}
