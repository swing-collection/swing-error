# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides 401 Error Handler View Module
======================================

This module contains a class-based view for handling HTTP 401 Unauthorized
errors in a Django application. It renders a custom template with error
details and sets the appropriate 401 status code in the response.
Additionally, it logs error details for debugging purposes.

Usage:
------
Include the `Handler401View` in your project's URL configuration for handling
401 errors. Add the following to your project's settings:

    HANDLER401 = 'swing.error.views.view_error_handler_401.Handler401View.as_view()'

Links:
------

"""

# =============================================================================
# Imports
# =============================================================================

# Import | Local Modules
from ..responses.response_http_401 import Http401Response
from ..views.view_error_handler_base import BaseErrorView

# =============================================================================
# Classes
# =============================================================================


class Handler401View(BaseErrorView):
    """
    401 Error Handler View
    ======================

    Handles HTTP 401 Unauthorized errors by rendering a custom template
    and using the Http401Response class.
    """

    error_type = "401"
    response_class = Http401Response


# =============================================================================
# Exports
# =============================================================================

HANDLER401 = "swing.error.views.view_error_handler_401.Handler401View"

__all__: list[str] = [
    "Handler401View",
    "HANDLER401",
]
