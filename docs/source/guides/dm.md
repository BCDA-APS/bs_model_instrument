# Guide: APS Data Management Plans

Provides a few examples of the plans that interact with APS Data Management (DM)
tools.

## Required

The DM tools rely on the existence of a set of environment variables that define various aspects of the DM system.

## Show any DM jobs still processing

Use the `dm_list_processing_jobs()` plan stub to show DM any workflow jobs that
are still running or pending.  These are installed by calling
`aps_dm_setup(DM_SETUP_SCRIPT)` in each session before you call any other DM
code.

Here, `DM_SETUP_SCRIPT` is the full path to the bash setup shell script provided
by DM for this account.  The exact path can be different for some installations.
If unsure, contact the APS DM team for advice.

Note: `aps_dm_setup` is not a bluesky plan stub.  Call it as a standard Python
function.

Here's an example:

```py
from instrument.utils.aps_functions import aps_dm_setup

aps_dm_setup("/home/dm/etc/dm.setup.sh")
```

## Start a new workflow job

The `dm_kickoff_workflow()` plan can be used to start a DM workflow job.  See
the source code for additional options (such as how often to report progress and
how to wait for the workflow to finish before the bluesky plan proceeds).

```py
from instrument.plans.dm_plans import dm_kickoff_workflow

# Use the run with `uid` from the catalog `cat`.
run = cat[uid]

# Create the dictionary of arguments for the chosen workflow.
argsDict = {
    "filePath": "path/to/data/file.mda",  # example
    "experimentName": "testing-2024-11",  # example
    "workflowName": "processing",  # existing workflow name
    # ... any other items required by the workflow
}

# Start the workflow job from the command line:
RE(dm_kickoff_workflow(run, argsDict))
```

In a plan, replace the call to `RE(...)` with `yield from ...`, such as:

```py
def a_plan():
    # earlier steps
    yield from dm_kickoff_workflow(run, argsDict)
    # later steps
```

## Start a new workflow job (Low-level)

If the `dm_kickoff_workflow()` plan stub does more than you want, you might consider the `dm_submit_workflow_job()`
plan stub.  The `dm_submit_workflow_job()` plan stub is
a thin wrapper around DM's `startProcessingJob()` function.
The plan stub converts this DM function into a bluesky plan, and reports the DM workflow job `id` once the job has been submitted.

As above, you'll need the `workflowName` and the `argsDict`.

From the command line: `RE(dm_submit_workflow_job(workflowName, argsDict))`

In a plan: `yield from dm_submit_workflow_job(workflowName, argsDict)`

## References

The `apstools`
[package](https://bcda-aps.github.io/apstools/latest/api/_utils.html#aps-data-management)
has more support to integrate various capabilities of the DM tools.

For more information about DM, see its [API
Reference](https://git.aps.anl.gov/DM/dm-docs/-/wikis/DM/Beamline-Services/API-Reference).

## Example session

Let's work through an example session at an APS beamline.  The instrument
package is named `mic_instrument`.  Start a new console session:

```bash
ipython -i -c "from mic_instrument.startup import *"
```

Make some imports and get the DM environment variables:

```py
from apstools.utils import dm_setup, dm_api_proc
import dm  # conda install apsu::aps-dm-api
from mic_instrument.plans import dm_submit_workflow_job

# Usually called when the instrument package starts.
# For some reason, we need to call this now.
dm_setup("/home/dm_id/etc/dm.setup.sh")
```

Get DM Processing API to make direct calls (diagnostic purposes).

```py
api = dm_api_proc()
```

To see all capabilities this DM api object offers: `dir(api)`.
To see all available workflows (with all their instructions):
`api.listWorkflows(api.username)`.
Show some basic `api` information:

```py
print(f"{api.username=!r}")
print(f'{len(api.listWorkflows("user19id"))=!r}')
```

Set some parameters to try starting a DM workflow.  We know the workflow
will take more parameters but we want to prove we can, at least, start
a DM workflow from a bluesky session.  Our account allows one workflow
now: `"xrf-maps"`.  Previously, a DM experiment named `"Bluesky202411"`
was created for our development work.

```py
WORKFLOW = "xrf-maps"  # api.listWorkflows(api.username)[0]
argsDict = dict(filePath="README.md", experimentName="Bluesky202411")
```

We now have just enough to start a DM workflow from a bluesky session.
We know the workflow will fail early since it expects a MDA data file,
not our `README.md` file.

```py
RE(dm_submit_workflow_job(WORKFLOW, argsDict))
```

DM can tell us how many workflow processing jobs, such as ours, have
been submitted:

```py
print(f"{len(api.listProcessingJobs())=!r}")
```

If we run this next command very soon, we can see our workflow job
is still processing (has not failed yet).

```py
RE(dm_list_processing_jobs())
```

This command will get the `id` of the most recent job:

```py
job_id = api.listProcessingJobs()[-1]["id"]
```

Use the `job_id` to view the processing status:

```py
details = api.getProcessingJobById(id=job_id, owner=api.username)
# Show the details in a readable format:
dict(details)
```

The DM api can tell you the workflow definition:

```py
wf_def = api.getWorkflowByName(owner=api.username, name=WORKFLOW)
```

This looks like a Python dictionary:

```py
dict(wf_def)
```

Some (but not all) workflows have a description.

```py
print(wf_def.get("description", "no description available"))
```

### Example Session

Here's our Bluesky IPython session, with input and output:

```py
In [1]: from apstools.utils import dm_setup, dm_api_proc
   ...: import dm  # conda install apsu::aps-dm-api
   ...: from mic_instrument.plans import dm_submit_workflow_job

In [3]: dm_setup("/home/dm_id/etc/dm.setup.sh")
Out[3]: '19id'

In [4]: api = dm_api_proc()

In [5]: print(f"{api.username=!r}")
   ...: print(f'{len(api.listWorkflows("user19id"))=!r}')
api.username='user19id'
len(api.listWorkflows("user19id"))=1

In [6]: WORKFLOW = "xrf-maps"  # api.listWorkflows(api.username)[0]
   ...: argsDict = dict(filePath="README.md", experimentName="Bluesky202411")

In [7]: RE(dm_submit_workflow_job(WORKFLOW, argsDict))
workflow='xrf-maps'  id='9276f545-6e17-45c0-b5c5-b4d36a75f4dd'
Out[7]: ()

In [8]: print(f"{len(api.listProcessingJobs())=!r}")
   ...:
len(api.listProcessingJobs())=17

In [9]: RE(dm_list_processing_jobs())
   ...:
Out[9]: ()

In [10]: job_id = api.listProcessingJobs()[-1]["id"]
    ...: job_id
Out[10]: '9276f545-6e17-45c0-b5c5-b4d36a75f4dd'

In [11]: details = api.getProcessingJobById(id=job_id, owner=api.username)
    ...: # Show the details in a readable format:
    ...: dict(details)
    ...:
Out[11]:
{'filePath': 'README.md',
 'experimentName': 'Bluesky202411',
 'workflow': {'name': 'xrf-maps',
  'version': '0.0.0',
  'description': 'Workflow for XRF-Maps X-ray fluorescence microscopy data analysis package.\nhttps://github.com/AdvancedPhotonSource/XRF-Maps\nKeyword Arguments:\n\tfilePath - Raw data file path.\n\tfit - <roi,roi_plus,nnls,tails,matrix> - Comma seperated list of fitting routines.\n\tdataDir (optional) - Directory containing raw data files.\n\tnthreads (optional) - Number of threads to use. default: all\n\tquantifyWith (optional) - File to use as quantification standard.\n\tdetectors (optional) - Detectors to process. default: 0,1,2,3 for 4 detectors\n\tgenerateAvgH5 (optional) - Generate .h5 file which is the average of all detectors. default: False\n\taddV9Layout (optional) - Generate .h5 file which has v9 layout able to open in IDL MAPS software. default: False\n\taddExchange (optional) - Add exchange group into hdf5 file with normalized data. default: False\n\texportCSV (optional) - Export Integrated spec, fitted, background to csv file. default: False\n\tupdateTheta <theta_pv_string> (optional) - Update the theta dataset value using theta_pv_string as new pv string ref.\n\tupdateAmps <us_amp>,<ds_amp> (optional) - Updates upstream and downstream amps if they changed inbetween scans.\n\tupdateQuantAmps <us_amp>,<ds_amp> (optional) - Updates upstream and downstream amps for quantification if they changed inbetween scans.\n\tquickAndDirty (optional) - Integrate the detector range into 1 spectra. default: False\n\toptimizeFitOverrideParams (optional) - Integrate the 8 largest mda datasets and fit with multiple params. 1 = matrix batch fit, 2 = batch fit without tails, 3 = batch fit with tails, 4 = batch fit with free E & everything else fixed.\n\toptimizer <lmfit, mpfit> (optional) - Choose which optimizer to use for optimizeFitOverrideParams.',
  'userAccount': 'user19id',
  'owner': 'user19id',
  'stages': {'00-CHECK-FILE': {'runIf': 'not "mda" in "$filePath"',
    'command': '/bin/echo "Skipping file $filePath. Waiting for mda file."',
    'childProcesses': {'0': {'stageId': '00-CHECK-FILE',
      'childProcessNumber': 0,
      'command': '/usr/bin/sudo -u user19id -- /bin/echo "Skipping file README.md. Waiting for mda file."',
      'workingDir': None,
      'status': 'done',
      'submitTime': 1732140753.1868541,
      'startTime': 1732140753.1877713,
      'endTime': 1732140753.55717,
      'runTime': 0.3693985939025879,
      'exitStatus': 0,
      'stdOut': 'Skipping file README.md. Waiting for mda file.\n',
      'stdErr': ''}},
    'nRunningChildProcesses': 0,
    'nQueuedChildProcesses': 0,
    'nCompletedChildProcesses': 1},
   '01-ANALYSIS-MACHINE': {'runIf': '"mda" in "$filePath"',
    'command': 'sh /home/dm_id/dm-workflows/scripts/machine.sh /home/dm_id/etc/dm.workflow_setup.sh "$analysisMachine"',
    'outputVariableRegexList': ['Analysis Machine: (?P<analysisMachine>.*)'],
    'childProcesses': {},
    'nRunningChildProcesses': 0,
    'nQueuedChildProcesses': 0,
    'status': 'skipped'},
   '02-PARSE-ARGS': {'runIf': '"mda" in "$filePath"',
    'command': 'sh /home/dm_id/dm-workflows/techniques/xrfMaps/args.sh /home/dm_id/etc/dm.workflow_setup.sh "$experimentName" "$fit" "$filePath" "$dataDir" "$nthreads" "$quantifyWith" "$detectors" "$generateAvgH5" "$addv9Layout" "$addExchange" "$exportCSV" "$updateTheta" "$updateAmps" "$updateQuantAmps" "$quickAndDirty" "$optimizeFitOverrideParams" "$optimizer" "$localWorkingDir" "$demand"',
    'outputVariableRegexList': ['Analysis Arguments: (?P<analysisArgs>.*)',
     'Local Working Directory: (?P<localWorkingDir>.*)',
     'Experiment Data Directory: (?P<dataDirectory>.*)',
     'Experiment Analysis Directory: (?P<analysisDirectory>.*)',
     'Use Demand Queue: (?P<demand>.*)'],
    'childProcesses': {},
    'nRunningChildProcesses': 0,
    'nQueuedChildProcesses': 0,
    'status': 'skipped'},
   '03-XRF-MAPS-LOCAL': {'runIf': '"mda" in "$filePath" and "$analysisMachine" != "polaris"',
    'command': 'sh /home/dm_id/dm-workflows/scripts/local.sh /home/dm_id/etc/dm.workflow_setup.sh $analysisMachine $localWorkingDir XRF_MAPS "$analysisArgs"',
    'childProcesses': {},
    'nRunningChildProcesses': 0,
    'nQueuedChildProcesses': 0,
    'status': 'skipped'},
   '04-GROUP': {'runIf': '"mda" in "$filePath" and "$analysisMachine" == "polaris"',
    'command': 'sh /home/dm_id/dm-workflows/apsGladierFlows/scripts/group.sh /home/dm_id/etc/dm.workflow_setup.sh "$experimentName"',
    'outputVariableRegexList': ['Globus Group: (?P<globusGroup>.*)'],
    'childProcesses': {},
    'nRunningChildProcesses': 0,
    'nQueuedChildProcesses': 0,
    'status': 'skipped'},
   '05-XRF-MAPS-POLARIS': {'runIf': '"mda" in "$filePath" and "$analysisMachine" == "polaris"',
    'command': 'sh /home/dm_id/dm-workflows/apsGladierFlows/scripts/gladier.sh /home/dm_id/etc/dm.workflow_setup.sh $experimentName $globusGroup $demand xrfMaps --result-directory $analysisDirectory $analysisArgs',
    'outputVariableRegexList': ['Flow Action ID: (?P<flowID>.*)',
     'URL: (?P<url>.*)',
     'Status: (?P<gladierStatus>.*)'],
    'childProcesses': {},
    'nRunningChildProcesses': 0,
    'nQueuedChildProcesses': 0,
    'status': 'skipped'},
   '06-MONITOR': {'runIf': '"mda" in "$filePath" and "$analysisMachine" == "polaris"',
    'command': 'sh /home/dm_id/dm-workflows/apsGladierFlows/scripts/monitor.sh /home/dm_id/etc/dm.workflow_setup.sh $flowID',
    'repeatPeriod': 5,
    'repeatUntil': '"$gladierStatus" == "SUCCEEDED" or "$gladierStatus" == "FAILED"',
    'maxRepeats': 999999,
    'outputVariableRegexList': ['Status: (?P<gladierStatus>.*)'],
    'childProcesses': {},
    'nRunningChildProcesses': 0,
    'nQueuedChildProcesses': 0,
    'status': 'skipped'},
   '07-PERMISSIONS': {'runIf': '"mda" in "$filePath"',
    'command': 'sh /home/dm_id/dm-workflows/scripts/permissions.sh /home/dm_id/etc/dm.workflow_setup.sh $experimentName data/',
    'childProcesses': {},
    'nRunningChildProcesses': 0,
    'nQueuedChildProcesses': 0,
    'status': 'skipped'},
   '08-MOVE': {'runIf': '"$analysisMachine" != "polaris" and (".master" in "$filePath" or ".mda" in "$filePath")',
    'command': 'sh /home/dm_id/dm-workflows/techniques/xrfMaps/07-move.sh $dataDirectory $analysisDirectory $analysisMachine $filePath',
    'childProcesses': {},
    'nRunningChildProcesses': 0,
    'nQueuedChildProcesses': 0,
    'status': 'skipped'},
   '09-DONE': {'command': '/bin/echo Job done.',
    'childProcesses': {'1': {'stageId': '09-DONE',
      'childProcessNumber': 1,
      'command': '/usr/bin/sudo -u user19id -- /bin/echo Job done.',
      'workingDir': None,
      'status': 'done',
      'submitTime': 1732140753.558312,
      'startTime': 1732140753.5592012,
      'endTime': 1732140753.5912957,
      'runTime': 0.032094478607177734,
      'exitStatus': 0,
      'stdOut': 'Job done.\n',
      'stdErr': ''}},
    'nRunningChildProcesses': 0,
    'nQueuedChildProcesses': 0,
    'nCompletedChildProcesses': 1}},
  'id': '66842cc752b9aa7b628c67bb'},
 'owner': 'user19id',
 'id': '9276f545-6e17-45c0-b5c5-b4d36a75f4dd',
 'submissionTime': 1732140753.1852503,
 'submissionTimestamp': '2024/11/20 16:12:33 CST',
 'countFiles': 1,
 'status': 'done',
 'startTime': 1732140753.1863618,
 'startTimestamp': '2024/11/20 16:12:33 CST',
 'stage': '09-DONE',
 'endTime': 1732140753.591535,
 'endTimestamp': '2024/11/20 16:12:33 CST',
 'runTime': 0.40517330169677734}

In [12]: wf_def = api.getWorkflowByName(owner=api.username, name=WORKFLOW)

In [13]: dict(wf_def)
Out[13]:
{'name': 'xrf-maps',
 'version': '0.0.0',
 'description': 'Workflow for XRF-Maps X-ray fluorescence microscopy data analysis package.\nhttps://github.com/AdvancedPhotonSource/XRF-Maps\nKeyword Arguments:\n\tfilePath - Raw data file path.\n\tfit - <roi,roi_plus,nnls,tails,matrix> - Comma seperated list of fitting routines.\n\tdataDir (optional) - Directory containing raw data files.\n\tnthreads (optional) - Number of threads to use. default: all\n\tquantifyWith (optional) - File to use as quantification standard.\n\tdetectors (optional) - Detectors to process. default: 0,1,2,3 for 4 detectors\n\tgenerateAvgH5 (optional) - Generate .h5 file which is the average of all detectors. default: False\n\taddV9Layout (optional) - Generate .h5 file which has v9 layout able to open in IDL MAPS software. default: False\n\taddExchange (optional) - Add exchange group into hdf5 file with normalized data. default: False\n\texportCSV (optional) - Export Integrated spec, fitted, background to csv file. default: False\n\tupdateTheta <theta_pv_string> (optional) - Update the theta dataset value using theta_pv_string as new pv string ref.\n\tupdateAmps <us_amp>,<ds_amp> (optional) - Updates upstream and downstream amps if they changed inbetween scans.\n\tupdateQuantAmps <us_amp>,<ds_amp> (optional) - Updates upstream and downstream amps for quantification if they changed inbetween scans.\n\tquickAndDirty (optional) - Integrate the detector range into 1 spectra. default: False\n\toptimizeFitOverrideParams (optional) - Integrate the 8 largest mda datasets and fit with multiple params. 1 = matrix batch fit, 2 = batch fit without tails, 3 = batch fit with tails, 4 = batch fit with free E & everything else fixed.\n\toptimizer <lmfit, mpfit> (optional) - Choose which optimizer to use for optimizeFitOverrideParams.',
 'userAccount': 'user19id',
 'owner': 'user19id',
 'stages': {'00-CHECK-FILE': {'runIf': 'not "mda" in "$filePath"',
   'command': '/bin/echo "Skipping file $filePath. Waiting for mda file."'},
  '01-ANALYSIS-MACHINE': {'runIf': '"mda" in "$filePath"',
   'command': 'sh /home/dm_id/dm-workflows/scripts/machine.sh /home/dm_id/etc/dm.workflow_setup.sh "$analysisMachine"',
   'outputVariableRegexList': ['Analysis Machine: (?P<analysisMachine>.*)']},
  '02-PARSE-ARGS': {'runIf': '"mda" in "$filePath"',
   'command': 'sh /home/dm_id/dm-workflows/techniques/xrfMaps/args.sh /home/dm_id/etc/dm.workflow_setup.sh "$experimentName" "$fit" "$filePath" "$dataDir" "$nthreads" "$quantifyWith" "$detectors" "$generateAvgH5" "$addv9Layout" "$addExchange" "$exportCSV" "$updateTheta" "$updateAmps" "$updateQuantAmps" "$quickAndDirty" "$optimizeFitOverrideParams" "$optimizer" "$localWorkingDir" "$demand"',
   'outputVariableRegexList': ['Analysis Arguments: (?P<analysisArgs>.*)',
    'Local Working Directory: (?P<localWorkingDir>.*)',
    'Experiment Data Directory: (?P<dataDirectory>.*)',
    'Experiment Analysis Directory: (?P<analysisDirectory>.*)',
    'Use Demand Queue: (?P<demand>.*)']},
  '03-XRF-MAPS-LOCAL': {'runIf': '"mda" in "$filePath" and "$analysisMachine" != "polaris"',
   'command': 'sh /home/dm_id/dm-workflows/scripts/local.sh /home/dm_id/etc/dm.workflow_setup.sh $analysisMachine $localWorkingDir XRF_MAPS "$analysisArgs"'},
  '04-GROUP': {'runIf': '"mda" in "$filePath" and "$analysisMachine" == "polaris"',
   'command': 'sh /home/dm_id/dm-workflows/apsGladierFlows/scripts/group.sh /home/dm_id/etc/dm.workflow_setup.sh "$experimentName"',
   'outputVariableRegexList': ['Globus Group: (?P<globusGroup>.*)']},
  '05-XRF-MAPS-POLARIS': {'runIf': '"mda" in "$filePath" and "$analysisMachine" == "polaris"',
   'command': 'sh /home/dm_id/dm-workflows/apsGladierFlows/scripts/gladier.sh /home/dm_id/etc/dm.workflow_setup.sh $experimentName $globusGroup $demand xrfMaps --result-directory $analysisDirectory $analysisArgs',
   'outputVariableRegexList': ['Flow Action ID: (?P<flowID>.*)',
    'URL: (?P<url>.*)',
    'Status: (?P<gladierStatus>.*)']},
  '06-MONITOR': {'runIf': '"mda" in "$filePath" and "$analysisMachine" == "polaris"',
   'command': 'sh /home/dm_id/dm-workflows/apsGladierFlows/scripts/monitor.sh /home/dm_id/etc/dm.workflow_setup.sh $flowID',
   'repeatPeriod': 5,
   'repeatUntil': '"$gladierStatus" == "SUCCEEDED" or "$gladierStatus" == "FAILED"',
   'maxRepeats': 999999,
   'outputVariableRegexList': ['Status: (?P<gladierStatus>.*)']},
  '07-PERMISSIONS': {'runIf': '"mda" in "$filePath"',
   'command': 'sh /home/dm_id/dm-workflows/scripts/permissions.sh /home/dm_id/etc/dm.workflow_setup.sh $experimentName data/'},
  '08-MOVE': {'runIf': '"$analysisMachine" != "polaris" and (".master" in "$filePath" or ".mda" in "$filePath")',
   'command': 'sh /home/dm_id/dm-workflows/techniques/xrfMaps/07-move.sh $dataDirectory $analysisDirectory $analysisMachine $filePath'},
  '09-DONE': {'command': '/bin/echo Job done.'}},
 'id': '66842cc752b9aa7b628c67bb'}

In [14]: print(wf_def.get("description", "no description available"))
Workflow for XRF-Maps X-ray fluorescence microscopy data analysis package.
https://github.com/AdvancedPhotonSource/XRF-Maps
Keyword Arguments:
	filePath - Raw data file path.
	fit - <roi,roi_plus,nnls,tails,matrix> - Comma seperated list of fitting routines.
	dataDir (optional) - Directory containing raw data files.
	nthreads (optional) - Number of threads to use. default: all
	quantifyWith (optional) - File to use as quantification standard.
	detectors (optional) - Detectors to process. default: 0,1,2,3 for 4 detectors
	generateAvgH5 (optional) - Generate .h5 file which is the average of all detectors. default: False
	addV9Layout (optional) - Generate .h5 file which has v9 layout able to open in IDL MAPS software. default: False
	addExchange (optional) - Add exchange group into hdf5 file with normalized data. default: False
	exportCSV (optional) - Export Integrated spec, fitted, background to csv file. default: False
	updateTheta <theta_pv_string> (optional) - Update the theta dataset value using theta_pv_string as new pv string ref.
	updateAmps <us_amp>,<ds_amp> (optional) - Updates upstream and downstream amps if they changed inbetween scans.
	updateQuantAmps <us_amp>,<ds_amp> (optional) - Updates upstream and downstream amps for quantification if they changed inbetween scans.
	quickAndDirty (optional) - Integrate the detector range into 1 spectra. default: False
	optimizeFitOverrideParams (optional) - Integrate the 8 largest mda datasets and fit with multiple params. 1 = matrix batch fit, 2 = batch fit without tails, 3 = batch fit with tails, 4 = batch fit with free E & everything else fixed.
	optimizer <lmfit, mpfit> (optional) - Choose which optimizer to use for optimizeFitOverrideParams.

```