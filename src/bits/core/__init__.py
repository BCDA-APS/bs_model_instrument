"""
Utility support to start bluesky sessions.

Also contains setup code that MUST run before other code in this directory.
"""

from bits.utils.aps_functions import aps_dm_setup
from bits.utils.config_loaders import iconfig
from bits.utils.helper_functions import debug_python
from bits.utils.helper_functions import mpl_setup

debug_python()
mpl_setup()
aps_dm_setup(iconfig.get("DM_SETUP_FILE"))
