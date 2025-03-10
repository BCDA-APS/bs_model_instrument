"""
RunEngine Metadata
==================

.. autosummary::
    ~MD_PATH
    ~get_md_path
    ~re_metadata
"""

import getpass
import logging
import os
import pathlib
import socket
import sys

import apstools
import bluesky
import databroker
import epics
import h5py
import intake
import matplotlib
import numpy
import ophyd
import pyRestTable
import pysumreg
import spec2nexus

from .config_loaders import iconfig

logger = logging.getLogger(__name__)
logger.bsdev(__file__)

re_config = iconfig.get("RUN_ENGINE", {})

DEFAULT_MD_PATH = pathlib.Path.home() / ".config" / "Bluesky_RunEngine_md"
HOSTNAME = socket.gethostname() or "localhost"
USERNAME = getpass.getuser() or "Bluesky user"
VERSIONS = dict(
    apstools=apstools.__version__,
    bluesky=bluesky.__version__,
    databroker=databroker.__version__,
    epics=epics.__version__,
    h5py=h5py.__version__,
    intake=intake.__version__,
    matplotlib=matplotlib.__version__,
    numpy=numpy.__version__,
    ophyd=ophyd.__version__,
    pyRestTable=pyRestTable.__version__,
    python=sys.version.split(" ")[0],
    pysumreg=pysumreg.__version__,
    spec2nexus=spec2nexus.__version__,
)
RE_CONFIG = iconfig.get("RUN_ENGINE", {})


def get_md_path():
    """
    Get path for RE metadata.

    ==============  ==============================================
    support         path
    ==============  ==============================================
    PersistentDict  Directory where dictionary keys are stored in separate files.
    StoredDict      File where dictionary is stored as YAML.
    ==============  ==============================================

    In either case, the 'path' can be relative or absolute.  Relative
    paths are with respect to the present working directory when the
    bluesky session is started.
    """
    md_path_name = RE_CONFIG.get("MD_PATH", DEFAULT_MD_PATH)
    path = pathlib.Path(md_path_name)
    logger.info("RunEngine metadata saved in directory: %s", str(path))
    return str(path)


def re_metadata(cat=None):
    """Programmatic metadata for the RunEngine."""
    md = {
        "login_id": f"{USERNAME}@{HOSTNAME}",
        "versions": VERSIONS,
        "pid": os.getpid(),
        "iconfig": iconfig,
    }
    if cat is not None:
        md["databroker_catalog"] = cat.name
    md.update(RE_CONFIG.get("DEFAULT_METADATA", {}))

    conda_prefix = os.environ.get("CONDA_PREFIX")
    if conda_prefix is not None:
        md["conda_prefix"] = conda_prefix
    return md


MD_PATH = get_md_path()
"""Storage path to save RE metadata between sessions."""
