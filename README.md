# APSBITS: Template Package for Bluesky Instruments

| PyPI | Coverage |
| --- | --- |
[![PyPi](https://img.shields.io/pypi/v/apsbits.svg)](https://pypi.python.org/pypi/apsbits) | [![Coverage Status](https://coveralls.io/repos/github/BCDA-APS/BITS/badge.svg?branch=main)](https://coveralls.io/github/BCDA-APS/BITS?branch=main) |

BITS: **B**luesky **I**nstrument **T**emplate **S**tructure

Template of a Bluesky Data Acquisition Instrument in console, notebook, &
queueserver.

## Production use of BITS

Please create a bits instrument using our template repository: https://github.com/BCDA-APS/DEMO-BITS


## Installing the BITS Package for Development

```bash
git clone github.com:BCDA-APS/BITS.git
cd BITS
conda create -y -n BITS_env python=3.11 pyepics
conda activate BITS_env
pip install -e ."[all]"
```

## Testing the apsbits base installation

On an ipython console

```py
from apsbits.demo_instrument.startup import *
listobjects()
RE(sim_print_plan())
RE(sim_count_plan())
RE(sim_rel_scan_plan())
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
