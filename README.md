# BITS: Template Package for Bluesky Instruments

BITS: **B**luesky **I**nstrument **T**emplate **S**tructure

Template for creating a Bluesky Data Acquisition Instrument to be used through a console, notebook, &
queueserver UI.

## Create repository from this template.

Creating a repository from a template
On GitHub, navigate to the main page of the repository.

Above the file list, click **Use this template**.

Afterwards select **Create a new repository**.

![Screenshot of the "Use this template" button and the dropdown menu expanded to show the "Open in a codespace" option.
](docs/resources/use-this-template-button.webp)

Alternatively, you can open the template in a codespace and publish your work to a new repository later. For more information, see [Creating a codespace from a template](https://docs.github.com/en/codespaces/developing-in-a-codespace/creating-a-codespace-from-a-template).

Use the Owner dropdown menu to select the account you want to own the repository.

![Screenshot of the owner menu for a new GitHub repository. The menu shows two options, octocat and github.](docs/resources/create-repository-owner.webp)
\
\
\
Type a name for your repository, and an optional description.

Click Create repository from template.

## Installing your own BITS instrument

```bash
export ENV_NAME=BITS_env

conda create -y -n $ENV_NAME python=3.11 pyepics
conda activate $ENV_NAME
pip install -e ."[all]"
```


## Create a new instrument
To create a new instrument run the following script specifying the name of your new bluesky instrument
```bash
python3 -m bits.utils.create_new_instrument "{instrument_name}" "src/"
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

Alternatively, run the QS host's startup command directly within the `./qserver/`
subdirectory.

```bash
cd ./qserver
start-re-manager --config=./qs-config.yml
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
