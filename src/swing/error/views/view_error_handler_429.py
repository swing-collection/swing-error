# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides 429 Error Handler View Module
======================================

This module contains a class-based view for handling HTTP 429 Too Many Requests
errors in a Django application. It renders a custom template with error
details and sets the appropriate 429 status code in the response.
Additionally, it logs error details for debugging purposes.

Usage:
------
Include the `Handler429View` in your project's URL configuration for handling
429 errors. Add the following to your project's settings:

    HANDLER429 = 'swing.error.views.view_error_handler_429.Handler429View.as_view()'

Links:
------

"""

# =============================================================================
# Imports
# =============================================================================

# Import | Local
# Import | Local Modules
from ..responses.response_http_429 import Http429Response
from ..views.view_error_handler_base import BaseErrorView

# =============================================================================
# Classes
# =============================================================================


class Handler429View(BaseErrorView):
    """
    429 Error Handler View
    ======================

    Handles HTTP 429 Too Many Requests errors by rendering a custom template
    and using the Http429Response class.
    """

    error_type = "429"
    response_class = Http429Response


# =============================================================================
# Exports
# =============================================================================

# Callable handler for use in Django's handler settings
HANDLER429 = Handler429View.as_view()

__all__: list[str] = [
    "Handler429View",
    "HANDLER429",
]
