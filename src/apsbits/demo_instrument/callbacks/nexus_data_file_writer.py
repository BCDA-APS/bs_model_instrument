"""
Nexus data file writer callback.

This module provides callbacks for writing data to Nexus data files.
"""

import logging
from typing import Any
from typing import Dict

from apsbits.utils.config_loaders import get_config

logger = logging.getLogger(__name__)
logger.bsdev(__file__)

# Get the configuration
iconfig = get_config()


class NexusWriter:
    """Writer for Nexus data files."""

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """
        Initialize the Nexus writer.

        Args:
            **kwargs: Additional configuration options.
        """
        self.file_extension = kwargs.pop("file_extension", "nxs")
        self.warn_missing = kwargs.pop("warn_missing", False)
        self.iconfig = kwargs.pop("iconfig", None)

    def __call__(self, name: str, doc: Dict[str, Any]) -> None:
        """
        Process a document from the Bluesky RunEngine.

        Args:
            name: The name of the document.
            doc: The document content.
        """
        if name == "start":
            logger.info("Starting new Nexus data file")
        elif name == "stop":
            logger.info("Stopping Nexus data file")


# Create a nexus writer instance
nxwriter = None
if iconfig.get("NEXUS_DATA_FILES", {}).get("ENABLE", False):
    nxwriter = NexusWriter(
        file_extension=iconfig.get("NEXUS_DATA_FILES", {}).get("FILE_EXTENSION", "nxs"),
        warn_missing=iconfig.get("NEXUS_DATA_FILES", {}).get("WARN_MISSING", False),
    )
