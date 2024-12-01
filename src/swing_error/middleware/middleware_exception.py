# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Provides Exception Middleware Class
===================================

This module provides middleware for global exception handling in a Django
application. The middleware captures unhandled exceptions and generates
structured error responses. It also handles specific HTTP status codes like
404 (Not Found) and can be extended for additional error handling as needed.

Usage:
------
Add the middleware to the `MIDDLEWARE` list in your `settings.py`:

MIDDLEWARE = [
    # other middleware
    'error_handler.middleware.ExceptionMiddleware',
]


"""  # noqa E501


# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
import logging
from typing import Callable, Any

# Import | Libraries
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import render

# Import | Local Modules
from ..responses import (
    Http400Response,
    Http401Response,
    Http403Response,
    Http404Response,
    Http500Response,
    # Add additional responses as needed
)

# =============================================================================
# Logger
# =============================================================================

logger = logging.getLogger(__name__)

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


    def __call__(self, request: HttpRequest) -> HttpResponse:
        """
        Handle the incoming request and capture unhandled exceptions.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            HttpResponse: The HTTP response, either from the next
                middleware/view or an error response in case of exceptions.
        """

        try:
            response = self.get_response(request)

            # Handle specific status codes dynamically
            if response.status_code == 400:
                return self.handle_custom_response(Http400Response, request)
            elif response.status_code == 401:
                return self.handle_custom_response(Http401Response, request)
            elif response.status_code == 403:
                return self.handle_custom_response(Http403Response, request)
            elif response.status_code == 404:
                return self.handle_custom_response(Http404Response, request)
            elif response.status_code == 500:
                return self.handle_custom_response(Http500Response, request)
            # Add additional status codes (405, 408, 410, 429) here

            return response

        except Exception as e:
            # Handle unexpected exceptions
            return self.handle_exception(e, request)


    def handle_custom_response(
        self,
        response_class: Callable[[HttpRequest], HttpResponse],
        request: HttpRequest
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
            f"Custom response for {response_class.status_code}: Path={request.path}"
        )
        return response_class(request=request)

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
            exc_info=True
        )

        # Return a JSON response with error details
        return JsonResponse(
            {
                "error": "Server Error",
                "message": "An unexpected error occurred. Please try again later."
            },
            status=500
        )