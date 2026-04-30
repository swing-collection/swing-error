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
implement a custom view, be sure it accepts `request` and `exception`
arguments and returns an `HttpResponseBadRequest`.

Usage:
------
Include the `Handler400View` in your project's URL configuration for handling
400 errors. Add the following to your project's settings:

    HANDLER400 = 'swing_error.views.Handler400View.as_view()'

Ensure you have a template at the specified `template_name` location.

Links:
------
- https://docs.djangoproject.com/en/stable/ref/urls/#django.conf.urls.handler400
- https://docs.djangoproject.com/en/stable/ref/request-response/#django.http.HttpResponseBadRequest

"""

# =============================================================================
# Imports
# =============================================================================

# Import | Local
# Import | Local Modules
from ..responses.response_http_400 import Http400Response
from ..views.view_error_handler_base import BaseErrorView

# =============================================================================
# Classes
# =============================================================================


class Handler400View(BaseErrorView):
    """
    400 Error Handler View
    ======================

    Handles HTTP 400 Bad Request errors by rendering a custom template
    and using the Http400Response class.
    """

    error_type = "400"
    response_class = Http400Response


# =============================================================================
# Exports
# =============================================================================

HANDLER400 = "swing.error.views.view_error_handler_400.Handler400View"

__all__: list[str] = [
    "Handler400View",
    "HANDLER400",
]
