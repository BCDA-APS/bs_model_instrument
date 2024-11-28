"""
Storage-backed Dictionary
=========================

A dictionary that writes its contents to YAML file.

Replaces ``bluesky.utils.PersistentDict``.

* Contents must be JSON serializable.
* Contents stored in a single human-readable YAML file.
* Sync to disk shortly after dictionary is updated.

.. autosummary::

    ~StoredDict
"""

__all__ = ["StoredDict"]

import collections.abc
import datetime
import json
import logging
import pathlib
import threading
import time

import yaml

logger = logging.getLogger(__name__)
logger.bsdev(__file__)


# (Internal) Dictionary of active ``StoredDict`` ``sync_agent`` threads.
#
# A single entry for each instance of ``StoredDict``.
# - Key is the ``id`` of an instance of ``StoredDict``.
# - Value is the ``threading`` object (if running) or ``None``.
# Keeping the ``threading`` object **outside** the ``StoredDict`` class
# avoids an error from ``copy.deepcopy(md)`` that happens during Bluesky runs::
#
#     TypeError: cannot pickle '_thread.lock' object
_sync_threads = {}


class StoredDict(collections.abc.MutableMapping):
    """
    Dictionary that syncs to storage.

    .. autosummary::

        ~flush
        ~popitem
        ~reload

    .. rubric:: Static methods

    All support for the YAML format is implemented in the static methods.

    .. autosummary::

        ~dump
        ~load

    ----
    """

    def __init__(self, file, delay=5, title=None, serializable=True):
        """
        StoredDict : Dictionary that syncs to storage

        PARAMETERS

        file : str or pathlib.Path
            Name of file to store dictionary contents.
        delay : number
            Time delay (s) since last dictionary update to write to storage.
            Default: 5 seconds.
        title : str or None
            Comment to write at top of file.
            Default: "Written by StoredDict."
        serializable : bool
            If True, validate new dictionary entries are JSON serializable.
        """
        self._file = pathlib.Path(file)
        self._delay = max(0, delay)
        self._title = title or f"Written by {self.__class__.__name__}."
        self.test_serializable = serializable

        self._sync_key = id(self)
        self._sync_deadline = time.time()
        self._sync_while_loop_period = 0.005
        self._sync_thread_abort = False
        # Need to keep the thread objects outside of the class.
        _sync_threads[self._sync_key] = None

        self._cache = {}
        self.reload()

    def __delitem__(self, key):
        """Delete dictionary value by key."""
        del self._cache[key]

    def __getitem__(self, key):
        """Get dictionary value by key."""
        return self._cache[key]

    def __iter__(self):
        """Iterate over the dictionary keys."""
        yield from self._cache

    def __len__(self):
        """Number of keys in the dictionary."""
        return len(self._cache)

    def __repr__(self):
        """representation of this object."""
        return f"<{self.__class__.__name__} {dict(self)!r}>"

    def __setitem__(self, key, value):
        """Write to the dictionary."""
        if self.test_serializable:
            json.dumps({key: value})
        self._cache[key] = value

        # Reset the deadline.
        self._sync_deadline = time.time() + self._delay
        logger.debug("new sync deadline in %f s.", self._delay)
        if _sync_threads[self._sync_key] is None:
            self._delayed_sync_to_storage()

    def _delayed_sync_to_storage(self):
        """
        Sync the metadata to storage.

        Start a time-delay thread.  New writes to the metadata dictionary will
        extend the deadline.  Sync once the deadline is reached.
        """

        def sync_agent():
            """Threaded task."""
            logger.debug("Starting sync_agent...")
            while time.time() < self._sync_deadline and not self._sync_thread_abort:
                time.sleep(self._sync_while_loop_period)
            logger.debug("Sync waiting period ended")

            StoredDict.dump(self._file, self._cache, title=self._title)

            _sync_threads[self._sync_key] = None
            self._sync_thread_abort = False

        _sync_threads[self._sync_key] = threading.Thread(target=sync_agent)
        _sync_threads[self._sync_key].start()

    def flush(self):
        """Force a write of the dictionary to disk"""
        logger.debug("flush()")
        if _sync_threads[self._sync_key] is None:
            StoredDict.dump(self._file, self._cache, title=self._title)
            # TODO: stop the thread
        else:
            self._sync_thread_abort = True

    def popitem(self):
        """
        Remove and return a (key, value) pair as a 2-tuple.

        Pairs are returned in LIFO (last-in, first-out) order.
        Raises KeyError if the dict is empty.
        """
        return self._cache.popitem()

    def reload(self):
        """Read dictionary from storage."""
        logger.debug("reload()")
        self._cache = StoredDict.load(self._file)

    @staticmethod
    def dump(file, contents, title=None):
        """Write dictionary to YAML file."""
        logger.debug("_dump(): file='%s', contents=%r, title=%r", file, contents, title)
        with open(file, "w") as f:
            if isinstance(title, str) and len(title) > 0:
                f.write(f"# {title}\n")
            f.write(f"# Dictionary contents written: {datetime.datetime.now()}\n\n")
            f.write(yaml.dump(contents, indent=2))

    @staticmethod
    def load(file):
        """Read dictionary from YAML file."""
        from .config_loaders import load_config_yaml

        file = pathlib.Path(file)
        logger.debug("_load('%s')", file)
        md = None
        if file.exists():
            md = load_config_yaml(file)
        return md or {}  # In case file is empty.
