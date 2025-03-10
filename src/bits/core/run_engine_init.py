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
from ..utils.stored_dict import StoredDict
from .best_effort_init import bec
from .catalog_init import cat

logger = logging.getLogger(__name__)
logger.bsdev(__file__)

re_config = iconfig.get("RUN_ENGINE", {})

RE = bluesky.RunEngine()
"""The bluesky RunEngine object."""

# Save/restore RE.md dictionary, in this precise order.
if MD_PATH is not None:
    handler_name = re_config.get("MD_STORAGE_HANDLER", "StoredDict")
    logger.debug(
        "Select %r to store 'RE.md' dictionary in %s.",
        handler_name,
        MD_PATH,
    )
    try:
        if handler_name == "PersistentDict":
            RE.md = bluesky.utils.PersistentDict(MD_PATH)
        else:
            RE.md = StoredDict(MD_PATH)
    except Exception as error:
        print(
            "\n"
            f"Could not create {handler_name} for RE metadata. Continuing"
            f" without saving metadata to disk. {error=}\n"
        )
        logger.warning("%s('%s') error:%s", handler_name, MD_PATH, error)

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
