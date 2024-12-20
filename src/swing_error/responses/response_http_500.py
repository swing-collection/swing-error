# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Provides HTTP 500 Response Class
================================

This module defines a custom HTTP 500 Internal Server Error response class for
handling HTTP 500 errors in a Django application. It inherits from Django's
HttpResponse class.

Usage:
------
Use this custom response class to return a 500 Internal Server Error response with
additional functionality if needed.

Links:
------
- https://docs.djangoproject.com/en/5.0/ref/urls/#django.conf.urls.handler500
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

class Http500Response(HttpResponse):
    """
    HTTP 500 Response Class
    =======================

    Custom HTTP 500 Internal Server Error response class.
    Inherits from Django's HttpResponse.

    Attributes:
        status_code (int): HTTP status code for the response.
    """

    status_code = 500

    def __init__(
        self,
        content: Union[bytes, str] = b'',
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the Http500Response with optional content, args, and kwargs.

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
            f"500 Internal Server Error: Response initialized with content: {self.content}"
        )


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    "Http500Response",
]
