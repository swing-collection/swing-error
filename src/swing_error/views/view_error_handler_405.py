-*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Provides 405 Error Handler View Module
======================================

This module contains a function-based and a class-based view for handling
HTTP 405 Method Not Allowed errors in a Django application. It renders a custom
template with error details and sets the appropriate 405 status code in the
response. Additionally, it logs error details for debugging purposes.

By default, this is handled by `django.views.defaults.permission_denied()`. If you
implement a custom view, be sure it accepts `request` and `exception` arguments
and returns an `HttpResponseNotAllowed`.

Usage:
------
Include the `Handler405View` in your project's URL configuration for handling
405 errors. Add the following to your project's settings:

    HANDLER405 = 'myapp.views.Handler405View.as_view()'

Ensure you have a template at the specified `template_name` location.

Links:
------
- https://docs.djangoproject.com/en/5.0/ref/request-response/#django.http.HttpResponseNotAllowed
- https://stackoverflow.com/questions/49162214/why-django-doesnt-have-error-page-handler-for-405-method-not-allowed

"""  # noqa E501


# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
from typing import Any, Dict
import logging

# Import | Libraries
from django.views.generic import TemplateView
from django.http import HttpRequest, HttpResponseNotAllowed
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

def handler_405_view(
    request: HttpRequest,
    exception: Any, 
    template_name: str = "errors/405.html"
) -> HttpResponseNotAllowed:
    """
    405 Error Handler View Function
    ===============================

    A callable view to handle HTTP 405 Method Not Allowed errors.

    Args:
        request (HttpRequest): The request object.
        exception (Any): The exception raised.
        template_name (str): The path to the template to be rendered.

    Returns:
        HttpResponseNotAllowed: The HTTP response with status code 405.
    """
    response = render(request, template_name, {
        "title": "Method Not Allowed",
        "header": "405 Error",
        "message": "The method is not allowed for the requested URL.",
        "redirect": GENERIC,
    })
    response.status_code = 405
    return response


# =============================================================================
# Class
# =============================================================================

class Handler405View(TemplateView):
    """
    405 Error Handler View Class
    ============================

    A class-based view to handle HTTP 405 Method Not Allowed errors.

    This view renders a custom template with error details and sets the 
    appropriate 405 status code in the response. Additionally, it logs 
    error details for debugging purposes.

    Attributes:
        template_name (str): The path to the template to be rendered.
        logger (logging.Logger): Logger instance for logging errors.
    """

    template_name: str = "errors/405.html"
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
            "title": "Method Not Allowed",
            "header": "405 Error",
            "message": "The method is not allowed for the requested URL.",
            "redirect": GENERIC,
        })
        return context

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Dict[str, Any]
    ) -> HttpResponseNotAllowed:
        """
        Handle GET requests by logging the error and rendering the response.

        Args:
            request (HttpRequest): The request object.
            *args (Any): Additional positional arguments.
            **kwargs (Dict[str, Any]): Additional keyword arguments.

        Returns:
            HttpResponseNotAllowed: The HTTP response with status code 405.
        """
        self.log_error(request)
        context = self.get_context_data(**kwargs)
        return HttpResponseNotAllowed(self.render_to_string(context))

    def log_error(self, request: HttpRequest) -> None:
        """
        Log the error details for debugging purposes.

        Args:
            request (HttpRequest): The request object.
        """
        self.logger.error(f"405 Method Not Allowed at {request.path}")


# =============================================================================
# Module Exports
# =============================================================================

HANDLER405 = "myapp.views.Handler405View.as_view()"

__all__ = [
    "handler_405_view",
    "Handler405View",
    "HANDLER405",
]
