.. _install:

Installation
============

It is easiest to start installation with a fresh ``conda`` environment. For
any packages that require installation of pre-compiled content (such as Qt,
PyQt, and others), install those packages with ``conda``.  For pure Python code,
use ``pip``.


.. code-block:: bash
    :linenos:

    export INSTALL_ENVIRONMENT_NAME=apsbits_env
    conda create -y -n "${INSTALL_ENVIRONMENT_NAME}" python pyepics
    conda activate "${INSTALL_ENVIRONMENT_NAME}"
    pip install apsbits

.. tip:: Replace the text ``INSTALL_ENVIRONMENT_NAME`` with the name you wish to use
    for this conda environment.

Install for development
-----------------------

For development and other activities, replace the ``pip`` command above with:

.. code-block:: bash
    :linenos:

    export INSTALL_ENVIRONMENT_NAME=apsbits_env
    git clone github.com:BCDA-APS/BITS.git
    cd BITS
    conda create -y -n "${INSTALL_ENVIRONMENT_NAME}" python pyepics
    conda activate "${INSTALL_ENVIRONMENT_NAME}"
    pip install -e ."[all]"


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
