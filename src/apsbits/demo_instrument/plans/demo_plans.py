"""Demo plans for the demo instrument.

This module contains example plans that demonstrate basic Bluesky functionality.
These plans are used for testing and demonstration purposes.
"""

from typing import Any, Dict, List, Optional, Union

from bluesky import plan_stubs as bps
from bluesky.preprocessors import run_decorator
from ophyd import Device, Signal

from apsbits.demo_instrument.devices import det, motor, motor1, motor2, motor3


@run_decorator(md={})
def demo_print_plan() -> Any:
    """Print a simple message using the demo detector.

    Returns:
        Any: The result of the plan execution.
    """
    yield from bps.read(det)
    yield from bps.print_console("Hello from demo_print_plan!")


@run_decorator(md={})
def demo_count_plan(num: int = 5) -> Any:
    """Perform a simple counting measurement.

    Args:
        num: Number of counts to perform. Defaults to 5.

    Returns:
        Any: The result of the plan execution.
    """
    yield from bps.count([det], num=num)


@run_decorator(md={})
def demo_rel_scan_plan(
    start: float = -1,
    stop: float = 1,
    num: int = 10,
    detector: Optional[Device] = None,
) -> Any:
    """Perform a relative scan with the specified parameters.

    Args:
        start: Starting position relative to current position. Defaults to -1.
        stop: Stopping position relative to current position. Defaults to 1.
        num: Number of points in the scan. Defaults to 10.
        detector: Detector to use for the scan. If None, uses the default detector.

    Returns:
        Any: The result of the plan execution.
    """
    if detector is None:
        detector = det
    yield from bps.rel_scan([detector], motor, start, stop, num)


@run_decorator(md={})
def demo_list_scan_plan(
    positions: List[float],
    detector: Optional[Device] = None,
) -> Any:
    """Perform a scan at specified positions.

    Args:
        positions: List of positions to scan.
        detector: Detector to use for the scan. If None, uses the default detector.

    Returns:
        Any: The result of the plan execution.
    """
    if detector is None:
        detector = det
    yield from bps.list_scan([detector], motor, positions)


@run_decorator(md={})
def demo_grid_scan_plan(
    start1: float = -1,
    stop1: float = 1,
    num1: int = 5,
    start2: float = -1,
    stop2: float = 1,
    num2: int = 5,
) -> Any:
    """Perform a 2D grid scan.

    Args:
        start1: Starting position for first motor. Defaults to -1.
        stop1: Stopping position for first motor. Defaults to 1.
        num1: Number of points for first motor. Defaults to 5.
        start2: Starting position for second motor. Defaults to -1.
        stop2: Stopping position for second motor. Defaults to 1.
        num2: Number of points for second motor. Defaults to 5.

    Returns:
        Any: The result of the plan execution.
    """
    yield from bps.grid_scan([det], motor1, start1, stop1, num1, motor2, start2, stop2, num2)


@run_decorator(md={})
def demo_inner_product_scan_plan(
    start: float = -1,
    stop: float = 1,
    num: int = 10,
) -> Any:
    """Perform an inner product scan.

    Args:
        start: Starting position. Defaults to -1.
        stop: Stopping position. Defaults to 1.
        num: Number of points in the scan. Defaults to 10.

    Returns:
        Any: The result of the plan execution.
    """
    yield from bps.inner_product_scan([det], motor1, start, stop, num, motor2, start, stop, num)


@run_decorator(md={})
def demo_adaptive_scan_plan(
    start: float = -1,
    stop: float = 1,
    min_step: float = 0.1,
    max_step: float = 1.0,
    target_delta: float = 0.1,
) -> Any:
    """Perform an adaptive scan.

    Args:
        start: Starting position. Defaults to -1.
        stop: Stopping position. Defaults to 1.
        min_step: Minimum step size. Defaults to 0.1.
        max_step: Maximum step size. Defaults to 1.0.
        target_delta: Target change in signal between points. Defaults to 0.1.

    Returns:
        Any: The result of the plan execution.
    """
    yield from bps.adaptive_scan(
        [det], motor, start, stop, min_step, max_step, target_delta
    ) 