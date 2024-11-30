# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides 410 Error Handler View Module
======================================

This module contains a function-based and a class-based view for handling
HTTP 410 Gone errors in a Django application. It renders a custom
template with error details and sets the appropriate 410 status code in the
response. Additionally, it logs error details for debugging purposes.

By default, this is handled by `django.views.defaults.permission_denied()`. If you
implement a custom view, be sure it accepts `request` and `exception` arguments
and returns an `HttpResponseGone`.

Usage:
------
Include the `Handler410View` in your project's URL configuration for handling
410 errors. Add the following to your project's settings:

    HANDLER410 = 'myapp.views.Handler410View.as_view()'

Ensure you have a template at the specified `template_name` location.

Links:
------
- https://docs.djangoproject.com/en/5.0/ref/request-response/#django.http.HttpResponseGone

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

class HttpResponseGone(HttpResponse):
    status_code = 410


# =============================================================================
# Functions
# =============================================================================

def handler_410_view(
    request: HttpRequest,
    exception: Any, 
    template_name: str = "errors/410.html"
) -> HttpResponseGone:
    """
    410 Error Handler View Function
    ===============================

    A callable view to handle HTTP 410 Gone errors.

    Args:
        request (HttpRequest): The request object.
        exception (Any): The exception raised.
        template_name (str): The path to the template to be rendered.

    Returns:
        HttpResponseGone: The HTTP response with status code 410.
    """
    response = render(request, template_name, {
        "title": "Gone",
        "header": "410 Error",
        "message": "The requested resource is no longer available on this server.",
        "redirect": GENERIC,
    })
    response.status_code = 410
    return response


# =============================================================================
# Classes
# =============================================================================

class Handler410View(TemplateView):
    """
    410 Error Handler View Class
    ============================

    A class-based view to handle HTTP 410 Gone errors.

    This view renders a custom template with error details and sets the 
    appropriate 410 status code in the response. Additionally, it logs 
    error details for debugging purposes.

    Attributes:
        template_name (str): The path to the template to be rendered.
        logger (logging.Logger): Logger instance for logging errors.
    """

    template_name: str = "errors/410.html"
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
            "title": "Gone",
            "header": "410 Error",
            "message": "The requested resource is no longer available on this server.",
            "redirect": GENERIC,
        })
        return context

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Dict[str, Any]
    ) -> HttpResponseGone:
        """
        Handle GET requests by logging the error and rendering the response.

        Args:
            request (HttpRequest): The request object.
            *args (Any): Additional positional arguments.
            **kwargs (Dict[str, Any]): Additional keyword arguments.

        Returns:
            HttpResponseGone: The HTTP response with status code 410.
        """
        self.log_error(request)
        context = self.get_context_data(**kwargs)
        return HttpResponseGone(self.render_to_string(context))

    def log_error(self, request: HttpRequest) -> None:
        """
        Log the error details for debugging purposes.

        Args:
            request (HttpRequest): The request object.
        """
        self.logger.error(f"410 Gone at {request.path}")


# =============================================================================
# Exports
# =============================================================================

HANDLER410 = "myapp.views.Handler410View.as_view()"

__all__ = [
    "handler_410_view",
    "Handler410View",
    "HANDLER410",
    "HttpResponseGone",
]
