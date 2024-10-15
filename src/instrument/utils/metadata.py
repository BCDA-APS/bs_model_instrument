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


def get_md_path():
    """Get PersistentDict directory for RE metadata."""
    path = iconfig.get("MD_PATH")
    if path is None:
        path = DEFAULT_MD_PATH
    else:
        path = pathlib.Path(path)
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
    md.update(iconfig.get("RUNENGINE_METADATA", {}))

    conda_prefix = os.environ.get("CONDA_PREFIX")
    if conda_prefix is not None:
        md["conda_prefix"] = conda_prefix
    return md


MD_PATH = get_md_path()
""" PersistentDict Directory to save RE metadata between sessions."""
