# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Provides HTTP 429 Response Class
================================

This module defines a custom HTTP 429 Too Many Requests response class for
handling HTTP 429 errors in a Django application. It inherits from Django's
HttpResponse class.

Usage:
------
Use this custom response class to return a 429 Too Many Requests response with
additional functionality if needed.

Links:
------
- https://docs.djangoproject.com/en/5.0/ref/urls/#django.conf.urls.handler429
- https://docs.djangoproject.com/en/5.0/ref/request-response/#django.http.HttpResponse

"""  # noqa E501


# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
import logging
from typing import Any, Union

# Import | Libraries
from django.http import HttpResponse

# Import | Local Modules
# None


# =============================================================================
# Class
# =============================================================================

class Http429Response(HttpResponse):
    """
    HTTP 429 Response Class
    =======================

    Custom HTTP 429 Too Many Requests response class.
    Inherits from Django's HttpResponse.

    Attributes:
        status_code (int): HTTP status code for the response.
    """

    status_code = 429

    def __init__(
        self,
        content: Union[bytes, str] = b'',
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the Http429Response with optional content, args, and kwargs.

        Args:
            content (bytes or str): The content to include in the
                response body.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(content, *args, **kwargs)
        self.log_error()

    def log_error(self) -> None:
        """
        Log the error details for debugging purposes.
        """
        logger = logging.getLogger(__name__)
        logger.error(
            f"429 Too Many Requests: Response initialized with content: {self.content}"
        )


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    "Http429Response",
]
