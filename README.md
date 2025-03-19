# APSBITS: Template Package for Bluesky Instruments

| PyPI | Coverage |
| --- | --- |
[![PyPi](https://img.shields.io/pypi/v/apsbits.svg)](https://pypi.python.org/pypi/apsbits) | [![Coverage Status](https://coveralls.io/repos/github/BCDA-APS/BITS/badge.svg)](https://coveralls.io/github/BCDA-APS/BITS) |

BITS: **B**luesky **I**nstrument **T**emplate**S**

Template of a Bluesky Data Acquisition Instrument in console, notebook, &
queueserver.

## Create repository from this template.



https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template

Creating a repository from a template
On GitHub, navigate to the main page of the repository.

Above the file list, click Use this template.

Select Create a new repository.

![Screenshot of the "Use this template" button and the dropdown menu expanded to show the "Open in a codespace" option.
](docs/resources/use-this-template-button.webp)

Alternatively, you can open the template in a codespace and publish your work to a new repository later. For more information, see Creating a codespace from a template.

Use the Owner dropdown menu to select the account you want to own the repository.

Screenshot of the owner menu for a new GitHub repository. The menu shows two options, octocat and github.
Type a name for your repository, and an optional description.

![Image 2](docs/resources/create-repo-from-template.webp)


Screenshot of a the first step in creating a repository. The "Repository name" field contains the text "hello-world" and is outlined in orange.
Choose a repository visibility. For more information, see About repositories.

![Image 3](docs/resources/create-repository-owner.webp)

Optionally, to include the directory structure and files from all branches in the template, and not just the default branch, select Include all branches.

Optionally, if the personal account or organization in which you're creating uses any GitHub Apps from GitHub Marketplace, select any apps you'd like to use in the repository.

Click Create repository from template.

## Installing your own BITS instrument

```bash
export ENV_NAME=BITS_env

conda create -y -n $ENV_NAME python=3.11 pyepics
conda activate $ENV_NAME
pip install -e ."[all]"
```


## Edit your instrument



## IPython console Start

To start the bluesky instrument session in a ipython execute the next command in a terminal:

```bash
ipython
```

## Jupyter Notebook Start
Start JupyterLab, a Jupyter notebook server, or a notebook, VSCode.

## Starting the BITS Package

```py
from instrument.startup import *
RE(make_devices())  # create all the ophyd-style control devices
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

## Configuration files

The files that can be configured to adhere to your preferences are:

- `configs/iconfig.yml` - configuration for data collection
- `configs/logging.yml` - configuration for session logging to console and/or files
- `qserver/qs-config.yml`    - contains all configuration of the QS host process. See the [documentation](https://blueskyproject.io/bluesky-queueserver/manager_config.html) for more details of the configuration.

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

### Shell script explained

A [shell script](./qserver/qs_host.sh) is used to start the QS host process. Below
are all the command options, and what they do.

```bash
(bstest) $ ./qserver/qs_host.sh help
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

Once the documentation builds, view the HTML pages using your web browser:

```bash
BROWSER ./docs/build/html/index.html &
```

### Adding to the documentation source

The documentation source is located in files and directories under
`./docs/source`.  Various examples are provided.

Documentation can be added in these formats:
[`.rst`](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)
(reStructured text), [`.md`](https://en.wikipedia.org/wiki/Markdown) (markdown),
and [`.ipynb`](https://jupyter.org/) (Jupyter notebook). For more information,
see the [Sphinx](https://www.sphinx-doc.org/) documentation.

## Warnings

### Bluesky Queueserver

The QS host process writes files into the `qserver/` directory. This directory can be
relocated. However, it should not be moved into the instrument package since
that might be installed into a read-only directory.

## How-To Guides
### How to use the template

Consider renaming this `instrument` package to be more clear that is specific to *this*
instrument.  This will be the name by which it is `pip` installed and also used with
`import`.  Let's use an example instrument package name `my_instrument` below to show which parts are edited.

1) Click on use as template button
2) Adjust the following parameters in the following files:
    - `pyproject.toml`
        - `[project]` `name =` *example: `my_instrument`*
        - `[project.urls]`  *change URLs for your repo*
        - `[tool.setuptools]` `package-dir = {"instrument" = "src/instrument"}` *example: `{"my_instrument" = "src/instrument"}`*
    - `src/instrument/init.py`
        - `__package__ = "instrument"` *example: `"my_instrument"`*
    - `src/instrument/configs/iconfig.yml`
        - `DATABROKER_CATALOG:` *change from `temp` to your catalog's name*
        - `beamline_id:` *one word beamline name (such as known by APS scheduling system)*
        - `instrument_name:` *descriptive name of your beamline*
        - `DM_SETUP_FILE:` *Path to DM bash setup file, comment out if you do not have*
        - `BEC:` *adjust for your preferences*
    - `qserver/qs-config.yml`
        - `startup_module: instrument.startup` *example: `my_instrument.startup`*
    - `docs/source/conf.py`
        - `import instrument` *example `import my_instrument`*
        - `project = "instrument"` *example: `"my_instrument"`*
        - `version = instrument.__version__` *example: `my_instrument.__version__`*

- [APS Data Management Plans](./docs/source/guides/dm.md)
