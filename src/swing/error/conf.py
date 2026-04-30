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

# Import | Standard Library
import logging
import traceback
from typing import Any, Callable

from django.conf import settings
from django.http import HttpRequest, HttpResponse

# =============================================================================
# Logger
# =============================================================================

logger: logging.Logger = logging.getLogger(name=__name__)


# =============================================================================
# Default Configuration
# =============================================================================

# Default CORS configuration for error responses
DEFAULT_CORS_CONFIG: dict[str, Any] = {
    "enabled": False,
    "allow_origins": ["*"],
    "allow_methods": [
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
        "OPTIONS",
        "HEAD",
    ],
    "allow_headers": [
        "Accept",
        "Accept-Language",
        "Content-Type",
        "Authorization",
        "X-Request-ID",
        "X-Correlation-ID",
    ],
    "expose_headers": [
        "X-Request-ID",
        "Retry-After",
        "X-Error-Code",
    ],
    "allow_credentials": False,
    "max_age": 86400,  # 24 hours
}

# Default error tracking configuration
DEFAULT_TRACKING_CONFIG: dict[str, Any] = {
    "enabled": False,
    "capture_exceptions": True,
    "capture_messages": True,
    "callback": None,  # Custom callback function path
    "extra_context": {},  # Additional context to include
}

# Default debug configuration
DEFAULT_DEBUG_CONFIG: dict[str, Any] = {
    "show_stack_trace": False,  # Show stack trace in error responses
    "show_request_info": False,  # Show request details in error responses
    "show_environment": False,  # Show environment variables (dangerous!)
    "include_sql_queries": False,  # Include SQL query log
}

# Default configuration for the error handling
DEFAULT_ERROR_SETTINGS: dict[str, dict[str, Any]] = {
    "base": {
        "status_code": 500,
        "default_message": "An error occurred",
        "default_details": {
            "title": "Error",
            "header": "An Error Occurred",
            "message": "Something went wrong.",
            "redirect": "Please return to the homepage.",
        },
        "log_errors": True,
    },
    "400": {
        "status_code": 400,
        "default_message": "Bad Request",
        "default_details": {
            "title": "Bad Request",
            "header": "400 Error",
            "message": "Sorry, your request could not be processed.",
            "redirect": "Please return to the homepage.",
        },
        "log_errors": True,
    },
    "401": {
        "status_code": 401,
        "default_message": "Unauthorized",
        "default_details": {
            "title": "Unauthorized",
            "header": "401 Error",
            "message": "Authentication is required to access this resource.",
            "redirect": "Please log in to continue.",
        },
        "log_errors": True,
    },
    "403": {
        "status_code": 403,
        "default_message": "Forbidden",
        "default_details": {
            "title": "Forbidden",
            "header": "403 Error",
            "message": "You do not have permission to access this resource.",
            "redirect": "Please return to the homepage.",
        },
        "log_errors": True,
    },
    "404": {
        "status_code": 404,
        "default_message": "Page Not Found",
        "default_details": {
            "title": "404 Error",
            "header": "Page Not Found",
            "message": "Sorry, the page you are looking for does not exist.",
            "redirect": "Return to the homepage.",
        },
        "log_errors": True,
    },
    "405": {
        "status_code": 405,
        "default_message": "Method Not Allowed",
        "default_details": {
            "title": "Method Not Allowed",
            "header": "405 Error",
            "message": "The requested method is not allowed for this resource.",
            "redirect": "Please return to the homepage.",
        },
        "log_errors": True,
    },
    "408": {
        "status_code": 408,
        "default_message": "Request Timeout",
        "default_details": {
            "title": "Request Timeout",
            "header": "408 Error",
            "message": "The server timed out waiting for your request.",
            "redirect": "Please try again.",
        },
        "log_errors": True,
    },
    "410": {
        "status_code": 410,
        "default_message": "Gone",
        "default_details": {
            "title": "Gone",
            "header": "410 Error",
            "message": "The requested resource is no longer available.",
            "redirect": "Please return to the homepage.",
        },
        "log_errors": True,
    },
    "429": {
        "status_code": 429,
        "default_message": "Too Many Requests",
        "default_details": {
            "title": "Too Many Requests",
            "header": "429 Error",
            "message": "You have sent too many requests. Please wait before trying again.",
            "redirect": "Please wait and try again later.",
        },
        "log_errors": True,
        "retry_after": 60,  # Default retry-after in seconds
    },
    "500": {
        "status_code": 500,
        "default_message": "Internal Server Error",
        "default_details": {
            "title": "Internal Server Error",
            "header": "500 Error",
            "message": "An unexpected error occurred on the server.",
            "redirect": "Please return to the homepage.",
        },
        "log_errors": True,
    },
}


# =============================================================================
# Configuration Functions
# =============================================================================


def get_error_config(
    error_type: str,
    key: str,
    default: Any = None,
) -> Any:
    """
    Retrieve error handler configuration for a specific error type
    from Django settings with fallback to defaults.

    Args:
        error_type (str): The error type (e.g., "400", "404", "base").
        key (str): The key to retrieve from the error configuration.
        default (Any): Default value if the key or type is not set.

    Returns:
        Any: The configuration value.

    Example:
        >>> get_error_config("404", "default_message")
        "Page Not Found"
        >>> get_error_config("404", "default_details")
        {"title": "404 Error", ...}
    """
    # First check user settings override
    user_config = getattr(settings, "ERROR_HANDLER_CONFIG", {})
    if error_type in user_config and key in user_config[error_type]:
        return user_config[error_type][key]

    # Then check default settings for this error type
    if error_type in DEFAULT_ERROR_SETTINGS:
        return DEFAULT_ERROR_SETTINGS[error_type].get(key, default)

    # Fall back to base configuration
    return DEFAULT_ERROR_SETTINGS["base"].get(key, default)


def get_all_error_types() -> list[str]:
    """
    Get a list of all supported error types.

    Returns:
        list[str]: List of error type codes (e.g., ["400", "401", ...]).
    """
    return [key for key in DEFAULT_ERROR_SETTINGS.keys() if key != "base"]


def get_cors_config() -> dict[str, Any]:
    """
    Get CORS configuration for error responses.

    Returns:
        dict[str, Any]: CORS configuration dictionary.
    """
    user_config = getattr(settings, "SWING_ERROR_CORS", {})
    config = DEFAULT_CORS_CONFIG.copy()
    config.update(user_config)
    return config


def get_tracking_config() -> dict[str, Any]:
    """
    Get error tracking configuration.

    Returns:
        dict[str, Any]: Error tracking configuration dictionary.
    """
    user_config = getattr(settings, "SWING_ERROR_TRACKING", {})
    config = DEFAULT_TRACKING_CONFIG.copy()
    config.update(user_config)
    return config


def get_debug_config() -> dict[str, Any]:
    """
    Get debug mode configuration.

    Only applies when Django's DEBUG setting is True.

    Returns:
        dict[str, Any]: Debug configuration dictionary.
    """
    if not getattr(settings, "DEBUG", False):
        # Return all-false config when not in debug mode
        return {key: False for key in DEFAULT_DEBUG_CONFIG}

    user_config = getattr(settings, "SWING_ERROR_DEBUG", {})
    config = DEFAULT_DEBUG_CONFIG.copy()
    config.update(user_config)
    return config


# =============================================================================
# CORS Functions
# =============================================================================


def add_cors_headers(
    response: HttpResponse,
    request: HttpRequest | None = None,
) -> HttpResponse:
    """
    Add CORS headers to an error response.

    Args:
        response (HttpResponse): The response to add headers to.
        request (HttpRequest | None): The request (for origin checking).

    Returns:
        HttpResponse: The response with CORS headers added.
    """
    config = get_cors_config()

    if not config.get("enabled", False):
        return response

    # Get request origin
    origin = None
    if request:
        origin = request.META.get("HTTP_ORIGIN")

    # Determine allowed origin
    allow_origins = config.get("allow_origins", ["*"])
    if "*" in allow_origins:
        response["Access-Control-Allow-Origin"] = "*"
    elif origin and origin in allow_origins:
        response["Access-Control-Allow-Origin"] = origin
        response["Vary"] = "Origin"

    # Add other CORS headers
    if config.get("allow_credentials", False):
        response["Access-Control-Allow-Credentials"] = "true"

    allow_methods = config.get("allow_methods", [])
    if allow_methods:
        response["Access-Control-Allow-Methods"] = ", ".join(allow_methods)

    allow_headers = config.get("allow_headers", [])
    if allow_headers:
        response["Access-Control-Allow-Headers"] = ", ".join(allow_headers)

    expose_headers = config.get("expose_headers", [])
    if expose_headers:
        response["Access-Control-Expose-Headers"] = ", ".join(expose_headers)

    max_age = config.get("max_age")
    if max_age:
        response["Access-Control-Max-Age"] = str(max_age)

    return response


# =============================================================================
# Error Tracking Functions
# =============================================================================


def capture_error(
    exception: Exception | None = None,
    message: str | None = None,
    request: HttpRequest | None = None,
    extra_context: dict[str, Any] | None = None,
) -> None:
    """
    Capture an error for tracking/reporting.

    This function sends errors to configured tracking services (e.g., Sentry)
    or calls a custom callback function.

    Args:
        exception (Exception | None): The exception that occurred.
        message (str | None): An error message (if no exception).
        request (HttpRequest | None): The HTTP request context.
        extra_context (dict[str, Any] | None): Additional context data.

    Example:
        >>> capture_error(exception=ValueError("Invalid input"), request=request)
        >>> capture_error(message="User not found", extra_context={"user_id": 123})
    """
    config = get_tracking_config()

    if not config.get("enabled", False):
        return

    # Build context
    context: dict[str, Any] = config.get("extra_context", {}).copy()
    if extra_context:
        context.update(extra_context)

    if request:
        context.update(
            {
                "request_path": request.path,
                "request_method": request.method,
                "request_user": str(getattr(request, "user", "anonymous")),
            }
        )

    # Try to use Sentry if available
    if config.get("capture_exceptions", True) or config.get(
        "capture_messages", True
    ):
        try:
            # Import | Libraries
            import sentry_sdk

            if exception and config.get("capture_exceptions", True):
                with sentry_sdk.push_scope() as scope:
                    for key, value in context.items():
                        scope.set_extra(key, value)
                    sentry_sdk.capture_exception(exception)
            elif message and config.get("capture_messages", True):
                with sentry_sdk.push_scope() as scope:
                    for key, value in context.items():
                        scope.set_extra(key, value)
                    sentry_sdk.capture_message(message)
        except ImportError:
            # Sentry not installed, try custom callback
            pass

    # Call custom callback if configured
    callback_path = config.get("callback")
    if callback_path:
        try:
            callback = _import_callback(callback_path)
            callback(
                exception=exception,
                message=message,
                request=request,
                context=context,
            )
        except Exception as e:
            logger.warning(f"Error tracking callback failed: {e}")


def _import_callback(callback_path: str) -> Callable:
    """
    Import a callback function from a dotted path.

    Args:
        callback_path (str): Dotted path to the callback (e.g., "myapp.module.func").

    Returns:
        Callable: The imported callback function.
    """
    # Import | Standard Library
    from importlib import import_module

    module_path, func_name = callback_path.rsplit(".", 1)
    module = import_module(module_path)
    return getattr(module, func_name)


# =============================================================================
# Debug Functions
# =============================================================================


def get_debug_info(
    exception: Exception | None = None,
    request: HttpRequest | None = None,
) -> dict[str, Any]:
    """
    Get debug information for error responses.

    Only returns information when DEBUG is True and configured to do so.

    Args:
        exception (Exception | None): The exception that occurred.
        request (HttpRequest | None): The HTTP request.

    Returns:
        dict[str, Any]: Debug information dictionary (empty if not in debug mode).
    """
    config = get_debug_config()
    debug_info: dict[str, Any] = {}

    if not any(config.values()):
        return debug_info

    # Stack trace
    if config.get("show_stack_trace") and exception:
        debug_info["stack_trace"] = traceback.format_exception(
            type(exception),
            exception,
            exception.__traceback__,
        )
        debug_info["exception_type"] = type(exception).__name__
        debug_info["exception_message"] = str(exception)

    # Request information
    if config.get("show_request_info") and request:
        debug_info["request"] = {
            "path": request.path,
            "method": request.method,
            "content_type": request.content_type,
            "headers": {
                k: v
                for k, v in request.headers.items()
                if k.lower() not in ("authorization", "cookie", "x-api-key")
            },
            "GET": dict(request.GET),
            "POST": dict(request.POST) if request.method == "POST" else {},
        }

    # Environment (dangerous - disabled by default)
    if config.get("show_environment"):
        # Import | Standard Library
        import os

        # Only show safe environment variables
        safe_vars = ["DJANGO_SETTINGS_MODULE", "DEBUG", "PYTHONPATH"]
        debug_info["environment"] = {
            k: v for k, v in os.environ.items() if k in safe_vars
        }

    # SQL queries (if django-debug-toolbar style logging is available)
    if config.get("include_sql_queries"):
        try:
            from django.db import connection

            debug_info["sql_queries"] = [
                {"sql": q["sql"], "time": q["time"]}
                for q in connection.queries[-10:]  # Last 10 queries
            ]
        except Exception:
            pass

    return debug_info


# =============================================================================
# Exports
# =============================================================================

__all__: list[str] = [
    # Settings
    "DEFAULT_ERROR_SETTINGS",
    "DEFAULT_CORS_CONFIG",
    "DEFAULT_TRACKING_CONFIG",
    "DEFAULT_DEBUG_CONFIG",
    # Config functions
    "get_error_config",
    "get_all_error_types",
    "get_cors_config",
    "get_tracking_config",
    "get_debug_config",
    # CORS
    "add_cors_headers",
    # Error tracking
    "capture_error",
    # Debug
    "get_debug_info",
]
