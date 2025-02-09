# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
URL Configuration
=================

This module defines the URL configuration for your Django project, including
custom error handlers for various HTTP status codes.

Usage:
------
Include the custom error handlers in your project's URL configuration to
handle specific errors with custom responses.

Links:
------
- https://docs.djangoproject.com/en/5.0/topics/http/urls/
- https://docs.djangoproject.com/en/5.0/topics/http/views/#customizing-error-views

"""  # noqa E501

# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
# None

# Import | Libraries
from django.urls import path
from django.conf.urls import (
    handler400,
    handler401,
    handler403,
    handler404,
    handler405,
    handler408,
    handler410,
    handler429,
    handler500,
)

# Import | Local Modules
from .views import (
    home_view,
    another_view
)
from .responses import (
    Http400Response,
    Http401Response,
    Http403Response,
    Http404Response,
    Http405Response,
    Http408Response,
    Http410Response,
    Http429Response,
    Http500Response
)

# =============================================================================
# URL Patterns
# =============================================================================

urlpatterns = [
    path('', home_view, name='home'),
    path('another/', another_view, name='another'),
    # Add other URL patterns here
]

# =============================================================================
# Error Handlers
# =============================================================================

handler400 = lambda request, exception=None: Http400Response("Bad Request: Invalid request.")
handler401 = lambda request, exception=None: Http401Response("Unauthorized: Authentication is required.")
handler403 = lambda request, exception=None: Http403Response("Forbidden: You do not have permission to access this page.")
handler404 = lambda request, exception=None: Http404Response("Not Found: The requested resource was not found.")
handler405 = lambda request, exception=None: Http405Response("Method Not Allowed: This endpoint only supports certain methods.")
handler408 = lambda request, exception=None: Http408Response("Request Timeout: The server timed out waiting for the request.")
handler410 = lambda request, exception=None: Http410Response("Gone: The requested resource is no longer available.")
handler429 = lambda request, exception=None: Http429Response("Too Many Requests: You have exceeded your request limit.")
handler500 = lambda request: Http500Response("Internal Server Error: An unexpected error occurred.")

# Error Handlers

handler400 = "..views.handler400"  # Error Handler - Bad Request
handler403 = "..views.handler403"  # Error Handler - HTTP Forbidden
handler404 = "..views.handler404"  # Error Handler - Page not Found
handler500 = "..views.handler500"  # Error Handler - Server Error








from django.conf.urls import handler404, handler500, handler403, handler400
from error_handler.handlers import handle_404, handle_500, handle_permission_denied, handle_bad_request

handler404 = handle_404
handler500 = handle_500
handler403 = handle_permission_denied
handler400 = handle_bad_request