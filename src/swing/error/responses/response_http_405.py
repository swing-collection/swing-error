# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Provides HTTP 405 Response Class
================================

This module defines a custom HTTP 405 Method Not Allowed response class for
handling HTTP 405 errors in a Django application. It extends the BaseErrorResponse
class for structured error handling and logging.

Usage:
------
Use this custom response class to return a 405 Method Not Allowed response with
additional functionality if needed.

Links:
------
- https://docs.djangoproject.com/en/stable/ref/urls/#django.conf.urls.handler405
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


class Http405Response(BaseErrorResponse):
    """
    HTTP 405 Response Class
    =======================

    Custom HTTP 405 Method Not Allowed response class.
    Extends the BaseErrorResponse for structured handling and logging.

    Attributes:
        status_code (int): HTTP status code for the response.
    """

    status_code = 405

    def __init__(
        self,
        *args: Any,
        message: str = "Method Not Allowed",
        details: str | dict[str, Any] | None = None,
        request: Any | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the Http405Response with optional message, details, and
        request.

        Args:
            *args: Additional positional arguments for the BaseErrorResponse.
            message (str): A brief description of the error
                (default: "Method Not Allowed").
            details (str | dict[str, Any] | None): Additional error details
                (default: None).
            request (Any | None): The HTTP request object for logging context
                (default: None).
            **kwargs: Additional keyword arguments for the BaseErrorResponse.
        """
        super().__init__(
            status_code=405,
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
    "Http405Response",
]
