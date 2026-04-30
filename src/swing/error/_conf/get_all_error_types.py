# Import | Local
from .defaults import DEFAULT_ERROR_SETTINGS


def get_all_error_types() -> list[str]:
    return [key for key in DEFAULT_ERROR_SETTINGS.keys() if key != "base"]
