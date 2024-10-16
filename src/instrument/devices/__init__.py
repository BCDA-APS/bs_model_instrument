"""Ophyd-style devices."""

from ophyd.sim import motor as sim_motor  # noqa: F401
from ophyd.sim import noisy_det as sim_det  # noqa: F401

from ..utils.aps_functions import host_on_aps_subnet

if host_on_aps_subnet():
    """
    below add any devices that will only load succesfully on the aps network
    """
    from .aps_source import aps  # noqa: F401

del host_on_aps_subnet
