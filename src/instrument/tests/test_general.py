"""
Test that instrument can be started.

Here is just enough testing to get a CI workflow started. More are possible.
"""

import pytest

from ..plans.sim_plans import sim_count_plan
from ..plans.sim_plans import sim_print_plan
from ..plans.sim_plans import sim_rel_scan_plan
from ..startup import RE
from ..startup import bec
from ..startup import cat
from ..startup import iconfig
from ..startup import peaks
from ..startup import running_in_queueserver
from ..startup import sd
from ..startup import specwriter


def test_startup():
    """Test that standard startup works."""
    assert cat is not None
    assert bec is not None
    assert peaks is not None
    assert sd is not None
    assert iconfig is not None
    assert RE is not None
    assert specwriter is not None
    if iconfig.get("DATABROKER_CATALOG", "temp") == "temp":
        assert len(cat) == 0
    assert not running_in_queueserver()


@pytest.mark.parametrize(
    "plan, n_uids",
    [
        [sim_print_plan, 0],
        [sim_count_plan, 1],
        [sim_rel_scan_plan, 1],
    ],
)
def test_sim_plans(plan, n_uids):
    """Test supplied simulator plans."""
    bec.disable_plots()
    n_runs = len(cat)
    uids = RE(plan())
    assert len(uids) == n_uids
    assert len(cat) == n_runs + len(uids)


def test_iconfig():
    """Test the instrument configuration."""
    version = iconfig.get("ICONFIG_VERSION", "0.0.0")
    assert version >= "2.0.0"

    cat_name = iconfig.get("DATABROKER_CATALOG")
    assert cat_name is not None
    assert cat_name == cat.name

    assert "RUN_ENGINE" in iconfig
    assert "DEFAULT_METADATA" in iconfig["RUN_ENGINE"]

    default_md = iconfig["RUN_ENGINE"]["DEFAULT_METADATA"]
    assert "beamline_id" in default_md
    assert "instrument_name" in default_md
    assert "proposal_id" in default_md
    assert "databroker_catalog" in default_md
    assert default_md["databroker_catalog"] == cat.name

    xmode = iconfig.get("XMODE_DEBUG_LEVEL")
    assert xmode is not None
