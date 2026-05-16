# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides 500 Error Handler View Module
======================================

This module contains a class-based view for handling HTTP 500 Internal Server Error
errors in a Django application. It renders a custom template with error
details and sets the appropriate 500 status code in the response.
Additionally, it logs error details for debugging purposes.

Usage:
------
Include the `Handler500View` in your project's URL configuration for handling
500 errors. Add the following to your project's settings:

    HANDLER500 = 'swing.error.views.view_error_handler_500.Handler500View.as_view()'

Links:
------

"""

# =============================================================================
# Imports
# =============================================================================

# Import | Local
# Import | Local Modules
from ..responses.response_http_500 import Http500Response
from ..views.view_error_handler_base import BaseErrorView

# =============================================================================
# Classes
# =============================================================================


class Handler500View(BaseErrorView):
    """
    500 Error Handler View
    ======================

    Handles HTTP 500 Internal Server Error errors by rendering a custom template
    and using the Http500Response class.
    """

    error_type = "500"
    response_class = Http500Response


# =============================================================================
# Exports
# =============================================================================

# Callable handler for use in Django's handler500 setting
HANDLER500 = Handler500View.as_view()

__all__: list[str] = [
    "Handler500View",
    "HANDLER500",
]
