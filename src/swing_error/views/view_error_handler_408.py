# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides 408 Error Handler View Module
======================================

This module contains a function-based and a class-based view for handling
HTTP 408 Request Timeout errors in a Django application. It renders a custom
template with error details and sets the appropriate 408 status code in the
response. Additionally, it logs error details for debugging purposes.

By default, this is handled by `django.views.defaults.permission_denied()`. If you
implement a custom view, be sure it accepts `request` and `exception` arguments
and returns an `HttpResponseRequestTimeout`.

Usage:
------
Include the `Handler408View` in your project's URL configuration for handling
408 errors. Add the following to your project's settings:

    HANDLER408 = 'myapp.views.Handler408View.as_view()'

Ensure you have a template at the specified `template_name` location.

Links:
------

"""  # noqa E501


# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
from typing import Any, Dict
import logging

# Import | Libraries
from django.views.generic import TemplateView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Import | Local Modules
# None


# =============================================================================
# Variables
# =============================================================================

GENERIC: str = "Please return to our home page"


# =============================================================================
# Custom Response Class
# =============================================================================

class HttpResponseRequestTimeout(HttpResponse):
    status_code = 408


# =============================================================================
# Function
# =============================================================================

def handler_408_view(
    request: HttpRequest,
    exception: Any, 
    template_name: str = "errors/408.html"
) -> HttpResponseRequestTimeout:
    """
    408 Error Handler View Function
    ===============================

    A callable view to handle HTTP 408 Request Timeout errors.

    Args:
        request (HttpRequest): The request object.
        exception (Any): The exception raised.
        template_name (str): The path to the template to be rendered.

    Returns:
        HttpResponseRequestTimeout: The HTTP response with status code 408.
    """
    response = render(request, template_name, {
        "title": "Request Timeout",
        "header": "408 Error",
        "message": "The server timed out waiting for the request.",
        "redirect": GENERIC,
    })
    response.status_code = 408
    return response


# =============================================================================
# Classes
# =============================================================================

class Handler408View(TemplateView):
    """
    408 Error Handler View Class
    ============================

    A class-based view to handle HTTP 408 Request Timeout errors.

    This view renders a custom template with error details and sets the 
    appropriate 408 status code in the response. Additionally, it logs 
    error details for debugging purposes.

    Attributes:
        template_name (str): The path to the template to be rendered.
        logger (logging.Logger): Logger instance for logging errors.
    """

    template_name: str = "errors/408.html"
    logger: logging.Logger = logging.getLogger(__name__)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Extend the base context data with custom error information.

        Args:
            **kwargs (Any): Additional keyword arguments.

        Returns:
            Dict[str, Any]: Context data for the template.
        """
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Request Timeout",
            "header": "408 Error",
            "message": "The server timed out waiting for the request.",
            "redirect": GENERIC,
        })
        return context

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Dict[str, Any]
    ) -> HttpResponseRequestTimeout:
        """
        Handle GET requests by logging the error and rendering the response.

        Args:
            request (HttpRequest): The request object.
            *args (Any): Additional positional arguments.
            **kwargs (Dict[str, Any]): Additional keyword arguments.

        Returns:
            HttpResponseRequestTimeout: The HTTP response with status code 408.
        """
        self.log_error(request)
        context = self.get_context_data(**kwargs)
        return HttpResponseRequestTimeout(self.render_to_string(context))

    def log_error(self, request: HttpRequest) -> None:
        """
        Log the error details for debugging purposes.

        Args:
            request (HttpRequest): The request object.
        """
        self.logger.error(f"408 Request Timeout at {request.path}")


# =============================================================================
# Exports
# =============================================================================

HANDLER408 = "myapp.views.Handler408View.as_view()"

__all__ = [
    "handler_408_view",
    "Handler408View",
    "HANDLER408",
    "HttpResponseRequestTimeout",
]
