# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides 400 Error Handler View Module
======================================

This module contains a function-based and a class-based view for handling
HTTP 400 Bad Request errors in a Django application. It renders a custom
template with error details and sets the appropriate 400 status code in the
response. Additionally, it logs error details for debugging purposes.

By default, this is handled by `django.views.defaults.bad_request()`. If you
implement a custom view, be sure it accepts `request` and `exception` arguments
and returns an `HttpResponseBadRequest`.

Usage:
------
Include the `Handler400View` in your project's URL configuration for handling
400 errors. Add the following to your project's settings:

    HANDLER400 = 'myapp.views.Handler400View.as_view()'

Ensure you have a template at the specified `template_name` location.

Links:
------
- https://docs.djangoproject.com/en/5.0/ref/urls/#django.conf.urls.handler400
- https://docs.djangoproject.com/en/5.0/ref/request-response/#django.http.HttpResponseBadRequest

"""  # noqa E501


# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
from typing import Any, Dict
import logging

# Import | Libraries
from django.views.generic import TemplateView
from django.http import HttpResponseBadRequest, HttpRequest
from django.shortcuts import render

# Import | Local Modules
from swing_error.responses.response_http_400 import Http400Response


# =============================================================================
# Variables
# =============================================================================

GENERIC: str = "Please return to our home page"


# =============================================================================
# Function
# =============================================================================

def handler_400_view(
    request: HttpRequest,
    exception: Any,
    template_name: str = "errors/error.html"
) -> HttpResponseBadRequest:
    """
    400 Error Handler View Function
    ===============================

    A callable, or a string representing the full Python import path to the
    view that should be called if the HTTP client has sent a request that
    caused an error condition and a response with a status code of 400.

    Args:
        request (HttpRequest): The request object.
        exception (Any): The exception raised.
        template_name (str): The path to the template to be rendered.

    Returns:
        HttpResponseBadRequest: The HTTP response with status code 400.
    """
    response = render(
        request,
        template_name,
        {
            "title": "Bad Request",
            "header": "400 Error",
            "message": "Sorry, Bad Request",
            "redirect": GENERIC,
        }
    )
    response.status_code = 400
    return response


# =============================================================================
# Class
# =============================================================================

class Handler400View(TemplateView):
    """
    400 Error Handler View Class
    ============================

    A class-based view to handle HTTP 400 Bad Request errors.

    This view renders a custom template with error details and sets the 
    appropriate 400 status code in the response. Additionally, it logs 
    error details for debugging purposes.

    Attributes:
        template_name (str): The path to the template to be rendered.
        logger (logging.Logger): Logger instance for logging errors.
    """

    template_name: str = "errors/error.html"
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
            "title": "Bad Request",
            "header": "400 Error",
            "message": "Sorry, Bad Request",
            "redirect": GENERIC,
        })
        return context

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Dict[str, Any]
    ) -> HttpResponseBadRequest:
        """
        Handle GET requests by logging the error and rendering the response.

        Args:
            request (HttpRequest): The request object.
            *args (Any): Additional positional arguments.
            **kwargs (Dict[str, Any]): Additional keyword arguments.

        Returns:
            HttpResponseBadRequest: The HTTP response with status code 400.
        """
        self.log_error(request)
        context = self.get_context_data(**kwargs)
        return HttpResponseBadRequest(self.render_to_string(context))

    def log_error(self, request: HttpRequest) -> None:
        """
        Log the error details for debugging purposes.

        Args:
            request (HttpRequest): The request object.
        """
        self.logger.error(f"400 Bad Request at {request.path}")


# =============================================================================
# Module Exports
# =============================================================================

HANDLER400 = "myapp.views.Handler400View.as_view()"

__all__ = [
    "handler_400_view",
    "Handler400View",
    "HANDLER400",
]
