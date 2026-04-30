# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Provides HTTP 408 Response Class
================================

This module defines a custom HTTP 408 Request Timeout response class for
handling HTTP 408 errors in a Django application. It extends the BaseErrorResponse
class for structured error handling and logging.

Usage:
------
Use this custom response class to return a 408 Request Timeout response with
additional functionality if needed.

Links:
------
- https://docs.djangoproject.com/en/stable/ref/urls/#django.conf.urls.handler408
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


class Http408Response(BaseErrorResponse):
    """
    HTTP 408 Response Class
    =======================

    Custom HTTP 408 Request Timeout response class.
    Extends the BaseErrorResponse for structured handling and logging.

    Attributes:
        status_code (int): HTTP status code for the response.
    """

    status_code = 408

    def __init__(
        self,
        *args: Any,
        message: str = "Request Timeout",
        details: str | dict[str, Any] | None = None,
        request: Any | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the Http408Response with optional message, details, and
        request.

        Args:
            *args: Additional positional arguments for the BaseErrorResponse.
            message (str): A brief description of the error
                (default: "Request Timeout").
            details (str | dict[str, Any] | None): Additional error details
                (default: None).
            request (Any | None): The HTTP request object for logging context
                (default: None).
            **kwargs: Additional keyword arguments for the BaseErrorResponse.
        """
        super().__init__(
            status_code=408,
            message=message,
            details=details,
            request=request,
            *args,
            **kwargs,
        )


# =============================================================================
# Exports
# =============================================================================

__all__: list[str] = [
    "Http408Response",
]
