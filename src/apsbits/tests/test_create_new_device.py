"""Tests for the create_new_device module.

This module contains tests for the device creation functionality, including:
- Device configuration validation
- YAML file handling
- Device class creation
- Error handling
"""

from pathlib import Path
from typing import TYPE_CHECKING

import pytest
import yaml

from apsbits.utils.create_new_device import DeviceConfig
from apsbits.utils.create_new_device import create_device_class
from apsbits.utils.create_new_device import create_new_device
from apsbits.utils.create_new_device import get_device_class

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
        "apsbits.utils.create_new_device.Path",
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
        name="test_device",
        device_type="sensor",
        class_name="TestSensor",
        parameters={"port": "COM1"},
        location="room_1",
    )

    create_new_device(config)

    assert "Creating new device: test_device" in caplog.text
    assert "Device created successfully" in caplog.text


def test_get_device_class_not_found() -> None:
    """Test that attempting to get a non-existent device class raises ImportError."""
    with pytest.raises(ImportError):
        get_device_class("NonExistentDevice")


def test_create_new_device_with_existing_config(temp_config_file: Path) -> None:
    """Test device creation with existing configuration file.

    Args:
        temp_config_file: Path to temporary config file
    """
    # Create initial config
    with open(temp_config_file, "w") as f:
        yaml.dump({"devices": {"existing_device": {"name": "existing_device"}}}, f)

    config = DeviceConfig(
        name="test_device",
        device_type="sensor",
        class_name="TestSensor",
        parameters={"port": "COM1"},
        location="room_1",
    )

    result = create_new_device(config, temp_config_file)

    # Verify both devices exist in config
    with open(temp_config_file, "r") as f:
        yaml_data = yaml.safe_load(f)

    assert "existing_device" in yaml_data["devices"]
    assert "test_device" in yaml_data["devices"]
    assert yaml_data["devices"]["test_device"] == result


def test_create_device_class_with_existing_file(temp_devices_dir: Path) -> None:
    """Test creation of device class when file already exists.

    Args:
        temp_devices_dir: Path to temporary devices directory
    """
    # Create initial file
    class_file = temp_devices_dir / "testdevice.py"
    class_file.write_text("# Existing content")

    create_device_class("TestDevice", "test_type")

    # Verify file was not overwritten
    assert class_file.read_text() == "# Existing content"


def test_create_new_device_with_invalid_config_file(temp_config_file: Path) -> None:
    """Test device creation with invalid configuration file.

    Args:
        temp_config_file: Path to temporary config file
    """
    # Create invalid YAML file
    temp_config_file.write_text("invalid: yaml: content: {")

    config = DeviceConfig(
        name="test_device",
        device_type="sensor",
        class_name="TestSensor",
        parameters={"port": "COM1"},
        location="room_1",
    )

    with pytest.raises(yaml.YAMLError):
        create_new_device(config, temp_config_file)


def test_create_new_device_with_duplicate_name(temp_config_file: Path) -> None:
    """Test device creation with duplicate device name.

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

    # Create first device
    create_new_device(config, temp_config_file)

    # Attempt to create device with same name
    with pytest.raises(ValueError, match="Device with name test_device already exists"):
        create_new_device(config, temp_config_file)


def test_create_device_class_with_invalid_name() -> None:
    """Test creation of device class with invalid name."""
    with pytest.raises(ValueError, match="Invalid class name"):
        create_device_class("123InvalidName", "test_type")


def test_create_new_device_without_config_file() -> None:
    """Test device creation without configuration file."""
    config = DeviceConfig(
        name="test_device",
        device_type="sensor",
        class_name="TestSensor",
        parameters={"port": "COM1"},
        location="room_1",
    )

    result = create_new_device(config)

    assert result["name"] == "test_device"
    assert result["type"] == "sensor"
    assert result["class"] == "TestSensor"
    assert result["parameters"]["port"] == "COM1"
    assert result["location"] == "room_1"
