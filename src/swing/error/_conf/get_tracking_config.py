# Import | Standard Library
from typing import Any

from django.conf import settings

# Import | Local
from .defaults import DEFAULT_TRACKING_CONFIG


def get_tracking_config() -> dict[str, Any]:
    user_config = getattr(settings, "SWING_ERROR_TRACKING", {})
    config = DEFAULT_TRACKING_CONFIG.copy()
    config.update(user_config)
    return config
