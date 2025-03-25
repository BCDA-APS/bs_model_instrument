"""Simulation plans for the demo instrument.

This module contains plans that simulate various data collection scenarios.
These plans are useful for testing and development purposes.
"""

from typing import Any
from typing import List
from typing import Optional

from bluesky import plan_stubs as bps
from bluesky.preprocessors import run_decorator
from ophyd import Device

from apsbits.demo_instrument.devices import det
from apsbits.demo_instrument.devices import motor
from apsbits.demo_instrument.devices import motor1
from apsbits.demo_instrument.devices import motor2


@run_decorator(md={})
def sim_count_plan(
    num: int = 5,
    noise: float = 0.1,
    detector: Optional[Device] = None,
) -> Any:
    """Simulate a counting measurement with noise.

    Args:
        num: Number of counts to perform. Defaults to 5.
        noise: Amount of noise to add to the measurement. Defaults to 0.1.
        detector: Detector to use for the scan. If None, uses the default detector.

    Returns:
        Any: The result of the plan execution.
    """
    if detector is None:
        detector = det
    yield from bps.count([detector], num=num, md={"noise": noise})


@run_decorator(md={})
def sim_scan_plan(
    start: float = -1,
    stop: float = 1,
    num: int = 10,
    noise: float = 0.1,
    detector: Optional[Device] = None,
) -> Any:
    """Simulate a scan with noise.

    Args:
        start: Starting position. Defaults to -1.
        stop: Stopping position. Defaults to 1.
        num: Number of points in the scan. Defaults to 10.
        noise: Amount of noise to add to the measurement. Defaults to 0.1.
        detector: Detector to use for the scan. If None, uses the default detector.

    Returns:
        Any: The result of the plan execution.
    """
    if detector is None:
        detector = det
    yield from bps.scan([detector], motor, start, stop, num, md={"noise": noise})


@run_decorator(md={})
def sim_grid_scan_plan(
    start1: float = -1,
    stop1: float = 1,
    num1: int = 5,
    start2: float = -1,
    stop2: float = 1,
    num2: int = 5,
    noise: float = 0.1,
) -> Any:
    """Simulate a 2D grid scan with noise.

    Args:
        start1: Starting position for first motor. Defaults to -1.
        stop1: Stopping position for first motor. Defaults to 1.
        num1: Number of points for first motor. Defaults to 5.
        start2: Starting position for second motor. Defaults to -1.
        stop2: Stopping position for second motor. Defaults to 1.
        num2: Number of points for second motor. Defaults to 5.
        noise: Amount of noise to add to the measurement. Defaults to 0.1.

    Returns:
        Any: The result of the plan execution.
    """
    yield from bps.grid_scan(
        [det],
        motor1,
        start1,
        stop1,
        num1,
        motor2,
        start2,
        stop2,
        num2,
        md={"noise": noise},
    )


@run_decorator(md={})
def sim_list_scan_plan(
    positions: List[float],
    noise: float = 0.1,
    detector: Optional[Device] = None,
) -> Any:
    """Simulate a scan at specified positions with noise.

    Args:
        positions: List of positions to scan.
        noise: Amount of noise to add to the measurement. Defaults to 0.1.
        detector: Detector to use for the scan. If None, uses the default detector.

    Returns:
        Any: The result of the plan execution.
    """
    if detector is None:
        detector = det
    yield from bps.list_scan([detector], motor, positions, md={"noise": noise})


@run_decorator(md={})
def sim_adaptive_scan_plan(
    start: float = -1,
    stop: float = 1,
    min_step: float = 0.1,
    max_step: float = 1.0,
    target_delta: float = 0.1,
    noise: float = 0.1,
) -> Any:
    """Simulate an adaptive scan with noise.

    Args:
        start: Starting position. Defaults to -1.
        stop: Stopping position. Defaults to 1.
        min_step: Minimum step size. Defaults to 0.1.
        max_step: Maximum step size. Defaults to 1.0.
        target_delta: Target change in signal between points. Defaults to 0.1.
        noise: Amount of noise to add to the measurement. Defaults to 0.1.

    Returns:
        Any: The result of the plan execution.
    """
    yield from bps.adaptive_scan(
        [det],
        motor,
        start,
        stop,
        min_step,
        max_step,
        target_delta,
        md={"noise": noise},
    )
