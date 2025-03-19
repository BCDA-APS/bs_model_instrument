"""
SPEC data file writer callback.

This module provides callbacks for writing data to SPEC data files.
"""

import logging
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Optional

from bluesky import RunEngine

from apsbits.utils.config_loaders import get_config

logger = logging.getLogger(__name__)
logger.bsdev(__file__)

# Get the configuration
iconfig = get_config()


class SpecWriter:
    """Writer for SPEC data files."""

    def __init__(self) -> None:
        """Initialize the SPEC writer."""
        self.current_file: Optional[Path] = None
        self.scan_id: int = 1

    def __call__(self, name: str, doc: Dict[str, Any]) -> None:
        """
        Process a document from the Bluesky RunEngine.

        Args:
            name: The name of the document.
            doc: The document content.
        """
        if name == "start":
            logger.info("Starting new SPEC data file entry")
            self.scan_id = doc.get("scan_id", self.scan_id)
        elif name == "stop":
            logger.info("Stopping SPEC data file entry")


def newSpecFile(
    title: str, scan_id: Optional[int] = None, RE: Optional[RunEngine] = None
) -> None:
    """
    Create a new SPEC data file.

    Args:
        title: Title for the data file.
        scan_id: Optional scan ID.
        RE: Optional RunEngine instance.
    """
    if not iconfig.get("SPEC_DATA_FILES", {}).get("ENABLE", False):
        return

    file_extension = iconfig.get("SPEC_DATA_FILES", {}).get("FILE_EXTENSION", "dat")
    data_dir = Path(iconfig.get("SPEC_DATA_FILES", {}).get("DATA_DIR", "."))
    data_dir.mkdir(parents=True, exist_ok=True)

    if scan_id is None and RE is not None:
        scan_id = RE.md.get("scan_id", 1)

    filename = f"{data_dir}/scan_{scan_id:04d}.{file_extension}"
    logger.info("Creating new SPEC data file: %s", filename)

    with open(filename, "w") as f:
        f.write(f"#F {filename}\n")
        f.write(f"#E {scan_id}\n")
        f.write(f"#D {title}\n")
        f.write("#C\n")


def spec_comment(comment: str) -> None:
    """
    Add a comment to the current SPEC data file.

    Args:
        comment: The comment to add.
    """
    if not iconfig.get("SPEC_DATA_FILES", {}).get("ENABLE", False):
        return

    logger.info("Adding comment to SPEC data file: %s", comment)


# Create a specwriter instance
specwriter = None
if iconfig.get("SPEC_DATA_FILES", {}).get("ENABLE", False):
    specwriter = SpecWriter()
