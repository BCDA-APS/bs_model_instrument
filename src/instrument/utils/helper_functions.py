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

from .config_loaders import iconfig

logger = logging.getLogger(__name__)
logger.bsdev(__file__)


def register_bluesky_magics():
    """The Bluesky Magick functions are useful with command-lines."""
    _ipython = get_ipython()
    if _ipython is not None:
        _ipython.register_magics(BlueskyMagics)


def running_in_queueserver():
    """Detect if running in the bluesky queueserver."""
    try:
        active = is_re_worker_active()
        # print(f"{active=!r}")
        return active
    except Exception as cause:
        print(f"{cause=}")
        return False


def debug_python():
    """"""
    # terse error dumps (Exception tracebacks)
    _ip = get_ipython()
    if _ip is not None:
        _xmode_level = iconfig.get("XMODE_DEBUG_LEVEL", "Minimal")
        _ip.run_line_magic("xmode", _xmode_level)
        print("\nEnd of IPython settings\n")
        logger.bsdev("xmode exception level: '%s'", _xmode_level)


def is_notebook():
    """
    Detect if running in a notebook.

    see: https://stackoverflow.com/a/39662359/1046449
    """
    try:
        shell = get_ipython().__class__.__name__
        if shell == "ZMQInteractiveShell":
            return True  # Jupyter notebook or qtconsole
        elif shell == "TerminalInteractiveShell":
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)

    except NameError:
        return False  # Probably standard Python interpreter


def mpl_setup():
    """
    Matplotlib setup based on environment (Notebook or non-Notebook).
    """
    if not running_in_queueserver():
        if not is_notebook():
            mpl.use("qtAgg")  # Set the backend early
            plt.ion()
