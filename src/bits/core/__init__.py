"""
Utility support to start bluesky sessions.

Also contains setup code that MUST run before other code in this directory.
"""

from ..utils.aps_functions import aps_dm_setup
from ..utils.config_loaders import iconfig
from ..utils.helper_functions import debug_python
from ..utils.helper_functions import mpl_setup

debug_python()
mpl_setup()
aps_dm_setup(iconfig.get("DM_SETUP_FILE"))
