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

To use these handlers, add to your project's root urls.py:

    from swing.error.urls import (
        handler400, handler403, handler404, handler500
    )

Or configure in settings.py:

    HANDLER400 = 'swing.error.views.view_error_handler_400.handler_400_view'
    HANDLER403 = 'swing.error.views.view_error_handler_403.handler_403_view'
    HANDLER404 = 'swing.error.views.view_error_handler_404.handler_404_view'
    HANDLER500 = 'swing.error.views.view_error_handler_500.handler_500_view'

Links:
------
- https://docs.djangoproject.com/en/stable/topics/http/urls/
- https://docs.djangoproject.com/en/stable/topics/http/views/#customizing-error-views

"""

# =============================================================================
# Imports
# =============================================================================

# Import | Libraries
from django.urls import path

# Import | Local Modules
from .views import (
    HANDLER400,
    HANDLER401,
    HANDLER403,
    HANDLER404,
    HANDLER405,
    HANDLER408,
    HANDLER410,
    HANDLER429,
    HANDLER500,
)

# =============================================================================
# URL Patterns
# =============================================================================

urlpatterns: list[object] = [
    # Add other URL patterns here
]

# =============================================================================
# Error Handlers
# =============================================================================

# These can be imported in your project's root urls.py
handler400 = HANDLER400
handler401 = HANDLER401
handler403 = HANDLER403
handler404 = HANDLER404
handler405 = HANDLER405
handler408 = HANDLER408
handler410 = HANDLER410
handler429 = HANDLER429
handler500 = HANDLER500


# =============================================================================
# Exports
# =============================================================================

__all__: list[str] = [
    "urlpatterns",
    "handler400",
    "handler401",
    "handler403",
    "handler404",
    "handler405",
    "handler408",
    "handler410",
    "handler429",
    "handler500",
]
# from error_handler.handlers import (
#     handle_404,
#     handle_500,
#     handle_bad_request,
#     handle_permission_denied,
# )

# handler404 = handle_404
# handler500 = handle_500
# handler403 = handle_permission_denied
# handler400 = handle_bad_request
