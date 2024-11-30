# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides 429 Error Handler View Module
======================================

This module contains a function-based and a class-based view for handling
HTTP 429 Too Many Requests errors in a Django application. It renders a custom
template with error details and sets the appropriate 429 status code in the
response. Additionally, it logs error details for debugging purposes and 
integrates with Django Ratelimit for rate limiting.

Usage:
------
Include the `Handler429View` in your project's URL configuration for handling
429 errors. Add the following to your project's settings:

    HANDLER429 = 'myapp.views.Handler429View.as_view()'

Ensure you have a template at the specified `template_name` location.

Links:
------
- https://django-ratelimit.readthedocs.io/en/latest/cookbook/429.html

"""  # noqa E501


# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
from typing import Any, Dict
import logging

# Import | Libraries
from django.views.generic import TemplateView
from django.http import HttpRequest
from django.shortcuts import render
from django_ratelimit.decorators import ratelimit

# Import | Local Modules
# None


# =============================================================================
# Variables
# =============================================================================

GENERIC: str = "Please return to our home page"


# =============================================================================
# Functions
# =============================================================================

@ratelimit(key='ip', rate='5/m', method='GET', block=True)
def handler_429_view(
    request: HttpRequest,
    exception: Any, 
    template_name: str = "errors/429.html"
) -> HttpResponseTooManyRequests:
    """
    429 Error Handler View Function
    ===============================

    A callable view to handle HTTP 429 Too Many Requests errors.

    Args:
        request (HttpRequest): The request object.
        exception (Any): The exception raised.
        template_name (str): The path to the template to be rendered.

    Returns:
        HttpResponseTooManyRequests: The HTTP response with status code 429.
    """
    response = render(request, template_name, {
        "title": "Too Many Requests",
        "header": "429 Error",
        "message": "You have sent too many requests in a given amount of time.",
        "redirect": GENERIC,
    })
    response.status_code = 429
    return response


# =============================================================================
# Classes
# =============================================================================

class Handler429View(TemplateView):
    """
    429 Error Handler View Class
    ============================

    A class-based view to handle HTTP 429 Too Many Requests errors.

    This view renders a custom template with error details and sets the 
    appropriate 429 status code in the response. Additionally, it logs 
    error details for debugging purposes.

    Attributes:
        template_name (str): The path to the template to be rendered.
        logger (logging.Logger): Logger instance for logging errors.
    """

    template_name: str = "errors/429.html"
    logger: logging.Logger = logging.getLogger(__name__)

    @ratelimit(key='ip', rate='5/m', method='GET', block=True)
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
            "title": "Too Many Requests",
            "header": "429 Error",
            "message": "You have sent too many requests in a given amount of time.",
            "redirect": GENERIC,
        })
        return context

    @ratelimit(key='ip', rate='5/m', method='GET', block=True)
    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Dict[str, Any]
    ) -> HttpResponseTooManyRequests:
        """
        Handle GET requests by logging the error and rendering the response.

        Args:
            request (HttpRequest): The request object.
            *args (Any): Additional positional arguments.
            **kwargs (Dict[str, Any]): Additional keyword arguments.

        Returns:
            HttpResponseTooManyRequests: The HTTP response with status code 429.
        """
        self.log_error(request)
        context = self.get_context_data(**kwargs)
        return HttpResponseTooManyRequests(self.render_to_string(context))

    def log_error(self, request: HttpRequest) -> None:
        """
        Log the error details for debugging purposes.

        Args:
            request (HttpRequest): The request object.
        """
        self.logger.error(f"429 Too Many Requests at {request.path}")


# =============================================================================
# Exports
# =============================================================================

HANDLER429 = "myapp.views.Handler429View.as_view()"

__all__ = [
    "handler_429_view",
    "Handler429View",
    "HANDLER429",
]