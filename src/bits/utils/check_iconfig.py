#!/usr/bin/env python3
"""
This script checks if the variable 'iconfig' is present in any module's global scope.

This is useful for ensuring that the instrument configuration variable is properly encapsulated
and that no module inadvertently holds a global reference to 'iconfig', except in the allowed
init_instrument module.
"""

import gc
import inspect
from typing import Any


def is_iconfig_in_memory() -> bool:
    """
    Check if the variable 'iconfig' exists in any module's global dictionary.

    Returns:
        bool: True if 'iconfig' is found in any module's globals, False otherwise.
    """
    for obj in gc.get_objects():
        # Check if the object is a dictionary (which module globals typically are)
        if isinstance(obj, dict):
            try:
                if 'iconfig' in obj:
                    value: Any = obj['iconfig']
                    # Optionally, check if the value is a module or a function
                    if inspect.ismodule(value) or inspect.isfunction(value):
                        print(f"Found 'iconfig' in globals: {value}")
                        return True
            except Exception:
                continue
    return False


def main() -> None:
    """
    Main function to check for the 'iconfig' variable in memory and output the result.
    """
    if is_iconfig_in_memory():
        print("Variable 'iconfig' IS present in memory.")
    else:
        print("Variable 'iconfig' is NOT present in memory.")


if __name__ == '__main__':
    main() 