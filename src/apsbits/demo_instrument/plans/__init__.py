"""Demo instrument plans.

This package contains various plans for the demo instrument.
"""

from apsbits.demo_instrument.plans.demo_plans import (
    demo_print_plan,
    demo_count_plan,
    demo_rel_scan_plan,
    demo_list_scan_plan,
    demo_grid_scan_plan,
    demo_inner_product_scan_plan,
    demo_adaptive_scan_plan,
)

from apsbits.demo_instrument.plans.dm_plans import (
    dm_count_plan,
    dm_scan_plan,
    dm_grid_scan_plan,
    dm_list_scan_plan,
    dm_adaptive_scan_plan,
)

from apsbits.demo_instrument.plans.sim_plans import (
    sim_count_plan,
    sim_scan_plan,
    sim_grid_scan_plan,
    sim_list_scan_plan,
    sim_adaptive_scan_plan,
)

__all__ = [
    # Demo plans
    "demo_print_plan",
    "demo_count_plan",
    "demo_rel_scan_plan",
    "demo_list_scan_plan",
    "demo_grid_scan_plan",
    "demo_inner_product_scan_plan",
    "demo_adaptive_scan_plan",
    # Data management plans
    "dm_count_plan",
    "dm_scan_plan",
    "dm_grid_scan_plan",
    "dm_list_scan_plan",
    "dm_adaptive_scan_plan",
    # Simulation plans
    "sim_count_plan",
    "sim_scan_plan",
    "sim_grid_scan_plan",
    "sim_list_scan_plan",
    "sim_adaptive_scan_plan",
]
