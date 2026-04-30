# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides HTTP 403 Response Class
=======================

This module defines a custom HTTP 403 response class for handling
HTTP 403 errors in a Django application. It extends the BaseErrorResponse
class for structured error handling and logging.

Usage:
------
Use this custom response class to return a 403 response with
additional functionality if needed.

Links:
------
- https://docs.djangoproject.com/en/stable/ref/request-response/

"""

# =============================================================================
# Imports
# =============================================================================

from typing import Any
from .response_error_base import BaseErrorResponse

# =============================================================================
# Class
# =============================================================================


class Http403Response(BaseErrorResponse):
    """
    HTTP 403 Response Class
    =======================

    Custom HTTP 403 response class.
    Extends BaseErrorResponse for structured error handling and logging.

    Attributes:
        status_code (int): HTTP status code (403).
        error_type (str): Error type identifier.
        default_message (str): Default message for this error.
    """

    status_code = 403
    error_type = "403"
    default_message = "Forbidden"

    def __init__(
        self,
        status_code: int | None = None,
        message: str | None = None,
        details: str | dict[str, Any] | None = None,
        request: Any | None = None,
        exception: Exception | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the Http403Response.

        Args:
            status_code (int | None): HTTP status code (uses class default if not provided).
            message (str | None): Error message (uses default if not provided).
            details (str | dict[str, Any] | None): Additional error details.
            request (Any | None): The HTTP request object.
            exception (Exception | None): The exception that caused this error.
            **kwargs: Additional arguments for BaseErrorResponse.
        """ 
        super().__init__(
            status_code=status_code or self.status_code,
            message=message or self.default_message,
            details=details,
            request=request,
            exception=exception,
            **kwargs,
        )


# =============================================================================
# Exports
# =============================================================================

__all__: list[str] = [
    "Http403Response",
]
