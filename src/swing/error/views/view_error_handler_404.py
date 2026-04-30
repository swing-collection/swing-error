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
- https://docs.djangoproject.com/en/stable/ref/urls/#django.conf.urls.handler404
- https://docs.djangoproject.com/en/stable/ref/request-response/#django.http.HttpResponseNotFound

"""

# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
import logging
from typing import Any

from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views.generic import TemplateView

# Import | Local Modules
# None


# =============================================================================
# Variables
# =============================================================================

GENERIC: str = "Please return to our home page"


# =============================================================================
# Functions
# =============================================================================


def handler_404_view(
    request: HttpRequest,
    exception: Any,
    template_name: str = "errors/404.html",
) -> HttpResponse:
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
    response: HttpResponse = render(
        request=request,
        template_name=template_name,
        context={
            "title": "Not Found",
            "header": "404 Error",
            "message": "The page you are looking for does not exist.",
            "redirect": GENERIC,
        },
    )
    response.status_code = 404
    return response


# =============================================================================
# Classes
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
    logger: logging.Logger = logging.getLogger(name=__name__)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """
        Extend the base context data with custom error information.

        Args:
            **kwargs (Any): Additional keyword arguments.

        Returns:
            dict[str, Any]: Context data for the template.
        """
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context.update(
            {
                "title": "Not Found",
                "header": "404 Error",
                "message": "The page you are looking for does not exist.",
                "redirect": GENERIC,
            }
        )
        return context

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: dict[str, Any],
    ) -> HttpResponseNotFound:
        """
        Handle GET requests by logging the error and rendering the response.

        Args:
            request (HttpRequest): The request object.
            *args (Any): Additional positional arguments.
            **kwargs (dict[str, Any]): Additional keyword arguments.

        Returns:
            HttpResponseNotFound: The HTTP response with status code 404.
        """
        self.log_error(request=request)
        context: dict[str, Any] = self.get_context_data(**kwargs)
        return HttpResponseNotFound(content=self.render_to_string(context))

    def log_error(self, request: HttpRequest) -> None:
        """
        Log the error details for debugging purposes.

        Args:
            request (HttpRequest): The request object.
        """
        self.logger.error(msg=f"404 Not Found at {request.path}")


# =============================================================================
# Exports
# =============================================================================

HANDLER404 = "swing.error.views.view_error_handler_404.handler_404_view"

__all__: list[str] = [
    "handler_404_view",
    "Handler404View",
    "HANDLER404",
]
