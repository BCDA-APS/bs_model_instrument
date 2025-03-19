"""
Start Bluesky Data Acquisition sessions of all kinds.

Includes:

* Python script
* IPython console
* Jupyter notebook
* Bluesky queueserver
"""

import logging
from apsbits.demo_instrument import iconfig

from apsbits.core.best_effort_init import bec  # noqa: F401
from apsbits.core.best_effort_init import peaks  # noqa: F401
from apsbits.core.catalog_init import cat  # noqa: F401
from apsbits.core.run_engine_init import RE  # noqa: F401
from apsbits.core.run_engine_init import sd  # noqa: F401
from apsbits.utils.aps_functions import aps_dm_setup

# Bluesky data acquisition setup
from apsbits.utils.helper_functions import register_bluesky_magics
from apsbits.utils.helper_functions import running_in_queueserver
from apsbits.utils.make_devices_yaml import make_devices  # noqa: F401

# User specific imports
from .plans import *  # noqa: F403

logger = logging.getLogger(__name__)
logger.bsdev(__file__)

aps_dm_setup(iconfig.get("DM_SETUP_FILE"))

if iconfig.get("USE_BLUESKY_MAGICS", False):
    register_bluesky_magics()

# Configure the session with callbacks, devices, and plans.
if iconfig.get("NEXUS_DATA_FILES", {}).get("ENABLE", False):
    from .callbacks.nexus_data_file_writer import nxwriter  # noqa: F401

if iconfig.get("SPEC_DATA_FILES", {}).get("ENABLE", False):
    from .callbacks.spec_data_file_writer import newSpecFile  # noqa: F401
    from .callbacks.spec_data_file_writer import spec_comment  # noqa: F401
    from .callbacks.spec_data_file_writer import specwriter  # noqa: F401

# These imports must come after the above setup.
if running_in_queueserver():
    ### To make all the standard plans available in QS, import by '*', otherwise import
    ### plan by plan.
    from apstools.plans import lineup2  # noqa: F401
    from bluesky.plans import *  # noqa: F403

else:
    # Import bluesky plans and stubs with prefixes set by common conventions.
    # The apstools plans and utils are imported by '*'.
    from apstools.plans import *  # noqa: F403
    from apstools.utils import *  # noqa: F403
    from bluesky import plan_stubs as bps  # noqa: F401
    from bluesky import plans as bp  # noqa: F401

    from apsbits.utils.controls_setup import oregistry  # noqa: F401
