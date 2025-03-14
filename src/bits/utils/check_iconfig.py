import gc
import inspect
from typing import Any


# Existing function to check if 'iconfig' is in memory

def is_iconfig_in_memory() -> bool:
    """
    Check if the variable 'iconfig' exists in any module's global dictionary.

    Returns:
        bool: True if 'iconfig' is found in any module's globals, False otherwise.
    """
    for obj in gc.get_objects():
        # Check if the object is a dictionary (usually module globals)
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


# New function to retrieve the instance of 'iconfig' from memory

def get_iconfig_instance() -> Any:
    """
    Retrieve the instance of 'iconfig' from any module's global scope.

    Returns:
        Any: The instance of 'iconfig' (typically a module or a function).

    Raises:
        RuntimeError: If no instance of 'iconfig' is found in memory.
    """
    for obj in gc.get_objects():
        # Check if the object is a dictionary (module globals)
        if isinstance(obj, dict):
            try:
                if 'iconfig' in obj:
                    value: Any = obj['iconfig']
                    if inspect.ismodule(value) or inspect.isfunction(value):
                        return value
            except Exception:
                continue
    raise RuntimeError("Instance 'iconfig' not found in memory.")


# Main function to execute checks

def main() -> None:
    """
    Main function to check for the 'iconfig' variable in memory and output the result.
    """
    if is_iconfig_in_memory():
        print("Variable 'iconfig' IS present in memory.")
        try:
            instance = get_iconfig_instance()
            print(f"Retrieved 'iconfig' instance: {instance}")
        except RuntimeError as error:
            print(str(error))
    else:
        print("Variable 'iconfig' is NOT present in memory.")


if __name__ == '__main__':
    main() 