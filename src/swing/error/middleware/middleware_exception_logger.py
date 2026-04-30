# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Provides Exception Logger Middleware Class
==========================================


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
    """Middleware for logging exceptions."""

    def __init__(
        self,
        get_response: Callable[[HttpRequest], HttpResponse],
    ) -> None:
        """Initialize the middleware."""
        self.get_response = get_response
        self.logger: logging.Logger = logging.getLogger("django")

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """ """
        response = self.get_response(request)
        return response

    def process_exception(
        self,
        request: HttpRequest,
        exception: Exception,
    ) -> None:
        """Log the exception that occurred during request processing."""
        del request
        self.logger.exception(str(object=exception))


# =============================================================================
# Exports
# =============================================================================

__all__: list[str] = [
    "ExceptionLoggerMiddleware",
]
