# Import | Standard Library
from typing import Any

from django.conf import settings

# Import | Local
from .defaults import DEFAULT_CORS_CONFIG


def get_cors_config() -> dict[str, Any]:
    user_config = getattr(settings, "SWING_ERROR_CORS", {})
    config = DEFAULT_CORS_CONFIG.copy()
    config.update(user_config)
    return config
