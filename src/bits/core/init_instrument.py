from typing import Any, Optional


# Module-level variable to store the instrument configuration loaded from iconfig
_instrument_config: Optional[Any] = None


def init_instrument() -> None:
    """
    Initialize the instrument configuration by loading configuration variables from iconfig.

    This function loads the configuration using iconfig's load_config method and stores it
    in memory for subsequent use. It ensures that all necessary configuration variables
    are available globally for the application and prevents direct calls to iconfig
    from core or utils modules.

    Raises:
        Exception: If loading configuration from iconfig fails.
    """
    global _instrument_config
    if _instrument_config is not None:
        # Configuration already initialized; no action needed.
        return
    try:
        from bits.config import iconfig  # Import iconfig from the configuration module
    except ImportError as e:
        raise ImportError("Failed to import iconfig from bits.config. Ensure that the configuration module is available.") from e
    _instrument_config = iconfig.load_config()


def get_instrument_config() -> Any:
    """
    Retrieve the instrument configuration loaded via init_instrument.

    Returns:
        Any: The configuration object with loaded variables.

    Raises:
        RuntimeError: If the configuration has not been initialized.
    """
    if _instrument_config is None:
        raise RuntimeError("Instrument configuration has not been initialized. Call init_instrument() first.")
    return _instrument_config 