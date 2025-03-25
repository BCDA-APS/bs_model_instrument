"""Demo instrument devices.

This module contains the device definitions for the demo instrument.
"""

from typing import Any
from typing import Dict
from typing import Optional

from ophyd import Device
from ophyd import Signal
from ophyd.sim import SynAxis
from ophyd.sim import SynGauss

# Create simulated devices
motor = SynAxis(name="motor", labels={"motors", "demo"})
motor1 = SynAxis(name="motor1", labels={"motors", "demo"})
motor2 = SynAxis(name="motor2", labels={"motors", "demo"})
motor3 = SynAxis(name="motor3", labels={"motors", "demo"})

# Create a simulated detector
det = SynGauss(
    "det", motor, "motor", center=0, Imax=1, sigma=1, labels={"detectors", "demo"}
)

__all__ = [
    "motor",
    "motor1",
    "motor2",
    "motor3",
    "det",
]
