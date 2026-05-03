# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Provides Optional Exception Logger Middleware
==============================================

A lightweight, optional middleware for logging uncaught request exceptions
without modifying the error response.

**Role & Decision:**
This middleware is kept as an OPT-IN alternative to `ExceptionMiddleware` for
projects that want simple logging-only behavior without structured error
response transformation. It:

- Logs all unhandled exceptions using Django's configured logger
- Does NOT modify the request/response flow
- Does NOT return structured error responses
- Complements `ExceptionMiddleware` for audit trails

**When to Use:**
- Projects using `ExceptionMiddleware` for error handling who also want
  centralized exception logging for compliance/audit purposes
- Custom error handling where you want raw exception logs without
  response transformation
- Debug/development environments requiring comprehensive exception traces

**When NOT to Use:**
- Use `ExceptionMiddleware` instead if you want structured error responses
- For typical production setups, `ExceptionMiddleware` provides all needed
  functionality (logs + responses)

**Usage:**
Add to `MIDDLEWARE` list in `settings.py` (optional, in addition to
`ExceptionMiddleware`):

    MIDDLEWARE = [
        # ... other middleware ...
        'swing.error.middleware.ExceptionMiddleware',  # For responses
        'swing.error.middleware.ExceptionLoggerMiddleware',  # Optional: For logs
    ]

**Note:**
This middleware is entirely optional. `ExceptionMiddleware` already logs
exceptions by default. Use this only if you need redundant logging or
integration with specific logging backends.
"""

# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
from collections.abc import Callable
import logging

from django.http import HttpRequest, HttpResponse

# Import | Local Modules


# =============================================================================
# Logger
# =============================================================================

logger: logging.Logger = logging.getLogger(name=__name__)

# =============================================================================
# Class
# =============================================================================


class ExceptionLoggerMiddleware:
    """Log unhandled exceptions through Django's configured logger."""

    def __init__(
        self,
        get_response: Callable[[HttpRequest], HttpResponse],
    ) -> None:
        """Store the downstream request handler used by Django."""
        self.get_response = get_response
        self.logger: logging.Logger = logging.getLogger("django")

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Delegate request handling to the next middleware or view."""
        response = self.get_response(request)
        return response

    def process_exception(
        self,
        request: HttpRequest,
        exception: Exception,
    ) -> None:
        """Record an exception raised while processing the request."""
        del request
        self.logger.exception(str(object=exception))


# =============================================================================
# Exports
# =============================================================================

__all__: list[str] = [
    "ExceptionLoggerMiddleware",
]
