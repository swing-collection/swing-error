# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides Demo URL Patterns
==========================

Defines URL patterns for the demo project. This includes:

- Admin panel routes for managing the application.
- Routes for the `swing_error` app, including a default route.

"""

# =============================================================================
# Imports
# =============================================================================

from django.contrib import admin
from django.urls import include, path
from django.urls.resolvers import URLResolver

# Import | Local
# Import | Local Modules
from . import views

# =============================================================================
# URL Patterns
# =============================================================================

urlpatterns: list[URLResolver] = [
    # Admin
    path(
        route="admin/",
        view=admin.site.urls,
    ),
    # Demo home
    path(
        route="",
        view=views.home,
        name="home",
    ),
    # Error test routes
    path(
        route="test/400/",
        view=views.test_400,
        name="test_400",
    ),
    path(
        route="test/401/",
        view=views.test_401,
        name="test_401",
    ),
    path(
        route="test/403/",
        view=views.test_403,
        name="test_403",
    ),
    path(
        route="test/404/",
        view=views.test_404,
        name="test_404",
    ),
    path(
        route="test/405/",
        view=views.test_405,
        name="test_405",
    ),
    path(
        route="test/408/",
        view=views.test_408,
        name="test_408",
    ),
    path(
        route="test/410/",
        view=views.test_410,
        name="test_410",
    ),
    path(
        route="test/429/",
        view=views.test_429,
        name="test_429",
    ),
    path(
        route="test/500/",
        view=views.test_500,
        name="test_500",
    ),
    path(
        route="test/exception/",
        view=views.test_exception,
        name="test_exception",
    ),
    # API routes
    path(
        route="api/json-error/",
        view=views.api_json_error,
        name="api_json_error",
    ),
    path(
        route="api/success/",
        view=views.api_success,
        name="api_success",
    ),
    # Swing error app routes
    path(
        route="error/",
        view=include(
            arg="swing.error.urls",
        ),
    ),
]
