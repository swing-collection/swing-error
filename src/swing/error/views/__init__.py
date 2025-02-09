# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Error Handler Views Module
==========================

This module aggregates all the custom error handler views for different HTTP
status codes in a Django application. Each handler renders a custom template 
with error details and sets the appropriate status code in the response. 
Additionally, they log error details for debugging purposes.

The following error handlers are included:
- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 405 Method Not Allowed
- 408 Request Timeout
- 410 Gone
- 429 Too Many Requests
- 500 Internal Server Error

Usage:
------
Include the desired error handler in your project's URL configuration for
handling specific errors. Add the following to your project's settings, for
example:

    HANDLER404 = 'myapp.views.Handler404View.as_view()'

Ensure you have a template at the specified `template_name` location for each
handler.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Local Modules
from .view_error_handler_400 import HANDLER400
from .view_error_handler_401 import HANDLER401
from .view_error_handler_403 import HANDLER403
from .view_error_handler_404 import HANDLER404
from .view_error_handler_405 import HANDLER405
from .view_error_handler_408 import HANDLER408
from .view_error_handler_410 import HANDLER410
from .view_error_handler_429 import HANDLER429
from .view_error_handler_500 import HANDLER500

__all__ = [
    "HANDLER400",
    "HANDLER401",
    "HANDLER403",
    "HANDLER404",
    "HANDLER405",
    "HANDLER408",
    "HANDLER410",
    "HANDLER429",
    "HANDLER500",
]