"""
Utility support to start bluesky sessions.

Also contains setup code that MUST run before other code in this directory.
"""

from ..utils.helper_functions import debug_python
from ..utils.helper_functions import mpl_setup

debug_python()
mpl_setup()
