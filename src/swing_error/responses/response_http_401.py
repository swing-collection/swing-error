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

    def __init__(
        self, content: Union[bytes, str] = b'', *args: Any, **kwargs: Any) -> None:
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
        logger.error(
            f"401 Unauthorized: Response initialized with content: {self.content}"
        )


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    "Http401Response",
]


# # -*- coding: utf-8 -*-
# """
# Custom HTTP 401 Response Class
# ==============================

# This module defines a custom HTTP 401 Unauthorized response class for handling
# HTTP 401 errors in a Django application. It extends Django's HttpResponse class
# with enhanced logging and JSON content support.

# Usage:
# ------
# Use this custom response class to return a 401 Unauthorized response with
# optional JSON content and enhanced logging.

# Links:
# ------
# - https://docs.djangoproject.com/en/5.0/ref/urls/#django.conf.urls.handler401
# - https://docs.djangoproject.com/en/5.0/ref/request-response/#django.http.HttpResponse

# """

# import json
# import logging
# from typing import Any, Dict, Optional, Union
# from django.http import HttpResponse


# class Http401Response(HttpResponse):
#     """
#     HTTP 401 Response Class
#     =======================

#     A custom HTTP 401 Unauthorized response class that provides enhanced
#     logging and JSON content support. Inherits from Django's HttpResponse.

#     Attributes:
#         status_code (int): HTTP status code for the response (401).
#     """

#     status_code = 401

#     def __init__(
#         self,
#         content: Optional[Union[str, Dict[str, Any]]] = None,
#         log_level: int = logging.ERROR,
#         request: Optional[Any] = None,
#         *args: Any,
#         **kwargs: Any
#     ) -> None:
#         """
#         Initialize the Http401Response with optional content, log level, and request details.

#         Args:
#             content (str or dict, optional): The content to include in the response body.
#                 Can be plain text or a JSON serializable dictionary.
#             log_level (int, optional): Logging level. Defaults to logging.ERROR.
#             request (HttpRequest, optional): The HTTP request object for logging context.
#             *args: Additional positional arguments.
#             **kwargs: Additional keyword arguments.
#         """
#         if isinstance(content, dict):
#             content = json.dumps(content)
#             kwargs.setdefault('content_type', 'application/json')
#         elif content is None:
#             content = "Unauthorized"

#         super().__init__(content, *args, **kwargs)
#         self.log_error(content, log_level, request)

#     def log_error(self, content: str, log_level: int, request: Optional[Any]) -> None:
#         """
#         Log the error details for debugging purposes.

#         Args:
#             content (str): The response content.
#             log_level (int): Logging level.
#             request (HttpRequest, optional): The HTTP request object for additional context.
#         """
#         logger = logging.getLogger(__name__)

#         if request:
#             logger.log(
#                 log_level,
#                 f"401 Unauthorized: {content}\nRequest Path: {request.path}\n"
#                 f"Method: {request.method}\nData: {getattr(request, 'body', None)}"
#             )
#         else:
#             logger.log(log_level, f"401 Unauthorized: {content}")


# # =============================================================================
# # Exports
# # =============================================================================

# __all__ = ["Http401Response"]