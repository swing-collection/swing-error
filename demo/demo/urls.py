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
from django.urls import path, include

# Import | Local Modules


# =============================================================================
# URL Patterns
# =============================================================================

urlpatterns = [
    path("admin/", admin.site.urls),  # Admin site URL
    path("error/", include("swing_error.urls")),  # Include the URLs from the swing_error app
    path("", include("swing_error.urls")),  # Include the URLs from the swing_error app
]
