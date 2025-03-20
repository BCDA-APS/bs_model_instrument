#!/usr/bin/env python3
"""
Create a new instrument from a fixed template.

Copies the template directory and updates pyproject.toml and .templatesyncignore.
"""

__version__ = "1.0.0"

import argparse
import re
import shutil
import sys
from pathlib import Path


def copy_instrument(template_dir: Path, destination_dir: Path) -> None:
    """
    Copy template directory to the destination.

    :param template_dir: Path to the template directory.
    :param destination_dir: Path to the new instrument directory.
    :return: None
    """
    shutil.copytree(str(template_dir), str(destination_dir))


def main() -> None:
    """
    Parse arguments and create the instrument.

    :return: None
    """
    parser = argparse.ArgumentParser(
        description="Create an instrument from a fixed template."
    )
    parser.add_argument(
        "name", type=str, help="New instrument name; must be a valid package name."
    )
    parser.add_argument("dest", type=str, help="Destination directory.")
    args = parser.parse_args()

    if re.fullmatch(r"[a-z][_a-z0-9]*", args.name) is None:
        print(f"Error: Invalid instrument name '{args.name}'.", file=sys.stderr)
        sys.exit(1)

    # Resolve the template path from the installed apsbits package.
    # __file__ is located at apsbits/utils/create_new_instrument.py, so moving
    # two levels up
    # points to the root of the apsbits package where demo_instrument is expected to be.
    template_path: Path = (
        Path(__file__).resolve().parent.parent / "demo_instrument"
    ).resolve()
    destination_parent: Path = Path(args.dest).resolve()
    new_instrument_dir: Path = destination_parent / args.name

    print(
        f"Creating instrument '{args.name}' from '{template_path}' into \
        '{new_instrument_dir}'."
    )

    if not template_path.exists():
        print(f"Error: Template '{template_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    if new_instrument_dir.exists():
        print(f"Error: Destination '{new_instrument_dir}' exists.", file=sys.stderr)
        sys.exit(1)

    try:
        copy_instrument(template_path, new_instrument_dir)
        print(f"Template copied to '{new_instrument_dir}'.")
    except Exception as exc:
        print(f"Error copying instrument: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Instrument '{args.name}' created.")


if __name__ == "__main__":
    main()
