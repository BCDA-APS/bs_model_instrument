.. _install:

Installation
============

It is easiest to start installation with a fresh ``conda`` environment. [#]_ For
any packages that require installation of pre-compiled content (such as Qt,
PyQt, and others), install those packages with ``conda``.  For pure Python code,
use ``pip`` [#]_ (which will be installed when the conda environment is
created).

The project comes pre-configured to install the content in the
``src/instrument`` directory as a package named ``instrument``.  This name can
be changed (by editing the ``name`` key in the ``pyproject.toml`` file) before
running the ``pip`` step. If the package is installed under a different name,
other code (such as ``qserver/qs_host.sh``) will need to be edited to find the new
package name.

.. note:: All of these commands start with the current working directory set
    to the base directory of this repository, the one with with
    ``pyproject.toml`` file and ``src`` directory.

.. [#] https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html
.. [#] https://python.land/virtual-environments/installing-packages-with-pip

Install for routine data acquisition
------------------------------------

These commands create a conda environment and then install all packages required
by this ``instrument`` package for routine data acquisition.

.. tip:: Replace the text ``model_instrument_env`` with the name you wish to use
    for this conda environment.

.. code-block:: bash
    :linenos:

    export INSTALL_ENVIRONMENT_NAME=model_instrument_env
    conda create -y -n "${INSTALL_ENVIRONMENT_NAME}" python pyqt=5 pyepics
    conda activate "${INSTALL_ENVIRONMENT_NAME}"
    pip install -e .

The ``pip install -e .`` command [#]_ means the code will be installed in
editable mode. You can continue to change the content in the ``src/instrument``
directory without need to reinstall after each change.

.. [#] https://stackoverflow.com/questions/42609943

Install for development
-----------------------

For development activities, replace the ``pip`` command above with:

.. code-block:: bash

    pip install -e .[dev]

Install everything
------------------

For development and other activities, replace the ``pip`` command above with:

.. code-block:: bash

    pip install -e .[all]

.. hint:: For `zsh` shell users,
.. code-block:: zsh

    pip install -e ."[all]"
