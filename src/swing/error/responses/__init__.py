# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Error Response Module
=====================

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

    Http404 = 'myapp.views.Handler404View.as_view()'

Ensure you have a template at the specified `template_name` location for each
handler.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Local Modules
from .response_http_400 import Http400Response
from .response_http_401 import Http401Response
from .response_http_403 import Http403Response
from .response_http_404 import Http404Response
from .response_http_405 import Http405Response
from .response_http_408 import Http408Response
from .response_http_410 import Http410Response
from .response_http_429 import Http429Response
from .response_http_500 import Http500Response

__all__ = [
    "Http400Response",
    "Http401Response",
    "Http403Response",
    "Http404Response",
    "Http405Response",
    "Http408Response",
    "Http410Response",
    "Http429Response",
    "Http500Response",
]
