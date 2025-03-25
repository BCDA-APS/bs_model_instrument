"""
Plans in support of APS Data Management
=======================================

.. autosummary::

    ~dm_kickoff_workflow
    ~dm_list_processing_jobs
    ~dm_submit_workflow_job
"""

import logging
<<<<<<< HEAD
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
=======
from typing import Any, Dict, List, Optional, Union
>>>>>>> d4841a2b133ec2f8de5bd85c87c97e12c58a69a1

from apstools.devices import DM_WorkflowConnector
from apstools.utils import dm_api_proc
from apstools.utils import share_bluesky_metadata_with_dm
from bluesky import plan_stubs as bps
from bluesky.preprocessors import run_decorator
<<<<<<< HEAD
from ophyd import Device

from apsbits.demo_instrument.devices import det
from apsbits.demo_instrument.devices import motor
from apsbits.demo_instrument.devices import motor1
from apsbits.demo_instrument.devices import motor2
=======
from ophyd import Device, Signal

from apsbits.demo_instrument.devices import det, motor, motor1, motor2, motor3
>>>>>>> d4841a2b133ec2f8de5bd85c87c97e12c58a69a1

logger = logging.getLogger(__name__)
logger.bsdev(__file__)


def dm_kickoff_workflow(run, argsDict, timeout=None, wait=False):
    """
    Start a DM workflow for this bluesky run and share run's metadata with DM.

    PARAMETERS:

    run (*obj*): Bluesky run object (such as 'run = cat[uid]').

    argsDict (*dict*): Dictionary of parameters needed by 'workflowName'.
        At minimum, most workflows expect these keys: 'filePath' and
        'experimentName'.  Consult the workflow for the expected
        content of 'argsDict'.

    timeout (*number*): When should bluesky stop reporting on this
        DM workflow job (if it has not ended). Units are seconds.
        Default is forever.

    wait (*bool*): Should this plan stub wait for the job to end?
        Default is 'False'.
    """
    dm_workflow = DM_WorkflowConnector(name="dm_workflow")

    if timeout is None:
        # Disable periodic reports, use a long time (s).
        timeout = 999_999_999_999

    yield from bps.mv(dm_workflow.concise_reporting, True)
    yield from bps.mv(dm_workflow.reporting_period, timeout)

    workflow_name = argsDict.pop["workflowName"]
    yield from dm_workflow.run_as_plan(
        workflow=workflow_name,
        wait=wait,
        timeout=timeout,
        **argsDict,
    )

    # Upload bluesky run metadata to APS DM.
    share_bluesky_metadata_with_dm(argsDict["experimentName"], workflow_name, run)

    # Users requested the DM workflow job ID be printed to the console.
    dm_workflow._update_processing_data()
    job_id = dm_workflow.job_id.get()
    job_stage = dm_workflow.stage_id.get()
    job_status = dm_workflow.status.get()
    print(f"DM workflow id: {job_id!r}  status: {job_status}  stage: {job_stage}")


def dm_list_processing_jobs(exclude=None):
    """
    Show all the DM jobs with status not excluded.

    Excluded status (default): 'done', 'failed'
    """
    yield from bps.null()  # make this a plan stub
    api = dm_api_proc()
    if exclude is None:
        exclude = ("done", "failed")

    for j in api.listProcessingJobs():
        if j["status"] not in exclude:
            print(
                f"id={j['id']!r}"
                f"  submitted={j.get('submissionTimestamp')}"
                f"  status={j['status']!r}"
            )


def dm_submit_workflow_job(workflowName, argsDict):
    """
    Low-level plan stub to submit a job to a DM workflow.

    It is recommended to use dm_kickoff_workflow() instead.
    This plan does not share run metadata with DM.

    PARAMETERS:

    workflowName (*str*): Name of the DM workflow to be run.

    argsDict (*dict*): Dictionary of parameters needed by 'workflowName'.
        At minimum, most workflows expect these keys: 'filePath' and
        'experimentName'.  Consult the workflow for the expected
        content of 'argsDict'.
    """
    yield from bps.null()  # make this a plan stub
    api = dm_api_proc()

    job = api.startProcessingJob(api.username, workflowName, argsDict)
    print(f"workflow={workflowName!r}  id={job['id']!r}")


@run_decorator(md={})
def dm_count_plan(
    num: int = 5,
    detector: Optional[Device] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> Any:
    """Perform a counting measurement with metadata.

    Args:
        num: Number of counts to perform. Defaults to 5.
        detector: Detector to use for the scan. If None, uses the default detector.
        metadata: Additional metadata to include in the run. Defaults to None.

    Returns:
        Any: The result of the plan execution.
    """
    if detector is None:
        detector = det
    if metadata is None:
        metadata = {}
    yield from bps.count([detector], num=num, md=metadata)


@run_decorator(md={})
def dm_scan_plan(
    start: float = -1,
    stop: float = 1,
    num: int = 10,
    detector: Optional[Device] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> Any:
    """Perform a scan with metadata.

    Args:
        start: Starting position. Defaults to -1.
        stop: Stopping position. Defaults to 1.
        num: Number of points in the scan. Defaults to 10.
        detector: Detector to use for the scan. If None, uses the default detector.
        metadata: Additional metadata to include in the run. Defaults to None.

    Returns:
        Any: The result of the plan execution.
    """
    if detector is None:
        detector = det
    if metadata is None:
        metadata = {}
    yield from bps.scan([detector], motor, start, stop, num, md=metadata)


@run_decorator(md={})
def dm_grid_scan_plan(
    start1: float = -1,
    stop1: float = 1,
    num1: int = 5,
    start2: float = -1,
    stop2: float = 1,
    num2: int = 5,
    metadata: Optional[Dict[str, Any]] = None,
) -> Any:
    """Perform a 2D grid scan with metadata.

    Args:
        start1: Starting position for first motor. Defaults to -1.
        stop1: Stopping position for first motor. Defaults to 1.
        num1: Number of points for first motor. Defaults to 5.
        start2: Starting position for second motor. Defaults to -1.
        stop2: Stopping position for second motor. Defaults to 1.
        num2: Number of points for second motor. Defaults to 5.
        metadata: Additional metadata to include in the run. Defaults to None.

    Returns:
        Any: The result of the plan execution.
    """
    if metadata is None:
        metadata = {}
    yield from bps.grid_scan(
        [det], motor1, start1, stop1, num1, motor2, start2, stop2, num2, md=metadata
    )


@run_decorator(md={})
def dm_list_scan_plan(
    positions: List[float],
    detector: Optional[Device] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> Any:
    """Perform a scan at specified positions with metadata.

    Args:
        positions: List of positions to scan.
        detector: Detector to use for the scan. If None, uses the default detector.
        metadata: Additional metadata to include in the run. Defaults to None.

    Returns:
        Any: The result of the plan execution.
    """
    if detector is None:
        detector = det
    if metadata is None:
        metadata = {}
    yield from bps.list_scan([detector], motor, positions, md=metadata)


@run_decorator(md={})
def dm_adaptive_scan_plan(
    start: float = -1,
    stop: float = 1,
    min_step: float = 0.1,
    max_step: float = 1.0,
    target_delta: float = 0.1,
    metadata: Optional[Dict[str, Any]] = None,
) -> Any:
    """Perform an adaptive scan with metadata.

    Args:
        start: Starting position. Defaults to -1.
        stop: Stopping position. Defaults to 1.
        min_step: Minimum step size. Defaults to 0.1.
        max_step: Maximum step size. Defaults to 1.0.
        target_delta: Target change in signal between points. Defaults to 0.1.
        metadata: Additional metadata to include in the run. Defaults to None.

    Returns:
        Any: The result of the plan execution.
    """
    if metadata is None:
        metadata = {}
    yield from bps.adaptive_scan(
        [det], motor, start, stop, min_step, max_step, target_delta, md=metadata
    )
