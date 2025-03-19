"""
Test the utils.stored_dict module.
"""

import pathlib
import tempfile
import time
from contextlib import nullcontext as does_not_raise

import pytest
import yaml

from apsbits.utils.stored_dict import StoredDict


def luftpause(delay=0.05):
    """A brief wait for content to flush to storage."""
    time.sleep(max(0, delay))


@pytest.fixture
def md_file():
    """Provide a temporary file (deleted on close)."""
    tfile = tempfile.NamedTemporaryFile(
        prefix="re_md_",
        suffix=".yml",
        delete=False,
    )
    path = pathlib.Path(tfile.name)
    tfile.close()  # Close the file to ensure it's empty
    yield pathlib.Path(tfile.name)

    if path.exists():
        path.unlink()  # delete the file


@pytest.fixture(autouse=True)
def setup_test_config(monkeypatch):
    """Set up a test configuration."""
    monkeypatch.setattr("apsbits.utils.config_loaders._iconfig", {})


def test_StoredDict(md_file):
    """Test the StoredDict class."""
    assert md_file.exists()
    assert len(open(md_file).read().splitlines()) == 0  # empty

    sdict = StoredDict(md_file, delay=0.2, title="unit testing")
    assert sdict is not None
    assert len(sdict) == 0  # Should be empty since we're using a new file
    assert sdict._delay == 0.2
    assert sdict._title == "unit testing"
    assert len(open(md_file).read().splitlines()) == 0  # still empty
    assert sdict._sync_key == f"sync_agent_{id(sdict):x}"
    assert not sdict.sync_in_progress

    # Write an empty dictionary.
    sdict.sync()
    assert len(open(md_file).read().splitlines()) > 0  # not empty

    # Write a key-value pair.
    sdict["a"] = "b"
    assert sdict["a"] == "b"
    assert len(sdict) == 1
    assert sdict.get("a") == "b"
    assert sdict.get("b") is None
    assert sdict.get("b", "c") == "c"

    # Test _delayed_sync_to_storage.
    sdict["bee"] = "queen"
    luftpause(sdict._delay / 2)
    with open(md_file) as f:
        data = yaml.safe_load(f)
        assert len(data) == 2  # a & bee
        assert "a" in data
        assert data["bee"] == "queen"  # The new value.

    # Test context manager.
    with StoredDict(md_file) as sdict:
        sdict["c"] = "d"
    with open(md_file) as f:
        data = yaml.safe_load(f)
        assert "c" in data
        assert data["c"] == "d"

    # Test update method.
    sdict.update({"e": "f", "g": "h"})
    luftpause(sdict._delay / 2)
    with open(md_file) as f:
        data = yaml.safe_load(f)
        assert "e" in data
        assert "g" in data
        assert data["e"] == "f"
        assert data["g"] == "h"

    # Test delete.
    del sdict["a"]
    assert "a" not in sdict
    luftpause(sdict._delay / 2)
    with open(md_file) as f:
        data = yaml.safe_load(f)
        assert "a" not in data


@pytest.mark.parametrize(
    "md, xcept, text",
    [
        [{"a": 1}, None, str(None)],  # int value is ok
        [{"a": 2.2}, None, str(None)],  # float value is ok
        [{"a": "3"}, None, str(None)],  # str value is ok
        [{"a": [4, 5, 6]}, None, str(None)],  # list value is ok
        [{"a": {"bb": [4, 5, 6]}}, None, str(None)],  # nested value is ok
        [{1: 1}, None, str(None)],  # int key is ok
        [{"a": object()}, TypeError, "not JSON serializable"],
        [{object(): 1}, TypeError, "keys must be str, int, float, "],
        [{"a": [4, object(), 6]}, TypeError, "not JSON serializable"],
        [{"a": {object(): [4, 5, 6]}}, TypeError, "keys must be str, int, "],
    ],
)
def test_set_exceptions(md, xcept, text, md_file):
    """Cases that might raise an exception."""
    sdict = StoredDict(md_file, delay=0.2, title="unit testing")
    context = does_not_raise() if xcept is None else pytest.raises(xcept)
    with context as reason:
        sdict.update(md)
    assert text in str(reason), f"{reason=}"


def test_popitem(md_file):
    """Can't popitem from empty dict."""
    sdict = StoredDict(md_file, delay=0.2, title="unit testing")
    with pytest.raises(KeyError) as reason:
        sdict.popitem()
    assert "dictionary is empty" in str(reason), f"{reason=}"


def test_repr(md_file):
    """__repr__"""
    sdict = StoredDict(md_file, delay=0.1, title="unit testing")
    sdict["a"] = 1
    assert repr(sdict) == "<StoredDict {'a': 1}>"
    assert str(sdict) == "<StoredDict {'a': 1}>"
