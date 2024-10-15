"""Ophyd-style devices."""

from ..utils.aps_functions import host_on_aps_subnet

if host_on_aps_subnet():
    from .aps_source import aps  # noqa: F401

del host_on_aps_subnet
