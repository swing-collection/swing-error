# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Swing Error Configuration Module
================================

This module provides configuration management for the swing.error app,
including default settings for all supported HTTP error codes and a
utility function to retrieve error-specific configurations.

Usage:
------
    from swing.error.conf import get_error_config

    message = get_error_config("404", "default_message")
    details = get_error_config("404", "default_details")

You can override these defaults in your Django settings:

    ERROR_HANDLER_CONFIG = {
        "404": {
            "default_message": "Custom not found message",
            "default_details": {
                "title": "Custom 404",
                ...
            }
        }
    }

CORS Configuration:
-------------------
    SWING_ERROR_CORS = {
        "enabled": True,
        "allow_origins": ["*"],  # Or specific origins
        "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "X-Request-ID"],
        "expose_headers": ["X-Request-ID", "Retry-After"],
        "max_age": 86400,
    }

Error Tracking (Sentry) Configuration:
--------------------------------------
    SWING_ERROR_TRACKING = {
        "enabled": True,
        "capture_exceptions": True,
        "capture_messages": True,
        "callback": "myapp.error_tracking.capture_error",  # Optional custom callback
    }

Debug Mode Configuration:
-------------------------
    SWING_ERROR_DEBUG = {
        "show_stack_trace": True,  # Show stack trace in responses (DEBUG only)
        "show_request_info": True,  # Show request details in responses (DEBUG only)
        "show_environment": False,  # Show environment variables (never recommended)
    }

"""

# =============================================================================
# Imports
# =============================================================================

# Import | Local
from ._conf.add_cors_headers import add_cors_headers
from ._conf.capture_error import capture_error
from ._conf.defaults import (
    DEFAULT_CORS_CONFIG,
    DEFAULT_DEBUG_CONFIG,
    DEFAULT_ERROR_SETTINGS,
    DEFAULT_TRACKING_CONFIG,
)
from ._conf.get_all_error_types import get_all_error_types
from ._conf.get_cors_config import get_cors_config
from ._conf.get_debug_config import get_debug_config
from ._conf.get_debug_info import get_debug_info
from ._conf.get_error_config import get_error_config
from ._conf.get_tracking_config import get_tracking_config

# =============================================================================
# Exports
# =============================================================================

__all__: list[str] = [
    "DEFAULT_ERROR_SETTINGS",
    "DEFAULT_CORS_CONFIG",
    "DEFAULT_TRACKING_CONFIG",
    "DEFAULT_DEBUG_CONFIG",
    "get_error_config",
    "get_all_error_types",
    "get_cors_config",
    "get_tracking_config",
    "get_debug_config",
    "add_cors_headers",
    "capture_error",
    "get_debug_info",
]
