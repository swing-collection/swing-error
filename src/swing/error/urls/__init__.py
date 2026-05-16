# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Swing Error - URL Configuration
=================================

URL patterns and error handler exports for the swing.error app.

Usage
-----
In your project's urls.py:

    from swing.error.urls import (
        handler400,
        handler403,
        handler404,
        handler500,
    )

Or use the helper function:

    from swing.error.urls import error_handlers
    handlers = error_handlers()

Or configure all handlers at once:

    from swing.error.urls import configure_error_handlers
    configure_error_handlers()

"""

# Import | Future
from __future__ import annotations

# Import | Standard Library
from typing import TYPE_CHECKING

# Import | Django
from django.urls import URLPattern

# Import | Local
from swing.error.urls.helpers import configure_error_handlers, error_handlers
from swing.error.views import (
    HANDLER400,
    HANDLER401,
    HANDLER403,
    HANDLER404,
    HANDLER405,
    HANDLER408,
    HANDLER410,
    HANDLER429,
    HANDLER500,
)

if TYPE_CHECKING:
    pass  # pylint: disable=unnecessary-pass


app_name = "swing_error"

# URL patterns (empty - error handlers are configured separately)
urlpatterns: list[URLPattern] = []

# Error handler exports
handler400 = HANDLER400
handler401 = HANDLER401
handler403 = HANDLER403
handler404 = HANDLER404
handler405 = HANDLER405
handler408 = HANDLER408
handler410 = HANDLER410
handler429 = HANDLER429
handler500 = HANDLER500


__all__: list[str] = [
    "app_name",
    "urlpatterns",
    "handler400",
    "handler401",
    "handler403",
    "handler404",
    "handler405",
    "handler408",
    "handler410",
    "handler429",
    "handler500",
    "error_handlers",
    "configure_error_handlers",
]
