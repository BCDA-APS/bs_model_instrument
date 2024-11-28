"""
Test the utils.stored_dict module.
"""

import pathlib
import tempfile
import threading
import time
from contextlib import nullcontext as does_not_raise

import pytest

from ..utils.config_loaders import load_config_yaml
from ..utils.stored_dict import StoredDict
from ..utils.stored_dict import _sync_threads


@pytest.fixture
def md_file():
    """Provide a temporary file (deleted on close)."""
    tfile = tempfile.NamedTemporaryFile(
        prefix="re_md_",
        suffix=".yml",
        delete=False,
    )
    path = pathlib.Path(tfile.name)
    yield pathlib.Path(tfile.name)

    if path.exists():
        path.unlink()  # delete the file


def test_StoredDict(md_file):
    """Test the StoredDict class."""
    assert md_file.exists()
    assert len(open(md_file).read().splitlines()) == 0  # empty

    sdict = StoredDict(md_file, delay=0.2, title="unit testing")
    assert sdict is not None
    assert len(sdict) == 0
    assert sdict._delay == 0.2
    assert sdict._title == "unit testing"
    assert len(open(md_file).read().splitlines()) == 0  # still empty

    # Check that the thread dictionary is setup.
    assert len(_sync_threads) > 0
    sync_key = id(sdict)
    assert sync_key == sdict._sync_key
    assert sync_key in _sync_threads

    # Write an empty dictionary.
    sdict.flush()
    buf = open(md_file).read().splitlines()
    assert len(buf) == 4
    assert buf[-1] == "{}"  # The empty dict.
    assert buf[0].startswith("# ")
    assert buf[1].startswith("# ")
    assert "unit testing" in buf[0]

    # Add a new {key: value} pair.
    assert _sync_threads[sync_key] is None
    sdict["a"] = 1
    assert _sync_threads[sync_key] is not None
    assert isinstance(_sync_threads[sync_key], threading.Thread)
    sdict.flush()
    time.sleep(3 * sdict._sync_while_loop_period)  # Luftpause for sync_agent.
    assert _sync_threads[sync_key] is None
    assert len(open(md_file).read().splitlines()) == 4

    # Change the only value.
    sdict["a"] = 2
    sdict.flush()
    time.sleep(3 * sdict._sync_while_loop_period)  # Luftpause.
    assert len(open(md_file).read().splitlines()) == 4  # Still.

    # Add another key.
    sdict["bee"] = "bumble"
    sdict.flush()
    time.sleep(3 * sdict._sync_while_loop_period)  # Luftpause.
    assert len(open(md_file).read().splitlines()) == 5

    # Test _delayed_sync_to_storage.
    sdict["bee"] = "queen"
    md = load_config_yaml(md_file)
    assert len(md) == 2  # a & bee
    assert "a" in md
    assert md["bee"] == "bumble"  # The old value.

    time.sleep(sdict._delay / 2)
    # Still not written ...
    assert load_config_yaml(md_file)["bee"] == "bumble"

    time.sleep(sdict._delay)
    # Should be written by now.
    assert load_config_yaml(md_file)["bee"] == "queen"

    del sdict["bee"]  # __delitem__
    assert "bee" not in sdict  # __getitem__


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
