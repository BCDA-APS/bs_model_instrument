.. _install:

Installation
============

It is easiest to start installation with a fresh ``conda`` environment. [#]_ For
any packages that require installation of pre-compiled content (such as Qt,
PyQt, and others), install those packages with ``conda``.  For pure Python code,
use ``pip`` [#]_ (which will be installed when the conda environment is
created).


Install for routine data acquisition
------------------------------------

You are welcome to set up your data acquisition repository as you see fit, however we reccomend using the Instrument Repository Template.
These commands create a conda environment and then install all packages required
by this ``instrument`` package for routine data acquisition.

.. tip:: Replace the text ``model_instrument_env`` with the name you wish to use
    for this conda environment.

.. code-block:: bash
    :linenos:

    export INSTALL_ENVIRONMENT_NAME=apsbits
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
