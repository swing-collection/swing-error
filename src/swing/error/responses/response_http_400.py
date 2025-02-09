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
- https://docs.djangoproject.com/en/5.0/ref/urls/#django.conf.urls.handler400
- https://docs.djangoproject.com/en/5.0/ref/request-response/#django.http.HttpResponseBadRequest

"""  # noqa E501


# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
import logging
from typing import Any, Optional, Union, Dict

# Import | Libraries
from django.http import HttpResponseBadRequest

# Import | Local Modules
from swing_error.responses.response_error_base import BaseErrorResponse


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
        details: Optional[Union[str, Dict[str, Any]]] = None,
        request: Optional[Any] = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the Http400Response with optional message, details, and
        request.

        Args:
            *args: Additional positional arguments for the BaseErrorResponse.
            message (str): A brief description of the error (default: "Bad Request").
            details (Optional[Union[str, Dict[str, Any]]]): Additional error details
                (default: None).
            request (Optional[Any]): The HTTP request object for logging context
                (default: None).
            **kwargs: Additional keyword arguments for the BaseErrorResponse.
        """
        super().__init__(
            400,
            message,
            details,
            request,
            *args,
            **kwargs,
        )


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    "Http400Response",
]
