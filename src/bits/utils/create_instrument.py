#!/usr/bin/env python3
"""
Script to create a new instrument based on the 'bits_instrument' template folder.

This script copies the template instrument folder into a new directory with the
provided instrument name and updates the pyproject.toml file with an entry under
[tool.instruments] reflecting the new instrument's relative path.
"""

import argparse
import logging
import shutil
import sys
from pathlib import Path
from typing import Any

try:
    import toml
except ImportError as exc:
    print("The 'toml' package is required to run this script. "
          "Please install it via 'pip install toml'.")
    sys.exit(1)


def copy_instrument(template_dir: Path, destination_dir: Path) -> None:
    """
    Copy the template instrument folder to a new destination.

    :param template_dir: Path to the template instrument directory.
    :param destination_dir: Path to the new instrument directory.
    :raises Exception: Propagates any exception raised during copy.
    """
    shutil.copytree(str(template_dir), str(destination_dir))


def update_pyproject(pyproject_path: Path, instrument_name: str, instrument_path: Path) -> None:
    """
    Update the pyproject.toml file by adding a new instrument entry.

    If the [tool.instruments] section does not exist, it will be created.

    :param pyproject_path: Path to the pyproject.toml file.
    :param instrument_name: The name of the new instrument.
    :param instrument_path: The path to the new instrument directory.
    """
    with pyproject_path.open("r", encoding="utf-8") as file:
        config: dict[str, Any] = toml.load(file)

    if "tool" not in config or not isinstance(config["tool"], dict):
        config["tool"] = {}

    if "instruments" not in config["tool"] or not isinstance(config["tool"]["instruments"], dict):
        config["tool"]["instruments"] = {}

    # Store the instrument path relative to the pyproject.toml location.
    relative_path: str = str(instrument_path.resolve().relative_to(pyproject_path.parent.resolve()))
    config["tool"]["instruments"][instrument_name] = {"path": relative_path}

    with pyproject_path.open("w", encoding="utf-8") as file:
        toml.dump(config, file)


def main() -> None:
    """
    Main function to create a new instrument based on a template and update pyproject.toml.
    """
    parser = argparse.ArgumentParser(
        description="Create a new instrument from the 'bits_instrument' template."
    )
    parser.add_argument(
        "name",
        type=str,
        help="Name of the new instrument (this will be used as the new directory name)."
    )
    parser.add_argument(
        "--template",
        type=str,
        default="bits_instrument",
        help="Path to the template instrument directory (default: bits_instrument)."
    )
    parser.add_argument(
        "--dest",
        type=str,
        default=".",
        help="Destination directory where the new instrument folder will be created (default: current directory)."
    )
    args = parser.parse_args()

    template_path: Path = Path(args.template).resolve()
    destination_parent: Path = Path(args.dest).resolve()
    new_instrument_dir: Path = destination_parent / args.name

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    logging.info(
        "Creating new instrument '%s' from template '%s' to destination '%s'.",
        args.name, template_path, new_instrument_dir
    )

    if not template_path.exists():
        logging.error("Template directory '%s' does not exist.", template_path)
        sys.exit(1)

    if new_instrument_dir.exists():
        logging.error("Destination directory '%s' already exists.", new_instrument_dir)
        sys.exit(1)

    try:
        copy_instrument(template_path, new_instrument_dir)
        logging.info("Copied template to '%s'.", new_instrument_dir)
    except Exception as exc:
        logging.error("Error copying instrument: %s", exc)
        sys.exit(1)

    pyproject_path: Path = Path("pyproject.toml").resolve()
    if not pyproject_path.exists():
        logging.error("pyproject.toml not found in the current directory!")
        sys.exit(1)

    try:
        update_pyproject(pyproject_path, args.name, new_instrument_dir)
        logging.info("Updated pyproject.toml with new instrument '%s'.", args.name)
    except Exception as exc:
        logging.error("Error updating pyproject.toml: %s", exc)
        sys.exit(1)

    logging.info("Instrument '%s' created successfully.", args.name)


if __name__ == "__main__":
    main() 