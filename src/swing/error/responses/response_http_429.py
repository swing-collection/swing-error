# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides HTTP 429 Response Class
=======================

This module defines a custom HTTP 429 response class for handling
HTTP 429 errors in a Django application. It extends the BaseErrorResponse
class for structured error handling and logging.

Usage:
------
Use this custom response class to return a 429 response with
additional functionality if needed.

Links:
------
- https://docs.djangoproject.com/en/stable/ref/request-response/

"""

# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
from typing import Any

# Import | Local
from .detect_retry_after import detect_retry_after
from .response_error_base import BaseErrorResponse

# =============================================================================
# Class
# =============================================================================


class Http429Response(BaseErrorResponse):
    """
    HTTP 429 Response Class
    =======================

    Custom HTTP 429 response class.
    Extends BaseErrorResponse for structured error handling and logging.

    Attributes:
        status_code (int): HTTP status code (429).
        error_type (str): Error type identifier.
        default_message (str): Default message for this error.
    """

    status_code = 429
    error_type = "429"
    default_message = "Too Many Requests"

    def __init__(
        self,
        status_code: int | None = None,
        message: str | None = None,
        details: str | dict[str, Any] | None = None,
        request: Any | None = None,
        exception: Exception | None = None,
        retry_after: int | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the Http429Response.

        Args:
            status_code (int | None): HTTP status code (uses class default if not provided).
            message (str | None): Error message (uses default if not provided).
            details (str | dict[str, Any] | None): Additional error details.
            request (Any | None): The HTTP request object.
            exception (Exception | None): The exception that caused this error.
            retry_after (int | None): Seconds to wait before retrying.
            **kwargs: Additional arguments for BaseErrorResponse.
        """
        # Handle retry_after separately since it's a header, not part of kwargs
        self.retry_after = retry_after or detect_retry_after(
            exception=exception,
            request=request,
        )
        super().__init__(
            status_code=status_code or self.status_code,
            message=message or self.default_message,
            details=details,
            request=request,
            exception=exception,
            **kwargs,
        )
        # Set Retry-After header if provided
        if self.retry_after is not None:
            self["Retry-After"] = str(self.retry_after)


# =============================================================================
# Exports
# =============================================================================

__all__: list[str] = [
    "Http429Response",
]
