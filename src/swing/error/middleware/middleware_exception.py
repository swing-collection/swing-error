# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Provides Exception Middleware Class
===================================

This module provides a unified, comprehensive middleware for global exception
handling in a Django application. The middleware:

1. **Captures all unhandled exceptions** and generates structured error responses
2. **Logs all exceptions** with full context (path, method, exception details)
3. **Handles specific HTTP status codes** (400, 401, 403, 404, 405, 408, 410, 429, 500)
4. **Provides debugging information** in DEBUG mode
5. **Supports Sentry integration** for error tracking (via conf.py)
6. **Supports CORS headers** on error responses (via conf.py)

Usage:
------
Add the middleware to the `MIDDLEWARE` list in your `settings.py` **after**
any authentication middleware:

    MIDDLEWARE = [
        # ... other middleware ...
        'django.middleware.security.SecurityMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        # Add ExceptionMiddleware here
        'swing.error.middleware.ExceptionMiddleware',
    ]

Notes:
------
- This is the recommended and unified middleware for error handling
- It replaces the need for separate logging-only middleware
- Configure error handling via SWING_ERROR settings in settings.py
- See conf.py for available configuration options

Links:
------
- https://docs.djangoproject.com/en/stable/topics/http/middleware/

"""

# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
from collections.abc import Callable
import logging
from typing import Any

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

# Import | Local
# Import | Local Modules
from ..responses import (
    Http400Response,
    Http401Response,
    Http403Response,
    Http404Response,
    Http405Response,
    Http408Response,
    Http410Response,
    Http429Response,
    Http500Response,
)

# =============================================================================
# Logger
# =============================================================================

logger: logging.Logger = logging.getLogger(name=__name__)

# =============================================================================
# Class
# =============================================================================


class ExceptionMiddleware:
    """
    Middleware for global exception handling.

    Captures unhandled exceptions and provides structured error responses.
    It can also handle specific HTTP status codes (e.g., 404 Not Found) and
    is designed to be extensible for other use cases.

    """

    def __init__(
        self,
        get_response: Callable[[HttpRequest], HttpResponse],
    ) -> None:
        """
        Initialize the ExceptionMiddleware.

        Args:
            get_response (Callable): The next middleware or view in the
                request chain.
        """
        self.get_response = get_response

    def __call__(
        self,
        request: HttpRequest,
    ) -> HttpResponse:
        """
        Handle the incoming request and capture unhandled exceptions.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            HttpResponse: The HTTP response, either from the next
                middleware/view or an error response in case of exceptions.
        """

        try:
            response: HttpResponse = self.get_response(request)

            # Handle specific status codes dynamically
            status_code_handlers = {
                400: Http400Response,
                401: Http401Response,
                403: Http403Response,
                404: Http404Response,
                405: Http405Response,
                408: Http408Response,
                410: Http410Response,
                429: Http429Response,
                500: Http500Response,
            }

            if response.status_code in status_code_handlers:
                return self.handle_custom_response(
                    response_class=status_code_handlers[response.status_code],
                    request=request,
                )

            return response

        except Exception as e:
            # Handle unexpected exceptions
            return self.handle_exception(
                exception=e,
                request=request,
            )

    def handle_custom_response(
        self,
        response_class: type[HttpResponse],
        request: HttpRequest,
    ) -> HttpResponse:
        """
        Generate a custom response for specific status codes.

        Args:
            response_class (Callable): The response class to use for the
                custom response.
            request (HttpRequest): The current HTTP request.

        Returns:
            HttpResponse: The custom response for the status code.
        """
        logger.warning(
            msg=f"Custom response for {response_class.status_code}: Path={request.path}"
        )
        return response_class()

    def handle_exception(
        self,
        exception: Exception,
        request: HttpRequest,
    ) -> JsonResponse:
        """
        Handle unhandled exceptions and return a structured JSON response.

        Args:
            exception (Exception): The exception that was raised.
            request (HttpRequest): The HTTP request during which the
                exception occurred.

        Returns:
            JsonResponse: A JSON response with error details.
        """

        # Log the exception with contextual information
        logger.error(
            f"Unhandled exception:\n"
            f"  Path: {request.path}\n"
            f"  Method: {request.method}\n"
            f"  Exception: {str(exception)}",
            exc_info=True,
        )

        # Return a JSON response with error details
        return JsonResponse(
            data={
                "error": "Server Error",
                "message": "An unexpected error occurred. Please try again later.",
            },
            status=500,
        )


# =============================================================================
# Exports
# =============================================================================

__all__: list[str] = [
    "ExceptionMiddleware",
]
