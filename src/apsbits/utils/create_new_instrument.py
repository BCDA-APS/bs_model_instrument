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


def create_qserver_config(destination_dir: Path) -> None:
    """
    Create a qserver config file in the destination directory.
    """
    qserver_config_path = destination_dir / "qserver.yml"
    with open(qserver_config_path, "w") as f:
        f.write("qserver: !QServer\n")

def create_qserver_startup_script(destination_dir: Path) -> None:
    """
    Create a qserver startup script in the destination directory.

    Copies the demo qserver host script to the user's scripts folder and updates
    the initialization package name.

    Parameters
    ----------
    destination_dir : Path
        Path to the destination directory where the script should be created
    """
    # Get path to demo qserver host script
    demo_script_path = Path(__file__).resolve().parent.parent / "demo_qserver" / "qs_host.sh"
    
    # Create scripts directory if it doesn't exist
    scripts_dir = destination_dir / "scripts"
    scripts_dir.mkdir(exist_ok=True)
    
    # Copy script to destination
    dest_script_path = scripts_dir / "qs_host.sh"
    
    # Read demo script and replace package name
    with open(demo_script_path, "r") as src:
        script_contents = src.read()
        
    # Get package name from destination dir
    package_name = destination_dir.name
    
    # Replace demo package with new package name
    updated_contents = script_contents.replace("demo_instrument", package_name)
    
    # Write updated script
    with open(dest_script_path, "w") as dest:
        dest.write(updated_contents)


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

    try:
        create_qserver_config(new_instrument_dir)
        print(f"Qserver config created in '{new_instrument_dir}'.")
    except Exception as exc:
        print(f"Error creating qserver config: {exc}", file=sys.stderr)
        sys.exit(1)
        

    print(f"Instrument '{args.name}' created.")


if __name__ == "__main__":
    main()
