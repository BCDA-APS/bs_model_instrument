#!/usr/bin/env python3
"""
Delete an instrument and its associated qserver configuration.

This script safely removes an instrument directory and its corresponding qserver
configuration directory from the workspace.
"""

__version__ = "1.0.0"

import argparse
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Tuple


def validate_instrument_name(name: str) -> bool:
    """
    Validate that the instrument name follows the required pattern.

    :param name: The instrument name to validate.
    :return: True if the name is valid, False otherwise.
    """
    return re.fullmatch(r"[a-z][_a-z0-9]*", name) is not None


def get_instrument_paths(name: str) -> Tuple[Path, Path]:
    """
    Get the paths to the instrument and qserver directories.

    :param name: The name of the instrument.
    :return: A tuple containing the instrument directory path and qserver directory
             path.
    """
    main_path: Path = Path(os.getcwd()).resolve()
    instrument_dir: Path = main_path / "src" / name
    qserver_dir: Path = main_path / "src" / f"{name}_qserver"

    return instrument_dir, qserver_dir


def delete_instrument(instrument_dir: Path, qserver_dir: Path) -> None:
    """
    Delete the instrument and qserver directories.

    :param instrument_dir: Path to the instrument directory.
    :param qserver_dir: Path to the qserver directory.
    :return: None
    """
    if instrument_dir.exists():
        shutil.rmtree(str(instrument_dir))
        print(f"Instrument directory '{instrument_dir}' removed.")
    else:
        print(f"Warning: Instrument directory '{instrument_dir}' does not exist.")

    if qserver_dir.exists():
        shutil.rmtree(str(qserver_dir))
        print(f"Qserver directory '{qserver_dir}' removed.")
    else:
        print(f"Warning: Qserver directory '{qserver_dir}' does not exist.")


def main() -> None:
    """
    Parse arguments and delete the instrument.

    :return: None
    """
    parser = argparse.ArgumentParser(
        description="Delete an instrument and its associated qserver configuration."
    )
    parser.add_argument("name", type=str, help="Name of the instrument to delete.")
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Skip confirmation prompt and delete immediately.",
    )
    args = parser.parse_args()

    if not validate_instrument_name(args.name):
        print(f"Error: Invalid instrument name '{args.name}'.", file=sys.stderr)
        sys.exit(1)

    instrument_dir, qserver_dir = get_instrument_paths(args.name)

    if not instrument_dir.exists() and not qserver_dir.exists():
        print(
            f"Error: Neither instrument '{args.name}' nor its qserver configuration "
            f"exist.",
            file=sys.stderr,
        )
        sys.exit(1)

    if not args.force:
        confirmation = input(
            f"Are you sure you want to delete instrument '{args.name}' and its "
            f"qserver configuration? [y/N]: "
        )
        if confirmation.lower() != "y":
            print("Deletion cancelled.")
            sys.exit(0)

    try:
        delete_instrument(instrument_dir, qserver_dir)
        print(
            f"Instrument '{args.name}' and its qserver configuration have been deleted."
        )
    except Exception as exc:
        print(f"Error deleting instrument: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
