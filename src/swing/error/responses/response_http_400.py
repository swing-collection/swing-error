# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides HTTP 400 Response Class
================================

This module defines a custom HTTP 400 Bad Request response class for handling
HTTP 400 errors in a Django application. It extends the BaseErrorResponse
class for structured error handling and logging.

Usage:
------
Use this custom response class to return a 400 Bad Request response with
additional functionality if needed.

Links:
------
- https://docs.djangoproject.com/en/stable/ref/urls/#django.conf.urls.handler400
- https://docs.djangoproject.com/en/stable/ref/request-response/#django.http.HttpResponseBadRequest

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
import logging
from typing import Any

# Import | Local Modules
from ..responses.response_error_base import BaseErrorResponse

# Import | Libraries


# =============================================================================
# Class
# =============================================================================


class Http400Response(BaseErrorResponse):
    """
    HTTP 400 Response Class
    =======================

    Custom HTTP 400 Bad Request response class.
    Extends the BaseErrorResponse for structured handling and logging.

    Attributes:
        status_code (int): HTTP status code for the response.
    """

    def __init__(
        self,
        *args: Any,
        message: str = "Bad Request",
        details: str | dict[str, Any] | None = None,
        request: Any | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the Http400Response with optional message, details, and
        request.

        Args:
            *args: Additional positional arguments for the BaseErrorResponse.
            message (str): A brief description of the error (default: "Bad Request").
            details (str | dict[str, Any] | None): Additional error details
                (default: None).
            request (Any | None): The HTTP request object for logging context
                (default: None).
            **kwargs: Additional keyword arguments for the BaseErrorResponse.
        """
        super().__init__(
            status_code=400,
            message=message,
            details=details,
            error_code=request,
            *args,
            **kwargs,
        )


# =============================================================================
# Exports
# =============================================================================

__all__: list[str] = [
    "Http400Response",
]
