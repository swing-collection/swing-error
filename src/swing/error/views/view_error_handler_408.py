# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides 408 Error Handler View Module
======================================

This module contains a class-based view for handling HTTP 408 Request Timeout
errors in a Django application. It renders a custom template with error
details and sets the appropriate 408 status code in the response.
Additionally, it logs error details for debugging purposes.

Usage:
------
Include the `Handler408View` in your project's URL configuration for handling
408 errors. Add the following to your project's settings:

    HANDLER408 = 'swing.error.views.view_error_handler_408.Handler408View.as_view()'

Links:
------

"""

# =============================================================================
# Imports
# =============================================================================

# Import | Local Modules
from ..responses.response_http_408 import Http408Response
from ..views.view_error_handler_base import BaseErrorView

# =============================================================================
# Classes
# =============================================================================


class Handler408View(BaseErrorView):
    """
    408 Error Handler View
    ======================

    Handles HTTP 408 Request Timeout errors by rendering a custom template
    and using the Http408Response class.
    """

    error_type = "408"
    response_class = Http408Response


# =============================================================================
# Exports
# =============================================================================

HANDLER408 = "swing.error.views.view_error_handler_408.Handler408View"

__all__: list[str] = [
    "Handler408View",
    "HANDLER408",
]
