# -*- coding: iso-8859-1 -*-

"""Model Bluesky Data Acquisition Instrument."""

from .utils.logging_setup import configure_logging

configure_logging()

__package__ = "instrument"
try:
    from setuptools_scm import get_version

    __version__ = get_version(root="..", relative_to=__file__)
    del get_version
except (LookupError, ModuleNotFoundError):
    from importlib.metadata import version

    __version__ = version(__package__)
