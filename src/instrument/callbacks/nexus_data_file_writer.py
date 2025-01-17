"""

NeXus Writer
============

Write scan(s) to a NeXus/HDF5 file.

.. autosummary::
    :nosignatures:

    ~MyNXWriter
    ~nxwriter
"""

import logging

from ..core.run_engine_init import RE
from ..utils.aps_functions import host_on_aps_subnet
from ..utils.config_loaders import iconfig

logger = logging.getLogger(__name__)
logger.bsdev(__file__)


if host_on_aps_subnet():
    from apstools.callbacks import NXWriterAPS as NXWriter
else:
    from apstools.callbacks import NXWriter


class MyNXWriter(NXWriter):
    """Patch to get sample title from metadata, if available."""

    def get_sample_title(self):
        """
        Get the title from the metadata or modify the default.

        default title: S{scan_id}-{plan_name}-{short_uid}
        """
        try:
            title = self.metadata["title"]
        except KeyError:
            # title = super().get_sample_title()  # the default title
            title = f"S{self.scan_id:05d}-{self.plan_name}-{self.uid[:7]}"
        return title


nxwriter = MyNXWriter()  # create the callback instance
"""The NeXus file writer object."""

if "NEXUS_DATA_FILES" in iconfig:
    RE.subscribe(nxwriter.receiver)  # write data to NeXus files

nxwriter.file_extension = iconfig.get("FILE_EXTENSION", "hdf")
warn_missing = iconfig.get("WARN_MISSING", False)
nxwriter.warn_on_missing_content = warn_missing
