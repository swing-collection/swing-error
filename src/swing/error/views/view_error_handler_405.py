# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides 405 Error Handler View Module
======================================

This module contains a class-based view for handling HTTP 405 Method Not Allowed
errors in a Django application. It renders a custom template with error
details and sets the appropriate 405 status code in the response.
Additionally, it logs error details for debugging purposes.

Usage:
------
Include the `Handler405View` in your project's URL configuration for handling
405 errors. Add the following to your project's settings:

    HANDLER405 = 'swing.error.views.view_error_handler_405.Handler405View.as_view()'

Links:
------

"""

# =============================================================================
# Imports
# =============================================================================

# Import | Local Modules
from ..responses.response_http_405 import Http405Response
from ..views.view_error_handler_base import BaseErrorView

# =============================================================================
# Classes
# =============================================================================


class Handler405View(BaseErrorView):
    """
    405 Error Handler View
    ======================

    Handles HTTP 405 Method Not Allowed errors by rendering a custom template
    and using the Http405Response class.
    """

    error_type = "405"
    response_class = Http405Response


# =============================================================================
# Exports
# =============================================================================

HANDLER405 = "swing.error.views.view_error_handler_405.Handler405View"

__all__: list[str] = [
    "Handler405View",
    "HANDLER405",
]
