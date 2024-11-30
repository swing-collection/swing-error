# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides HTTP 400 Response Class
================================

This module defines a custom HTTP 400 Bad Request response class for handling
HTTP 400 errors in a Django application. It inherits from Django's
HttpResponseBadRequest class.

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
from typing import Any, Optional, Union

# Import | Libraries
from django.http import HttpResponseBadRequest

# Import | Local Modules
# None


# =============================================================================
# Class
# =============================================================================

class Http400Response(HttpResponseBadRequest):
    """
    HTTP 400 Response Class
    =======================

    Custom HTTP 400 Bad Request response class.
    Inherits from Django's HttpResponseBadRequest.

    Attributes:
        status_code (int): HTTP status code for the response.
    """

    status_code = 400

    def __init__(
        self,
        content: Union[bytes, str] = b'',
        *args: Any,
        **kwargs: Any
    ) -> None:
        """
        Initialize the Http400Response with optional content, args, and kwargs.

        Args:
            content (bytes or str): The content to include in the response
                body.
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
            f"400 Bad Request: Response initialized with content: {self.content}"
        )


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    "Http400Response",
]
