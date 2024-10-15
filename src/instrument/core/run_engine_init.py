"""
Setup the Bluesky RunEngine, provides ``RE`` and ``sd``.
========================================================

.. autosummary::
    ~RE
    ~sd
"""

import logging

import bluesky
from bluesky.utils import ProgressBarManager

from ..utils.config_loaders import iconfig
from ..utils.controls_setup import connect_scan_id_pv
from ..utils.controls_setup import set_control_layer
from ..utils.controls_setup import set_timeouts
from ..utils.metadata import MD_PATH
from ..utils.metadata import re_metadata
from .best_effort_init import bec
from .catalog_init import cat

logger = logging.getLogger(__name__)
logger.bsdev(__file__)

re_config = iconfig.get("RUN_ENGINE", {})

RE = bluesky.RunEngine()
"""The bluesky RunEngine object."""

# Save/restore RE.md dictionary, in this precise order.
if MD_PATH is not None:
    RE.md = bluesky.utils.PersistentDict(MD_PATH)
RE.md.update(re_metadata(cat))  # programmatic metadata
RE.md.update(re_config.get("DEFAULT_METADATA", {}))

sd = bluesky.SupplementalData()
"""Baselines & monitors for ``RE``."""

RE.subscribe(cat.v1.insert)
RE.subscribe(bec)
RE.preprocessors.append(sd)

set_control_layer()
set_timeouts()  # MUST happen before ANY EpicsSignalBase (or subclass) is created.

connect_scan_id_pv(RE)  # if configured

if re_config.get("USE_PROGRESS_BAR", True):
    # Add a progress bar.
    pbar_manager = ProgressBarManager()
    RE.waiting_hook = pbar_manager
