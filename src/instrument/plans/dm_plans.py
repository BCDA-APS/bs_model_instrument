"""
Plans in support of APS Data Management
=======================================

.. autosummary::

    ~dm_kickoff_workflow
    ~dm_list_processing_jobs
    ~dm_submit_workflow_job
"""

import logging

from apstools.devices import DM_WorkflowConnector
from apstools.utils import dm_api_proc
from apstools.utils import share_bluesky_metadata_with_dm
from bluesky import plan_stubs as bps

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
