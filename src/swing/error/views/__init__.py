# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Swing Error - Views Package
=============================

Class-based views for handling HTTP error responses.

Each error handler view extends BaseErrorView and provides:
- Custom template rendering
- Configurable error messages via settings
- Structured error responses
- Optional error logging

Supported Error Codes:
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
Configure in settings.py:

    HANDLER404 = 'swing.error.views.Handler404View'

Or import and use directly:

    from swing.error import Handler404View

    class MyCustom404View(Handler404View):
        template_name = "myapp/404.html"

"""

# =============================================================================
# Imports
# =============================================================================

from swing.error.views.view_error_handler_400 import HANDLER400, Handler400View
from swing.error.views.view_error_handler_401 import HANDLER401, Handler401View
from swing.error.views.view_error_handler_403 import HANDLER403, Handler403View
from swing.error.views.view_error_handler_404 import HANDLER404, Handler404View
from swing.error.views.view_error_handler_405 import HANDLER405, Handler405View
from swing.error.views.view_error_handler_408 import HANDLER408, Handler408View
from swing.error.views.view_error_handler_410 import HANDLER410, Handler410View
from swing.error.views.view_error_handler_429 import HANDLER429, Handler429View
from swing.error.views.view_error_handler_500 import HANDLER500, Handler500View
from swing.error.views.view_error_handler_base import BaseErrorView

__all__ = [
    # Base class
    "BaseErrorView",
    # View classes
    "Handler400View",
    "Handler401View",
    "Handler403View",
    "Handler404View",
    "Handler405View",
    "Handler408View",
    "Handler410View",
    "Handler429View",
    "Handler500View",
    # Handler path strings
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
