# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides Base Error Response Class
==================================

This module provides a base class for HTTP error responses, offering
structured JSON formatting, logging, and extensibility for custom error
handling in Django applications.

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
- https://docs.djangoproject.com/en/5.0/ref/urls/#django.conf.urls.handler400
- https://docs.djangoproject.com/en/5.0/ref/request-response/#django.http.HttpResponseBadRequest

"""  # noqa E501


# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
import json
import logging
from typing import Any, Dict, Optional, Union

# Import | Libraries
from django.http import JsonResponse, HttpRequest

# Import | Local Modules
# None


# =============================================================================
# Logger
# =============================================================================

# Configure logger
logger = logging.getLogger(__name__)


# =============================================================================
# Class
# =============================================================================

class BaseErrorResponse(JsonResponse):
    """
    Base Error Response Class
    =========================

    A base class for HTTP error responses, providing structured JSON
    formatting, logging, and extensibility.

    Attributes:
        status_code (int): HTTP status code for the response.
        message (str): Short description of the error.
        details (Optional[Union[str, Dict[str, Any]]]): Additional details
            about the error.
        error_code (Optional[str]): Optional application-specific error code.
        request (Optional[HttpRequest]): The HTTP request object, used for
            logging.

    """

    def __init__(
        self,
        status_code: int,
        message: str,
        details: Optional[Union[str, Dict[str, Any], list]] = None,
        error_code: Optional[str] = None,
        request: Optional[HttpRequest] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the BaseErrorResponse.

        Args:
            status_code (int): The HTTP status code for the error response.
            message (str): A brief message describing the error.
            details (Optional[Union[str, Dict[str, Any], list]]): Additional
                error details (default: None).
            error_code (Optional[str]): Optional application-specific error
                code (default: None).
            request (Optional[HttpRequest]): The HTTP request object for
                logging context (default: None).
            *args: Additional positional arguments for JsonResponse.
            **kwargs: Additional keyword arguments for JsonResponse.
        """

        # Prepare the structured content for the error response.
        # `to_dict` method formats the message, details, and optional error
        # code into a consistent dictionary structure for the response body.
        content = self.to_dict(message, details, error_code)

        # Initialize the JsonResponse with the structured content and status
        # code. Additional arguments (`args` and `kwargs`) can be passed to
        # customize the response further (e.g., custom headers).
        super().__init__(
            content,
            status=status_code,
            *args,
            **kwargs
        )

        # Log the error with all relevant context, including the status code,
        # message, details, and request information (if available).
        # This ensures the error is captured in logs for debugging purposes.
        self.log_error(
            status_code,
            message,
            details,
            request,
        )

    @staticmethod
    def to_dict(
        message: str,
        details: Optional[Union[str, Dict[str, Any], list]],
        error_code: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Convert the error response into a structured dictionary.

        Args:
            message (str): A brief message describing the error.
            details (Optional[Union[str, Dict[str, Any], list]]): Additional
                error details.
            error_code (Optional[str]): Optional application-specific error
                code.

        Returns:
            Dict[str, Any]: A structured dictionary for the error response.
        """

        # Create a structured response dictionary for the error response.
        # The `message` provides a brief description of the error.
        # The `details` offer additional context or information about the
        # error. If `details` is not provided, it defaults to "No additional
        # details provided."
        response = {
            "error": message,
            "details": details or "No additional details provided."
        }

        # Optionally include an application-specific error code if `error_code`
        # is provided. This can help clients or downstream systems identify and
        # handle specific errors programmatically.
        if error_code:
            response["code"] = error_code

        # Return the structured dictionary, which will be used as the content
        # for the JSON response.
        return response

    def log_error(
        self,
        status_code: int,
        message: str,
        details: Optional[Union[str, Dict[str, Any], list]],
        request: Optional[HttpRequest],
    ) -> None:
        """
        Log the error details with contextual information.

        Args:
            status_code (int): The HTTP status code.
            message (str): Short description of the error.
            details (Optional[Union[str, Dict[str, Any], list]]): Additional error details.
            request (Optional[HttpRequest]): The HTTP request object for contextual logging.
        """

        # Construct the base log message with the HTTP status code and error
        # message. Includes the error `details` (if provided) to give more
        # context about the issue.
        log_message = (
            f"HTTP {status_code}: {message}\n"
            f"Details: {details}\n"
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
                f"Headers: {dict(request.headers)}\n"
            )
            # If the request has a body, decode and log it for debugging
            # purposes. Uses `errors='replace'` to avoid decoding errors for
            # non-UTF-8 content.
            if request.body:
                log_message += f"Body: {request.body.decode(errors='replace')}\n"

        # Log the constructed message as an error, ensuring the stack trace
        # and details are captured in the application's logs for debugging.
        logger.error(log_message)
