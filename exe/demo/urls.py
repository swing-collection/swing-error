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

# Import | Standard Library

# Import | Libraries
from django.contrib import admin
from django.urls import include, path
from django.urls.resolvers import URLResolver

# Import | Local Modules


# =============================================================================
# URL Patterns
# =============================================================================

urlpatterns: list[URLResolver] = [
    path(
        route="admin/",
        view=admin.site.urls,
    ),
    path(
        route="error/",
        view=include(
            arg="swing.error.urls",
        ),
    ),
    path(
        route="",
        view=include(arg="swing.error.urls"),
    ),
]
