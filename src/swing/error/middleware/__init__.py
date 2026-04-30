# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Swing Error Middleware Module
=============================

This module provides middleware classes for global exception handling in Django
applications.

Recommended Middleware:
-----------------------
- **ExceptionMiddleware**: The unified, comprehensive middleware that handles
  all exception capturing, logging, and error response generation. This is the
  recommended approach for error handling in swing-error.

Usage:
------
Add to your Django settings.py MIDDLEWARE list:

    MIDDLEWARE = [
        # ... other middleware ...
        'swing.error.middleware.ExceptionMiddleware',
    ]

"""

# =============================================================================
# Imports
# =============================================================================

# Import | Local
from .middleware_exception import ExceptionMiddleware

# =============================================================================
# Exports
# =============================================================================

__all__: list[str] = [
    "ExceptionMiddleware",
]
