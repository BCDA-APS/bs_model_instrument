#!/usr/bin/env python3
"""
Script to create a new instrument based on the 'src/bits/demo_instrument' template
folder.

This script copies the template instrument folder into a new directory with the
provided instrument name (which must be a valid Python package name) and updates
the pyproject.toml file with an entry under [tool.instruments] reflecting the
new instrument's relative path.

The script includes a version flag and can be executed directly without needing to
install the bits package.
"""

__version__ = "1.0.0"

import argparse
import logging
import re
import shutil
import sys
from pathlib import Path
from typing import Any

try:
    import toml
except ImportError:
    print(
        "The 'toml' package is required to run this script. "
        "Please install it via 'pip install toml'."
    )
    sys.exit(1)


def copy_instrument(template_dir: Path, destination_dir: Path) -> None:
    """
    Copy the template instrument folder to a new destination.

    Args:
        template_dir (Path): Path to the template instrument directory.
        destination_dir (Path): Path to the new instrument directory.

    Raises:
        Exception: Propagates any exception raised during copying.
    """
    shutil.copytree(str(template_dir), str(destination_dir))


def update_pyproject(
    pyproject_path: Path, instrument_name: str, instrument_path: Path
) -> None:
    """
    Update the pyproject.toml file by adding a new instrument entry.

    If the [tool.instruments] section does not exist, it will be created.

    Args:
        pyproject_path (Path): Path to the pyproject.toml file.
        instrument_name (str): The name of the new instrument.
        instrument_path (Path): The path to the new instrument directory.
    """
    with pyproject_path.open("r", encoding="utf-8") as file:
        config: dict[str, Any] = toml.load(file)

    if "tool" not in config or not isinstance(config["tool"], dict):
        config["tool"] = {}

    if "instruments" not in config["tool"] or not isinstance(
        config["tool"]["instruments"], dict
    ):
        config["tool"]["instruments"] = {}

    # Store the instrument path relative to the pyproject.toml location.
    relative_path: str = str(
        instrument_path.resolve().relative_to(pyproject_path.parent.resolve())
    )
    config["tool"]["instruments"][instrument_name] = {"path": relative_path}

    with pyproject_path.open("w", encoding="utf-8") as file:
        toml.dump(config, file)


def main() -> None:
    """
    Main function to create a new instrument based on a template and update
    pyproject.toml.

    This function parses command-line arguments (including a --version flag) to ensure
    the script
    can be run standalone without needing to install the entire bits package.
    Validates that the new instrument name is a valid Python package name (lowercase
    letters,
    digits, and underscores, starting with a letter).
    """
    parser = argparse.ArgumentParser(
        description="Create a new instrument from the 'src/bits/demo_instrument' "
        "template."
    )
    parser.add_argument(
        "name",
        type=str,
        help="Name of the new instrument (this will be used as the new directory "
        "name and must be a valid package name).",
    )
    parser.add_argument(
        "--template",
        type=str,
        default="src/bits/demo_instrument",
        help="Path to the template instrument directory "
        "(default: src/bits/demo_instrument).",
    )
    parser.add_argument(
        "--dest",
        type=str,
        default=".",
        help="Destination directory where the new instrument folder will be created "
        "(default: current directory).",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show the version of this script and exit.",
    )
    args = parser.parse_args()

    # Validate that the instrument name is a valid Python package name.
    if re.fullmatch(r"[a-z][_a-z0-9]*", args.name) is None:
        logging.error(
            "Invalid instrument name '%s'. Please use a valid Python package name "
            "(lowercase letters, digits, and underscores, starting with a letter).",
            args.name,
        )
        sys.exit(1)

    template_path: Path = Path(args.template).resolve()
    destination_parent: Path = Path(args.dest).resolve()
    new_instrument_dir: Path = destination_parent / args.name

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.info(
        "Creating new instrument '%s' from template '%s' to destination '%s'.",
        args.name,
        template_path,
        new_instrument_dir,
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
