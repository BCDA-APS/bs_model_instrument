from typing import Any

import pytest

from instrument.startup import RE
from instrument.startup import make_devices


@pytest.fixture(scope="session")
def runengine_with_devices() -> Any:
    """
    Initialize the RunEngine with devices for testing.

    This fixture calls RE with the output of make_devices() to mimic
    the behavior previously performed in the startup module.

    Returns:
        Any: An instance of the RunEngine with devices configured.
    """
    return RE(make_devices())
