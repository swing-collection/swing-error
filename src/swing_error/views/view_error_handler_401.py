# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides 401 Error Handler View Module
======================================

This module contains a function-based and a class-based view for handling
HTTP 401 Unauthorized errors in a Django application. It renders a custom
template with error details and sets the appropriate 401 status code in the
response. Additionally, it logs error details for debugging purposes.

By default, this is handled by `django.views.defaults.permission_denied()`. If
youvimplement a custom view, be sure it accepts `request` and `exception`
argumentsvand returns an `HttpResponse`.

Usage:
------
Include the `Handler401View` in your project's URL configuration for handling
401 errors. Add the following to your project's settings:

    HANDLER401 = 'myapp.views.Handler401View.as_view()'

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
# Functions
# =============================================================================

def handler_401_view(
    request: HttpRequest,
    exception: Any, 
    template_name: str = "errors/401.html"
) -> HttpResponse:
    """
    401 Error Handler View Function
    ===============================

    A callable view to handle HTTP 401 Unauthorized errors.

    Args:
        request (HttpRequest): The request object.
        exception (Any): The exception raised.
        template_name (str): The path to the template to be rendered.

    Returns:
        HttpResponse: The HTTP response with status code 401.
    """
    response = render(request, template_name, {
        "title": "Unauthorized",
        "header": "401 Error",
        "message": "Authorization is required to access this page.",
        "redirect": GENERIC,
    })
    response.status_code = 401
    return response


# =============================================================================
# Classes
# =============================================================================

class Handler401View(TemplateView):
    """
    401 Error Handler View Class
    ============================

    A class-based view to handle HTTP 401 Unauthorized errors.

    This view renders a custom template with error details and sets the 
    appropriate 401 status code in the response. Additionally, it logs 
    error details for debugging purposes.

    Attributes:
        template_name (str): The path to the template to be rendered.
        logger (logging.Logger): Logger instance for logging errors.

    """

    template_name: str = "errors/401.html"
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
            "title": "Unauthorized",
            "header": "401 Error",
            "message": "Authorization is required to access this page.",
            "redirect": GENERIC,
        })

        return context

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Dict[str, Any]
    ) -> HttpResponse:
        """
        Handle GET requests by logging the error and rendering the response.

        Args:
            request (HttpRequest): The request object.
            *args (Any): Additional positional arguments.
            **kwargs (Dict[str, Any]): Additional keyword arguments.

        Returns:
            HttpResponse: The HTTP response with status code 401.

        """
        self.log_error(request)

        context = self.get_context_data(**kwargs)

        return HttpResponse(self.render_to_string(context), status=401)

    def log_error(self, request: HttpRequest) -> None:
        """
        Log the error details for debugging purposes.

        Args:
            request (HttpRequest): The request object.

        """

        self.logger.error(f"401 Unauthorized at {request.path}")


# =============================================================================
# Exports
# =============================================================================

HANDLER401 = "myapp.views.Handler401View.as_view()"

__all__ = [
    "handler_401_view",
    "Handler401View",
    "HANDLER401",
]
