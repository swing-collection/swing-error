# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides 410 Error Handler View Module
======================================

This module contains a class-based view for handling HTTP 410 Gone
errors in a Django application. It renders a custom template with error
details and sets the appropriate 410 status code in the response.
Additionally, it logs error details for debugging purposes.

Usage:
------
Include the `Handler410View` in your project's URL configuration for handling
410 errors. Add the following to your project's settings:

    HANDLER410 = 'swing.error.views.view_error_handler_410.Handler410View.as_view()'

Links:
------

"""

# =============================================================================
# Imports
# =============================================================================

# Import | Local
# Import | Local Modules
from ..responses.response_http_410 import Http410Response
from ..views.view_error_handler_base import BaseErrorView

# =============================================================================
# Classes
# =============================================================================


class Handler410View(BaseErrorView):
    """
    410 Error Handler View
    ======================

    Handles HTTP 410 Gone errors by rendering a custom template
    and using the Http410Response class.
    """

    error_type = "410"
    response_class = Http410Response


# =============================================================================
# Exports
# =============================================================================

HANDLER410 = "swing.error.views.view_error_handler_410.Handler410View"

__all__: list[str] = [
    "Handler410View",
    "HANDLER410",
]
