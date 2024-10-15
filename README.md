# model_instrument

Model of a Bluesky Data Acquisition Instrument in console, notebook, & queueserver.

## Demo

```py
from instrument.startup import *
from instrument.tests.sim_plans import *

RE(sim_print_plan())
RE(sim_count_plan())
RE(sim_rel_scan_plan())
```

## Installation

Set up the development environment.

```bash
conda create -y -n model_instrument python=3.11 pyepics
conda activate model_instrument
pip install -e ."[all]"
```

## IPython console

```bash
ipython
```

```py
from instrument.startup import *
```

## Jupyter notebook

Start JupyterLab, a Jupyter notebook server, or a notebook, VSCode.

Start the data acquisition:

```py
from instrument.startup import *
```

See this [example](./docs/source/demo.ipynb).

## Configuration files

- `configs/iconfig.yml` - configuration for data collection
- `configs/logging.yml` - configuration for session logging to console and/or files

## queueserver

The queueserver has a host process that manages a RunEngine. Client sessions
will interact with that host process.  See [qs/README](./qs/README.md) for more
details.

### Run a queueserver host process

Use the queueserver host management script.  This option stops the server (if it
is running) and then starts it.  This is the usual way to (re)start the QS host
process.

```bash
./qs/qs_host.sh restart
```

### Run a queueserver client GUI

At this time, there is one GUI recommended for use with the bluesky queueserver.
Other GUI clients are in development and show promise of improvements.  For now,
use this one.

```bash
queue-monitor &
```

## Support for the Bluesky Queueserver.

File [`qs-config.yml`](../qs/qs-config.yml) contains all configuration of the QS
host process. See the
[documentation](https://blueskyproject.io/bluesky-queueserver/manager_config.html)
for more details of the configuration.

The QS host process writes files into this directory. This directory can be
relocated. However, it should not be moved into the instrument package since
that might be installed into a read-only directory.

### shell script

A [shell script](./qs_host.sh) is used to start the QS host process. Typically,
it is run in the background: `./qs/qs_host.sh restart`.  This command looks for
a running QS host process.  If found, that process is stopped.  Then, a new QS
host process is started in a
[screen](https://www.gnu.org/software/screen/manual/screen.html) session.

```bash
(bstest) $ ./qs/qs_host.sh help
Usage: qs_host.sh {start|stop|restart|status|checkup|console|run} [NAME]

    COMMANDS
        console   attach to process console if process is running in screen
        checkup   check that process is running, restart if not
        restart   restart process
        run       run process in console (not screen)
        start     start process
        status    report if process is running
        stop      stop process

    OPTIONAL TERMS
        NAME      name of process (default: bluesky_queueserver-)
```

Alternatively, run the QS host's startup comand directly within the `qs/`
subdirectory.

```bash
cd ./qs
start-re-manager --config=./qs-config.yml
```

## Testing

Use this command to run the test suite locally:

`pytest -vvv --lf ./src`
