# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Swing Error - Reusable Django Error Pages
============================================

A fully-featured reusable Django app for handling HTTP error pages
with customizable templates, middleware, and response classes.

This package provides:

- Class-based views for all common HTTP error codes (400-500)
- Customizable error response classes
- Exception middleware for automatic error handling
- Configurable via Django settings (ERROR_HANDLER_CONFIG)
- CORS support for API error responses
- Error tracking integration (Sentry-compatible)
- Debug mode with stack traces

Quick Start
-----------
1. Add to INSTALLED_APPS:

    INSTALLED_APPS = [
        ...
        "swing.error",
    ]

2. Configure error handlers in urls.py:

    from swing.error.urls import (
        handler400,
        handler403,
        handler404,
        handler500,
    )

3. Optionally customize via settings:

    ERROR_HANDLER_CONFIG = {
        "404": {
            "template": "myapp/404.html",
            "default_message": "Page not found",
        }
    }

Example
-------
    from swing.error import (
        Handler404View,
        Handler500View,
        Http404Response,
        error_handlers,
    )

"""

# Import | Future
from __future__ import annotations

# Import | Standard Library
import importlib
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from swing.error.middleware import ExceptionMiddleware
    from swing.error.responses import (
        BaseErrorResponse,
        Http400Response,
        Http401Response,
        Http403Response,
        Http404Response,
        Http405Response,
        Http408Response,
        Http410Response,
        Http429Response,
        Http500Response,
    )
    from swing.error.urls import (
        configure_error_handlers,
        error_handlers,
        handler400,
        handler403,
        handler404,
        handler500,
    )
    from swing.error.views import (
        BaseErrorView,
        Handler400View,
        Handler401View,
        Handler403View,
        Handler404View,
        Handler405View,
        Handler408View,
        Handler410View,
        Handler429View,
        Handler500View,
    )


# =============================================================================
# Module metadata
# =============================================================================

__author__ = "Lars van Vianen"
__copyright__ = "Copyright (c) 2024 Scape Press"
__credits__ = ["Lars van Vianen"]
__license__ = "Proprietary"
__version__ = "1.1.0"
__maintainer__ = "Lars van Vianen"
__email__ = "lars@scape.press"
__status__ = "Alpha"

default_app_config = "swing.error.apps.SwingErrorConfig"


# =============================================================================
# Lazy-loaded public API
# =============================================================================

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    # Views
    "BaseErrorView": (
        "swing.error.views.view_error_handler_base",
        "BaseErrorView",
    ),
    "Handler400View": (
        "swing.error.views.view_error_handler_400",
        "Handler400View",
    ),
    "Handler401View": (
        "swing.error.views.view_error_handler_401",
        "Handler401View",
    ),
    "Handler403View": (
        "swing.error.views.view_error_handler_403",
        "Handler403View",
    ),
    "Handler404View": (
        "swing.error.views.view_error_handler_404",
        "Handler404View",
    ),
    "Handler405View": (
        "swing.error.views.view_error_handler_405",
        "Handler405View",
    ),
    "Handler408View": (
        "swing.error.views.view_error_handler_408",
        "Handler408View",
    ),
    "Handler410View": (
        "swing.error.views.view_error_handler_410",
        "Handler410View",
    ),
    "Handler429View": (
        "swing.error.views.view_error_handler_429",
        "Handler429View",
    ),
    "Handler500View": (
        "swing.error.views.view_error_handler_500",
        "Handler500View",
    ),
    # Responses
    "BaseErrorResponse": (
        "swing.error.responses.response_error_base",
        "BaseErrorResponse",
    ),
    "Http400Response": (
        "swing.error.responses.response_http_400",
        "Http400Response",
    ),
    "Http401Response": (
        "swing.error.responses.response_http_401",
        "Http401Response",
    ),
    "Http403Response": (
        "swing.error.responses.response_http_403",
        "Http403Response",
    ),
    "Http404Response": (
        "swing.error.responses.response_http_404",
        "Http404Response",
    ),
    "Http405Response": (
        "swing.error.responses.response_http_405",
        "Http405Response",
    ),
    "Http408Response": (
        "swing.error.responses.response_http_408",
        "Http408Response",
    ),
    "Http410Response": (
        "swing.error.responses.response_http_410",
        "Http410Response",
    ),
    "Http429Response": (
        "swing.error.responses.response_http_429",
        "Http429Response",
    ),
    "Http500Response": (
        "swing.error.responses.response_http_500",
        "Http500Response",
    ),
    # Middleware
    "ExceptionMiddleware": (
        "swing.error.middleware",
        "ExceptionMiddleware",
    ),
    # URL helpers
    "error_handlers": (
        "swing.error.urls.helpers",
        "error_handlers",
    ),
    "configure_error_handlers": (
        "swing.error.urls.helpers",
        "configure_error_handlers",
    ),
    "handler400": (
        "swing.error.urls",
        "handler400",
    ),
    "handler403": (
        "swing.error.urls",
        "handler403",
    ),
    "handler404": (
        "swing.error.urls",
        "handler404",
    ),
    "handler500": (
        "swing.error.urls",
        "handler500",
    ),
    # Configuration
    "get_error_config": (
        "swing.error.conf",
        "get_error_config",
    ),
    "DEFAULT_ERROR_SETTINGS": (
        "swing.error.conf",
        "DEFAULT_ERROR_SETTINGS",
    ),
}


def __getattr__(name: str) -> Any:
    """Lazy-load public API symbols on first access."""
    if name in _LAZY_IMPORTS:
        module_name, attr_name = _LAZY_IMPORTS[name]
        module = importlib.import_module(module_name)
        return getattr(module, attr_name)
    msg = f"module {__name__!r} has no attribute {name!r}"
    raise AttributeError(msg)


def __dir__() -> list[str]:
    """List available public API symbols."""
    return list(_LAZY_IMPORTS.keys()) + [
        "__version__",
        "__author__",
        "__email__",
        "default_app_config",
    ]


__all__: list[str] = list(_LAZY_IMPORTS.keys())
