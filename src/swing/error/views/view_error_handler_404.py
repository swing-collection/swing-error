# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides 404 Error Handler View Module
======================================

This module contains a class-based view for handling HTTP 404 Not Found
errors in a Django application. It renders a custom template with error
details and sets the appropriate 404 status code in the response.
Additionally, it logs error details for debugging purposes.

Usage:
------
Include the `Handler404View` in your project's URL configuration for handling
404 errors. Add the following to your project's settings:

    HANDLER404 = 'swing.error.views.view_error_handler_404.Handler404View.as_view()'

Links:
------

"""

# =============================================================================
# Imports
# =============================================================================

# Import | Local
# Import | Local Modules
from ..responses.response_http_404 import Http404Response
from ..views.view_error_handler_base import BaseErrorView

# =============================================================================
# Classes
# =============================================================================


class Handler404View(BaseErrorView):
    """
    404 Error Handler View
    ======================

    Handles HTTP 404 Not Found errors by rendering a custom template
    and using the Http404Response class.
    """

    error_type = "404"
    response_class = Http404Response


# =============================================================================
# Exports
# =============================================================================

HANDLER404 = "swing.error.views.view_error_handler_404.Handler404View"

__all__: list[str] = [
    "Handler404View",
    "HANDLER404",
]
