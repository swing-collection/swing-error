# Import | Standard Library
from typing import Any

from django.conf import settings

# Import | Local
from .defaults import DEFAULT_ERROR_SETTINGS


def get_error_config(error_type: str, key: str, default: Any = None) -> Any:
    user_config = getattr(settings, "ERROR_HANDLER_CONFIG", {})
    if error_type in user_config and key in user_config[error_type]:
        return user_config[error_type][key]

    if error_type in DEFAULT_ERROR_SETTINGS:
        return DEFAULT_ERROR_SETTINGS[error_type].get(key, default)

    return DEFAULT_ERROR_SETTINGS["base"].get(key, default)
