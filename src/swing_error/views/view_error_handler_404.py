# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Provides 404 Error Handler View Module
======================================

This module contains a function-based and a class-based view for handling
HTTP 404 Not Found errors in a Django application. It renders a custom
template with error details and sets the appropriate 404 status code in the
response. Additionally, it logs error details for debugging purposes.

By default, this is handled by `django.views.defaults.page_not_found()`. If you
implement a custom view, be sure it accepts `request` and `exception` arguments
and returns an `HttpResponseNotFound`.

Usage:
------
Include the `Handler404View` in your project's URL configuration for handling
404 errors. Add the following to your project's settings:

    HANDLER404 = 'myapp.views.Handler404View.as_view()'

Ensure you have a template at the specified `template_name` location.

Links:
------
- https://docs.djangoproject.com/en/5.0/ref/urls/#django.conf.urls.handler404
- https://docs.djangoproject.com/en/5.0/ref/request-response/#django.http.HttpResponseNotFound

"""  # noqa E501


# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
from typing import Any, Dict
import logging

# Import | Libraries
from django.views.generic import TemplateView
from django.http import HttpRequest, HttpResponseNotFound
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

def handler_404_view(
    request: HttpRequest,
    exception: Any, 
    template_name: str = "errors/404.html"
) -> HttpResponseNotFound:
    """
    404 Error Handler View Function
    ===============================

    A callable view to handle HTTP 404 Not Found errors.

    Args:
        request (HttpRequest): The request object.
        exception (Any): The exception raised.
        template_name (str): The path to the template to be rendered.

    Returns:
        HttpResponseNotFound: The HTTP response with status code 404.
    """
    response = render(request, template_name, {
        "title": "Not Found",
        "header": "404 Error",
        "message": "The page you are looking for does not exist.",
        "redirect": GENERIC,
    })
    response.status_code = 404
    return response


# =============================================================================
# Class
# =============================================================================

class Handler404View(TemplateView):
    """
    404 Error Handler View Class
    ============================

    A class-based view to handle HTTP 404 Not Found errors.

    This view renders a custom template with error details and sets the 
    appropriate 404 status code in the response. Additionally, it logs 
    error details for debugging purposes.

    Attributes:
        template_name (str): The path to the template to be rendered.
        logger (logging.Logger): Logger instance for logging errors.
    """

    template_name: str = "errors/404.html"
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
            "title": "Not Found",
            "header": "404 Error",
            "message": "The page you are looking for does not exist.",
            "redirect": GENERIC,
        })
        return context

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Dict[str, Any]
    ) -> HttpResponseNotFound:
        """
        Handle GET requests by logging the error and rendering the response.

        Args:
            request (HttpRequest): The request object.
            *args (Any): Additional positional arguments.
            **kwargs (Dict[str, Any]): Additional keyword arguments.

        Returns:
            HttpResponseNotFound: The HTTP response with status code 404.
        """
        self.log_error(request)
        context = self.get_context_data(**kwargs)
        return HttpResponseNotFound(self.render_to_string(context))

    def log_error(self, request: HttpRequest) -> None:
        """
        Log the error details for debugging purposes.

        Args:
            request (HttpRequest): The request object.
        """
        self.logger.error(f"404 Not Found at {request.path}")


# =============================================================================
# Module Exports
# =============================================================================

HANDLER404 = "myapp.views.Handler404View.as_view()"

__all__ = [
    "handler_404_view",
    "Handler404View",
    "HANDLER404",
]
