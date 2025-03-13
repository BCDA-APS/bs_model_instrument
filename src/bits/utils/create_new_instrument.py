#!/usr/bin/env python3
"""
Create a new instrument from a fixed template.

Copies the template directory and updates pyproject.toml.
"""

import argparse
import re
import shutil
import sys
from pathlib import Path
from typing import Any
import toml


def copy_instrument(template_dir: Path, destination_dir: Path) -> None:
    """
    Copy template to destination.
    """
    shutil.copytree(str(template_dir), str(destination_dir))


def update_pyproject(
    pyproject_path: Path, instrument_name: str, instrument_path: Path
) -> None:
    """
    Add the instrument to pyproject.toml.
    """
    with pyproject_path.open("r", encoding="utf-8") as file:
        config: dict[str, Any] = toml.load(file)

    config.setdefault("tool", {})
    config["tool"].setdefault("instruments", {})

    relative_path: str = str(
        instrument_path.resolve().relative_to(pyproject_path.parent.resolve())
    )
    config["tool"]["instruments"][instrument_name] = {"path": relative_path}

    with pyproject_path.open("w", encoding="utf-8") as file:
        toml.dump(config, file)


def main() -> None:
    """
    Parse args and create the instrument.
    """
    parser = argparse.ArgumentParser(
        description="Create an instrument from a fixed template."
    )
    parser.add_argument(
        "name", type=str, help="New instrument name (must be a valid package name)."
    )
    parser.add_argument(
        "dest", type=str, help="Destination directory (default: current directory)."
    )
    args = parser.parse_args()

    if re.fullmatch(r"[a-z][_a-z0-9]*", args.name) is None:
        print(f"Error: Invalid instrument name '{args.name}'.", file=sys.stderr)
        sys.exit(1)

    template_path: Path = Path("src/bits/demo_instrument").resolve()
    destination_parent: Path = Path(args.dest).resolve()
    new_instrument_dir: Path = destination_parent / args.name

    print(f"Creating instrument '{args.name}' from '{template_path}' into \
          '{new_instrument_dir}'.")

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

    pyproject_path: Path = Path("pyproject.toml").resolve()
    if not pyproject_path.exists():
        print("Error: pyproject.toml not found.", file=sys.stderr)
        sys.exit(1)

    try:
        update_pyproject(pyproject_path, args.name, new_instrument_dir)
        print(f"pyproject.toml updated with '{args.name}'.")
    except Exception as exc:
        print(f"Error updating pyproject.toml: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Instrument '{args.name}' created.")


if __name__ == "__main__":
    main()
