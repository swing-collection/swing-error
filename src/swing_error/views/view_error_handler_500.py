# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Provides 500 Error Handler View Module
======================================

This module contains a function-based and a class-based view for handling
HTTP 500 Internal Server Error errors in a Django application. It renders a custom
template with error details and sets the appropriate 500 status code in the
response. Additionally, it logs error details for debugging purposes.

By default, this is handled by `django.views.defaults.server_error()`. If you
implement a custom view, be sure it accepts `request` arguments
and returns an `HttpResponseServerError`.

Usage:
------
Include the `Handler500View` in your project's URL configuration for handling
500 errors. Add the following to your project's settings:

    HANDLER500 = 'myapp.views.Handler500View.as_view()'

Ensure you have a template at the specified `template_name` location.

Links:
------
- https://docs.djangoproject.com/en/5.0/ref/urls/#django.conf.urls.handler500
- https://docs.djangoproject.com/en/5.0/ref/request-response/#django.http.HttpResponseServerError

"""  # noqa E501


# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
from typing import Any, Dict
import logging

# Import | Libraries
from django.views.generic import TemplateView
from django.http import HttpRequest, HttpResponseServerError
from django.shortcuts import render

# Import | Local Modules
# None


# =============================================================================
# Variables
# =============================================================================

GENERIC: str = "Please return to our home page"


# =============================================================================
# Function
# =============================================================================

def handler_500_view(
    request: HttpRequest, 
    template_name: str = "errors/500.html"
) -> HttpResponseServerError:
    """
    500 Error Handler View Function
    ===============================

    A callable view to handle HTTP 500 Internal Server Error errors.

    Args:
        request (HttpRequest): The request object.
        template_name (str): The path to the template to be rendered.

    Returns:
        HttpResponseServerError: The HTTP response with status code 500.
    """
    response = render(request, template_name, {
        "title": "Internal Server Error",
        "header": "500 Error",
        "message": "An unexpected error occurred on the server.",
        "redirect": GENERIC,
    })
    response.status_code = 500
    return response


# =============================================================================
# Class
# =============================================================================

class Handler500View(TemplateView):
    """
    500 Error Handler View Class
    ============================

    A class-based view to handle HTTP 500 Internal Server Error errors.

    This view renders a custom template with error details and sets the 
    appropriate 500 status code in the response. Additionally, it logs 
    error details for debugging purposes.

    Attributes:
        template_name (str): The path to the template to be rendered.
        logger (logging.Logger): Logger instance for logging errors.
    """

    template_name: str = "errors/500.html"
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
            "title": "Internal Server Error",
            "header": "500 Error",
            "message": "An unexpected error occurred on the server.",
            "redirect": GENERIC,
        })
        return context

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Dict[str, Any]
    ) -> HttpResponseServerError:
        """
        Handle GET requests by logging the error and rendering the response.

        Args:
            request (HttpRequest): The request object.
            *args (Any): Additional positional arguments.
            **kwargs (Dict[str, Any]): Additional keyword arguments.

        Returns:
            HttpResponseServerError: The HTTP response with status code 500.
        """
        self.log_error(request)
        context = self.get_context_data(**kwargs)
        return HttpResponseServerError(self.render_to_string(context))

    def log_error(self, request: HttpRequest) -> None:
        """
        Log the error details for debugging purposes.

        Args:
            request (HttpRequest): The request object.
        """
        self.logger.error(f"500 Internal Server Error at {request.path}")


# =============================================================================
# Module Exports
# =============================================================================

HANDLER500 = "myapp.views.Handler500View.as_view()"

__all__ = [
    "handler_500_view",
    "Handler500View",
    "HANDLER500",
]
