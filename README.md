# APSBITS: Template Package for Bluesky Instruments

| PyPI | Coverage |
| --- | --- |
[![PyPi](https://img.shields.io/pypi/v/apsbits.svg)](https://pypi.python.org/pypi/apsbits) | [![Coverage Status](https://coveralls.io/repos/github/BCDA-APS/BITS/badge.svg?branch=main)](https://coveralls.io/github/BCDA-APS/BITS?branch=main) |

BITS: **B**luesky **I**nstrument **T**emplate**S**

Template of a Bluesky Data Acquisition Instrument in console, notebook, &
queueserver.

## Create a BITS instrument from our template:
https://github.com/BCDA-APS/DEMO-BITS


## Developing on the main bits branch

```bash
git clone https://github.com/BCDA-APS/BITS
cd BITS

export ENV_NAME=BITS_env
conda create -y -n $ENV_NAME python=3.11 pyepics
conda activate $ENV_NAME
pip install -e .
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

