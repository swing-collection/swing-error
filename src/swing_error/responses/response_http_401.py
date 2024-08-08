# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Provides HTTP 401 Response Class
================================

This module defines a custom HTTP 401 Unauthorized response class for handling
HTTP 401 errors in a Django application. It inherits from Django's
HttpResponse class.

Usage:
------
Use this custom response class to return a 401 Unauthorized response with
additional functionality if needed.

Links:
------
- https://docs.djangoproject.com/en/5.0/ref/urls/#django.conf.urls.handler401
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

class Http401Response(HttpResponse):
    """
    HTTP 401 Response Class
    =======================

    Custom HTTP 401 Unauthorized response class.
    Inherits from Django's HttpResponse.

    Attributes:
        status_code (int): HTTP status code for the response.
    """

    status_code = 401

    def __init__(self, content: Union[bytes, str] = b'', *args: Any, **kwargs: Any) -> None:
        """
        Initialize the Http401Response with optional content, args, and kwargs.

        Args:
            content (bytes or str): The content to include in the response body.
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
        logger.error(f"401 Unauthorized: Response initialized with content: {self.content}")


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    "Http401Response",
]