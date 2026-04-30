# Import | Standard Library
from typing import Any

from django.conf import settings

# Import | Local
from .defaults import DEFAULT_DEBUG_CONFIG


def get_debug_config() -> dict[str, Any]:
    if not getattr(settings, "DEBUG", False):
        return {key: False for key in DEFAULT_DEBUG_CONFIG}

    user_config = getattr(settings, "SWING_ERROR_DEBUG", {})
    config = DEFAULT_DEBUG_CONFIG.copy()
    config.update(user_config)
    return config
