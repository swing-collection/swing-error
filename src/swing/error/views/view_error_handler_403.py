# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides 403 Error Handler View Module
======================================

This module contains a class-based view for handling HTTP 403 Forbidden
errors in a Django application. It renders a custom template with error
details and sets the appropriate 403 status code in the response.
Additionally, it logs error details for debugging purposes.

Usage:
------
Include the `Handler403View` in your project's URL configuration for handling
403 errors. Add the following to your project's settings:

    HANDLER403 = 'swing.error.views.view_error_handler_403.Handler403View.as_view()'

Links:
------

"""

# =============================================================================
# Imports
# =============================================================================

# Import | Local Modules
from ..responses.response_http_403 import Http403Response
from ..views.view_error_handler_base import BaseErrorView

# =============================================================================
# Classes
# =============================================================================


class Handler403View(BaseErrorView):
    """
    403 Error Handler View
    ======================

    Handles HTTP 403 Forbidden errors by rendering a custom template
    and using the Http403Response class.
    """

    error_type = "403"
    response_class = Http403Response


# =============================================================================
# Exports
# =============================================================================

HANDLER403 = "swing.error.views.view_error_handler_403.Handler403View"

__all__: list[str] = [
    "Handler403View",
    "HANDLER403",
]
