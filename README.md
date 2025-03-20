# APSBITS: Template Package for Bluesky Instruments

| PyPI | Coverage |
| --- | --- |
[![PyPi](https://img.shields.io/pypi/v/apsbits.svg)](https://pypi.python.org/pypi/apsbits) | [![Coverage Status](https://coveralls.io/repos/github/BCDA-APS/BITS/badge.svg?branch=main)](https://coveralls.io/github/BCDA-APS/BITS?branch=main) |

BITS: **B**luesky **I**nstrument **T**emplate **S**tructure

Template of a Bluesky Data Acquisition Instrument in console, notebook, &
queueserver.

## Installing the BITS Package for Development
```
git clone github.com:BCDA-APS/BITS.git
cd BITS
conda create -y -n BITS_env python=3.11 pyepics
conda activate BITS_env
pip install -e ."[all]"
```

## Creating a New Instrument
```bash
create-bits "YOUR_INSTRUMENT_NAME" "src/"
pip install -e ."[all]"
```

## IPython console Start

To start the bluesky instrument session in a ipython execute the next command in a terminal:

```bash
ipython
```

## Jupyter Notebook Start
Start JupyterLab, a Jupyter notebook server, or a notebook, VSCode.

## Starting the BITS Package

```py
from YOUR_INSTRUMENT_NAME.startup import *
```

For example, if you created an instrument named "test_instrument":
```
from test_instrument.startup import *
```

## Run Sim Plan Demo

To run some simulated plans that ensure the installation worked as expected
please run the next commands inside an ipython session or a jupyter notebook
after starting the data acquisition:

```py
RE(sim_print_plan())
RE(sim_count_plan())
RE(sim_rel_scan_plan())
```

See this [example](./docs/source/demo.ipynb).


## queueserver

The queueserver has a host process that manages a RunEngine. Client sessions
will interact with that host process.

### Run a queueserver host process

Use the queueserver host management script to start the QS host process.  The
`restart` option stops the server (if it is running) and then starts it.  This is
the usual way to (re)start the QS host process. Using `restart`, the process
runs in the background.

```bash
./qserver/qs_host.sh restart
```

### Run a queueserver client GUI

To run the gui client for the queueserver you can use the next command inside the terminal:

```bash
queue-monitor &
```

Alternatively, run the QS host's startup command directly within the `./qserver/`
subdirectory.

```bash
cd ./qserver
start-re-manager --config=./qs-config.yml
```

## Testing

Use this command to run the test suite locally:

```bash
pytest -vvv --lf ./src
```

## Documentation

<details>
<summary>prerequisite</summary>

To build the documentation locally, install [`pandoc`](https://pandoc.org/) in
your conda environment:

```bash
conda install conda-forge::pandoc
```

</details>

Use this command to build the documentation locally:

```bash
make -C docs clean html
```
