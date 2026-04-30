# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Provides HTTP 429 Response Class
================================

This module defines a custom HTTP 429 Too Many Requests response class for
handling HTTP 429 errors in a Django application. It extends the BaseErrorResponse
class for structured error handling and logging.

Usage:
------
Use this custom response class to return a 429 Too Many Requests response with
additional functionality if needed.

Links:
------
- https://docs.djangoproject.com/en/stable/ref/urls/#django.conf.urls.handler429
- https://docs.djangoproject.com/en/stable/ref/request-response/#django.http.HttpResponse

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
from typing import Any

# Import | Local Modules
from .response_error_base import BaseErrorResponse


# =============================================================================
# Class
# =============================================================================


class Http429Response(BaseErrorResponse):
    """
    HTTP 429 Response Class
    =======================

    Custom HTTP 429 Too Many Requests response class.
    Extends the BaseErrorResponse for structured handling and logging.

    Attributes:
        status_code (int): HTTP status code for the response.
    """

    status_code = 429

    def __init__(
        self,
        *args: Any,
        message: str = "Too Many Requests",
        details: str | dict[str, Any] | None = None,
        request: Any | None = None,
        retry_after: int | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the Http429Response with optional message, details, and
        request.

        Args:
            *args: Additional positional arguments for the BaseErrorResponse.
            message (str): A brief description of the error
                (default: "Too Many Requests").
            details (str | dict[str, Any] | None): Additional error details
                (default: None).
            request (Any | None): The HTTP request object for logging context
                (default: None).
            retry_after (int | None): Number of seconds until the client
                should retry (default: None).
            **kwargs: Additional keyword arguments for the BaseErrorResponse.
        """
        super().__init__(
            status_code=429,
            message=message,
            details=details,
            request=request,
            *args,
            **kwargs,
        )
        # Add Retry-After header if specified
        if retry_after is not None:
            self["Retry-After"] = str(retry_after)


# =============================================================================
# Exports
# =============================================================================

__all__: list[str] = [
    "Http429Response",
]
