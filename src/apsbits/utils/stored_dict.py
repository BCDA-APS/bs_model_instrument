"""
A dictionary that persists to disk.

This module provides a dictionary that automatically saves its contents to disk.
"""

import logging
import pathlib
import time
from typing import Any
from typing import Union

import yaml

logger = logging.getLogger(__name__)
logger.bsdev(__file__)


class StoredDict(dict):
    """
    A dictionary that persists to disk.

    This class provides a dictionary that automatically saves its contents to disk.
    It is designed to be used as a drop-in replacement for a regular dictionary.
    """

    def __init__(
        self,
        filename: Union[str, pathlib.Path],
        delay: float = 0.5,
        title: str = "metadata",
    ) -> None:
        """
        Initialize the StoredDict.

        Args:
            filename: Path to the file to store the dictionary in.
            delay: Delay in seconds before saving to disk.
            title: Title for the metadata section.
        """
        super().__init__()
        self._filename = pathlib.Path(filename)
        self._delay = delay
        self._title = title
        self._sync_key = f"sync_agent_{id(self):x}"
        self.sync_in_progress = False
        self._last_save = 0.0
        self._load()

    def _load(self) -> None:
        """Load the dictionary from disk."""
        if self._filename.exists():
            try:
                with open(self._filename) as f:
                    data = yaml.safe_load(f)
                    if data is not None:
                        self.update(data)
            except Exception as e:
                logger.error(f"Error loading {self._filename}: {e}")

    def _save(self) -> None:
        """Save the dictionary to disk."""
        try:
            with open(self._filename, "w") as f:
                yaml.dump(dict(self), f)
            self._last_save = time.time()
        except Exception as e:
            logger.error(f"Error saving {self._filename}: {e}")

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Set a key-value pair and schedule a save.

        Args:
            key: The key to set.
            value: The value to set.
        """
        super().__setitem__(key, value)
        self._schedule_save()

    def __delitem__(self, key: str) -> None:
        """
        Delete a key-value pair and schedule a save.

        Args:
            key: The key to delete.
        """
        super().__delitem__(key)
        self._schedule_save()

    def update(self, *args: Any, **kwargs: Any) -> None:
        """
        Update the dictionary and schedule a save.

        Args:
            *args: Positional arguments to update with.
            **kwargs: Keyword arguments to update with.
        """
        super().update(*args, **kwargs)
        self._schedule_save()

    def _schedule_save(self) -> None:
        """Schedule a save to disk."""
        if time.time() - self._last_save >= self._delay:
            self._save()

    def sync(self) -> None:
        """Force a save to disk."""
        self._save()

    def __enter__(self) -> "StoredDict":
        """Enter the context manager."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit the context manager and save."""
        self.sync()
