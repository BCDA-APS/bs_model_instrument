"""
Generic utility helper functions
================================

.. autosummary::
    ~register_bluesky_magics
    ~running_in_queueserver
    ~debug_python
    ~mpl_setup
    ~is_notebook
"""

import logging

import matplotlib as mpl
import matplotlib.pyplot as plt
from bluesky.magics import BlueskyMagics
from bluesky_queueserver import is_re_worker_active
from IPython import get_ipython

from apsbits.utils.config_loaders import iconfig

logger = logging.getLogger(__name__)
logger.bsdev(__file__)


def register_bluesky_magics() -> None:
    """
    Register Bluesky magics if an IPython environment is detected.

    This function registers the BlueskyMagics if get_ipython() returns a valid IPython
      instance.
    """
    ipython = get_ipython()
    if ipython is not None:
        ipython.register_magics(BlueskyMagics)


def running_in_queueserver() -> bool:
    """
    Detect if running in the bluesky queueserver.

    Returns:
        bool: True if running in the queueserver, False otherwise.
    """
    try:
        active: bool = is_re_worker_active()
        return active
    except Exception as cause:
        print(f"{cause=}")
        return False


def debug_python() -> None:
    """
    Enable detailed debugging for Python exceptions in the IPython environment.

    This function adjusts the xmode settings for exception tracebacks based on the
      configuration.
    """
    ipython = get_ipython()
    if ipython is not None:
        xmode_level: str = iconfig.get("XMODE_DEBUG_LEVEL", "Minimal")
        ipython.run_line_magic("xmode", xmode_level)
        print("\nEnd of IPython settings\n")
        logger.bsdev("xmode exception level: '%s'", xmode_level)


def is_notebook() -> bool:
    """
    Detect if the current environment is a Jupyter Notebook.

    Returns:
        bool: True if running in a notebook (Jupyter notebook or qtconsole),
        False otherwise.
    """
    try:
        shell: str = get_ipython().__class__.__name__
        if shell == "ZMQInteractiveShell":
            return True  # Jupyter notebook or qtconsole
        elif shell == "TerminalInteractiveShell":
            return False  # Terminal running IPython
        else:
            return False  # Other type
    except NameError:
        return False  # Standard Python interpreter


def mpl_setup() -> None:
    """
    Configure the Matplotlib backend based on the current environment.

    For non-queueserver and non-notebook environments, attempts to use the 'qtAgg'
      backend.
    If 'qtAgg' is not available due to missing dependencies, falls back to the 'Agg'
      backend.

    Returns:
        None
    """
    if not running_in_queueserver():
        if not is_notebook():
            try:
                mpl.use("qtAgg")
                plt.ion()
                logger.bsdev("Using qtAgg backend for matplotlib.")
            except Exception as exc:
                logger.error(
                    "qtAgg backend is not available, falling back to Agg backend. \
                    Error: %s",
                    exc,
                )
                mpl.use("Agg")
