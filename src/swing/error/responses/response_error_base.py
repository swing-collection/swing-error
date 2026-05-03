# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides Base Error Response Class
==================================

This module provides a base class for HTTP error responses, offering
structured JSON formatting, logging, CORS support, error tracking integration,
and extensibility for custom error handling in Django applications.

Usage:
------
Use this class as a base for defining specific HTTP error response classes,
such as 400 Bad Request, 404 Not Found, or 500 Internal Server Error.

Example:
--------
from error_handler.responses import BaseErrorResponse

def handle_error(request):
    return BaseErrorResponse(
        status_code=400,
        message="Bad Request",
        details={"field": "Invalid input"},
        request=request
    )

Links:
------
- https://docs.djangoproject.com/en/stable/ref/urls/#django.conf.urls.handler400
- https://docs.djangoproject.com/en/stable/ref/request-response/#django.http.HttpResponseBadRequest

"""

# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
import logging
from typing import Any, TypeAlias

from django.http import HttpRequest, HttpResponse

# Import | Local
# Import | Local Modules
from .._utils.scrub_sensitive_data import scrub_sensitive_data
from ..conf import (
    add_cors_headers,
    add_security_headers,
    capture_error,
    get_debug_info,
)
from .._utils.get_accept_header import get_accept_header
from .._utils.get_preferred_content_type import get_preferred_content_type
from .renderers import get_renderer

# =============================================================================
# Logger
# =============================================================================

# Configure logger
logger: logging.Logger = logging.getLogger(name=__name__)

ErrorDetails: TypeAlias = str | dict[str, Any] | list[Any] | None


# =============================================================================
# Class
# =============================================================================


class BaseErrorResponse(HttpResponse):
    """
    Base Error Response Class
    =========================

    A base class for HTTP error responses, providing structured JSON
    formatting, logging, CORS headers, error tracking, and extensibility.

    Attributes:
        status_code (int): HTTP status code for the response.
        message (str): Short description of the error.
        details (str | dict[str, Any] | None): Additional details
            about the error.
        error_code (str | None): Optional application-specific error code.
        request (HttpRequest | None): The HTTP request object, used for
            logging and CORS.

    Features:
        - Structured JSON error responses
        - Automatic CORS headers (when enabled in settings)
        - Sentry/error tracking integration (when enabled)
        - Debug mode with stack traces and request info
        - Comprehensive logging

    """

    def __init__(
        self,
        status_code: int,
        message: str,
        details: ErrorDetails = None,
        error_code: str | None = None,
        request: HttpRequest | None = None,
        exception: Exception | None = None,
        include_debug: bool = True,
        renderer: str | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the BaseErrorResponse.

        Args:
            status_code (int): The HTTP status code for the error response.
            message (str): A brief message describing the error.
            details (str | dict[str, Any] | list | None): Additional
                error details (default: None).
            error_code (str | None): Optional application-specific error
                code (default: None).
            request (HttpRequest | None): The HTTP request object for
                logging context (default: None).
            exception (Exception | None): The exception that caused this
                error (default: None). Used for error tracking and debug info.
            include_debug (bool): Whether to include debug info when in
                DEBUG mode (default: True).
            *args: Additional positional arguments for JsonResponse.
            **kwargs: Additional keyword arguments for JsonResponse.

        """

        # Get debug information if applicable
        debug_info: dict[str, Any] = {}
        if include_debug:
            debug_info = get_debug_info(exception=exception, request=request)

        # Prepare the structured content for the error response.
        # `to_dict` method formats the message, details, and optional error
        # code into a consistent dictionary structure for the response body.
        content: dict[str, Any] = self.to_dict(
            message=message,
            details=details,
            error_code=error_code,
            debug_info=debug_info,
            request=request,
            status_code=status_code,
        )

        renderer_name = renderer or self.get_renderer_name(request=request)
        rendered_content, content_type = get_renderer(renderer_name)(
            content,
            status_code,
        )

        clean_kwargs = {
            key: value
            for key, value in kwargs.items()
            if key not in {"data", "content_type"}
        }
        super().__init__(
            content=rendered_content,
            status=status_code,
            content_type=content_type,
            *args,
            **clean_kwargs,
        )

        # Add CORS headers if enabled
        add_cors_headers(response=self, request=request)
        add_security_headers(response=self)

        # Add error code header if provided
        if error_code:
            self["X-Error-Code"] = error_code

        # Log the error with all relevant context, including the status code,
        # message, details, and request information (if available).
        # This ensures the error is captured in logs for debugging purposes.
        self.log_error(
            status_code=status_code,
            message=message,
            details=details,
            request=request,
        )

        # Send to error tracking (Sentry, etc.) if configured
        if exception or status_code >= 500:
            capture_error(
                exception=exception,
                message=f"HTTP {status_code}: {message}",
                request=request,
                extra_context={
                    "status_code": status_code,
                    "error_code": error_code,
                    "details": details,
                },
            )

    @staticmethod
    def to_dict(
        message: str,
        details: ErrorDetails,
        error_code: str | None = None,
        debug_info: dict[str, Any] | None = None,
        request: HttpRequest | None = None,
        status_code: int | None = None,
    ) -> dict[str, Any]:
        """
        Convert the error response into a structured dictionary.

        Args:
            message (str): A brief message describing the error.
            details (str | dict[str, Any] | list | None): Additional
                error details.
            error_code (str | None): Optional application-specific error
                code.
            debug_info (dict[str, Any] | None): Debug information to include
                (only in DEBUG mode).

        Returns:
            dict[str, Any]: A structured dictionary for the error response.
        """

        # Create a structured response dictionary for the error response.
        # The `message` provides a brief description of the error.
        # The `details` offer additional context or information about the
        # error. If `details` is not provided, it defaults to "No additional
        # details provided."
        response: dict[str, Any] = {
            "error": message,
            "details": details or "No additional details provided.",
        }

        # Optionally include an application-specific error code if `error_code`
        # is provided. This can help clients or downstream systems identify and
        # handle specific errors programmatically.
        if error_code:
            response["code"] = error_code

        if request is not None:
            response["instance"] = request.path

        if status_code is not None:
            response["status"] = status_code

        # Include debug information if provided (only in DEBUG mode)
        if debug_info:
            response["debug"] = debug_info

        # Return the structured dictionary, which will be used as the content
        # for the JSON response.
        return response

    @staticmethod
    def get_renderer_name(request: HttpRequest | None) -> str:
        """Resolve the response renderer for the incoming request."""
        if request is None:
            return "json"

        preferred_type = get_preferred_content_type(request)
        if preferred_type == "html":
            accept_header = get_accept_header(request).lower()
            if "application/problem+json" in accept_header:
                return "problem+json"
            return "json"
        return preferred_type

    def log_error(
        self,
        status_code: int,
        message: str,
        details: ErrorDetails,
        request: HttpRequest | None,
    ) -> None:
        """
        Log the error details with contextual information.

        Args:
            status_code (int): The HTTP status code.
            message (str): Short description of the error.
            details (str | dict[str, Any] | list | None): Additional error details.
            request (HttpRequest | None): The HTTP request object for contextual logging.
        """

        # Construct the base log message with the HTTP status code and error
        # message. Includes the error `details` (if provided) to give more
        # context about the issue.
        safe_details = scrub_sensitive_data(details)
        log_message: str = (
            f"HTTP {status_code}: {message}\n" f"Details: {safe_details}\n"
        )

        # If a request object is available, include additional contextual
        # information.
        if request:
            log_message += (
                # Logs the URL path of the request.
                f"Request Path: {request.path}\n"
                # Logs the HTTP method (e.g., GET, POST).
                f"Method: {request.method}\n"
                # Logs all request headers as a dictionary.
                f"Headers: {scrub_sensitive_data(dict(request.headers))}\n"
            )
            # If the request has a body, decode and log it for debugging
            # purposes. Uses `errors='replace'` to avoid decoding errors for
            # non-UTF-8 content.
            if request.body:
                log_message += f"Body: {scrub_sensitive_data(request.body.decode(errors='replace'))}\n"

        # Log the constructed message as an error, ensuring the stack trace
        # and details are captured in the application's logs for debugging.
        logger.error(msg=log_message)


# =============================================================================
# Exports
# =============================================================================

__all__: list[str] = [
    "BaseErrorResponse",
]
