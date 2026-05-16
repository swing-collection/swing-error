# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Swing Error - URL Helpers
===========================

Helper functions for configuring error handlers in Django projects.
"""

# Import | Future
from __future__ import annotations

# Import | Standard Library
from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    pass


def error_handlers() -> dict[str, Callable[..., Any]]:
    """Return a dictionary of error handler callables.

    Use this to configure Django's error handlers in urls.py:

        from swing.error.urls import error_handlers
        handlers = error_handlers()
        handler400 = handlers["400"]
        handler403 = handlers["403"]
        handler404 = handlers["404"]
        handler500 = handlers["500"]

    Or use the simpler configure function:

        from swing.error.urls import configure_error_handlers
        configure_error_handlers()

    Returns:
        Dictionary mapping status codes to handler view callables.

    """
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

    return {
        "400": HANDLER400,
        "401": HANDLER401,
        "403": HANDLER403,
        "404": HANDLER404,
        "405": HANDLER405,
        "408": HANDLER408,
        "410": HANDLER410,
        "429": HANDLER429,
        "500": HANDLER500,
    }


def configure_error_handlers() -> None:
    """Configure Django's global error handlers.

    Call this function in your project's urls.py to automatically
    set up all error handlers:

        from swing.error.urls import configure_error_handlers
        configure_error_handlers()

    This sets the module-level handler400, handler403, handler404,
    and handler500 variables that Django looks for.

    """
    import sys

    from swing.error.views import (
        HANDLER400,
        HANDLER403,
        HANDLER404,
        HANDLER500,
    )

    # Get the calling module (typically urls.py)
    frame = sys._getframe(1)
    calling_module = frame.f_globals

    # Set the handler variables
    calling_module["handler400"] = HANDLER400
    calling_module["handler403"] = HANDLER403
    calling_module["handler404"] = HANDLER404
    calling_module["handler500"] = HANDLER500


__all__: list[str] = [
    "error_handlers",
    "configure_error_handlers",
]
