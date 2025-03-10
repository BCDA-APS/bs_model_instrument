"""
Databroker catalog, provides ``cat``
====================================

.. autosummary::
    ~cat
"""

import logging

import databroker

from ..utils.config_loaders import iconfig

logger = logging.getLogger(__name__)
logger.bsdev(__file__)

TEMPORARY_CATALOG_NAME = "temp"

catalog_name = iconfig.get("DATABROKER_CATALOG", TEMPORARY_CATALOG_NAME)
if catalog_name == TEMPORARY_CATALOG_NAME:
    _cat = databroker.temp().v2
else:
    _cat = databroker.catalog[catalog_name].v2

cat = _cat
"""Databroker catalog object, receives new data from ``RE``."""

logger.info("Databroker catalog: %s", cat.name)
